# htmx-grimoire

An agent skill for writing, reviewing and debugging **htmx 4**.

## What is in it

The skill lives in [`htmx-grimoire/`](htmx-grimoire/):

- **`SKILL.md`**: the htmx 4 behaviours that surprise people, the htmx 2 names and their replacements,
  core vocabulary, the server's half of the contract, how to choose an approach, and a checklist to run before
  handing code over.
- **`references/`**, generated from the official htmx docs (`four-dev` branch, htmx 4.0.0):
  - `api/`: one page per attribute, plus events, headers, config, JavaScript methods and tags
  - `patterns/`: 19 UI patterns such as active search, infinite scroll, inline edit, dialogs and LLM streaming
  - `extensions/`: 17 extensions, including `hx-sse`, `hx-ws`, `hx-live` and `htmx-2-compat`
  - `guides/`: upgrading from htmx 2, debugging, morphing, events, `hx-live` and more
  - `docs.md`: the main htmx documentation page

## How it differs from `htmx-guidance`

`htmx-guidance` is a single 745-line `SKILL.md` that summarises htmx 4 inline. This skill takes a different shape:

| | `htmx-guidance` | `htmx-grimoire` |
|---|---|---|
| Layout | One file, everything inline | Shorter core file plus 89 reference files loaded on demand |
| Source of exact syntax | A hand-written summary | The official docs, bundled |
| Emphasis | Attribute-by-attribute overview | Leads with what fails quietly in htmx 4 (explicit `:inherited`, renamed attributes and events) |
| Upgrades and debugging | A section on htmx 2 vs 4 differences | Step-by-step upgrade and debugging guides |
| When it triggers | Requests that mention htmx | Also hypermedia-style requests that do not name htmx (active search, inline edit, token streaming "without a JS framework") |

In a small benchmark (3 tasks, 3 runs each, graded with mechanical checks for htmx 4 correctness), output written
with `htmx-grimoire` passed 100% of the checks against 96% for `htmx-guidance`. It also took about twice as long and
used about twice the tokens (188s vs 96s and 101k vs 58k tokens on average), because the agent reads reference files.
The sample is small; treat the numbers as an indication only.

## Install

Give your agent this URL and ask it to install the skill:

```
https://github.com/namzug16/htmx-grimoire
```

For example: "Install the skill from https://github.com/namzug16/htmx-grimoire".

To install by hand, copy the `htmx-grimoire/` folder into your agent's skills directory. For Claude Code:

```sh
git clone https://github.com/namzug16/htmx-grimoire
cp -r htmx-grimoire/htmx-grimoire ~/.claude/skills/
```

Use `.claude/skills/` inside a project instead to install it for that project only.

## Updating the references

`references/` is generated; do not edit it by hand. To refresh it from upstream:

```sh
python tools/sync_docs.py
```

This clones the `four-dev` branch of [bigskysoftware/htmx](https://github.com/bigskysoftware/htmx) and rebuilds
`htmx-grimoire/references/`. `references/SOURCE.md` records the commit and htmx version it was built from.

## Credits

The bundled references are the htmx documentation from [bigskysoftware/htmx](https://github.com/bigskysoftware/htmx),
reformatted as plain markdown.
