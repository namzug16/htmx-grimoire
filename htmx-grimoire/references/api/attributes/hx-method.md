# hx-method

> Specifies HTTP method for request

The `hx-method` attribute specifies the HTTP method (verb) to use for the request. It is typically paired with `hx-action` to separate the URL from the method.

## Syntax

```html
<button hx-action="/api/users" hx-method="post">
    Create User
</button>
```

## Priority

`hx-method` overrides both `formmethod` on submitter buttons and the native `method` attribute on forms:

```html
<!-- Always sends PUT regardless of native method or submitter -->
<form hx-action="/items/1" hx-method="put" method="post">
    <input name="name">
    <button>Save</button>
</form>
```

A shorthand attribute such as `hx-post` sets the URL and the method together, so it wins over `hx-method`:

```html
<!-- Sends POST. The hx-method value is ignored. -->
<button hx-post="/items" hx-method="put">Save</button>
```

When `hx-method` is omitted, htmx falls back to `formmethod`, then native `method`, then `GET`. See `hx-action` Method Resolution for the full chain.

## Notes

* Valid values: `get`, `post`, `put`, `patch`, `delete`, `query` (case-insensitive)
* If no method can be determined from any source, defaults to `GET`
* The shorthand attributes `hx-get`, `hx-post`, etc. combine URL and method into one attribute

## Example

```html
<!-- Explicit method -->
<button hx-action="/api/users/123" hx-method="delete">
    Delete User
</button>

<!-- Equivalent shorthand -->
<button hx-delete="/api/users/123">
    Delete User
</button>

<!-- Server-rendered dynamic method -->
<form hx-action="/resources/${id}" hx-method="${method}" hx-target="this">
    <input name="name">
    <button>${action_label}</button>
</form>
```
