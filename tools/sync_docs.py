#!/usr/bin/env python3
"""Rebuild htmx-grimoire/references/ from the upstream htmx 4 docs.

Usage:
    python tools/sync_docs.py [path-to-htmx-checkout]

Without an argument, shallow-clones the four-dev branch into a temp dir.
The upstream pages are written for the website: they carry frontmatter, mock
server scripts that power the live demos, and site-relative links. This strips
all of that so the files read cleanly as plain markdown references.
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = "https://github.com/bigskysoftware/htmx.git"
BRANCH = "four-dev"
CONTENT = "www/src/content"
OUT = Path(__file__).resolve().parent.parent / "htmx-grimoire" / "references"

# upstream dir -> local dir
FOLDERS = {
    "patterns": "patterns",
    "extensions": "extensions",
    "reference/01-attributes": "api/attributes",
}
# upstream dir -> one local file; these pages are too small to be worth a file each
MERGED = {
    "reference/02-headers": ("api/headers.md", "HTTP Headers"),
    "reference/03-events": ("api/events.md", "Events"),
    "reference/04-config": ("api/config.md", "Configuration"),
    "reference/05-methods": ("api/methods.md", "JavaScript Methods"),
    "reference/06-tags": ("api/tags.md", "Tags"),
}
# upstream file -> local file
FILES = {
    "docs.md": "docs.md",
    "docs/hx-live-guide.md": "guides/hx-live.md",
    "docs/htmx-events-guide.md": "guides/events.md",
    "docs/morphing-swaps-guide.md": "guides/morphing.md",
    "docs/hcon-guide.md": "guides/hcon.md",
    "docs/whats-new-in-htmx-4.md": "guides/whats-new-in-htmx-4.md",
    "docs/extension-authoring-guide.md": "guides/extension-authoring.md",
    "docs/extension-htmx-4-migration-guide.md": "guides/extension-migration.md",
    "docs/htmax.md": "guides/htmax.md",
}
# skills shipped in the htmx repo itself, outside the docs tree -> local file
SKILLS = {
    "src/skills/htmx-debugging.md": "guides/debugging.md",
    "src/skills/htmx-upgrade-from-htmx2.md": "guides/upgrade-from-htmx-2.md",
}
# quirks.md is skipped on purpose: upstream still describes htmx 2 behaviour there.

FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)
LEADING_SCRIPT = re.compile(r"\A(?:\s*<(script|style)[^>]*>.*?</\1>)+\s*", re.S)
SRI = re.compile(r' integrity="__SRI_\w+__" crossorigin="anonymous"')
DEMO_DIV = re.compile(r'^<div id="demo-content"[^>]*></div>\n', re.M)
INTERNAL_LINK = re.compile(r"\[((?:[^\[\]]|\[[^\]]*\])*)\]\((?:/|#)[^)\s]*\)")
TOC_MIN_LINES = 300


def meta(front, key):
    m = re.search(rf'^{key}:\s*"?(.*?)"?\s*$', front, re.M)
    return m.group(1) if m else ""


def toc(body):
    lines, fenced = [], False
    for line in body.splitlines():
        if line.startswith("```"):
            fenced = not fenced
        m = None if fenced else re.match(r"(##|###) (.+)", line)
        if m:
            lines.append(f"{'  ' if m.group(1) == '###' else ''}- {m.group(2)}")
    return "## Contents\n\n" + "\n".join(lines) + "\n\n"


def drop_demos(text):
    """Remove the live demo markup; it repeats the code block just above it."""
    out, fenced, depth, styling = [], False, 0, False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            fenced = not fenced
        if not fenced and (styling or line.startswith("<style>")):
            styling = "</style>" not in line
            continue
        if not fenced and (depth or re.match(r'\s*<div class="not-prose demo-container', line)):
            depth += len(re.findall(r"<div\b", line)) - len(re.findall(r"</div>", line))
            continue
        out.append(line)
    return "\n".join(out)


def space_headings(text):
    out, fenced = [], False
    for line in text.splitlines():
        if line.startswith("```"):
            fenced = not fenced
        if not fenced and line.startswith("#") and out and out[-1].strip():
            out.append("")
        out.append(line)
    return "\n".join(out)


def clean(text, version):
    front = ""
    m = FRONTMATTER.match(text)
    if m:
        front, text = m.group(1), text[m.end():]
    text = LEADING_SCRIPT.sub("", text)
    text = DEMO_DIV.sub("", text)
    text = space_headings(drop_demos(text))
    text = SRI.sub("", text).replace("__VERSION__", version)
    # Site-relative links point nowhere once the page leaves the website.
    text = INTERNAL_LINK.sub(r"\1", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"

    head = f"# {meta(front, 'title')}\n\n" if meta(front, "title") else ""
    if meta(front, "description"):
        head += f"> {meta(front, 'description')}\n\n"
    if text.count("\n") > TOC_MIN_LINES:
        head += toc(text)
    return head + text


def demote(text):
    """Push every heading down one level so a page can sit under a parent title."""
    out, fenced = [], False
    for line in text.splitlines():
        if line.startswith("```"):
            fenced = not fenced
        out.append("#" + line if not fenced and line.startswith("#") else line)
    return "\n".join(out) + "\n"


def pages(folder):
    for f in sorted(folder.glob("*.md")):
        if f.name != "index.md" and not re.search(r"^soon:\s*true", f.read_text(), re.M):
            yield f


def write(src, dest, version):
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(clean(src.read_text(), version))


def main():
    tmp = None
    if len(sys.argv) > 1:
        root = Path(sys.argv[1])
    else:
        tmp = tempfile.mkdtemp()
        subprocess.run(["git", "clone", "--depth", "1", "--branch", BRANCH, REPO, tmp], check=True)
        root = Path(tmp)
    content = root / CONTENT
    pkg = subprocess.run(["git", "-C", str(root), "show", "HEAD:package.json"],
                         capture_output=True, text=True, check=True).stdout
    version = json.loads(pkg)["version"]

    if OUT.exists():
        shutil.rmtree(OUT)
    count = 0
    for src, dest in FILES.items():
        write(content / src, OUT / dest, version)
        count += 1
    for src, dest in FOLDERS.items():
        for f in pages(content / src):
            write(f, OUT / dest / re.sub(r"^\d+-", "", f.name), version)
            count += 1
    for src, dest in SKILLS.items():
        text = subprocess.run(["git", "-C", str(root), "show", f"HEAD:{src}"],
                              capture_output=True, text=True, check=True).stdout
        (OUT / dest).write_text(FRONTMATTER.sub("", text).lstrip())
        count += 1
    for src, (dest, title) in MERGED.items():
        parts = [demote(clean(f.read_text(), version)) for f in pages(content / src)]
        names = [re.match(r"## (.+)", part).group(1) for part in parts]
        index = "".join(f"- {name}\n" for name in names)
        (OUT / dest).write_text(f"# {title}\n\n## Contents\n\n{index}\n" + "\n".join(parts))
        count += 1

    rev = subprocess.run(["git", "-C", str(root), "rev-parse", "--short", "HEAD"],
                         capture_output=True, text=True).stdout.strip()
    (OUT / "SOURCE.md").write_text(
        f"Generated by tools/sync_docs.py from {REPO} ({BRANCH} @ {rev}, htmx {version}).\n"
        "Do not edit by hand; rerun the script to refresh.\n")
    if tmp:
        shutil.rmtree(tmp)
    print(f"wrote {count} files to {OUT}")


if __name__ == "__main__":
    main()
