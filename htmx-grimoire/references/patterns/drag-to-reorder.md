# Drag to Reorder

> Change order of records with drag and drop

## Basic usage

This pattern integrates the [Sortable.js](https://sortablejs.github.io/Sortable/) library with htmx to persist drag-and-drop reordering on the server.

On the client, wrap your items in a form that posts on the Sortable `end` event.

```html
<form class="sortable" hx-post="/items" hx-trigger="end"
      hx-on:load="new Sortable(this, {
                      animation: 150,
                      ghostClass: 'sortable-ghost',
                      filter: '.htmx-indicator',
                      onMove: e => !e.related.classList.contains('htmx-indicator'),
                      onEnd: function () { this.option('disabled', true) }
                  })"
      hx-on::after:swap="Sortable.get(this).option('disabled', false)">
  <div class="htmx-indicator">Updating...</div>
  <div><input type="hidden" name="item" value="1"/>Item 1</div>
  <div><input type="hidden" name="item" value="2"/>Item 2</div>
  <div><input type="hidden" name="item" value="3"/>Item 3</div>
</form>
```

- `hx-post` sends the new order to `/items`.
- `hx-trigger`=`"end"` fires when Sortable finishes a drag. Note that the `end` event bubbles up to the form.
- Each item has a hidden input, so the server receives the ids in their new order.
- The `.htmx-indicator` div shows while the request is in flight. htmx hides it again when the response completes.
- `hx-on:load` builds the Sortable instance when htmx processes the form.  Note that this is just for convenience, you could easily move this to a vanilla setup script.
