# Events

## Contents

- htmx:config:request
- htmx:before:request
- htmx:after:request
- htmx:finally:request
- htmx:before:swap
- htmx:after:swap
- htmx:finally:swap
- htmx:before:cleanup
- htmx:after:cleanup
- htmx:confirm
- htmx:error
- htmx:abort
- htmx:before:init
- htmx:after:init
- htmx:before:process
- htmx:after:process
- htmx:before:on:init
- htmx:before:history:update
- htmx:after:history:update
- htmx:after:history:push
- htmx:after:history:replace
- htmx:before:history:restore
- htmx:before:viewTransition
- htmx:after:viewTransition
- load
- intersect
- every
- htmx:before:response
- htmx:before:settle
- htmx:after:settle
- htmx:response:error

## htmx:config:request

> Fires before request data is encoded

The `htmx:config:request` event fires after request values are collected and validated, but before encoding and sending.

### When It Fires

After htmx has constructed the request context but before `htmx:confirm` or `htmx:before:request`.

### Event Detail

The event provides a `ctx` object with the following structure:

```javascript
{
    sourceElement,  // Element that triggered the request
    sourceEvent,    // Event that triggered it
    target,         // Where the response will go
    select,         // hx-select value
    selectOOB,      // hx-select-oob value
    swap,           // hx-swap value
    push,           // hx-push-url value
    replace,        // hx-replace-url value
    transition,     // Whether to use view transitions
    request: {
        validate,     // Whether to validate the form
        action,       // Request URL
        method,       // HTTP method
        headers,      // Request headers object
        body,         // Request body (FormData)
        credentials,  // Fetch credentials mode
        mode,         // Fetch mode
        cache,        // Fetch cache mode
        timeout,      // Timeout in milliseconds
        // ... any other fetch options
    }
}
```

You can modify any property to change the request.

Call `evt.preventDefault()` to cancel the request.

### Examples

#### Add authentication to all requests

```javascript
document.body.addEventListener('htmx:config:request', function(evt) {
    evt.detail.ctx.request.headers['X-Auth-Token'] = getAuthToken();
});
```

#### Set longer timeout for specific endpoint

```javascript
htmx.on('htmx:config:request', (evt) => {
    if (evt.detail.ctx.request.action.includes('/slow-endpoint')) {
        evt.detail.ctx.request.timeout = 30000;
    }
});
```

#### Include credentials for CORS requests

```javascript
document.body.addEventListener('htmx:config:request', function(evt) {
    if (evt.detail.ctx.request.action.startsWith('https://api.example.com')) {
        evt.detail.ctx.request.credentials = 'include';
        evt.detail.ctx.request.mode = 'cors';
    }
});
```

#### Cancel request based on condition

```javascript
htmx.on('htmx:config:request', (evt) => {
    if (!isUserAuthorized()) {
        evt.preventDefault();
    }
});
```

### Notes

- This is the ideal place to modify request configuration globally
- Changes made here apply after `hx-config` attributes are processed
- Use this for cross-cutting concerns like authentication, logging, or global timeouts

## htmx:before:request

> Fires immediately before `fetch()`

The `htmx:before:request` event fires immediately before the `fetch()` call is made.

### When It Fires

Right before the network request is sent, after all configuration and validation.

### Event Detail

- `ctx` - Request context object with final request configuration

### Example

```javascript
htmx.on('htmx:before:request', (evt) => {
  console.log('Sending request to:', evt.detail.ctx.request.action);
  // Show loading indicator
});
```

Cancel this event to prevent the request from being sent.

## htmx:after:request

> Fires after `response.text()`

The `htmx:after:request` event fires immediately after the `fetch()` call resolves and the response is received.

### When It Fires

After the server responds, before content swapping occurs.

### Event Detail

- `ctx` - Request context including response data

### Example

```javascript
htmx.on('htmx:after:request', (evt) => {
  console.log('Response status:', evt.detail.ctx.response.status);
  // Hide loading indicator
});
```

The response is available but hasn't been swapped into the DOM yet.

## htmx:finally:request

> Fires after lifecycle ends, including failures

The `htmx:finally:request` event fires when request completes, fails, or is cancelled.

### When It Fires

After request processing ends. It does not fire if processing stops before the request begins issuing, such as after validation failure or cancellation of `htmx:config:request`.

### Event Detail

- `ctx` - Request context object

### Example

```javascript
htmx.on('htmx:finally:request', (evt) => {
  console.log('Request complete:', evt.detail.ctx);
  // Always hide loading indicator, clean up resources
});
```

Useful for cleanup operations started after the request begins issuing.

## htmx:before:swap

> Fires before DOM update

The `htmx:before:swap` event fires after response content is parsed but before it's inserted or swapped into the DOM.

### When It Fires

After the response is received and parsed, but before any DOM modifications occur.

### Event Detail

- `ctx` - Request context including parsed response
- `tasks` - Array of swap tasks to be performed

### Example

```javascript
htmx.on('htmx:before:swap', (evt) => {
  console.log('About to swap:', evt.detail.ctx.response);
  // Modify response before swapping
  // Or cancel swap by calling evt.preventDefault()
});
```

Cancel this event to prevent the swap from occurring.

## htmx:after:swap

> Fires after DOM update

The `htmx:after:swap` event fires after new content has been swapped into the DOM.

### When It Fires

Immediately after the DOM swap operation completes, before elements are processed.

### Event Detail

- `ctx` - Request context including swap details

### Example

```javascript
htmx.on('htmx:after:swap', (evt) => {
  console.log('Content swapped into:', evt.detail.ctx.target);
  // Initialize widgets, scroll to position, etc.
});
```

The new content is in the DOM but may not be fully processed by htmx yet.

## htmx:finally:swap

> At the end of swap lifecycle

The `htmx:finally:swap` event fires at the very end of the swap cycle, whether successful or failed.

### When It Fires

After all swap processing completes, similar to a `finally` block in try/catch. Fires after `htmx:after:swap` on the success path, or after an error if the swap fails.

### Event Detail

- `ctx` - Request context object

### Example

```javascript
htmx.on('htmx:finally:swap', (evt) => {
  console.log('Swap complete:', evt.detail.ctx);
  // Always hide loading indicator, clean up resources
});
```

Useful for cleanup operations that should always run after a swap, regardless of success or failure.

## htmx:before:cleanup

> Fires before element data removal

The `htmx:before:cleanup` event fires before htmx removes listeners and internal data from an element.

### When It Fires

- Before an element is removed from the DOM during a swap
- Before htmx re-processes an element

### Event Detail

Empty - no additional context provided.

### Example

```javascript
htmx.on('htmx:before:cleanup', (evt) => {
  console.log('Cleaning up:', evt.target);
  // Save state or clean up custom data
});
```

Use this to perform cleanup operations before htmx removes its data.

## htmx:after:cleanup

> Fires after element data removal

The `htmx:after:cleanup` event fires after htmx has removed all listeners and internal data from an element.

### When It Fires

- After an element has been removed from the DOM
- After htmx has detached all event listeners

### Event Detail

Empty - no additional context provided.

### Example

```javascript
htmx.on('htmx:after:cleanup', (evt) => {
  console.log('Cleanup complete:', evt.target);
});
```

The element no longer has htmx behaviors attached at this point.

## htmx:confirm

> Fires before handling `hx-confirm`

The `htmx:confirm` event fires only when an element has an `hx-confirm` attribute. It allows you to replace the default `window.confirm()` dialog with a custom confirmation UI.

### When It Fires

After the request context is built, before the request is sent, when the triggering element has `hx-confirm` set.

### Event Detail

- `ctx` - Request context object
- `issueRequest` - Callback function to call to proceed with the request
- `dropRequest` - Callback function to call to cancel the request

If you call `evt.preventDefault()`, you **must** call either `issueRequest()` or `dropRequest()`. Failing to call one of them will leave the request pending indefinitely.

### Example

```javascript
htmx.on('htmx:confirm', (evt) => {
  evt.preventDefault(); // Prevent default window.confirm() dialog

  // Show custom modal
  showCustomModal(evt.detail.ctx.confirm).then((confirmed) => {
    if (confirmed) {
      evt.detail.issueRequest(); // User confirmed — proceed
    } else {
      evt.detail.dropRequest(); // User cancelled — drop the request
    }
  });
});
```

Cancel the default event and call either `issueRequest()` to proceed with the request or `dropRequest()` to cancel it.

## htmx:error

> Fires after request or swap exception

The `htmx:error` event fires when an exception occurs during the request or swap process.

### When It Fires

- Network errors (connection failed, timeout)
- Swap errors (invalid content, DOM errors)
- Any other exception during the htmx request lifecycle

This event does **not** fire for HTTP error statuses (4xx/5xx) — use `htmx:response:error` for those.

### Event Detail

- `ctx` - Request context at time of error
- `error` - The exception object

### Example

```javascript
htmx.on('htmx:error', (evt) => {
  console.error('Request failed:', evt.detail.error);
  console.log('Context:', evt.detail.ctx);
  // Show error message to user
});
```

Use this for centralized error handling and user feedback.

## htmx:abort

> Aborts in-flight request

The `htmx:abort` event is a control event that, when fired on an element, aborts its ongoing request.

### When To Fire It

Fire this event to programmatically cancel a request that's in progress.

### Event Detail

Not applicable - this is a control event you trigger, not one you listen for.

### Example

```javascript
// Abort request on a specific element
htmx.trigger('#myElement', 'htmx:abort');

// Abort all requests in a container
document.querySelectorAll('#container [hx-get]').forEach(el => {
  htmx.trigger(el, 'htmx:abort');
});
```

The element's ongoing request will be cancelled when this event is received.

## htmx:before:init

> Fires before element initialization

The `htmx:before:init` event fires before a specific element is initialized with htmx metadata.

### When It Fires

During element processing, before htmx attaches its internal metadata structure to the element.

### Event Detail

Empty - no additional context provided.

### Example

```javascript
htmx.on('htmx:before:init', (evt) => {
  console.log('Initializing element:', evt.target);
});
```

Cancel this event to prevent htmx from initializing the element. 

This runs early in the initialization lifecycle, before attributes are fully parsed.

## htmx:after:init

> Fires after element initialization

The `htmx:after:init` event fires after an element has been fully initialized and all event listeners have been attached.

### When It Fires

After htmx has completely set up an element with all its behaviors, triggers, and event listeners.

### Event Detail

Empty - no additional context provided.

### Example

```javascript
htmx.on('htmx:after:init', (evt) => {
  console.log('Element ready:', evt.target);
  // Element is fully initialized and ready for interaction
});
```

The element is fully ready for htmx interactions at this point.

## htmx:before:process

> Fires before DOM node processing

The `htmx:before:process` event fires before htmx begins processing a DOM node or subtree to attach htmx behaviors.

### When It Fires

- During initial page load processing
- After new content is swapped into the DOM
- When `htmx.process()` is called manually

### Event Detail

Empty - no additional context provided.

### Example

```javascript
htmx.on('htmx:before:process', (evt) => {
  console.log('About to process:', evt.target);
});
```

Cancel this event to prevent htmx from processing the element.

## htmx:after:process

> Fires after DOM node processing

The `htmx:after:process` event fires after htmx has finished processing a DOM node or subtree.

### When It Fires

- After initial page load processing completes
- After new content has been processed and behaviors attached
- After `htmx.process()` completes

### Event Detail

Empty - no additional context provided.

### Example

```javascript
htmx.on('htmx:after:process', (evt) => {
  console.log('Finished processing:', evt.target);
  // Initialize third-party widgets on processed content
});
```

This is useful for initializing JavaScript widgets after htmx processes new content.

## htmx:before:on:init

> Fires before htmx wires the hx-on attributes on an element

The `htmx:before:on:init` event fires before htmx binds the `hx-on` attributes on an element.

Cancel it to leave those attributes unbound.

### When It Fires

During `htmx.process()`, after `htmx:before:process` and before element initialization.

htmx fires it once for the processed root, and once for each descendant that carries an `hx-on` attribute.

### Event Detail

Empty - no additional context provided.

### Example

```javascript
htmx.on('htmx:before:on:init', (evt) => {
  if (evt.target.closest('.no-inline-handlers')) {
    evt.preventDefault();
  }
});
```

### Notes

* The event bubbles and is cancelable.
* `preventDefault()` stops htmx from binding the `hx-on` attributes on that element only. Processing continues for the rest of the tree.

### See Also

* `hx-on`
* `htmx:before:process`
* `htmx:before:init`

## htmx:before:history:update

> Fires before browser history update

The `htmx:before:history:update` event fires before htmx pushes or replaces a browser history state.

### When It Fires

Before `history.pushState()` or `history.replaceState()` is called.

### Event Detail

- `history` - Object with `type` ("push" or "replace") and `path`
- `sourceElement` - Element that triggered the navigation
- `response` - Response object

### Example

```javascript
htmx.on('htmx:before:history:update', (evt) => {
  console.log('Updating history:', evt.detail.history.type, evt.detail.history.path);
  // Modify path or cancel history update
});
```

Cancel this event to prevent the history update.

## htmx:after:history:update

> Fires after browser history update

The `htmx:after:history:update` event fires after htmx has updated the browser history state.

### When It Fires

After `history.pushState()` or `history.replaceState()` completes.

### Event Detail

- `history` - Object with `type` ("push" or "replace") and `path`
- `sourceElement` - Element that triggered the navigation
- `response` - Response object

### Example

```javascript
htmx.on('htmx:after:history:update', (evt) => {
  console.log('History updated to:', evt.detail.history.path);
  // Update analytics, breadcrumbs, etc.
});
```

The URL bar now reflects the new path.

## htmx:after:history:push

> Fires after history push

The `htmx:after:history:push` event fires specifically after a `history.pushState()` operation (creates new history entry).

### When It Fires

After a new history entry is pushed, allowing forward/back navigation to this point.

### Event Detail

- `path` - The path that was pushed into history

### Example

```javascript
htmx.on('htmx:after:history:push', (evt) => {
  console.log('Pushed to history:', evt.detail.path);
  // Track navigation in analytics
});
```

This creates a new entry in the browser's history stack.

## htmx:after:history:replace

> Fires after history replacement

The `htmx:after:history:replace` event fires specifically after a `history.replaceState()` operation (replaces current history entry).

### When It Fires

After the current history entry is replaced, without creating a new back button entry.

### Event Detail

- `path` - The path that replaced the current history entry

### Example

```javascript
htmx.on('htmx:after:history:replace', (evt) => {
  console.log('Replaced history with:', evt.detail.path);
});
```

This modifies the current history entry without affecting the back button.

## htmx:before:history:restore

> Fires before history restoration

The `htmx:before:history:restore` event fires when the user navigates back or forward through history (popstate event).

### When It Fires

When the browser's back or forward button is clicked, before content is restored.

### Event Detail

- `path` - The path being restored
- `cacheMiss` - Boolean indicating if content needs to be fetched

### Example

```javascript
htmx.on('htmx:before:history:restore', (evt) => {
  console.log('Restoring:', evt.detail.path);
  if (evt.detail.cacheMiss) {
    console.log('Will fetch from server');
  }
});
```

Cancel this event to prevent history restoration and handle it manually.

## htmx:before:viewTransition

> Fires before view transition starts

The `htmx:before:viewTransition` event fires before a View Transition starts (if browser supports View Transitions API and `htmx.config.transitions` is
`true`).

### When It Fires

Before the swap operation begins its view transition animation.

Fires on the element that triggered the swap, or on `document` when there is none.

### Event Detail

- `task` - Transition callback function. Replace it to wrap the transition.
- `ctx` - The request context driving the swap

### Example

```javascript
htmx.on('htmx:before:viewTransition', (evt) => {
  console.log('Starting view transition');
  // Customize transition behavior
});
```

Replace `detail.task` to run your own work around the transition. The
replacement is awaited in place of the original:

```javascript
htmx.on('htmx:before:viewTransition', (evt) => {
  let task = evt.detail.task;
  evt.detail.task = async () => {
    await prepare(evt.detail.ctx);
    await task();
  };
});
```

## htmx:after:viewTransition

> Fires after view transition completes

The `htmx:after:viewTransition` event fires after a View Transition animation completes.

### When It Fires

After the View Transition API finishes animating the swap operation.

Fires on the element that triggered the swap, or on `document` when there is none.

### Event Detail

- `task` - Transition callback information
- `ctx` - The request context driving the swap

### Example

```javascript
htmx.on('htmx:after:viewTransition', (evt) => {
  console.log('View transition complete');
  // Perform actions after transition animation
});
```

The swap and transition are both complete at this point.

## load

> Fires after element initialization

The `load` event is a _synthetic_ event that fires immediately on element initialization, mimicking the standard DOM `load` event.  It is not a real event and cannot be listened for, but can be used in an `hx-trigger`.

### When It Fires

Right before `htmx:after:init`, providing a familiar event name for developers.

### Event Detail

Empty - no additional context provided.

### Example

```html
<div hx-get="/content" hx-trigger="load">
  Loading...
</div>
```

This provides compatibility with standard DOM patterns.

## intersect

> Fires when element enters viewport

The `intersect` trigger event fires when an element enters the viewport, detected via IntersectionObserver.

### When It Fires

When an element becomes visible in the viewport, used by `hx-trigger``="intersect"`.

### Event Detail

Empty - no additional context provided.

### Example

```html
<div id="lazy" hx-get="/lazy-content" hx-trigger="intersect">
  Content loads when scrolled into view
</div>
```

```javascript
htmx.on('#lazy', 'intersect', (evt) => {
  console.log('Element visible:', evt.target);
});
```

This enables lazy loading and infinite scroll patterns.

## every

> Fires at each polling interval

The `every` trigger event fires periodically at a specified interval, used for polling.

### When It Fires

At regular intervals specified in the `hx-trigger` attribute (e.g., `every 2s`).

### Event Detail

Empty - no additional context provided.

### Example

```html
<div id="status" hx-get="/status" hx-trigger="every 5s">
  Status updates every 5 seconds
</div>
```

```javascript
htmx.on('#status', 'every', (evt) => {
  console.log('Polling:', evt.target);
});
```

Useful for live updates, status checks, and real-time data display.

## htmx:before:response

> Fires after `fetch()`, before `response.text()`

The `htmx:before:response` event fires after a fetch response arrives but before htmx reads the response body.

### When It Fires

After the network response is received, before the body is consumed or any swap begins.

### Event Detail

- `ctx.response.raw` - The raw Response object (body not yet consumed)
- `ctx.response.status` - The HTTP status code
- `ctx.response.headers` - The response headers

### Example

```javascript
htmx.on('htmx:before:response', (evt) => {
  const status = evt.detail.ctx.response.status;
  const headers = evt.detail.ctx.response.headers;

  console.log('Response status:', status);
  console.log('Content-Type:', headers.get('content-type'));

  // Handle error status codes before body is consumed
  if (status >= 400) {
    console.log('Error response received');
  }
});
```

Cancel this event to skip normal response processing, including body consumption and the swap.

## htmx:before:settle

> Fires after DOM insertion, before settle tasks

The `htmx:before:settle` event fires after new content is inserted into the DOM but before CSS transitions are applied.

### When It Fires

After the swap completes, right before htmx runs the settle phase (which applies CSS transitions and removes old attributes).

### Event Detail

- `task` - The swap task being settled
- `newContent` - Array of newly inserted nodes, which can include text nodes
- `settleTasks` - Array of pending settle callbacks (e.g. CSS transition steps)

### Example

```javascript
htmx.on('htmx:before:settle', (evt) => {
  console.log('About to settle', evt.detail.newContent.length, 'node(s)');
  // Modify elements before transitions run
});
```

## htmx:after:settle

> Fires after settle tasks

The `htmx:after:settle` event fires after htmx finishes the settle phase, including any CSS transitions.

### When It Fires

After all settle tasks (CSS transitions, attribute cleanup) have completed for newly swapped content.

### Event Detail

- `task` - The swap task that was settled
- `newContent` - Array of settled nodes, which can include text nodes
- `settleTasks` - Array of settle tasks that ran

### Example

```javascript
htmx.on('htmx:after:settle', (evt) => {
  console.log('Settle complete for', evt.detail.newContent.length, 'node(s)');
  // Safe to interact with fully-settled DOM
});
```

The DOM is fully stable at this point — all transitions have run and temporary attributes have been cleaned up.

## htmx:response:error

> Fires for HTTP status 400 or higher

The `htmx:response:error` event fires when the server responds with an HTTP error status code (400 or higher).

### When It Fires

After `htmx:after:request` and before the swap phase, when `response.status >= 400`.

This event does **not** fire for network errors or timeouts — use `htmx:error` for those.

### Event Detail

- `ctx` - The full request context, including:
  - `ctx.response.status` - The HTTP status code
  - `ctx.response.headers` - Response headers
  - `ctx.text` - The response body

### Example

```javascript
htmx.on('htmx:response:error', (evt) => {
  let status = evt.detail.ctx.response.status;
  console.error(`HTTP ${status} error`);
});
```

### Migration from htmx 2

This event replaces htmx 2's `htmx:responseError`. The event detail structure has changed — the response
information is now available via `evt.detail.ctx.response` rather than directly on `evt.detail`.

### See Also

- `hx-status`
- `htmx.config.noSwap`
