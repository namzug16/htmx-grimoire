# Edit in Place

> Update a record without page refresh

## Basic usage

On the client, display the current values with a button that fetches the edit form.

```html
<div hx-target:inherited="this" hx-swap:inherited="outerHTML">
    <p>Name: Joe Smith</p>
    <p>Email: joe@smith.org</p>
    <button hx-get="/users/1/edit">Edit</button>
</div>
```

- `hx-target`=`"this"` sets the target to the `<div>` itself.
- `hx-swap`=`"outerHTML"` replaces the entire `<div>` with the response.
- `hx-get` on the button requests the edit form.

On the server, respond with a form pre-filled with the current values.

```html
<form hx-put="/users/1" hx-target:inherited="this" hx-swap:inherited="outerHTML">
    <label>Name <input name="name" value="Joe Smith"></label>
    <label>Email <input name="email" value="joe@smith.org"></label>
    <button type="submit">Save</button>
    <button type="button" hx-get="/users/1">Cancel</button>
</form>
```

- `hx-put` submits the form as a `PUT` request.
- **Save** submits the form, and the server responds with the updated view mode HTML.
- **Cancel** re-fetches the view mode without saving.

## Notes

### REST conventions

The endpoints follow standard REST conventions:

- `GET /users/1`: retrieve the view
- `GET /users/1/edit`: retrieve the edit form
- `PUT /users/1`: update the resource

The URL represents the resource, and the HTTP method indicates the action.
