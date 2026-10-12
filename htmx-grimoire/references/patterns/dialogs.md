# Dialogs

> Show modals and popups on demand

## Basic usage

Use the native [`<dialog>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/dialog) element. The browser gives you the backdrop, the focus trap, Escape to close, and correct stacking. You write no JavaScript.

```html
<button command="show-modal" commandfor="modal">Open a Modal</button>

<dialog id="modal" closedby="any">
  <h1>Modal Dialog</h1>
  <p>This is the modal content.</p>
  <button command="close" commandfor="modal">Close</button>
</dialog>
```

- [`command`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/button#command)=`"show-modal"` opens the dialog as a modal. `command="close"` closes it.
- [`commandfor`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/button#commandfor) names the target dialog by `id`.
- [`closedby`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/dialog#closedby)=`"any"` also closes the dialog on a backdrop click or on Escape.

A modal dialog renders in the [top layer](https://developer.mozilla.org/en-US/docs/Glossary/Top_layer), above all page content. Its position in the DOM does not matter, so put it where it belongs in your markup.

## Loading content from the server

Add htmx attributes to the same button. It fetches the content and opens the dialog in one click.

```html
<button hx-get="/modal-body"
        hx-target="#modal-body"
        command="show-modal"
        commandfor="modal">
  Open a Modal
</button>

<dialog id="modal" closedby="any">
  <div id="modal-body">Loading...</div>
  <button command="close" commandfor="modal">Close</button>
</dialog>
```

- `hx-get` requests the content.
- `hx-target`=`"#modal-body"` puts the response inside the dialog.
- The dialog opens at once, so the user sees the loading state. The content replaces it when it arrives.

To load the whole dialog instead of its body, target the dialog itself with `hx-swap`=`"innerHTML"`. Keep the `<dialog>` element in the page so `commandfor` can always find it.

## Notes

### Browser support

`command` and `commandfor` are recent. If you must support an older browser, call [`showModal()`](https://developer.mozilla.org/en-US/docs/Web/API/HTMLDialogElement/showModal) instead:

```html
<button hx-get="/modal-body"
        hx-target="#modal-body"
        onclick="modal.showModal()">
  Open a Modal
</button>
```

`<dialog>` itself has been available in every major browser since 2022.

### Confirmations

For a yes or no question, you do not need a dialog at all. `hx-confirm` shows the browser confirm and only sends the request when the user accepts.

```html
<button hx-delete="/contact/1" hx-confirm="Are you sure?">Delete</button>
```

To collect a value, use the `hx-prompt` extension. It shows a native prompt and sends the answer in the `HX-Prompt` request header.

### Centering with a CSS reset

The browser centers a modal dialog with `margin: auto`. A CSS reset that sets `margin: 0` on every element removes that, and the dialog stretches to the viewport edges. Tailwind's preflight does this. Put the margin back:

```css
dialog:modal {
  margin: auto;
}
```

### Styling the backdrop

Style the backdrop with the [`::backdrop`](https://developer.mozilla.org/en-US/docs/Web/CSS/::backdrop) pseudo-element.

```css
dialog::backdrop {
  background: rgb(0 0 0 / 0.5);
}
```
