# LLM Streaming Response

> Stream a reply into the page token by token

In this demo a language model produces its answer a token at a time. Rather than wait for the whole reply, there is
a stream of tokens via an SSE response.   The `hx-sse` extension handles this stream and places
the content that is returned from the server into the appropriate target.

## Explanation

The code is pretty simple: the form targets the transcript and appends to it, exactly as it would for a normal request.

```html
<script src="https://cdn.jsdelivr.net/npm/htmx.org/dist/ext/hx-sse.js"></script>

<div id="conversation"></div>

<form hx-get="/generate"
      hx-target="#conversation" hx-swap="beforeend scroll:bottom"
      hx-disable="find fieldset"
      hx-on::before:request="this.reset()">

  <fieldset>
    <input name="prompt" placeholder="Ask anything...">
    <button>Ask</button>
  </fieldset>

  <button type="button" hx-get="/clear" hx-target="#conversation" hx-swap="innerHTML">
    Clear
  </button>
</form>
```

- The request lives on the `<form>`, so it fires on submit and carries the form fields. Enter works as well as the button.
- `hx-swap`=`"beforeend"` appends each event, so turns build up instead of replacing each other. `scroll:bottom` keeps the newest text in view.
- `hx-target` points at the transcript.
- `hx-disable`=`"find fieldset"` disables the prompt and the Ask button until the reply finishes. A `<fieldset>` disables everything inside it, so one attribute covers both. This works because SSE defaults to `sse.releaseOn:end`.
- Clear sits outside the fieldset, so it stays available while a reply is arriving.
- There is no `hx-sse:connect` here. The extension handles any response that arrives as `text/event-stream`, so a normal request is enough.

To let users type ahead while tokens are still arriving, have the server send `hx:release` after initial response is in place. The fieldset re-enables but tokens keep appending.

The server side answers with a response type of `text/event-stream`, which causes the SSE extension to take over.  It
treats each unnamed event as content to be swapped into the target:

```http
HTTP/1.1 200 OK
Content-Type: text/event-stream

data: <p>What is hypermedia?</p>

data: Hypermedia

data: is

data: a system

```

Everything appends in order, so the question lands as a block and the tokens flow after it as the answer. The connection closes when the model is done.

Clear is an ordinary request. The server stops the generation still in progress and answers with an empty body, which empties the transcript:

```html
<button type="button" hx-get="/clear" hx-target="#conversation" hx-swap="innerHTML">
  Clear
</button>
```

Cancelling on the server rather than in the browser keeps one source of truth. The generation stops where it is produced, instead of the client walking away from a reply the server keeps writing.

## See also

- `hx-sse` for named events, persistent connections, and reconnection.
- Progress Bar when the server reports progress rather than content.
