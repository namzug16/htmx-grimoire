# Keyboard Shortcuts

> Bind keyboard shortcuts to interactive elements

## Basic usage

On the client, add a keyboard event to `hx-trigger` alongside `click`.

```html
<button hx-trigger="click, keyup[altKey&&shiftKey&&code=='KeyD'] from:body"
        hx-post="/doit">
  Do It! (Alt+Shift+D)
</button>
```

- `hx-trigger` accepts multiple events separated by commas.
- `keyup[altKey&&shiftKey&&code=='KeyD']` uses an event filter to match only the Alt+Shift+D combination.
- `from:body` makes the shortcut global: the listener is on the `<body>`, not the button itself.

On the server, respond with the result content:

```html
<span>Done!</span>
```

## Notes

### Browser shortcut conflicts

Test each shortcut in every browser/OS you support. Some combinations, such as `Ctrl+W` and `Ctrl+N`, reach the browser before the page.

### Gotcha: Use `code`, not `key`

[`code`](https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent/code) identifies the physical key. [`key`](https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent/key) gives the character the key produces, which the modifiers and the keyboard layout change.

`code` is also layout independent. `code=='KeyD'` matches the same physical key on QWERTY, AZERTY, and Dvorak. Use `key` only when you want the character, such as `key=='?'`.

### Keyboard event properties

The filter expression inside `[...]` has access to the raw [KeyboardEvent](https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent) properties: `key`, `code`, `altKey`, `ctrlKey`, `shiftKey`, and `metaKey`. Combine them with `&&` and `||` to match any shortcut.

For details on key values, see [Keyboard Events on javascript.info](https://javascript.info/keyboard-events).
