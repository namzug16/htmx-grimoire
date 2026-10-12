# Delete in Place

> Remove a record without page refresh

## Basic usage

On the client, set up the table body with inherited attributes so every delete button shares the same behavior.

```html
<tbody hx-confirm:inherited="Are you sure?"
       hx-target:inherited="closest tr"
       hx-swap:inherited="outerHTML swap:500ms">
  <tr>
    <td>Angie MacDowell</td>
    <td>angie@macdowell.org</td>
    <td>Active</td>
    <td>
      <button hx-delete="/contact/1">Delete</button>
    </td>
  </tr>
  ...
</tbody>
```

- `hx-confirm` prompts the user before sending the request. The `:inherited` modifier lets every button in the body inherit it.
- `hx-target`=`"closest tr"` targets the row containing the button.
- `hx-swap`=`"outerHTML swap:500ms"` replaces the entire row after a 500ms swap delay, giving the fade-out transition time to play.
- `hx-delete` sends a DELETE request to the server.

On the server, respond with an empty body and a `200` status. The row is replaced with nothing (it just disappears).

## Notes

### Fade-out animation

During the swap delay, htmx adds the `htmx-swapping` class to the target row. Use it to trigger a CSS opacity transition so the row fades out before it's removed.

```css
tr.htmx-swapping td {
  opacity: 0;
  transition: opacity 500ms ease-out;
}
```
