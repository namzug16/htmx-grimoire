# Active Search

> Filter search results as you type

## Basic usage

On the client, create a search input that targets a results container.

```html
<input type="search" name="search"
       hx-post="/search"
       hx-trigger="input changed delay:200ms, keyup[key=='Enter'], load"
       hx-target="#results"
       hx-indicator=".htmx-indicator">

<tbody id="results"></tbody>
```

- `hx-post` sends the input value to `/search`.
- `hx-trigger` combines three triggers:
  - [`input`](https://developer.mozilla.org/en-US/docs/Web/API/Element/input_event) `changed` `delay:200ms` debounces keystrokes and ignores keys that don't change the value (e.g. arrows).
  - `keyup[key=='Enter']` sends immediately on Enter, using an event filter.
  - `load` populates the table on page load.
- `hx-target` puts the response into the `#results` tbody.
- `hx-indicator` shows a loading indicator while the request is in flight.

On the server, respond with matching table rows:

```html
<tr>
  <td>Venus</td>
  <td>Grimes</td>
  <td>venus.grimes@example.com</td>
</tr>
<tr>
  <td>Fletcher</td>
  <td>Owen</td>
  <td>fletcher.owen@example.com</td>
</tr>
```

## Notes

### Indicators

The `htmx-indicator` class hides an element by default and shows it while a request is in flight:

```html
<span class="htmx-indicator">Searching...</span>
```
