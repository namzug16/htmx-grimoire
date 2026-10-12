# What's New in htmx 4

> An exhaustive catalog of everything that changed in htmx 4.0.

## Contents

- Breaking Changes
  - `fetch()` replaces `XMLHttpRequest`
  - Explicit inheritance
  - Error responses swap
  - `hx-delete` excludes form data
  - No history cache
  - OOB swap order
  - `hx-trigger` `queue` modifier removed
  - `hx-trigger` `from:` and `target:` selector quoting
  - 60-second timeout
  - Extension loading
- Renames and Removals
  - Attributes
  - Events
  - Config
  - Request headers
  - Response headers
  - JavaScript API
- What's New
  - Attributes
  - `hx-swap` scroll modifiers
  - `hx-swap` styles
  - Status code swaps
  - `<hx-partial>`
  - View transitions
  - JSX compatibility
  - JavaScript methods
  - Auto-logged events
  - Request Context in Events
  - Events
  - Config keys
  - Core extensions

## Breaking Changes

### `fetch()` replaces `XMLHttpRequest`

All requests use the native [`fetch()` API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API). This cannot be
reverted.

### Explicit inheritance

Add `:inherited` to any attribute that should inherit down the DOM tree.

```html
<!-- htmx 2: implicit inheritance -->
<div hx-confirm="Are you sure?">
    <button hx-delete="/item/1">Delete</button>
</div>

<!-- htmx 4: explicit inheritance -->
<div hx-confirm:inherited="Are you sure?">
    <button hx-delete="/item/1">Delete</button>
</div>
```

Works on any attribute: `hx-boost``:inherited`, 
`hx-target``:inherited`, `hx-confirm``:inherited`,
etc.

Use `:append` to add to an inherited value instead of replacing it:

```html

<div hx-include:inherited="#global-fields">
    <!-- appends .extra to the inherited value -->
    <form hx-include:inherited:append=".extra">...</form>
</div>
```

Revert: `htmx.config.implicitInheritance` `= true`

### Error responses swap

htmx 4 swaps all HTTP responses. Only [`204`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/204)
and [`304`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/304) do not swap.

htmx 2 did not swap `4xx` and `5xx` responses. In htmx 4, if your server returns HTML with a `422` or `500`, that HTML
gets swapped into the target. Design your error responses to work as swap content, or use 
`hx-status` to control per-code behavior.

Revert: `htmx.config.noSwap` `= [204, 304, '4xx', '5xx']`

### `hx-delete` excludes form data

Like `hx-get`, `hx-delete` no longer includes the
enclosing form's inputs.

Fix: add `hx-include``="closest form"` where needed.

### No history cache

History no longer caches pages in [localStorage](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage).
When navigating back, htmx re-fetches the page and swaps it into `<body>`, or into the `[hx-history-elt]` element if
one is present, the same behavior as htmx 2.

Use `htmx.config.history` `= "reload"` for a full page reload instead. Use
`htmx.config.history = false` to disable.

### OOB swap order

In htmx 2, out-of-band (`hx-swap-oob`) elements swapped **before** the main
content.

In htmx 4, the main content swaps first. OOB and `<hx-partial>` elements swap after (in document order).

This matters if an OOB swap creates or modifies DOM that the main swap depends on. If your app relies on that ordering,
restructure so each swap is independent.

### `hx-trigger` `queue` modifier removed

The `queue` modifier on `hx-trigger` (e.g. `hx-trigger="click queue:all"`) no longer
works. Request queuing is now controlled exclusively by `hx-sync`.

```html
<!-- htmx 2 -->
<div hx-trigger="click queue:all" hx-get="/test">...</div>

<!-- htmx 4: use hx-sync instead -->
<div hx-trigger="click" hx-get="/test" hx-sync="this:queue all">...</div>
```

### `hx-trigger` `from:` and `target:` selector quoting

In htmx 2, selectors with spaces in `from:` used parentheses: `from:(form input)`. In htmx 4, HCON parses these
modifier values, so selectors containing spaces or commas must be wrapped in single quotes:

```html
<!-- htmx 2 -->
<input hx-trigger="keyup from:(closest form)">

<!-- htmx 4 -->
<input hx-trigger="keyup from:'closest form'">
```

Comma-separated selectors also need quoting: `target:'.a, .b'`.

### 60-second timeout

htmx 2 had no timeout (`0`). htmx 4 sets `defaultTimeout` to `60000`.

Revert: `htmx.config.defaultTimeout = 0`

### Extension loading

Include extension scripts directly. No attribute needed:

```html

<script src="/path/to/htmx.js"></script>
<script src="/path/to/ext/sse.js"></script>
```

Restrict which extensions can load:

```html

<meta name="htmx-config" content='{"extensions": "sse, ws"}'>
```

Extension authors use `htmx.registerExtension(name, methodMap)` to register.

See Extension System for details.

## Renames and Removals

### Attributes

Do the `hx-disable` rename **before** upgrading. In htmx 2, `hx-disable` meant "skip htmx processing on this element". In htmx 4, that role is `hx-ignore`, and `hx-disable` now does what `hx-disabled-elt` used to do.

| htmx 2.x          | htmx 4.x                                                                                           | Type    | Notes                                                                                              |
|-------------------|----------------------------------------------------------------------------------------------------|---------|----------------------------------------------------------------------------------------------------|
| [`hx-disable`](https://htmx.org/attributes/hx-disable/)           | `hx-ignore`                                                     | renamed | Rename this first to avoid conflicts.                                                              |
| [`hx-disabled-elt`](https://htmx.org/attributes/hx-disabled-elt/) | `hx-disable`                                                   | renamed | Rename this after `hx-disable` becomes `hx-ignore`.                                                |
| [`hx-vars`](https://htmx.org/attributes/hx-vars/)                 | `hx-vals`                                                         | removed | Use the `js:` prefix.                                                                              |
| [`hx-params`](https://htmx.org/attributes/hx-params/)             | `htmx:config:request`                                     | removed | Configure request parameters in the event.                                                         |
| [`hx-prompt`](https://htmx.org/attributes/hx-prompt/)             | `hx-prompt` extension                                                     | removed | You can also use a one-liner with `hx-on`.          |
| [`hx-ext`](https://htmx.org/attributes/hx-ext/)                   | —                                                                                                  | removed | Include extension scripts directly.                                           |
| [`hx-disinherit`](https://htmx.org/attributes/hx-disinherit/)     | —                                                                                                  | removed | Not needed. Inheritance is explicit.                                                               |
| [`hx-inherit`](https://htmx.org/attributes/hx-inherit/)           | —                                                                                                  | removed | Not needed. Inheritance is explicit.                                                               |
| [`hx-request`](https://htmx.org/attributes/hx-request/)           | `hx-config`                                                     | removed | —                                                                                                  |
| [`hx-history`](https://htmx.org/attributes/hx-history/)           | —                                                                                                  | removed | No [localStorage](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage).           |

### Events

All events follow a new pattern: `htmx:phase:action[:sub-action]`. Most error events are consolidated to `htmx:error`. HTTP error responses use `htmx:response:error`.

| htmx 2.x                    | htmx 4.x                                                                          | Type    | Notes                               |
|-----------------------------|-----------------------------------------------------------------------------------|---------|-------------------------------------|
| `htmx:afterOnLoad`          | `htmx:after:init`                            | renamed | —                                   |
| `htmx:afterProcessNode`     | `htmx:after:init`                            | renamed | —                                   |
| `htmx:afterRequest`         | `htmx:after:request`                      | renamed | —                                   |
| `htmx:afterSettle`          | `htmx:after:settle`                        | renamed | —                                   |
| `htmx:afterSwap`            | `htmx:after:swap`                            | renamed | —                                   |
| `htmx:beforeCleanupElement` | `htmx:before:cleanup`                    | renamed | —                                   |
| `htmx:beforeHistorySave`    | `htmx:before:history:update`      | renamed | —                                   |
| `htmx:beforeOnLoad`         | `htmx:before:init`                          | renamed | —                                   |
| `htmx:beforeProcessNode`    | `htmx:before:process`                    | renamed | —                                   |
| `htmx:beforeRequest`        | `htmx:before:request`                    | renamed | —                                   |
| `htmx:beforeSwap`           | `htmx:before:swap`                          | renamed | —                                   |
| `htmx:configRequest`        | `htmx:config:request`                    | renamed | —                                   |
| `htmx:historyCacheMiss`     | `htmx:before:history:restore`    | renamed | —                                   |
| `htmx:historyRestore`       | `htmx:before:history:restore`    | renamed | —                                   |
| `htmx:load`                 | `htmx:after:init`                            | renamed | —                                   |
| `htmx:oobAfterSwap`         | `htmx:after:swap`                            | renamed | —                                   |
| `htmx:oobBeforeSwap`        | `htmx:before:swap`                          | renamed | —                                   |
| `htmx:pushedIntoHistory`    | `htmx:after:history:push`       | renamed | —                                   |
| `htmx:replacedInHistory`    | `htmx:after:history:replace` | renamed | —                                   |
| `htmx:responseError`        | `htmx:response:error`                    | renamed | HTTP error responses use this event. |
| `htmx:sendError`            | `htmx:error`                                      | renamed | —                                   |
| `htmx:swapError`            | `htmx:error`                                      | renamed | —                                   |
| `htmx:targetError`          | `htmx:error`                                      | renamed | —                                   |
| `htmx:timeout`              | `htmx:error`                                      | renamed | —                                   |
| `htmx:validation:validate`  | —                                                                                 | removed | Use native browser form validation.  |
| `htmx:validation:failed`    | —                                                                                 | removed | Use native browser form validation.  |
| `htmx:validation:halted`    | —                                                                                 | removed | Use native browser form validation.  |
| `htmx:xhr:loadstart`        | —                                                                                 | removed | htmx uses `fetch()` now.             |
| `htmx:xhr:loadend`          | `htmx:finally:request`                  | removed | htmx uses `fetch()` now.             |
| `htmx:xhr:progress`         | —                                                                                 | removed | htmx uses `fetch()` now.             |
| `htmx:xhr:abort`            | `htmx:error`                                      | removed | htmx uses `fetch()` now.             |

### Config

| htmx 2.x                 | htmx 4.x                                                                   | Type            | Notes                                                                                                                                                |
|--------------------------|----------------------------------------------------------------------------|-----------------|------------------------------------------------------------------------------------------------------------------------------------------------------|
| `defaultSwapStyle`       | `defaultSwap`                 | renamed         | —                                                                                                                                                    |
| `globalViewTransitions`  | `transitions`                 | renamed         | —                                                                                                                                                    |
| `historyEnabled`         | `history`                         | renamed         | —                                                                                                                                                    |
| `includeIndicatorStyles` | `includeIndicatorCSS` | renamed         | —                                                                                                                                                    |
| `timeout`                | `defaultTimeout`           | renamed         | —                                                                                                                                                    |
| `defaultTimeout`         | `60000`                                                                    | default changed | Was `0` (no timeout).                                                                                                                                |
| `defaultSettleDelay`     | `1`                                                                        | default changed | Was `20`.                                                                                                                                            |
| `addedClass`             | —                                                                          | removed         | The `htmx-added` CSS class is still applied during swaps.                                                                                            |
| `allowEval`              | —                                                                          | removed         | —                                                                                                                                                    |
| `allowNestedOobSwaps`    | —                                                                          | removed         | —                                                                                                                                                    |
| `allowScriptTags`        | —                                                                          | removed         | —                                                                                                                                                    |
| `attributesToSettle`     | —                                                                          | removed         | —                                                                                                                                                    |
| `defaultSwapDelay`       | —                                                                          | removed         | —                                                                                                                                                    |
| `disableSelector`        | `hx-ignore`                             | removed         | —                                                                                                                                                    |
| `getCacheBusterParam`    | —                                                                          | removed         | —                                                                                                                                                    |
| `historyCacheSize`       | —                                                                          | removed         | —                                                                                                                                                    |
| `ignoreTitle`            | —                                                                          | removed         | Still works per swap via `hx-swap``="... ignoreTitle:true"`.                                                     |
| `inlineStyleNonce`       | —                                                                          | removed         | Indicator CSS now uses [Constructable Stylesheets](https://developer.mozilla.org/en-US/docs/Web/API/CSSStyleSheet/CSSStyleSheet), so no nonce is needed. |
| `methodsThatUseUrlParams` | —                                                                         | removed         | —                                                                                                                                                    |
| `refreshOnHistoryMiss`   | —                                                                          | removed         | —                                                                                                                                                    |
| `responseHandling`       | `hx-status`                             | removed         | Use with `noSwap`.                                                                                          |
| `scrollBehavior`         | —                                                                          | removed         | —                                                                                                                                                    |
| `scrollIntoViewOnBoost`  | —                                                                          | removed         | —                                                                                                                                                    |
| `selfRequestsOnly`       | `htmx.config.mode`                   | removed         | —                                                                                                                                                    |
| `settlingClass`          | —                                                                          | removed         | The `htmx-settling` CSS class is still applied during swaps.                                                                                         |
| `swappingClass`          | —                                                                          | removed         | The `htmx-swapping` CSS class is still applied during swaps.                                                                                         |
| `triggerSpecsCache`      | —                                                                          | removed         | —                                                                                                                                                    |
| `useTemplateFragments`   | —                                                                          | removed         | —                                                                                                                                                    |
| `withCredentials`        | `hx-config`                             | removed         | —                                                                                                                                                    |
| `wsBinaryType`           | —                                                                          | removed         | —                                                                                                                                                    |
| `wsReconnectDelay`       | —                                                                          | removed         | —                                                                                                                                                    |

### Request headers

| htmx 2.x          | htmx 4.x                                                | Type            | Notes                                                 |
|-------------------|---------------------------------------------------------|-----------------|-------------------------------------------------------|
| `HX-Trigger`      | `HX-Source`             | changed format  | Format is `tagName#id`, e.g. `button#submit`.        |
| `HX-Target`       | `HX-Target`             | changed format  | Format is `tagName#id`.                              |
| `HX-Trigger-Name` | `HX-Source`             | removed         | —                                                     |
| `HX-Prompt`       | `hx-prompt` extension          | restored by ext | Load the extension.                                   |
| —                 | `HX-Request-Type` | new             | `"full"` or `"partial"`.                          |
| —                 | `Accept`                                                | new             | Core requests send `text/html`; `hx-sse` adds `text/event-stream`. |

### Response headers

| htmx 2.x                 | htmx 4.x                                      | Type      | Notes                           |
|--------------------------|-----------------------------------------------|-----------|---------------------------------|
| `HX-Trigger-After-Swap`  | `HX-Trigger` | removed   | You can also use JavaScript.    |
| `HX-Trigger-After-Settle`| `HX-Trigger` | removed   | You can also use JavaScript.    |
| `HX-Trigger`             | `HX-Trigger` | unchanged | —                               |
| `HX-Location`            | `HX-Location` | unchanged | —                             |
| `HX-Push-Url`            | `HX-Push-Url` | unchanged | —                             |
| `HX-Redirect`            | `HX-Redirect` | unchanged | —                             |
| `HX-Refresh`             | `HX-Refresh` | unchanged | —                               |
| `HX-Replace-Url`         | `HX-Replace-Url` | unchanged | —                       |
| `HX-Retarget`            | `HX-Retarget` | unchanged | —                             |
| `HX-Reswap`              | `HX-Reswap`   | unchanged | —                               |
| `HX-Reselect`            | `HX-Reselect` | unchanged | —                             |

### JavaScript API

| htmx 2.x                 | htmx 4.x                      | Type      | Notes                                                                    |
|--------------------------|-------------------------------|-----------|--------------------------------------------------------------------------|
| `htmx.addClass()`        | `element.classList.add()`     | removed   | Use native JavaScript.                                                   |
| `htmx.removeClass()`     | `element.classList.remove()`  | removed   | Use native JavaScript.                                                   |
| `htmx.toggleClass()`     | `element.classList.toggle()`  | removed   | Use native JavaScript.                                                   |
| `htmx.closest()`         | `element.closest()`           | removed   | Use native JavaScript.                                                   |
| `htmx.remove()`          | `element.remove()`            | removed   | Use native JavaScript.                                                   |
| `htmx.off()`             | `removeEventListener()`       | removed   | `htmx.on()` returns the callback.                                        |
| `htmx.location()`        | `htmx.ajax()`                 | removed   | —                                                                        |
| `htmx.defineExtension()` | `htmx.registerExtension()`    | renamed   | —                                                                        |
| `htmx.logAll()`          | `htmx.config.logAll = true`   | removed   | htmx logs via `console.*`.                                               |
| `htmx.logNone()`         | —                             | removed   | —                                                                        |
| `htmx.logger`            | `console.*`                   | removed   | Observability tools capture `console.error`, `console.warn`, and `console.log`. |
| `htmx.onLoad()`          | `htmx.onLoad()`               | changed   | Now listens on `htmx:after:process`, not `htmx:after:init`. |

Still available: `htmx.ajax()`, `htmx.config`, `htmx.find()`, `htmx.findAll()`, `htmx.on()`, `htmx.onLoad()`, `htmx.parseInterval()`, `htmx.process()`, `htmx.swap()`, `htmx.trigger()`.

## What's New

### Attributes

| Attribute                                          | Purpose                                                               |
|----------------------------------------------------|-----------------------------------------------------------------------|
| `hx-action`     | Specify URL, with optional `hx-method`. Supports progressive enhancement via native `action`/`method` fallback |
| `hx-method`     | Specify HTTP method (overrides native `method` and `formmethod`)      |
| `hx-query`       | Issue a `QUERY` request, which sends parameters in the body           |
| `hx-config`     | Per-element request config (JSON or `key:value` syntax)               |
| `hx-ignore`     | Disable htmx processing (was `hx-disable`)                            |
| `hx-validate` | Control form validation behavior                                      |

### `hx-swap` scroll modifiers

The `show` and `scroll` modifiers no longer support the combined `selector:position` syntax. Use separate keys instead:

```html
<!-- htmx 2 (broken in 4) -->
<div hx-swap="innerHTML show:#other:top"></div>

<!-- htmx 4 -->
<div hx-swap="innerHTML show:top showTarget:#other"></div>
<div hx-swap="innerHTML scroll:bottom scrollTarget:#other"></div>
```

### `hx-swap` styles

```html

<div hx-get="/data" hx-swap="innerMorph">...</div>
<div hx-get="/data" hx-swap="outerMorph">...</div>
<div hx-get="/text" hx-swap="textContent">...</div>
<div hx-get="/remove" hx-swap="delete">...</div>
```

- `innerMorph` / `outerMorph`: morph swaps using the idiomorph algorithm. Better for preserving state in complex UIs.
- `textContent`: set the target's text content (no HTML parsing).
- `delete`: remove the target element entirely.

New aliases for existing swap styles (both old and new names work):

| New       | Equivalent to |
|-----------|---------------|
| `before`  | `beforebegin` |
| `after`   | `afterend`    |
| `prepend` | `afterbegin`  |
| `append`  | `beforeend`   |

### Status code swaps

Set different swap behavior per HTTP status code:

```html

<form hx-post="/save"
      hx-status:422="swap:innerHTML target:#errors select:#validation-errors"
      hx-status:5xx="swap:none push:false">
    <!-- form fields -->
</form>
```

Available config keys: `swap:`, `target:`, `select:`, `push:`, `replace:`, `transition:`.

Supports exact codes (`404`), single-digit wildcards (`50x`), and range wildcards (`5xx`). Evaluated in order of
specificity.

### `<hx-partial>`

Target multiple elements from one response. An alternative to `hx-swap-oob` for when you need explicit control over targeting and swap strategy:

```html
<hx-partial hx-target="#messages" hx-swap="beforeend">
    <div>New message</div>
</hx-partial>

<hx-partial hx-target="#count">
    <span>5</span>
</hx-partial>
```

Each `<hx-partial>` specifies its own `hx-target` and `hx-swap` strategy. See Multi-Target Updates for full documentation.

### View transitions

[View Transitions API](https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API) support is available but
disabled by default.

Enable: `htmx.config.transitions` `= true`

### JSX compatibility

Frameworks that don't support `:` in attribute names can use 
`metaCharacter` to replace it:

```js
htmx.config.metaCharacter = "-";
// hx-ws-connect instead of hx-ws:connect
// hx-confirm-inherited instead of hx-confirm:inherited
```

### JavaScript methods

- `htmx.timeout(time)`: returns a promise that resolves after a delay (number ms, or interval string `'500ms'`/`'1s'`/`'5m'`)

`htmx.takeClass` is **removed** from core. Equivalent functionality is exposed by the `hx-live` extension on the `htmx.live` namespace:

```js
htmx.live.take(target, className, source)   // strip class from `source`, add to `target`
htmx.live.forEvent(...args)                 // race events/timeouts
htmx.live.nextFrame()                       // promise that resolves on next animation frame
htmx.live.q(selector)                       // jQuery-like proxy rooted at documentElement
htmx.live.debounce(ms[, fn])                // global debounce
htmx.live.refresh()                         // recompute every live expression
```

Inside `hx-live`/`hx-on` expression scope these are available unprefixed (`take`, `forEvent`, `nextFrame`, `q`, `debounce`, `toggle`) with the current element used as the implicit context, see the `hx-live` extension docs.

### Auto-logged events

Internally-dispatched events route to the console as follows:

- If `detail.error` is set on the event, output goes to `console.error` (the Error instance is inlined first when applicable, so DevTools renders the stack). This covers request failures, hx-on handler exceptions, and other thrown paths. Apps that listen for `htmx:error` get the same data via the event.
- If `detail.warn` is set, output goes to `console.warn`.
- Otherwise, the event is logged at `console.log` (silent by default; set `htmx.config.logAll = true` to surface).

This restores the htmx 2.x convention: if you want an internal failure path to show up in the console, fire an event with `detail.error` (or `detail.warn`); no per-site `console.error` needed.

### Request Context in Events

All events provide a consistent `ctx` object with request/response information.

### Events

| Event                                                                        | Fires                                             |
|------------------------------------------------------------------------------|---------------------------------------------------|
| `htmx:after:cleanup`                 | After element cleanup                             |
| `htmx:after:history:update`   | After history update                              |
| `htmx:after:process`                 | After element processing                          |
| `htmx:before:response`             | Before response body is read (cancellable)        |
| `htmx:before:settle`                 | Before settle phase                               |
| `htmx:after:settle`                   | After settle phase                                |
| `htmx:before:viewTransition` | Before a view transition starts                   |
| `htmx:after:viewTransition`   | After a view transition completes                 |
| `htmx:finally:request`             | When request completes, fails, or is cancelled |

### Config keys

| Config                                                                 | Default         | Purpose                                                       |
|------------------------------------------------------------------------|-----------------|---------------------------------------------------------------|
| `extensions`               | `''`            | Comma-separated list of allowed extension names               |
| `mode`                           | `'same-origin'` | Fetch mode (replaces `selfRequestsOnly`)                      |
| `inlineScriptNonce` | `''`            | Nonce for inline scripts                                      |
| `metaCharacter`         | `':'`           | Separator character in attribute/event names                  |
| `morphIgnore`             | `["data-htmx-powered"]` | Attribute name prefixes to preserve during morph              |
| `morphScanLimit`       |                 | Max elements to scan during morph matching                    |
| `morphSkip`                 | `'[hx-morph-skip]'`            | CSS selector for elements to skip during morph                |
| `morphSkipChildren` | `'[hx-morph-skip-children]'`            | CSS selector for elements whose children to skip during morph |

### Core extensions

htmx 4 ships with a bunch of "core" extensions now. The SSE and WebSocket extensions have been significantly rewritten, and `hx-multipart`,
`hx-live`, `hx-targets`, `hx-ptag`, `hx-csp`, `hx-download`, `hx-prompt`, and `hx-history-cache` are new. See their
upgrade guides for details.

| Extension                                                  | Category       | Description                                         |
|------------------------------------------------------------|----------------|-----------------------------------------------------|
| `hx-multipart`                 | Streaming HTML | Stream HTML with `multipart/mixed`                  |
| `hx-sse`                             | Streaming HTML | Stream HTML with `text/event-stream` (SSE) (upgrade guide) |
| `hx-ws`                               | Streaming HTML | Stream HTML and send data over WebSockets (upgrade guide) |
| `hx-browser-indicator` | UX             | Show tab's spinner with `hx-browser-indicator`      |
| `hx-live`                           | UX             | Our own DOM-based reactive scripting solution       |
| `hx-pending`                     | UX             | Show custom content during requests                 |
| `hx-prompt`                       | UX             | Prompt before requests with `hx-prompt='Reason?'`   |
| `hx-preload`                     | Performance    | Preload on hover (upgrade guide) |
| `hx-history-cache`         | Performance    | Restore back/forward pages from `sessionStorage`    |
| `hx-ptag`                           | Performance    | Skip unchanged polls with `HX-PTag: "v42"`          |
| `hx-download`                   | Swaps          | Download files with `hx-swap='download'`            |
| `hx-head`                           | Swaps          | Merge `<head>` tags with `hx-head='merge'`          |
| `hx-targets`                     | Swaps          | Target many elements with `hx-targets='.selector'`  |
| `hx-upsert`                       | Swaps          | Update or insert elements with `hx-swap='upsert'`   |
| `htmx-2-compat`               | Compatibility  | Restore htmx 2.x defaults and event names on htmx 4 |
| `hx-alpine-compat`         | Compatibility  | Run htmx alongside Alpine.js without conflicts      |
| `hx-csp`                             | Security       | Make htmx work under strict Content Security Policy |
