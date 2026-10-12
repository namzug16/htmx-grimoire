# Configuration

## Contents

- htmx.config
- htmx.config.defaultSwap
- htmx.config.defaultTimeout
- htmx.config.extensions
- htmx.config.history
- htmx.config.implicitInheritance
- htmx.config.includeIndicatorCSS
- htmx.config.indicatorClass
- htmx.config.logAll
- htmx.config.mode
- htmx.config.morphIgnore
- htmx.config.morphSkip
- htmx.config.morphSkipChildren
- htmx.config.noSwap
- htmx.config.prefix
- htmx.config.requestClass
- htmx.config.transitions
- htmx.version
- htmx.config.defaultFocusScroll
- htmx.config.defaultSettleDelay
- htmx.config.inlineScriptNonce
- htmx.config.morphScanLimit
- htmx.config.metaCharacter
- htmx.config.allowEmptySwapAfterOOB

## htmx.config

> Configures htmx behavior globally

The `htmx.config` object holds the current htmx configuration. You can modify it in JavaScript or set values using a `<meta>` tag.

### Configure via Meta Tag

Set config values with HCON:

```html
<meta name="htmx-config"
      content="defaultSwap:outerHTML defaultTimeout:5000">
```

Or JSON:

```html
<meta name="htmx-config"
      content='{"defaultSwap":"outerHTML","defaultTimeout":5000}'>
```

### Configure via JavaScript

Modify config values directly:

```javascript
htmx.config.defaultSwap = 'outerHTML';
htmx.config.defaultTimeout = 5000;
```

### Available Options

| Option | Default | Description |
|--------|---------|-------------|
| `logAll` | `false` | Log all htmx events |
| `prefix` | `"data-hx-"` | Secondary attribute prefix recognized alongside `hx-` |
| `metaCharacter` | `undefined` | Character used instead of `:` in attribute names |
| `transitions` | `false` | Enable view transitions |
| `history` | `true` | Enable history support |
| `mode` | `"same-origin"` | Request mode for `fetch()` |
| `defaultSwap` | `"innerHTML"` | Default swap style |
| `allowEmptySwapAfterOOB` | `false` | Allow empty main swap after OOB extraction |
| `defaultFocusScroll` | `false` | Scroll to a focused element after swapping |
| `defaultSettleDelay` | `1` | Delay before settling in milliseconds |
| `indicatorClass` | `"htmx-indicator"` | CSS class for indicators |
| `requestClass` | `"htmx-request"` | CSS class during requests |
| `includeIndicatorCSS` | `true` | Include default indicator CSS |
| `defaultTimeout` | `60000` | Request timeout in milliseconds |
| `extensions` | `""` | Extensions to load |
| `morphIgnore` | `["data-htmx-powered"]` | Attributes to ignore during morphing |
| `morphSkip` | `"[hx-morph-skip]"` | Elements to skip while morphing |
| `morphSkipChildren` | `"[hx-morph-skip-children]"` | Elements whose children are not morphed |
| `morphScanLimit` | `10` | Siblings scanned while matching elements |
| `noSwap` | `[204, 304]` | HTTP status codes that skip swaps |
| `implicitInheritance` | `false` | Enable implicit attribute inheritance |
| `inlineScriptNonce` | `undefined` | Nonce added to inline scripts |

### See Also

- HCON
- `hx-config`

## htmx.config.defaultSwap

> Sets default swap style for responses

The `htmx.config.defaultSwap` option sets the default swap style when `hx-swap` is not specified.

**Default:** `"innerHTML"`

### Valid Values

- `"innerHTML"` - Replace inner content
- `"outerHTML"` - Replace entire element
- `"beforebegin"` - Insert before element
- `"afterbegin"` - Insert as first child
- `"beforeend"` - Insert as last child
- `"afterend"` - Insert after element
- `"delete"` - Delete the target element
- `"none"` - Don't swap content

### Example

```javascript
htmx.config.defaultSwap = "outerHTML";
```

```html
<meta name="htmx-config" content='{"defaultSwap":"outerHTML"}'>
```

## htmx.config.defaultTimeout

> Sets default request timeout in `ms`

The `htmx.config.defaultTimeout` option sets the default timeout for all htmx requests.

**Default:** `60000` (60 seconds)

### Example

```javascript
htmx.config.defaultTimeout = 30000; // 30 seconds
```

```html
<meta name="htmx-config" content='{"defaultTimeout":30000}'>
```

Requests that exceed this timeout will be aborted.

## htmx.config.extensions

> Restricts extension registration by name

The `htmx.config.extensions` option restricts extension registration to listed names.

```html
<meta name="htmx-config" content='extensions:"preload,hx-pending"'>
<script src="/htmx.js"></script>
<script src="/hx-preload.js"></script>
<script src="/hx-pending.js"></script>
```

Both extension scripts still need to be loaded. The config only controls whether their calls to `htmx.registerExtension()` succeed.

### Default

```text
""
```

An empty string allows every loaded extension to register.

### Extension Names

List names passed to `htmx.registerExtension()`, separated by commas:

```javascript
htmx.registerExtension('preload', { /* ... */ })
htmx.registerExtension('hx-pending', { /* ... */ })
```

### Configure Before Loading htmx

htmx reads the extension allowlist during initialization. Put the `htmx-config` meta element before the htmx script.

Changing `htmx.config.extensions` afterward does not change the active allowlist.

### See Also

- `htmx.registerExtension()`
- Extensions

## htmx.config.history

> Controls htmx browser history management

The `htmx.config.history` option controls browser history during navigation.

**Default:** `true`

| Value | Behavior |
|-------|----------|
| `true` | htmx pushes URLs into history and restores them on back/forward by fetching the page via `GET` and swapping `innerHTML` on `body`. |
| `false` | htmx does not push URLs into history or intercept back/forward navigation. |
| `"reload"` | htmx pushes URLs into history normally, but on back/forward navigation calls `location.reload()` instead of attempting to restore via ajax. |

### Examples

```javascript
// Disable history entirely
htmx.config.history = false;

// Push URLs, but use full page reload on back/forward
htmx.config.history = "reload";
```

```html
<meta name="htmx-config" content='{"history":false}'>
<meta name="htmx-config" content='{"history":"reload"}'>
```

The `"reload"` option is useful when pages use client-side state (e.g. from hyperscript or Alpine.js) that cannot be reconstructed from a plain `innerHTML` swap.

## htmx.config.implicitInheritance

> Enables implicit attribute inheritance

The `htmx.config.implicitInheritance` option, when set to `true`, causes child elements to implicitly inherit htmx attributes from parent elements.

**Default:** `false`

### Example

```javascript
htmx.config.implicitInheritance = true;
```

```html
<meta name="htmx-config" content='{"implicitInheritance":true}'>
```

When enabled, attributes like `hx-target` on a parent apply to all child elements unless overridden.

## htmx.config.includeIndicatorCSS

> Includes built-in loading indicator CSS

The `htmx.config.includeIndicatorCSS` option controls whether htmx adds built-in loading indicator styles.

The styles hide `indicatorClass` content until `requestClass` marks it as active.

**Default:** `true`

### Syntax

Disable built-in styles when providing your own:

```html
<meta name="htmx-config" content="includeIndicatorCSS:false">
```

### See Also

- `hx-indicator`
- `htmx.config.indicatorClass`
- `htmx.config.requestClass`

## htmx.config.indicatorClass

> Sets class hidden by built-in indicator CSS

The `htmx.config.indicatorClass` option sets the CSS class used to mark loading indicator content.

Add this class in your markup:

```html
<img id="spinner" class="htmx-indicator" alt="Loading">
```

htmx does not add the class. Built-in indicator CSS hides it until `requestClass` marks the indicator or an ancestor as active.

**Default:** `"htmx-indicator"`

### Syntax

Use a custom class:

```html
<meta name="htmx-config" content='indicatorClass:"loading"'>

<img id="spinner" class="loading" alt="Loading">
```

### See Also

- `hx-indicator`
- `htmx.config.includeIndicatorCSS`
- `htmx.config.requestClass`

## htmx.config.logAll

> Logs all htmx events to console

The `htmx.config.logAll` option, when set to `true`, causes htmx to surface event-level output via `console.log`.

**Default:** `false`

Errors and warnings always flow to `console.error` / `console.warn` regardless of this flag. `logAll` controls only the chatty event-by-event output that's useful when debugging behavior. Most of the time you don't need it.

### Example

```javascript
htmx.config.logAll = true;
```

```html
<meta name="htmx-config" content='{"logAll":true}'>
```

Observability tools (Sentry, DataDog RUM, LogRocket, etc.) capture `console.*` automatically, so htmx logs flow into your existing pipeline without any extra setup.

## htmx.config.mode

> Sets request mode for `fetch()`

The `htmx.config.mode` option sets the default `mode` for Fetch requests.

Per-element `hx-config` cannot override it. htmx resets that value to the global mode so injected markup cannot widen request scope from `same-origin` to `cors`.

**Default:** `"same-origin"`

### Valid Values

- `"same-origin"` - Only allow same-origin requests (default, most secure)
- `"cors"` - Allow cross-origin requests
- `"no-cors"` - Limited cross-origin requests
- `"navigate"` - Navigation mode

### Example

```javascript
htmx.config.mode = "cors";
```

```html
<meta name="htmx-config" content='{"mode":"cors"}'>
```

### Security

The default `"same-origin"` means the browser will reject any cross-origin fetch outright,
even if an attacker injects an `hx-get` pointing to an external URL.

If your app legitimately needs CORS (e.g. an API on a different subdomain), set `mode` globally
and pair it with a `Content-Security-Policy` `connect-src` directive to limit reachable origins:

```html
<meta http-equiv="Content-Security-Policy"
      content="connect-src 'self' https://api.example.com">
```

This way, even if an attacker injects a target URL, CSP blocks connections to origins you
haven't explicitly allowed.

## htmx.config.morphIgnore

> Preserves attribute prefixes during morphing

The `htmx.config.morphIgnore` option lists attribute prefixes to preserve during morphing.

An attribute is preserved when its name starts with a listed prefix.

**Default:** `["data-htmx-powered"]`

### Example

```javascript
htmx.config.morphIgnore = ["data-htmx-powered", "data-analytics"];
```

```html
<meta name="htmx-config" content='{"morphIgnore":["data-htmx-powered","data-analytics"]}'>
```

Add `"data-"` to preserve every `data-*` attribute.

Exact names also work. For example, `"style"` preserves only the `style` attribute.

### Use Cases

- Preserve client-side state stored in `data-*` attributes (e.g. from the `hx-live` `data` proxy)
- Prevent CSP violations from inline `style` attribute copying (add `"style"`)
- Protect framework-managed attributes from being overwritten during morph

### See Also

- `morphSkip` — CSS selector for elements to completely skip during morph
- `morphSkipChildren` — CSS selector for elements whose children are preserved

## htmx.config.morphSkip

> Skips morphing for specific elements

The `htmx.config.morphSkip` option is a CSS selector for elements to skip during morphing.

Matching elements won't be morphed. They stay exactly as they are.

**Default:** `'[hx-morph-skip]'`

Add `hx-morph-skip` to any element in your server templates to freeze it entirely during morph:

```html
<custom-widget hx-morph-skip>...</custom-widget>
```

Or override with any CSS selector:

```javascript
htmx.config.morphSkip = ".no-morph";
```

### Use Cases

**Third-party widgets:**
Preserve complex widgets that manage their own state.

**Active animations:**
Skip elements with ongoing CSS or JavaScript animations.

**Client-side state:**
Protect elements with complex state that would be lost.

**Multiple selectors:**
```javascript
htmx.config.morphSkip = ".widget, .animated, custom-element";
```

See `hx-morph-skip` for the attribute.

## htmx.config.morphSkipChildren

> Skips morphing children of specific elements

The `htmx.config.morphSkipChildren` option is a CSS selector for elements whose children won't be morphed.

The element itself updates (attributes change). Its children stay untouched.

**Default:** `'[hx-morph-skip-children]'`

Add `hx-morph-skip-children` to any element in your server templates to freeze its children during morph while still allowing its own attributes to update:

```html
<lit-component hx-morph-skip-children value="{{value}}">...</lit-component>
```

Or override with any CSS selector:

```javascript
htmx.config.morphSkipChildren = "my-component";
```

### Use Cases

**Custom web components:**
Update component attributes but preserve managed children.

**Client-managed DOM:**
Let JavaScript frameworks control their own DOM trees.

**Multiple components:**
```javascript
htmx.config.morphSkipChildren = "my-component, other-component, .skip-kids";
```

### Difference from morphSkip

- **`morphSkip`:** Freezes entire element (no changes at all)
- **`morphSkipChildren`:** Updates element attributes, freezes children only

See `hx-morph-skip-children` for the attribute.

## htmx.config.noSwap

> Sets HTTP status codes that skip swap

The `htmx.config.noSwap` option is an array of HTTP status codes for which htmx will not perform a content swap.

**Default:** `[204, 304]`

### Example

```javascript
htmx.config.noSwap = [204, 304, 205];
```

```html
<meta name="htmx-config" content='{"noSwap":[204,304,205]}'>
```

Responses with these status codes will trigger events but won't swap content.

### See Also

- `hx-status`
- `htmx:response:error`

## htmx.config.prefix

> Sets secondary attribute prefix

The `htmx.config.prefix` option sets a secondary attribute prefix that htmx recognises in addition to the primary `hx-` prefix, which always works regardless of this setting.

**Default:** `"data-hx-"`

This means `data-hx-get`, `data-hx-target`, etc. work out of the box alongside `hx-get`, `hx-target`, etc. — matching the htmx 2 dual-attribute behaviour.

When both prefixes are present on the same element, `hx-` wins.

### Disable the secondary prefix

```html
<meta name="htmx-config" content='{"prefix":""}'>
```

### Use a custom secondary prefix

```html
<meta name="htmx-config" content='{"prefix":"data-boost-"}'>
```

Now both `hx-get` and `data-boost-get` are recognised.

### Important: Set via meta tag

The prefix is read once during htmx initialisation. Setting it via JavaScript after the page has loaded will not apply correctly, as elements will already have been processed.

Always configure the prefix using the meta tag:

```html
<meta name="htmx-config" content='{"prefix":"data-hx-"}'>
```

## htmx.config.requestClass

> Sets class applied during requests

The `htmx.config.requestClass` option sets the CSS class htmx adds while a request is running.

htmx adds it to the element selected by `hx-indicator`. Without `hx-indicator`, htmx adds it to the request source.

**Default:** `"htmx-request"`

### Syntax

Use a custom request-state class:

```html
<meta name="htmx-config" content='requestClass:"is-loading"'>
```

```css
.is-loading {
  opacity: 0.5;
}
```

htmx removes the class when the request ends.

### See Also

- `hx-indicator`
- `htmx.config.includeIndicatorCSS`
- `htmx.config.indicatorClass`

## htmx.config.transitions

> Enables View Transitions API support

The `htmx.config.transitions` option, when set to `true`, causes htmx to use the View Transitions API for smooth animations between page updates.

**Default:** `false`

### Example

```javascript
htmx.config.transitions = false;
```

```html
<meta name="htmx-config" content='{"transitions":false}'>
```

Requires browser support for the View Transitions API.

## htmx.version

> Reports current htmx version (read-only)

The `htmx.version` property contains the current htmx version string (read-only).

### Example

```javascript
console.log(htmx.version)
```

## htmx.config.defaultFocusScroll

> Scrolls to focused element after swap

The `htmx.config.defaultFocusScroll` option, when set to `true`, causes htmx to scroll the focused element into view after each swap.

**Default:** `false`

### Example

```javascript
htmx.config.defaultFocusScroll = true;
```

```html
<meta name="htmx-config" content='{"defaultFocusScroll":true}'>
```

Useful when swapping content that moves focus to a new element and you want the user's view to follow.

See also: `htmx.config`

## htmx.config.defaultSettleDelay

> Sets swap-to-settle delay in `ms`

The `htmx.config.defaultSettleDelay` option controls how long htmx waits between the swap phase and the settle phase (when CSS transition classes are removed).

**Default:** `1` (1 millisecond)

### Example

```javascript
htmx.config.defaultSettleDelay = 100;
```

```html
<meta name="htmx-config" content='{"defaultSettleDelay":100}'>
```

Increase this value if CSS transitions are not completing before htmx removes the transition classes.

See also: `htmx.config`

## htmx.config.inlineScriptNonce

> Sets nonce on inline scripts generated by htmx

The `htmx.config.inlineScriptNonce` option sets `nonce` on generated inline scripts.

Use it with a Content Security Policy that requires script nonces.

**Default:** `undefined` (no nonce added)

### Example

```javascript
htmx.config.inlineScriptNonce = "abc123";
```

```html
<meta name="htmx-config" content='{"inlineScriptNonce":"abc123"}'>
```

The nonce value should match the one provided in your `Content-Security-Policy` header.

See also: `htmx.config`

## htmx.config.morphScanLimit

> Limits siblings scanned during morph matching

The `htmx.config.morphScanLimit` option limits siblings scanned during morph matching.

Higher values improve accuracy for long lists without IDs at a performance cost.

**Default:** `10`

### Example

```javascript
htmx.config.morphScanLimit = 20;
```

```html
<meta name="htmx-config" content='{"morphScanLimit":20}'>
```

If morphing produces unexpected reorders in long lists, try increasing this limit.

See also: `htmx.config`

## htmx.config.metaCharacter

> Replaces `:` in attribute modifiers

The `htmx.config.metaCharacter` option allows you to replace the `:` character used in attribute modifiers (e.g., `hx-get:inherited`) with a custom character of your choice.

**Default:** `undefined` (uses `:`)

### Example

```javascript
htmx.config.metaCharacter = "-";
```

```html
<meta name="htmx-config" content='{"metaCharacter":"-"}'>
```

With the above setting, you would write `hx-get-inherited` instead of `hx-get:inherited`. This can help avoid conflicts with templating engines or parsers that treat `:` specially.

See also: `htmx.config`

## htmx.config.allowEmptySwapAfterOOB

> Controls whether OOB swaps prevent empty main swaps

The `htmx.config.allowEmptySwapAfterOOB` option controls whether out-of-band swaps prevent the main swap when the response body is empty after OOB extraction.

Override it per element with `swapEmpty`.

**Default:** `false`. When `false`, OOB swaps prevent the empty main swap. When `true`, the main swap runs even if only OOB elements were in the response.

Note: `<hx-partial>` elements always prevent empty main swaps regardless of this setting. Partials are designed as true response separators where the server has explicit control.

### Values

- `false` — OOB swaps prevent the empty main swap (default)
- `true` — allow the main swap even after OOB extraction leaves no content

### Example

```javascript
htmx.config.allowEmptySwapAfterOOB = true;
```

```html
<meta name="htmx-config" content='{"allowEmptySwapAfterOOB":true}'>
```

Override per element with the `swapEmpty` modifier on `hx-swap`:

```html
<!-- skip the main swap on an empty response for this element only -->
<div hx-swap="innerHTML swapEmpty:false"></div>

<!-- force the main swap even on an empty response -->
<div hx-swap="innerHTML swapEmpty:true"></div>
```
