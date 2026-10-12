---
name: htmx-grimoire
description: Write, review and debug htmx 4 code, with accurate htmx 4 syntax and the full official docs, patterns and extension references bundled. This skill covers htmx 4 only. Use it whenever the task touches htmx 4 in any way - hx-* attributes in HTML or server templates (Jinja, Django, ERB, Blade, Go templates, Thymeleaf, JSX/templ, etc.), endpoints that return HTML fragments, HX-* request/response headers, hx-live or hx-on scripting, SSE/WebSocket streaming of HTML, htmx extensions, or moving a codebase up to htmx 4. Also use it when the user asks for hypermedia-style UI without naming htmx (active search, infinite scroll, inline edit, lazy loading, modals, tabs, polling, progress bars, live updates, LLM token streaming "without a JS framework"). htmx 4 changed many defaults and names, so answers from memory are usually outdated and subtly wrong - consult this skill even for small htmx snippets.
---

# htmx

htmx lets any element issue an HTTP request on any event and swap the **HTML** response anywhere in the DOM. The server
renders HTML fragments; there is no JSON layer and no client-side state store. Good htmx code is mostly a matter of
choosing a trigger, a target and a swap, then having the server return the right fragment.

This skill is for **htmx 4 only**. Every example, default and name in it is htmx 4, and everything you write with it
should be too. Most htmx material in the wild (and in your memory) predates htmx 4, and a lot of it silently does the
wrong thing now. Sections 1 and 2 exist to correct that; skim them every time.

If the project turns out to be on an older htmx and the user is not asking to move to 4, say so and stop relying on
this skill for syntax: its contents would be wrong there.

- Upgrading a codebase to htmx 4: follow `references/guides/upgrade-from-htmx-2.md` step by step (it starts with the
  automated checker, `npx htmx.org@4 upgrade-check ./path`). The `htmx-2-compat` extension allows a gradual move.
- Debugging ("nothing happens", wrong content swapped): work through `references/guides/debugging.md`. First moves
  are `htmx.config.logAll = true` and the Network tab.

Install:

```html
<script src="https://cdn.jsdelivr.net/npm/htmx.org@4.0.0/dist/htmx.min.js"></script>
<!-- extensions are plain scripts loaded after htmx; there is no hx-ext attribute -->
<script src="https://cdn.jsdelivr.net/npm/htmx.org@4.0.0/dist/ext/hx-sse.min.js"></script>
```

Load htmx with a normal blocking `<script>` in `<head>`. `htmax.js` is a single-file bundle of htmx plus the popular
extensions (`references/guides/htmax.md`).

## 1. The behaviours that surprise people in htmx 4

These are the defaults that differ from older htmx or from intuition. Each one produces code that looks right and fails
quietly, which is why they are worth checking on every task.

**Inheritance is explicit.** An attribute on a parent does nothing for its children unless it carries `:inherited`.

```html
<!-- children do NOT pick up the target -->
<div hx-target="#out"> <button hx-get="/a">A</button> </div>

<!-- children do -->
<div hx-target:inherited="#out"> <button hx-get="/a">A</button> </div>
```

This applies to every attribute, including `hx-boost`, `hx-confirm`, `hx-headers` (CSRF tokens on `<body>`!),
`hx-swap`, `hx-include`, `hx-sync`. A child can extend rather than override an inherited value with `:append`
(`hx-vals:append="source:btn"`).

**Error responses are swapped.** Every status swaps except `204` and `304`. A `422` or `500` with an HTML body lands in
the target. So render error responses as deliberate fragments, and route them with `hx-status`:

```html
<form hx-post="/register" hx-target="#result"
      hx-status:422="target:#errors"
      hx-status:5xx="swap:none">
```

`hx-status` keys: `swap:`, `target:`, `select:`, `push:`, `replace:`, `transition:`. Most specific pattern wins
(`404` over `50x` over `5xx`). The server should answer validation failures with `422` plus the error HTML.

**GET and DELETE do not send the enclosing form.** Only requests with a body (`POST`, `PUT`, `PATCH`, `QUERY`) include
it. Add `hx-include="closest form"` when a `hx-get`/`hx-delete` button needs those values. An element's own `value`
is always sent (so `hx-get` on an `<input>` or `<select>` works as expected).

**OOB and partial swaps run after the main swap**, in document order. Do not rely on an out-of-band element existing
before the main content lands.

**A response made only of `hx-swap-oob` / `<hx-partial>` elements leaves the main target alone.** Handy for "update
three things, replace nothing". Add `swapEmpty:true` to `hx-swap` if you do want the target emptied.

**History re-fetches the page.** There is no local snapshot. Any URL you push with `hx-push-url` must return a full
page when requested directly, and the back button costs a request. `hx-history-elt` limits what is restored.

**Requests are same-origin and time out at 60s.** Cross-origin needs `htmx.config.mode = "cors"` globally;
`hx-config` cannot widen it. Long requests need `hx-config="timeout:5m"` or a streaming extension.

**Selectors with spaces need quotes in `hx-trigger`.** `from:'closest form'`, `target:'.a, .b'`. The older
parentheses form `from:(closest form)` does not parse.

**`hx-disable` changed meaning.** In 4 it disables elements during a request (the old `hx-disabled-elt`). The old
"do not process this subtree" meaning is now `hx-ignore`.

**Morph swaps keep user input.** `innerMorph`/`outerMorph` preserve focus, scroll and typed values, so they cannot
reset a form. Use `outerHTML`/`innerHTML` when you want a clean slate. Morphing matches on `id`, so give stable ids.

**No upload progress.** htmx 4 uses `fetch()`, which does not report it. Use a dedicated uploader if progress matters.

**Inline JS needs eval.** `hx-on`, trigger filters (`click[ctrlKey]`) and `js:` values use `new Function()`. Under a
strict CSP, use the `hx-csp` extension (`references/extensions/hx-csp.md`).

## 2. Outdated names and their htmx 4 replacements

The left column is what memory tends to produce. None of it is valid here; write the right column.

| Outdated (do not write) | htmx 4 |
|---|---|
| `hx-target="#x"` on a parent | `hx-target:inherited="#x"` |
| `htmx:afterSwap`, `htmx:beforeRequest`, `htmx:configRequest` | `htmx:after:swap`, `htmx:before:request`, `htmx:config:request` |
| `htmx:load`, `htmx:afterOnLoad` | `htmx:after:init` (or `htmx.onLoad()`) |
| `htmx:responseError`; `htmx:sendError`/`swapError`/`timeout` | `htmx:response:error`; all others are `htmx:error` |
| `evt.detail.xhr`, `evt.detail.target`, `evt.detail.parameters`, `evt.detail.headers` | `evt.detail.ctx` (`ctx.sourceElement`, `ctx.target`, `ctx.request.body`, `ctx.request.headers`, `ctx.response`) |
| `hx-ext="sse"` | include the extension script, nothing else |
| `sse-connect`, `sse-swap`, `ws-connect`, `ws-send` | `hx-sse:connect`, `hx-ws:connect`, `hx-ws:send` (rewritten; read the extension doc) |
| `hx-disabled-elt` | `hx-disable` |
| `hx-disable` | `hx-ignore` |
| `hx-request='{"timeout":5000}'` | `hx-config="timeout:5s"` |
| `hx-vars`, `hx-params` | `hx-vals` with `js:` prefix; `htmx:config:request` |
| `hx-prompt` | `hx-prompt` extension |
| `hx-trigger="click queue:all"` | `hx-sync="this:queue all"` |
| `hx-swap="innerHTML show:#el:top"` | `hx-swap="innerHTML show:top showTarget:#el"` |
| `HX-Trigger` request header, `HX-Trigger-Name` | `HX-Source` (format `tag#id`); `HX-Target` is also `tag#id` |
| `HX-Trigger-After-Swap` / `-After-Settle` | `HX-Trigger` |
| `htmx.config.defaultSwapStyle`, `globalViewTransitions`, `historyEnabled`, `timeout` | `defaultSwap`, `transitions`, `history`, `defaultTimeout` |
| `responseHandling` config | `hx-status:*` attributes + `htmx.config.noSwap` |
| `htmx.defineExtension`, `htmx.addClass/removeClass/closest/remove/off`, `htmx.logAll()` | `htmx.registerExtension`, native DOM methods, `htmx.config.logAll = true` |
| idiomorph extension | built-in `innerMorph` / `outerMorph` |

The full catalogue is `references/guides/whats-new-in-htmx-4.md`.

## 3. Core vocabulary

Requests: `hx-get`, `hx-post`, `hx-put`, `hx-patch`, `hx-delete`, `hx-query` (or `hx-action` + `hx-method`).
Default trigger: `change` for `input`/`textarea`/`select`, `submit` for `form`, `click` for everything else.

**`hx-trigger`** - `event[filter] modifier...`, comma-separated for several.
Modifiers: `once`, `changed`, `delay:500ms` (debounce), `throttle:1s`, `from:<sel>`, `target:<sel>`, `prevent`,
`stop`, `halt`, `capture`, `passive`. Synthetic events: `load`, `revealed`, `intersect` (`root:`, `rootMargin:`,
`threshold:`), `every 2s`.

**`hx-target`** - CSS selector or extended selector: `this`, `closest <sel>`, `find <sel>`, `next [sel]`,
`previous [sel]`, `body`, `host`, `global <sel>`. Default is the element itself. Prefer relative selectors over
generated ids in repeated markup (table rows, list items).

**`hx-swap`** - default `innerHTML`.

| Style | Effect |
|---|---|
| `innerHTML` / `outerHTML` | replace the target's children / the target itself |
| `innerMorph` / `outerMorph` | merge into the existing DOM, preserving focus, input values, scroll, transitions |
| `outerSync` | morph the target's attributes, replace its children |
| `before`, `prepend`, `append`, `after` | insert relative to the target (aliases of `beforebegin`, `afterbegin`, `beforeend`, `afterend`) |
| `textContent` | set text, no HTML parsing |
| `delete` / `none` | remove the target / swap nothing (headers, OOB and partials still apply) |

Modifiers follow the style: `swap:200ms`, `settle:100ms`, `transition:true`, `scroll:top|bottom`,
`show:top|bottom`, `scrollTarget:<sel>`, `showTarget:<sel>`, `focusScroll:true`, `ignoreTitle:true`, `strip:true`,
`swapEmpty:true`, `target:<sel>`.

**Other attributes** - `hx-select` / `hx-select-oob` (pick parts of the response), `hx-include`, `hx-vals`,
`hx-headers`, `hx-indicator`, `hx-disable`, `hx-confirm`, `hx-sync`, `hx-push-url` / `hx-replace-url`, `hx-boost`,
`hx-preserve`, `hx-encoding`, `hx-validate`, `hx-config`, `hx-ignore`, `hx-on`. Each has a page in
`references/api/attributes/`.

Structured values (`hx-vals`, `hx-headers`, `hx-config`, the config meta tag, swap/trigger modifiers) are HCON:
`key:value key2:"two words" flag`, or plain JSON. Prefix with `js:` to evaluate at request time:
`hx-vals='js:{y: window.scrollY}'`.

## 4. The server's half of the contract

htmx code is only half written until the endpoint is. When you write or describe an interaction, always say what
the server returns: the status code, the fragment, and any `HX-*` headers.

- **Return fragments, not JSON, not full pages**, for htmx requests. `HX-Request: true` marks them.
  `HX-Request-Type` is `partial` for a targeted swap and `full` when the target is `body` (boosted links, history
  restore) or `hx-select` is in use, so a single route can serve both: full layout for `full` or non-htmx requests,
  bare fragment for `partial`. Send `Vary: HX-Request` (or `HX-Request-Type`) if the response is cacheable.
- **Use real status codes.** `422` with the re-rendered form for validation errors, `204` for "nothing to swap",
  `200` with an empty body to make an `outerHTML` target disappear.
- **Escape user content.** Injected HTML can carry `hx-*` attributes; wrap any raw user HTML in `hx-ignore`.
- **Send the CSRF token** with `hx-headers:inherited` on `<body>` or `<html>`.
- **Response headers steer the client**: `HX-Trigger` (fire client events, with optional JSON detail),
  `HX-Retarget`, `HX-Reswap`, `HX-Reselect`, `HX-Push-Url`, `HX-Replace-Url`, `HX-Location` (client-side navigate
  without reload), `HX-Redirect` (full navigation), `HX-Refresh`. They are ignored on 3xx responses, so reply 2xx.
  A plain `302` to a login page gets followed by `fetch()` and swapped into the target; use `HX-Redirect` instead.

Match the project's server stack and template language. If none is evident, show the raw HTML the endpoint returns
and keep the handler pseudo-code minimal rather than inventing a framework.

## 5. Choosing an approach

**Updating more than one region** (in rough order of preference):

1. Widen the target so one fragment covers both regions. Simplest; nothing to coordinate.
2. `hx-swap-oob="true"` on an extra element in the response: replaces the element with the same `id`. Best for
   one-for-one replacement (a counter, a flash message). Table rows and `<li>` need a `<template>` wrapper.
3. `<hx-partial hx-target="#list" hx-swap="beforeend">...</hx-partial>`: any selector, any swap style, any content.
   Use when the piece is not keyed by id or needs append/prepend. Write it as
   `<template hx-type="partial" ...>` if the template engine strips unknown tags.
4. `HX-Trigger: contactAdded` response header plus `hx-trigger="contactAdded from:body"` on the regions that should
   refresh themselves. Costs an extra request per listener but decouples the endpoint from the page layout.

**Concurrent requests**: `hx-sync="<selector>:<strategy>"` with `drop`, `abort`, `replace`,
`queue first|last|all`. State the strategy explicitly rather than leaning on the default (the docs and the 4.0.0
source disagree about what it is). Typical: `hx-sync="this:replace"` on a search box so stale responses never win.

**Loading states**: while a request is in flight htmx adds the `htmx-request` class to the requesting element (or
to the elements named by `hx-indicator`), and `hx-disable` sets `disabled` on the elements it selects (`"this"`,
`"find button"`, `"closest fieldset"`) for the same period. A loading button is just CSS keyed on that class:

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

- Use your own classes with `display` when the label should be replaced. The built-in `htmx-indicator` class fades
  opacity and keeps its space, which suits a spinner sitting beside the label:
  `<button hx-post="/save">Save <img class="htmx-indicator" src="/spinner.svg" alt=""></button>`.
- For a submit button inside `<form hx-post>`, the form is the requesting element. The CSS above still works
  because the class is on an ancestor; disable with `hx-disable="find button"` on the form.
- To avoid a flash on fast responses, add a transition delay
  (`references/api/attributes/hx-indicator.md`, "Delaying the Indicator"). For placeholder content or optimistic UI
  rather than a busy button, use the `hx-pending` extension (`references/extensions/hx-pending.md`).

**Client-side behaviour**, lightest tool first:

1. Plain HTML and CSS: `<dialog>` with `command`/`commandfor`, `<details>`, `:has()`, `popover`.
2. `hx-on:<event>="..."` inline handlers. `this` is the element, `event` the event, and for htmx events `ctx` is in
   scope. `hx-on::after:request` is shorthand for `hx-on:htmx:after:request`.
3. The `hx-live` extension for reactive bits: `q('next input')`, `toggle()`, `take()`, `data.count++`,
   `:text="..."`, `:hidden="..."`. Read `references/guides/hx-live.md` before writing any of it; the API is new and
   not guessable.
4. Alpine.js or hyperscript if the project already uses them (`hx-alpine-compat` extension for Alpine).
5. A real JS widget, initialised in `htmx.onLoad(elt => ...)` so it also runs on swapped-in content.

Reaching for `htmx.ajax()` or hand-written `fetch` + DOM updates is usually a sign that an attribute would do.

**Server push / streaming**: polling (`hx-trigger="every 2s"`, or `load delay:1s` for self-terminating polls) is the
simplest and often enough. For real streaming prefer SSE (`hx-sse`): a normal `hx-get`/`hx-post` whose response is
`text/event-stream` streams into its target, and `hx-sse:connect` holds a reconnecting connection open. WebSockets
(`hx-ws`) only when the client must also push. Read the extension doc first; all three were rewritten for htmx 4.

**Navigation**: `hx-boost:inherited="true"` on a container turns links and forms into body swaps with history.
It is optional and somewhat controversial; do not add it unless asked or already in use.

## 6. Bundled references

Everything under `references/` is generated from the official htmx 4 docs (see `references/SOURCE.md`). Read the
relevant file before writing anything beyond the basics above; guessing at htmx 4 details is how outdated syntax leaks in.

**Patterns** - complete worked examples with client markup and server response. When the task matches one, start
from it rather than composing from scratch.

| Need | File in `references/patterns/` |
|---|---|
| Search as you type | `active-search.md` |
| Inline field validation | `active-validation.md` |
| Checkbox table with bulk actions | `bulk-actions.md` |
| "Load more" button / infinite scroll | `click-to-load.md`, `infinite-scroll.md` |
| Inline edit / delete a row | `edit-in-place.md`, `delete-in-place.md` |
| Modals | `dialogs.md` |
| Tabs | `tabs.md` |
| Deferred / lazy content | `lazy-load.md` |
| Dependent dropdowns | `linked-selects.md` |
| Polling, job progress | `polling.md`, `progress-bar.md` |
| Server push (ticker, notifications) | `live-updates.md` |
| LLM / chat token streaming | `llm-streaming-response.md` |
| File upload | `file-upload.md` |
| Clear a form after submit | `reset-on-submit.md` |
| Keyboard shortcuts | `keyboard-shortcuts.md` |
| Drag to reorder | `drag-to-reorder.md` |

**Guides** in `references/guides/`

| File | Read when |
|---|---|
| `hx-live.md` | writing any client-side scripting with `q()`, `data`, `:attr` bindings, `hx-live` |
| `events.md` | listening to, cancelling or modifying requests/swaps in JS; the `ctx` object |
| `morphing.md` | using or debugging `innerMorph`/`outerMorph`, `hx-morph-skip` |
| `hcon.md` | unsure how to quote a structured attribute value |
| `debugging.md` | a request does not fire, a swap does not happen, or the wrong content lands |
| `upgrade-from-htmx-2.md` | carrying out a 2 to 4 migration in a codebase (ordered steps, search patterns) |
| `whats-new-in-htmx-4.md` | the exhaustive list of renames/removals; translating an older example into htmx 4 |
| `extension-authoring.md`, `extension-migration.md` | writing or porting an extension |
| `htmax.md` | using the all-in-one bundle |

**API** in `references/api/`

- `attributes/<name>.md` - one page per attribute (`hx-swap.md`, `hx-trigger.md`, `hx-on.md`, `hx-sync.md`,
  `hx-status.md`, `hx-swap-oob.md`, `hx-boost.md`, ...). The authority on exact syntax.
- `events.md`, `headers.md`, `config.md`, `methods.md`, `tags.md` - one file per category with a contents list;
  grep for the heading you need (for example `## HX-Location`, `## htmx:config:request`, `## htmx.ajax()`).

**Extensions** in `references/extensions/` - `hx-sse.md`, `hx-ws.md`, `hx-multipart.md` (streaming);
`hx-live.md` (full hx-live reference), `hx-pending.md`, `hx-prompt.md`, `hx-browser-indicator.md` (UX);
`hx-preload.md`, `hx-history-cache.md`, `hx-ptag.md` (performance); `hx-download.md`, `hx-head.md`,
`hx-targets.md`, `hx-upsert.md` (swaps); `hx-csp.md` (security); `htmx-2-compat.md`, `hx-alpine-compat.md`.
Suggest one when it removes hand-written code, and always include its `<script>` tag when you use it. If the
project sets the `extensions` config whitelist, the extension's registration name must be on it, and that is not
always the file name (`hx-sse.js` registers as `sse`, `hx-preload.js` as `preload`).

**`references/docs.md`** - the full narrative documentation (about 2000 lines, contents list at the top). Use it for
topics not covered above: security and CSP, caching, web components, view transitions, history, boosting.

## 7. Before you hand over htmx code

A short self-check that catches most real bugs:

- Does any attribute on a parent need `:inherited`?
- Are event names colon-separated, and is `detail.ctx` used rather than `detail.xhr`?
- For each request: is the server response described (status, fragment, headers), and is it a fragment rather than
  a full page or JSON?
- What happens on a 4xx/5xx? Is the error HTML going somewhere sensible?
- Do `hx-get`/`hx-delete` elements that need form values have `hx-include`?
- Does every `id` targeted by `hx-target`, `hx-swap-oob` or a morph still exist after the swap? (`outerHTML` on a
  target whose replacement lacks the id breaks the next request.)
- Is each used extension's script included after htmx?
- Slow request: is there an indicator or a disabled state?
