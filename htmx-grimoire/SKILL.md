---
name: htmx-grimoire
description: Write, review and debug new htmx 4 code with a compact htmx 4 checklist, curated UI patterns, and hx-live references. Use for htmx 4 snippets, server-rendered HTML fragments, hx-* attributes, HX-* headers, hx-live scripting, SSE/WebSocket HTML streaming, and hypermedia UI patterns such as active search, inline edit, infinite scroll, modals, polling, progress bars, live updates, or LLM token streaming without a JS framework. This skill is optimized for starting new htmx 4 projects, not migrating older htmx codebases.
---

# htmx 4 compact guide

htmx lets any element issue an HTTP request on any event and swap the **HTML** response anywhere in the DOM. The server
returns HTML fragments, not JSON view-models.

This skill is for **new htmx 4 code**. Do not use it as a migration playbook for htmx 1/2/3 projects.

Install:

```html
<script src="https://cdn.jsdelivr.net/npm/htmx.org@4.0.0/dist/htmx.min.js"></script>
```

Extensions are normal scripts loaded after htmx; there is no `hx-ext` attribute:

```html
<script src="https://cdn.jsdelivr.net/npm/htmx.org@4.0.0/dist/ext/hx-sse.min.js"></script>
```

## Load references sparingly

Do **not** read the whole reference tree by default. Start from this file. Read one pattern only when the task directly
matches it. Read the hx-live guide/reference only before writing hx-live code.

- `references/patterns/` - worked examples for common UI flows.
- `references/guides/hx-live.md` - hx-live guide.
- `references/extensions/hx-live.md` - hx-live extension reference.

## htmx 4 rules that most often prevent bugs

**Inheritance is explicit.** A parent attribute does nothing for children unless it has `:inherited`.

```html
<div hx-target:inherited="#out">
  <button hx-get="/contacts">Load</button>
</div>
```

This matters for `hx-target`, `hx-swap`, `hx-headers` (CSRF), `hx-include`, `hx-sync`, `hx-boost`, `hx-confirm`, etc.

**Error responses are swapped.** Every status swaps except `204` and `304`. Return deliberate error fragments and route
them with `hx-status` when needed.

```html
<form hx-post="/register" hx-target="#result"
      hx-status:422="target:#errors"
      hx-status:5xx="swap:none">
```

**GET and DELETE do not include enclosing form fields.** Add `hx-include="closest form"` when a `hx-get` or `hx-delete`
button needs form values. The requesting element's own value is still sent.

**Event names use colon segments.** Examples: `htmx:after:swap`, `htmx:before:request`, `htmx:config:request`,
`htmx:response:error`. In event handlers, use `event.detail.ctx`, not old `xhr`/`target`/`parameters` fields.

**OOB and partial swaps happen after the main swap**, in document order. A response made only of `hx-swap-oob` or
`<hx-partial>` elements leaves the main target alone unless `hx-swap="... swapEmpty:true"` is set.

**History re-fetches the page.** A URL pushed with `hx-push-url` must also work as a direct full-page request.

**Requests are same-origin and time out after 60s.** Cross-origin requires `htmx.config.mode = "cors"` globally. Long
requests need `hx-config="timeout:5m"` or streaming.

**Selectors with spaces in `hx-trigger` need quotes.** Use `from:'closest form'`, not old parenthesized syntax.

**Morph swaps preserve user input.** `innerMorph`/`outerMorph` keep focus, scroll and typed values. Use `innerHTML` or
`outerHTML` when you want a clean reset.

**Inline JS needs eval.** `hx-on`, trigger filters and `js:` values use `new Function()`. Avoid them under strict CSP
unless the project intentionally uses the `hx-csp` extension.

## Core attributes

Requests: `hx-get`, `hx-post`, `hx-put`, `hx-patch`, `hx-delete`, `hx-query`.

Default trigger: `change` for `input`/`textarea`/`select`, `submit` for `form`, `click` for everything else.

`hx-trigger="event[filter] modifier..."` supports `once`, `changed`, `delay:500ms`, `throttle:1s`, `from:<sel>`,
`target:<sel>`, `prevent`, `stop`, `halt`, `capture`, `passive`, plus synthetic `load`, `revealed`, `intersect`,
`every 2s`.

`hx-target` accepts CSS selectors plus `this`, `closest <sel>`, `find <sel>`, `next [sel]`, `previous [sel]`, `body`,
`host`, `global <sel>`. Prefer relative selectors in repeated rows/cards.

`hx-swap` defaults to `innerHTML`. Common styles: `innerHTML`, `outerHTML`, `innerMorph`, `outerMorph`, `outerSync`,
`before`, `prepend`, `append`, `after`, `textContent`, `delete`, `none`. Common modifiers: `swap:200ms`,
`settle:100ms`, `transition:true`, `scroll:top|bottom`, `show:top|bottom`, `scrollTarget:<sel>`, `showTarget:<sel>`,
`focusScroll:true`, `ignoreTitle:true`, `strip:true`, `swapEmpty:true`, `target:<sel>`.

Structured values (`hx-vals`, `hx-headers`, `hx-config`, swap/trigger modifiers) use HCON (`key:value key2:"two words"`)
or JSON. Prefix with `js:` only when a value must be evaluated at request time.

## Server contract

Every htmx interaction needs the server half specified:

- Return HTML fragments for htmx partial requests. Use `HX-Request: true` / `HX-Request-Type` when branching between
  full-page and fragment responses. Add `Vary: HX-Request` or `Vary: HX-Request-Type` for cacheable responses.
- Use real status codes: `422` with re-rendered form errors, `204` for no swap, `200` with empty body to erase an
  `outerHTML` target.
- Escape user content. If raw user HTML is displayed, wrap it with `hx-ignore`.
- Send CSRF tokens via `hx-headers:inherited` on `<body>` or `<html>`.
- Response headers can steer the client: `HX-Trigger`, `HX-Retarget`, `HX-Reswap`, `HX-Reselect`, `HX-Push-Url`,
  `HX-Replace-Url`, `HX-Location`, `HX-Redirect`, `HX-Refresh`. They are ignored on 3xx responses; reply 2xx.

## Choosing an approach

**Updating multiple regions**, simplest first:

1. Widen the target so one fragment covers all changed regions.
2. Add `hx-swap-oob="true"` elements in the response for one-for-one replacements by `id`.
3. Use `<hx-partial hx-target="#list" hx-swap="beforeend">...</hx-partial>` for arbitrary extra swaps.
4. Use `HX-Trigger` plus listeners such as `hx-trigger="contactAdded from:body"` when regions should refresh
   independently.

**Concurrent requests:** use `hx-sync="<selector>:<strategy>"` with `drop`, `abort`, `replace`, or `queue first|last|all`.
Typical search input: `hx-sync="this:replace"` so stale responses do not win.

**Loading states:** while a request is in flight, htmx adds `htmx-request` to the requesting element or `hx-indicator`
targets. `hx-disable` disables matching controls until the request settles.

```html
<button hx-post="/save" hx-disable="this">
  <span class="idle">Save</span>
  <span class="busy">Saving…</span>
</button>
```

```css
.busy { display: none; }
.htmx-request .idle, .htmx-request.idle { display: none; }
.htmx-request .busy, .htmx-request.busy { display: inline; }
```

**Client-side behaviour**, lightest first:

1. HTML/CSS: `<dialog>`, `<details>`, `popover`, `:has()`.
2. `hx-on:<event>="..."` for tiny inline behaviour. `this` is the element; `event.detail.ctx` has htmx context.
3. `hx-live` for local reactive behaviour. Read `references/guides/hx-live.md` first; do not guess the API.
4. A real JS widget initialized with `htmx.onLoad(elt => ...)` so swapped-in content is initialized too.

**Server push / streaming:** polling is usually enough (`hx-trigger="every 2s"`). For real streaming prefer SSE
(`hx-sse`): stream HTML into a target, or keep a reconnecting `hx-sse:connect` open. Use WebSockets only when the
client must also push data.

**Navigation:** `hx-boost:inherited="true"` turns links/forms under a container into body swaps with history. Do not add
it unless requested or already used.

## Pattern reference index

Read only the matching file:

| Need | File |
|---|---|
| Search as you type | `references/patterns/active-search.md` |
| Inline validation | `references/patterns/active-validation.md` |
| Checkbox table actions | `references/patterns/bulk-actions.md` |
| Load more / infinite scroll | `references/patterns/click-to-load.md`, `references/patterns/infinite-scroll.md` |
| Inline edit / delete | `references/patterns/edit-in-place.md`, `references/patterns/delete-in-place.md` |
| Modals | `references/patterns/dialogs.md` |
| Tabs | `references/patterns/tabs.md` |
| Lazy content | `references/patterns/lazy-load.md` |
| Dependent dropdowns | `references/patterns/linked-selects.md` |
| Polling / progress | `references/patterns/polling.md`, `references/patterns/progress-bar.md` |
| Live updates | `references/patterns/live-updates.md` |
| LLM/chat token streaming | `references/patterns/llm-streaming-response.md` |
| File upload | `references/patterns/file-upload.md` |
| Reset form after submit | `references/patterns/reset-on-submit.md` |
| Keyboard shortcuts | `references/patterns/keyboard-shortcuts.md` |
| Drag to reorder | `references/patterns/drag-to-reorder.md` |

## Final self-check

- Parent attributes that should affect children use `:inherited`.
- Event names are htmx 4 names, and JS uses `event.detail.ctx`.
- Each request has a clear server response: status, fragment, headers.
- 4xx/5xx responses land somewhere intentional.
- `hx-get`/`hx-delete` controls that need form values have `hx-include`.
- Targets and OOB ids still exist after swaps.
- Used extensions have scripts loaded after htmx.
- Slow requests have loading/disabled states.
