# Bulk Actions

> Perform actions on multiple records

## How It Works

Wrap a table in a `<form>`. Each row has a checkbox, and an action bar appears when any are checked. Clicking a row toggles its checkbox.

```html
<form hx-target:inherited="this" hx-swap:inherited="outerHTML">

    <div id="action-bar" class="hidden">
        <span>With selected:</span>
        <button hx-post="/activate">Activate</button>
        <button hx-post="/deactivate">Deactivate</button>
        <button hx-post="/delete">Delete</button>
    </div>

    <table>
        <thead>
        <tr>
            <th><input type="checkbox" class="select-all"></th>
            <th>Name</th>
            <th>Email</th>
            <th>Status</th>
        </tr>
        </thead>
        <tbody>
        <tr>
            <td><input type="checkbox" name="selected" value="joe@smith.org"></td>
            <td>Joe Smith</td>
            <td>joe@smith.org</td>
            <td>Active</td>
        </tr>
        ...
        </tbody>
    </table>
</form>
```

- `hx-target`=`"this"` and `hx-swap`=`"outerHTML"` on the form mean every action replaces the entire form with the server's response.
- Each action button uses `hx-post` to a different endpoint. Only checked `name="selected"` values are submitted.
- Use `hx-target:inherited` to avoid repeating target declarations on each action button.

### Clickable rows

Make the whole row a click target so users don't have to aim for the small checkbox:

```html
<tr _="on click
       if event.target.tagName !== 'INPUT'
         toggle @checked on the <input[name='selected']/> in me
         then send change to the <input[name='selected']/> in me">
    <td><input type="checkbox" name="selected" value="joe@smith.org"></td>
    ...
</tr>
```

The `if event.target.tagName !== 'INPUT'` guard prevents double-toggling when clicking directly on the checkbox. Highlighting the selected row is pure CSS:

```css
tr:has(input:checked) {
    background: var(--selected-bg);
}
```

### Conditional action bar

Show the action bar only when at least one checkbox is checked. With CSS `:has()`:

```css
.action-bar { display: none; }
form:has(input[name="selected"]:checked) .action-bar { display: flex; }
```

Or with hyperscript on the `<tbody>` (for browsers without `:has()` support):

```html
<tbody _="on change from <input[name='selected']/>
          if (<input[name='selected']:checked/> in closest <form/>).length > 0
            show #action-bar
          else
            hide #action-bar
          end">
```

### Select all

A checkbox in the header toggles all row checkboxes:

```html
<input type="checkbox"
       _="on change
          set checked to my.checked
          then for cb in <input[name='selected']/> in closest <form/>
            set cb.checked to checked
          then send checkChange to closest <form/>">
```

### Server response

The server processes the selected emails, performs the bulk action, and re-renders the full table. Selections are cleared and statuses reflect the update:

```html
<!-- POST /activate with selected=joe@smith.org&selected=kim@yee.org -->
<form hx-target:inherited="this" hx-swap:inherited="outerHTML">
    <!-- ...updated table rows... -->
    <output>Activated 1 user</output>
</form>
```
