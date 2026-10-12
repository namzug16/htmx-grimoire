# HTTP Headers

## Contents

- HX-Request
- HX-Request-Type
- HX-Current-URL
- HX-Source
- HX-Target
- HX-Boosted
- HX-History-Restore-Request
- HX-Trigger
- HX-Location
- HX-Redirect
- HX-Refresh
- HX-Retarget
- HX-Reswap
- HX-Reselect
- HX-Replace-Url
- HX-Push
- HX-Push-Url

## HX-Request

> Indicates request was made by htmx

The `HX-Request` header indicates the request was made by htmx.

It's value is always `true`.

### Syntax

```http
HX-Request: true
```

Use it to detect htmx requests on the server:

```python
if request.headers.get('HX-Request'):
    # This is an htmx request
    return render_template('partial.html')
else:
    # This is a regular browser request
    return render_template('full.html')
```

## HX-Request-Type

> Indicates `partial` or `full` page request

The `HX-Request-Type` request header indicates if request targets a specific element or the whole page.

### Syntax

```http
HX-Request-Type: partial

// or

HX-Request-Type: full
```

### Values

This header is added automatically.

#### `full`

Used when the target is the document body, or when selecting elements from the response (with `hx-select`).

```html
<!-- If target is body (explicit) -->
<button hx-get=... hx-target="body">

<!-- If target is body (implicit) -->
<a href=... hx-boost="true">

<!-- If selecting elements from response -->
<div hx-get=... hx-select=".content">
```

**Note:** `hx-boost="true"` implicitly sets `hx-target="body"`.

#### `partial`

Used when the target is any other element.

```html
<!-- If target is any element (except body) -->
<button hx-get="..." hx-target="#results">...</button>

<!-- If target is not set (defaults to this element) -->
<div hx-post="...">...</div>
```

### Example

Use it on the server to customize response behavior:

```python
request_type = request.headers.get('HX-Request-Type')
if request_type == 'full':
    return render_full_page()
else:
    return render_fragment()
```

## HX-Current-URL

> Contains browser URL when request started

The `HX-Current-URL` request header contains the browser's URL when the request was made.

Use it to understand page context or build relative URLs.

### Syntax

The header is included as follows:

```http
HX-Current-URL: https://example.com/products
```

Read the current URL from the request:

```python
current_url = request.headers.get('HX-Current-URL')
```

## HX-Source

> Identifies element that triggered the request

The `HX-Source` request header contains the element that triggered the request. Format is `tag#id` like `button#submit`.

Elements without an ID use only the tag name like `div` or `form`.

### Example

Check which element triggered the request.

```python
source = request.headers.get('HX-Source')
if source == 'button#submit-btn':
    # Handle button submission
    return handle_button_submit()
```

## HX-Target

> Identifies element that will receive response

The `HX-Target` request header identifies the element that will receive the response.

This header is only included when a target is specified.

Format: `<tag>#<id>` (e.g. `div#results`) or just `<tag>` for elements without an ID.

### Syntax

The header is included as follows:

```http
HX-Target: div#results
```

Return different content for different targets:

```python
target = request.headers.get('HX-Target')
if target == 'div#sidebar':
    return render_template('sidebar_content.html')
```

### See Also

- `hx-target`
- `HX-Retarget`

## HX-Boosted

> Indicates boosted navigation request

The `HX-Boosted` request header is set to `true` when the request comes from a boosted element via `hx-boost`.

Boosted elements are regular links and forms that htmx intercepts to enhance.

### Example

Detect boosted navigation.

```python
if request.headers.get('HX-Boosted') == 'true':
    # Boosted requests get the full layout
    return render_template('page.html')
else:
    # Regular htmx requests get a fragment
    return render_template('fragment.html')
```

### See Also

- `hx-boost`

## HX-History-Restore-Request

> Indicates history navigation (back/forward)

The `HX-History-Restore-Request` request header is set to `true` when the user navigates back or forward in history.

htmx restores the previous state without a full page reload. Use this to skip side effects during history restoration.

### Example

Skip analytics for restored pages.

```python
if request.headers.get('HX-History-Restore-Request'):
    # Don't log analytics or run side effects
    return render_content()
else:
    log_page_view()
    return render_content()
```

## HX-Trigger

> Triggers client-side events with `htmx.trigger()`

The `HX-Trigger` response header triggers client-side events after the swap has completed.

### Basic Usage

Send a single event:

```http
HX-Trigger: myEvent
```

By default, the event is dispatched on the element that made the request and bubbles. Use `from:body` when listening elsewhere.

Listen from markup with `hx-on`:

```html
<div hx-on="myEvent from:body -> this.classList.add('updated')"></div>
```

Send multiple events:

```http
HX-Trigger: event1, event2
```

### Event Detail

Send event detail with a JSON object:

```http
HX-Trigger: {"notification":"Hello World"}
```

Scalar values are available on `detail.value`:

```html
<div hx-on="notification from:body -> alert(value)"></div>
```

You can also listen from JavaScript:

```javascript
document.body.addEventListener("notification", (evt) => {
    alert(evt.detail.value); // "Hello World"
});
```

Send multiple detail fields with a nested object:

```http
HX-Trigger: {"notification":{"level":"info", "message":"Saved"}}
```

Each nested property is copied onto the event detail:

```html
<div hx-on="notification from:body -> this.dataset.level = level; this.textContent = message"></div>
```

Send multiple events with detail by adding properties to the top-level JSON object:

```http
HX-Trigger: {"notification":"Saved", "refreshList":true}
```

```html
<div hx-on="notification from:body -> this.textContent = value;
            refreshList from:body -> this.dataset.refresh = value"></div>
```

### Targeting Other Elements

Trigger an event on another element with `target`:

```http
HX-Trigger: {"notification":{"target":"#notifications", "message":"Saved"}}
```

The `target` value is resolved as a selector. The event is dispatched on that element instead of the source element.

```html
<div id="notifications" hx-on="notification -> this.textContent = message"></div>
```

This can update client-owned state while the response swaps normal HTML elsewhere:

```http
HX-Trigger: {"cartUpdated":{"target":"#cart", "count":3}}
```

```html
<div id="cart" data-count="0" hx-on="cartUpdated -> data.count = count">
    Cart (<span :text="data.count"></span>)
</div>
```

_This example uses the `hx-live` extension._

### Notes

Response headers are not processed on 3xx response codes. Return a 2xx status when using this header.

In htmx 2, there were three variants: `HX-Trigger`, `HX-Trigger-After-Swap`, and `HX-Trigger-After-Settle`. In htmx 4, these were consolidated into a single `HX-Trigger` header that fires after the swap completes.

### See Also

- `htmx.trigger()`

## HX-Location

> Redirect without a full page load

The `HX-Location` response header redirects without reloading the page.

### Syntax

Return a path:

```http
HX-Location: /dashboard
```

`HX-Location` calls `htmx.ajax()`. The header above is equivalent to:

```js
htmx.ajax('GET', '/dashboard', { push: 'true' })
```

Use any serializable `htmx.ajax()` option. Include `path`:

```text
# HCON
HX-Location: path:/search target:#results select:#matches

# JSON
HX-Location: {"path":"/search","target":"#results","select":"#matches"}
```

### Notes

`HX-Location` is not processed on 3xx responses. Return a 2xx response instead.

## HX-Redirect

> Redirects by setting `location.href`

The `HX-Redirect` response header redirects to a new URL with a full page reload.

Use it for non-htmx endpoints or pages that require a full browser load.

For AJAX navigation inside an htmx application, use `HX-Location`.

Response headers are not processed on 3xx response codes. Return a 2xx status when using this header.

### Example

```http
HX-Redirect: /dashboard
```

```python
return Response(
    "Redirecting...",
    headers={'HX-Redirect': '/dashboard'}
)
```

### See Also

- `HX-Location`

## HX-Refresh

> Reloads page with `location.reload()`

The `HX-Refresh` response header, when set to `true`, reloads the entire page.

Use this when you need to reset all page state after an action.

### Example

```http
HX-Refresh: true
```

```python
return Response(
    "Changes saved",
    headers={'HX-Refresh': 'true'}
)
```

## HX-Retarget

> Overrides swap target from server

The `HX-Retarget` response header overrides the element that will receive the swapped content, replacing whatever `hx-target` was set on the triggering element.

### Syntax

```http
HX-Retarget: #new-target
```

The value is a CSS selector for the new target element.

Redirect a form submission result to a different container:

```python
return Response(
    content,
    headers={'HX-Retarget': '#notifications'}
)
```

### Notes

- Overrides `hx-target` on the source element
- Evaluated after the response is received, before swapping

See also: `hx-target`, `HX-Reswap`

### See Also

- `HX-Target`

## HX-Reswap

> Overrides swap style from server

The `HX-Reswap` response header overrides the swap style used when inserting the response, replacing whatever `hx-swap` was set on the triggering element.

### Syntax

```http
HX-Reswap: outerHTML
```

Accepts the same values as `hx-swap`, including modifiers.

Force an outer replacement regardless of what the element specified:

```python
return Response(
    content,
    headers={'HX-Reswap': 'outerHTML'}
)
```

With modifiers:

```http
HX-Reswap: innerHTML transition:true
```

### Notes

- Overrides `hx-swap` on the source element
- Evaluated after the response is received, before swapping

See also: `hx-swap`, `HX-Retarget`

## HX-Reselect

> Overrides content selection from server

The `HX-Reselect` response header overrides which part of the response is used for swapping, replacing whatever `hx-select` was set on the triggering element.

### Syntax

```http
HX-Reselect: #content
```

The value is a CSS selector applied to the response HTML to extract the content to swap in.

Return a full page but tell htmx to only use a specific fragment:

```python
return Response(
    full_page_html,
    headers={'HX-Reselect': '#main-content'}
)
```

### Notes

- Overrides `hx-select` on the source element
- Evaluated after the response is received, before swapping

See also: `hx-select`, `HX-Retarget`, `HX-Reswap`

## HX-Replace-Url

> Replaces current URL in browser history

The `HX-Replace-Url` response header replaces the current browser history URL.

It does not create a new history entry.

If present, this header overrides any behavior defined with attributes.

### Possible Values

- A URL to replace the current URL in the location bar. May be relative or absolute, as per [`history.replaceState()`](https://developer.mozilla.org/en-US/docs/Web/API/History/replaceState), but must have the same origin as the current URL.
- `false` — prevents the browser's current URL from being updated.

### Example

```http
HX-Replace-Url: /dashboard
```

### Notes

- Response headers are not processed on 3xx response codes.

See also: `hx-replace-url`, `HX-Push-Url`

## HX-Push

> Deprecated; use `HX-Push-Url` instead

The `HX-Push` response header has been replaced by HX-Push-Url. Use `HX-Push-Url` in all new code.

## HX-Push-Url

> Pushes URL into browser history stack

The `HX-Push-Url` response header pushes a URL into browser history.

It creates a new entry for back and forward navigation.

If present, this header overrides any behavior defined with attributes.

### Possible Values

- A URL to be pushed into the location bar. May be relative or absolute, as per [`history.pushState()`](https://developer.mozilla.org/en-US/docs/Web/API/History/pushState).
- `false` — prevents the browser's history from being updated.

### Example

```http
HX-Push-Url: /dashboard
```

### Notes

- Response headers are not processed on 3xx response codes.

See also: `hx-push-url`, `HX-Replace-Url`
