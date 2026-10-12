# Click to Load

> Load more items when you click a button

## Basic usage

On the client, put a button at the end of your list.

```html
<button hx-get="/comments?page=2"
        hx-swap="outerHTML"
        hx-target="this">
  Show more comments
</button>
```

When clicked, it extends the list (without any client-side state).

- `hx-get` requests `/comments?page=2`.
- `hx-swap`=`"outerHTML"` sets the strategy to replace the target.
- `hx-target`=`"this"` sets the target to itself.

On the server, respond with the next items plus a button pointing to `?page=3`:

```html
<div class="comment">...</div>
<div class="comment">...</div>
<div class="comment">...</div>

<!-- When there are no more pages, just omit this button -->
<button hx-get="/comments/?page=3"
        hx-swap="outerHTML"
        hx-target="this">
  Show more comments
</button>
```

Because `outerHTML` replaces the old button, the new one takes its place.
