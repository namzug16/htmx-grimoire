# Polling

> Check for updates at regular intervals

## Basic usage

Add an `every <time>` trigger to poll an endpoint.

```html
<div id="server-status" hx-get="/status" hx-trigger="every 2s" hx-swap="outerMorph">
  <span>CPU 34%</span>
</div>
```

- `hx-trigger`=`"every 2s"` fires a request every two seconds.
- `hx-swap`=`"outerMorph"` replaces the element with the response. A morph keeps focus, scroll position, and CSS transitions intact.

The server returns the same element with fresh data:

```html
<div id="server-status" hx-get="/status" hx-trigger="every 2s" hx-swap="outerMorph">
  <span>CPU 61%</span>
</div>
```

The interval unit is `ms`, `s`, or `m`. A bare number is milliseconds.

```html
<div hx-get="/status" hx-trigger="every 500ms">...</div>
<div hx-get="/status" hx-trigger="every 1m">...</div>
```

## Stopping the poll

htmx clears the interval when the element leaves the DOM. To stop the poll, return the element without the trigger attributes.

```html
<!-- server response when there is nothing more to watch -->
<div id="server-status">
  <span>Job complete</span>
</div>
```

The demo above uses this to pause. The Pause button posts to `/toggle`, and the server renders the card without `hx-get` and `hx-trigger`.

## Conditional polling

Add a filter after the interval. The request only fires when the expression is true.

```html
<div hx-get="/status"
     hx-trigger="every 2s [document.visibilityState === 'visible']"
     hx-swap="outerMorph">
  ...
</div>
```

This stops network traffic while the tab is in the background. The interval still runs, so the poll resumes as soon as the user comes back.

## Notes

### Load polling

To poll only until a job ends, use `hx-trigger="load delay:1s"` instead of `every`. The server controls each next request, and the poll ends when the response omits the trigger. See Progress Bar for a full example.

### Skip unchanged responses

Each poll costs a full response body even when nothing changed. The `hx-ptag` extension adds a per-element tag. The server compares the incoming tag, then returns `304 Not Modified`, and htmx skips the swap.

### Choose an interval

Each poll is a full request. A 1 second interval on a page with 1000 users is 1000 requests per second. Poll no faster than the data changes.

For high-frequency updates, a persistent connection costs less. See the `hx-sse` extension.

### Overlapping requests

htmx queues requests for the same element, and keeps at most one waiting. A slow response does not stack up parallel requests. Use `hx-sync` to change this.
