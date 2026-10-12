# File Upload

> Upload files with progress and validation

## Basic usage

On the client, set `hx-encoding` to `multipart/form-data`:

```html
<form hx-post="/upload"
      hx-encoding="multipart/form-data">
    <input type="file" name="file">
    <input type="text" name="name">
    <button>Submit</button>
</form>
```

- `hx-encoding`=`"multipart/form-data"` sends the form as [`FormData`](https://developer.mozilla.org/en-US/docs/Web/API/FormData), required for file uploads.
- `hx-post` submits the form to `/upload`.

On the server, respond with a success or error message:

```html
<p>File uploaded successfully.</p>
```

## Preserving file selection on errors

When a form re-renders with validation errors, file inputs lose their selection. Add `hx-preserve` to keep it:

```html
<form hx-post="..."
      hx-swap="outerHTML"
      hx-encoding="multipart/form-data">
    <input hx-preserve type="file" name="file">
    <input type="text" name="name">
    <button>Submit</button>
</form>
```

Try it in the demo: select a file, then submit with empty fields. The form re-renders with errors, but your file selection stays.

Alternatively, place the file input outside the swap target using the [`form` attribute](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input#form):

```html
<input form="my-form" type="file" name="file">

<form id="my-form" hx-post="..."
      hx-encoding="multipart/form-data">
    <button>Submit</button>
</form>
```

The input is outside the form element, so it is never replaced during swaps.

## Upload progress

htmx 4 sends requests with the native [`fetch`](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API) API, which, sadly, does not report upload progress.

If you want more fully featured upload consider one of the following JavaScript libraries:

- [Uppy](https://uppy.io)
- [FilePond](https://pqina.nl/filepond/)
- [Dropzone](https://www.dropzone.dev)
