# Live Updates

> Push updates over a persistent connection

In this demo the server holds the connection open and pushes a row whenever a price moves. The `hx-sse` extension keeps the stream alive for as long as the page is on screen.

## Explanation

The code for the ticker is trivial: one attribute opens the connection.

```html
<script src="https://cdn.jsdelivr.net/npm/htmx.org/dist/ext/hx-sse.js"></script>

<div hx-sse:connect="/ticker" hx-config="sse.releaseOn:end">
  <span class="htmx-indicator">Live</span>

  <table>
    <tbody id="quotes">
      <tr id="q-HTMX"><td>HTMX</td><td>142.10</td></tr>
      <tr id="q-REST"><td>REST</td><td>88.45</td></tr>
    </tbody>
  </table>
</div>
```

- `hx-sse:connect` opens the connection on `load` and holds it open.
- `sse.releaseOn:end` holds the request open until the stream ends. The connection element keeps the `htmx-request` class for that whole time, so the `htmx-indicator` badge inside it stays lit. `hx-sse:connect` defaults to `immediate`, which releases the request as soon as the connection opens and darkens the badge.

The server pushes out HTML content when a price move occurs: an `<hx-partial>` that targets the row it updates:

```http
HTTP/1.1 200 OK
Content-Type: text/event-stream

data: <hx-partial hx-target="#q-HTMX" hx-swap="outerHTML"><tr id="q-HTMX">...</tr></hx-partial>

data: <hx-partial hx-target="#q-REST" hx-swap="outerHTML"><tr id="q-REST">...</tr></hx-partial>

```

## Notes

A partial's `hx-target` is an ordinary selector, so one connection can update any part of the page. The connection 
element does not even have to contain what it updates.

### Why not just `hx-get`?

An ordinary `hx-get` whose response is of content type `text/event-stream` also streams, as in 
LLM Streaming Response.  Why not just use that?

`hx-sse:connect` adds the two configuration options that are good for long-lived connections:

- Reconnection: A plain `hx-get` stream ends for good when the connection drops, an `hx-sse:connect` element retries with backoff.
- Background pausing: An `hx-sse:connect` element closes when the tab it is on is hidden and resumes when it returns. Browsers cap connections per origin so this saves connections.

Both are available via the `hx-config` attribute, so you can ask for them either way:

```html
<div hx-get="/ticker" hx-trigger="load"
     hx-config="sse.reconnect:true sse.pauseOnBackground:true"></div>
```

`hx-sse:connect` is shorthand for this config, plus it triggers on `load` rather than `click`.

### Closing

The connection closes when the element leaves the DOM. To close it from the server, send a named event and name it:

```html
<div hx-sse:connect="/ticker" hx-sse:close="market-closed"></div>
```

## See also

- LLM Streaming Response when the user asks for something and the answer arrives in pieces.
- Polling when updates are rare enough that holding a connection open is not worth it.
- `hx-sse` for named events, replay, and the full configuration.
