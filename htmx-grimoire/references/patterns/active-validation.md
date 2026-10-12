# Active Validation

> Validate form input as you type

## Basic usage

On the client, the input validates on each keystroke (debounced).

```html
<input name="username"
       hx-post="/check-username"
       hx-trigger="input changed delay:300ms"
       hx-target="next span">

<span></span>
```

- `hx-post` sends the value to `/check-username`.
- `hx-trigger` fires on [`input`](https://developer.mozilla.org/en-US/docs/Web/API/Element/input_event) after a 300ms `delay`, and only when the value has `changed`.
- `hx-target`=`"next span"` puts the response into the next sibling `<span>`.

On the server, respond with a validation message:

```html
<span class="error">That username is taken.</span>
```

Or an empty `<span>` when valid.
