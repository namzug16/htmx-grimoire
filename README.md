# htmx-grimoire

An agent skill for writing, reviewing and debugging **new htmx 4 projects** without loading the full htmx docs.

## What is in it

The skill lives in [`htmx-grimoire/`](htmx-grimoire/):

- **`SKILL.md`**: a compact htmx 4 checklist: surprising defaults, core attributes, server contract,
  approach selection, pattern index and final review checklist.
- **`references/`**, curated from the official htmx docs (`four-dev` branch, htmx 4.0.0):
  - `patterns/`: 19 UI patterns such as active search, infinite scroll, inline edit, dialogs and LLM streaming
  - `guides/hx-live.md`: the hx-live guide
  - `extensions/hx-live.md`: the hx-live extension reference

The full API docs, general narrative docs, extension catalogue, and htmx 2 → 4 migration material are intentionally
not bundled. This skill is optimized for starting new htmx 4 projects with low token overhead, not for migrations.

## How it differs from `htmx-guidance`

`htmx-guidance` is a single 745-line `SKILL.md` that summarises htmx 4 inline. This skill takes a different shape:

| | `htmx-guidance` | `htmx-grimoire` |
|---|---|---|
| Layout | One file, everything inline | Compact core file plus a small curated pattern/hx-live reference set |
| Source of exact syntax | A hand-written summary | Compact htmx 4 rules plus official worked patterns |
| Emphasis | Attribute-by-attribute overview | New-project correctness: `:inherited`, server fragments, status handling, streaming and hx-live |
| Upgrades and debugging | A section on htmx 2 vs 4 differences | Not a migration skill; migration docs are deliberately excluded |
| When it triggers | Requests that mention htmx | Also hypermedia-style requests that do not name htmx (active search, inline edit, token streaming "without a JS framework") |

Earlier versions bundled almost the entire official documentation. In a small benchmark that improved checked htmx 4
correctness only marginally, while roughly doubling runtime and token use because agents read reference files. The
current version keeps the high-signal parts: the compact checklist, official patterns, and hx-live docs.

## Install

Install with the Skills CLI:

```sh
npx skills add namzug16/htmx-grimoire
```

To install only this skill explicitly:

```sh
npx skills add namzug16/htmx-grimoire --skill htmx-grimoire
```

## Updating the references

`references/` is generated as a curated subset; do not edit it by hand. To refresh it from upstream:

```sh
python3 tools/sync_docs.py
```

This clones the `four-dev` branch of [bigskysoftware/htmx](https://github.com/bigskysoftware/htmx) and rebuilds only
the pattern and hx-live references. `references/SOURCE.md` records the commit and htmx version it was built from.

## Credits

The bundled references are the htmx documentation from [bigskysoftware/htmx](https://github.com/bigskysoftware/htmx),
reformatted as plain markdown.
