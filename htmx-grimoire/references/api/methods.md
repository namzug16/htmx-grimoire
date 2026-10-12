# JavaScript Methods

## Contents

- htmx.ajax()
- htmx.find()
- htmx.findAll()
- htmx.on()
- htmx.onLoad()
- htmx.parseInterval()
- htmx.process()
- htmx.registerExtension()
- htmx.initialize()
- htmx.timeout()
- htmx.trigger()
- htmx.swap()

## htmx.ajax()

> Issues an htmx request

Use `htmx.ajax()` to issue a request from JavaScript with htmx request, response, and swap behavior.

```javascript
await htmx.ajax('GET', '/messages', '#messages')
```

htmx swaps the response into `#messages` and resolves the promise after the request finishes.

### Syntax

```javascript
htmx.ajax(method, url)
htmx.ajax(method, url, target)
htmx.ajax(method, url, options)
```

Pass a selector or element as the target:

```javascript
await htmx.ajax('GET', '/messages', '#messages')

await htmx.ajax(
  'GET',
  '/messages',
  document.querySelector('#messages')
)
```

Use an options object to configure the request and swap:

```javascript
await htmx.ajax('POST', '/messages', {
  target: '#messages',
  swap: 'beforeend',
  values: {
    body: 'Hello'
  }
})
```

### Parameters

#### `method`

The HTTP method. Method names are case-insensitive.

```javascript
await htmx.ajax('GET', '/messages')
await htmx.ajax('post', '/messages')
await htmx.ajax('DELETE', '/messages/42')
```

#### `url`

The request URL.

```javascript
await htmx.ajax('GET', '/messages?limit=10')
```

#### `target`

Pass a selector or element as the third argument.

```javascript
await htmx.ajax('GET', '/messages', '#messages')
```

An unmatched target selector rejects the returned promise.

#### `options`

Use an options object for more control. It accepts request context fields:

```javascript
await htmx.ajax('POST', '/messages', {
  source: '#new-message',
  target: '#messages',
  swap: 'beforeend',
  values: {
    body: 'Hello'
  },
  headers: {
    'X-Requested-By': 'compose-form'
  }
})
```

Supported fields include:

| Field | Description |
|---|---|
| `source` | Element or selector used for attributes, values, and lifecycle events |
| `event` | Event that triggered the request |
| `target` | Element or selector that receives the response |
| `swap` | Serialized `hx-swap` value |
| `select` | Content selected from the response |
| `selectOOB` | Out-of-band content selected from the response |
| `transition` | Whether to use a view transition |
| `values` | Values added to the request |
| `headers` | Request headers |

With no source or target, htmx uses `document.body`.

### Set the Source

Set `source` when the request should behave as if it came from an element:

```javascript
await htmx.ajax('POST', '/messages', {
  source: '#new-message',
  target: '#messages',
  swap: 'beforeend'
})
```

The source provides inherited htmx attributes, form values, and the element used for lifecycle events. An unmatched source selector rejects the returned promise.

If `target` is omitted, the source becomes the default target.

### Control the Swap

Pass a serialized `hx-swap` value with `swap`:

```javascript
await htmx.ajax('GET', '/messages', {
  target: '#messages',
  swap: 'innerHTML transition:true'
})
```

Select part of the response with `select`:

```javascript
await htmx.ajax('GET', '/messages', {
  target: '#messages',
  swap: 'innerHTML',
  select: '#unread'
})
```

Use `selectOOB` for out-of-band content.

### Send Values

Pass request values with `values`:

```javascript
await htmx.ajax('POST', '/messages', {
  values: {
    body: 'Hello',
    draft: false
  }
})
```

For `GET` and `DELETE`, htmx adds the values to the URL query. Other methods send them in the request body.

A source form contributes its values automatically:

```javascript
await htmx.ajax('POST', '/messages', {
  source: '#new-message'
})
```

Explicit values replace form values with the same names.

### Set Headers

Pass request headers with `headers`:

```javascript
await htmx.ajax('GET', '/messages', {
  headers: {
    'X-Request-Source': 'inbox'
  }
})
```

### Pass the Event

Pass the triggering event when calling `htmx.ajax()` from an event listener:

```javascript
button.addEventListener('click', event => {
  htmx.ajax('POST', '/messages', {
    source: button,
    event
  })
})
```

### Return Value

`htmx.ajax()` returns a `Promise` that resolves after the request finishes.

```javascript
await htmx.ajax('GET', '/messages', '#messages')
console.log('Request complete')
```

### See Also

- `htmx.swap()`
- `hx-swap`
- `hx-target`
- `hx-select`

## htmx.find()

> Finds first matching element

The `htmx.find()` function finds the first element matching a CSS selector.

### Syntax

```javascript
// Find from document
htmx.find(selector)

// Find within element
htmx.find(element, selector)
```

### Parameters

- `selector` - CSS selector string
- `element` - Optional element to search within

### Example

```javascript
// Find from document
let button = htmx.find('#myButton');

// Find within specific element
let container = htmx.find('#container');
let input = htmx.find(container, 'input[type="text"]');
```

### Return Value

Returns the first matching element, or `null` if no match found.

## htmx.findAll()

> Finds all matching elements

The `htmx.findAll()` function finds all elements matching a CSS selector.

### Syntax

```javascript
// Find from document
htmx.findAll(selector)

// Find within element
htmx.findAll(element, selector)
```

### Parameters

- `selector` - CSS selector string
- `element` - Optional element to search within

### Example

```javascript
// Find all buttons from document
let buttons = htmx.findAll('button');

// Find all inputs within form
let form = htmx.find('#myForm');
let inputs = htmx.findAll(form, 'input');
```

### Return Value

Returns an array of matching elements (empty array if no matches).

## htmx.on()

> Listens for htmx events

The `htmx.on()` function registers an event listener for htmx events.

### Syntax

```javascript
// Listen on document
htmx.on(event, callback)

// Listen on specific element
htmx.on(element, event, callback)
```

### Parameters

- `event` - Event name to listen for
- `callback` - Function to call when event fires
- `element` - Optional element to listen on (defaults to document)

### Example

```javascript
// Listen for all htmx requests
htmx.on('htmx:before:request', (evt) => {
  console.log('Request starting:', evt.detail);
});

// Listen on specific element
htmx.on('#myForm', 'htmx:after:swap', (evt) => {
  console.log('Form updated');
});
```

### Return Value

Returns the callback function, which can be used to remove the listener later.

## htmx.onLoad()

> Executes callback when elements load

The `htmx.onLoad()` function registers a callback to execute when new content is processed by htmx.

### Syntax

```javascript
htmx.onLoad(callback)
```

### Parameters

- `callback` - Function to call with the loaded element

### Example

```javascript
htmx.onLoad((element) => {
  console.log('New content loaded:', element);
  // Initialize widgets, attach listeners, etc.
});
```

This is useful for initializing JavaScript widgets or attaching event listeners to dynamically loaded content.

## htmx.parseInterval()

> Parses time intervals to milliseconds

The `htmx.parseInterval()` function parses time interval strings into milliseconds.

### Syntax

```javascript
htmx.parseInterval(str)
```

### Parameters

- `str` - Time interval as number or string (e.g., "2s", "500ms", "1m")

### Supported Units

- `ms` - milliseconds (default if no unit specified)
- `s` - seconds
- `m` - minutes

### Example

```javascript
htmx.parseInterval(1000)      // 1000 (already in ms)
htmx.parseInterval("2s")      // 2000
htmx.parseInterval("500ms")   // 500
htmx.parseInterval("1.5m")    // 90000
```

### Return Value

Returns the interval in milliseconds, or `undefined` if parsing fails.

## htmx.process()

> Processes htmx attributes on element

The `htmx.process()` function initializes htmx attributes on an element and its descendants.

### Syntax

```javascript
htmx.process(element)
htmx.process(element, force)
```

### Parameters

- `element` - DOM element to process
- `force` - (optional) when `true`, cleans up and resets existing htmx state before processing. Use after manually mutating hx attributes on an already-initialized element

### Usage

Use when dynamically adding HTML with htmx attributes to the page:

```javascript
// Add new content to the page
const newContent = document.createElement('div');
newContent.innerHTML = '<button hx-get="/api/data">Load</button>';
document.body.appendChild(newContent);

// Process htmx attributes on the new content
htmx.process(newContent);
```

Use `force` after manually mutating hx attributes on an already-initialized element:

```javascript
const btn = document.querySelector('#my-btn');
btn.setAttribute('hx-trigger', 'keyup');
htmx.process(btn, true);
```

### Notes

* Automatically called by htmx after swaps
* Useful when manually inserting HTML with htmx attributes
* Processes the element and all descendants
* Triggers `htmx:before:process` event before processing
* Initializes event listeners for `hx-get`, `hx-post`, etc.
* Sets up boosted links and forms
* Processes `hx-on` attributes
* When `force` is `true`, triggers `htmx:before:cleanup` before reinitializing

## htmx.registerExtension()

> Registers htmx extension

The `htmx.registerExtension()` function registers an htmx extension.

`htmx.defineExtension()` is an alias.

### Syntax

```javascript
htmx.registerExtension(name, extension)
```

### Parameters

- `name` - String name for the extension
- `extension` - Extension object with hook methods

### Usage

```javascript
htmx.registerExtension('my-ext', {
  init: function(api) {
    // Called when extension is registered
  },
  onEvent: function(name, evt) {
    // Called for htmx events
  }
});
```

### Extension Methods

Extensions can implement these hook methods:

- `init(api)` - Called when extension registers
- `onEvent(name, evt)` - Called for htmx events
- `transformResponse(text, xhr, elt)` - Modify response before processing
- `isInlineSwap(swapStyle)` - Return true if custom swap style should be processed
- `handleSwap(swapStyle, target, fragment, settleInfo)` - Handle custom swap styles
- `encodeParameters(xhr, parameters, elt)` - Modify request parameters

### Notes

* Same as `htmx.defineExtension()` - both names work
* Extension must be in `htmx.config.extensions` list to load (unless list is empty)
* Extensions are only registered once (duplicate registrations ignored)
* `init` method receives internal API for advanced integrations

## htmx.initialize()

> Manually initializes htmx

The `htmx.initialize()` function sets up htmx history handling and processes `document.body`. It is called automatically on `DOMContentLoaded` (or on the next tick if the document is already loaded), but can be called manually when htmx is loaded asynchronously or after a streaming response has delivered the full page.

### Syntax

```javascript
htmx.initialize()
```

### Parameters

None.

### Usage

Call after loading htmx asynchronously to ensure history handling and element initialization run at the right time:

```javascript
import('https://cdn.jsdelivr.net/npm/htmx.org/dist/htmx.min.js').then(() => {
    htmx.initialize();
});
```

Call from a streaming extension after the full page has arrived:

```javascript
// inside an hx-streaming extension handler
htmx.initialize();
```

### Notes

* Safe to call multiple times — history listeners are only registered once
* Equivalent to setting up history handling then calling `htmx.process(document.body)`

## htmx.timeout()

> Creates timeout `Promise`

The `htmx.timeout()` function creates a promise that resolves after a specified time interval.

### Syntax

```javascript
await htmx.timeout(time)
```

### Parameters

- `time` - Time to wait (number in ms or string like "2s", "500ms")

### Example

```javascript
// Wait 2 seconds
await htmx.timeout("2s");
console.log("2 seconds passed");

// Wait 1000ms
await htmx.timeout(1000);
console.log("1 second passed");
```

### Return Value

Returns a Promise that resolves after the specified time. If time is 0 or negative, resolves immediately.

## htmx.trigger()

> Triggers custom events

The `htmx.trigger()` function dispatches a custom event on an element.

### Syntax

```javascript
htmx.trigger(element, eventName, detail, bubbles)
```

### Parameters

- `element` - Element or CSS selector to trigger event on
- `eventName` - Name of the event to trigger
- `detail` - Optional detail object to pass with event (default: `{}`)
- `bubbles` - Whether event bubbles (default: `true`)

### Example

```javascript
// Trigger event on element
htmx.trigger('#myElement', 'customEvent', {
  message: 'Hello'
});

// Trigger without bubbling
htmx.trigger(document.body, 'myEvent', {}, false);
```

### Return Value

Returns `true` if the event was not cancelled, `false` otherwise.

## htmx.swap()

> Swaps HTML content

Use `htmx.swap()` to run the swap lifecycle without issuing a request.

```javascript
await htmx.swap({
  text: '<p>Done</p>',
  target: '#result'
})
```

htmx swaps the content into `#result` with the default swap style.

For requests, use `htmx.ajax()`.

### Syntax

```javascript
htmx.swap(ctx)
```

Set the content, target, and swap style in the context:

```javascript
await htmx.swap({
  text: '<p>Done</p>',
  target: '#result',
  swap: 'outerHTML transition:true'
})
```

### Context

#### `text`

The HTML string to swap.

```javascript
await htmx.swap({
  text: '<strong>Saved</strong>',
  target: '#status'
})
```

#### `target`

The target element or selector. It defaults to `document.body`.

```javascript
await htmx.swap({
  text: 'Saved',
  target: document.querySelector('#status')
})
```

```javascript
await htmx.swap({
  text: 'Saved',
  target: '#status'
})
```

#### `swap`

A serialized `hx-swap` value.

```javascript
await htmx.swap({
  text: 'Saved',
  target: '#status',
  swap: 'innerHTML transition:true settle:100ms'
})
```

It defaults to `htmx.config.defaultSwap`.

#### Other Fields

| Field | Description |
|---|---|
| `sourceElement` | Element used for relative selectors and swap events |
| `select` | Content selected from `text` |
| `selectOOB` | Out-of-band content selected from `text` |
| `transition` | Whether to use a view transition |

### Set the Source

Set `sourceElement` when a target or swap modifier uses a relative selector:

```javascript
let button = document.querySelector('#save')

await htmx.swap({
  text: 'Saved',
  target: 'closest .result',
  sourceElement: button
})
```

The source element also receives swap lifecycle events.

### Select Response Content

Use `select` to swap part of the content:

```javascript
await htmx.swap({
  text: '<p id="message">Saved</p><p>Ignored</p>',
  target: '#status',
  select: '#message'
})
```

Use `selectOOB` for out-of-band content.

### Events

`htmx.swap()` fires:

- `htmx:before:swap`
- `htmx:before:settle`
- `htmx:after:settle`
- `htmx:after:swap`
- `htmx:finally:swap`

Swap events fire on `sourceElement`. Settle events fire on each swap target.

### Return Value

`htmx.swap()` returns a `Promise` that resolves after the swap finishes.

```javascript
await htmx.swap({
  text: 'Saved',
  target: '#result'
})
console.log('Swap complete')
```

### Notes

- `htmx.swap()` processes main, out-of-band, and `<hx-partial>` content.
- `htmx.swap()` does not issue a request.

### See Also

- `htmx.ajax()`
- `hx-swap`
- `hx-target`
