# Tabs

> Switch between content panels using tabs

## Server-driven tabs

The server owns which tab is selected. Each response carries the full tab strip and the panel, so the selected tab is part of the returned HTML.

This follows [HATEOAS](https://en.wikipedia.org/wiki/HATEOAS). The application state lives in the hypermedia, not in client-side variables.

On the client, start with an empty container that loads the first tab.

```html
<div id="tabs"
     hx-get="/tabs/1"
     hx-trigger="load"
     hx-target:inherited="this"
     hx-swap:inherited="innerMorph">
</div>
```

- `hx-trigger`=`"load"` fetches the first tab when the element enters the DOM.
- `hx-target`=`"this"` with the `:inherited` modifier makes every tab button inside target the container.
- `hx-swap`=`"innerMorph"` replaces the strip and the panel together. A morph keeps focus on the tab you activated, so keyboard navigation survives the swap.

On the server, return the tab strip and the panel for the requested tab.

```html
<div role="tablist">
  <button id="tab-1" role="tab" aria-controls="panel" aria-selected="true"  tabindex="0"  hx-get="/tabs/1">Overview</button>
  <button id="tab-2" role="tab" aria-controls="panel" aria-selected="false" tabindex="-1" hx-get="/tabs/2">Install</button>
  <button id="tab-3" role="tab" aria-controls="panel" aria-selected="false" tabindex="-1" hx-get="/tabs/3">Extensions</button>
</div>

<div id="panel" role="tabpanel">
  Overview content...
</div>
```

Only `aria-selected` and `tabindex` change between responses. The `tabindex` values are a [roving tabindex](https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/#kbd_roving_tabindex): the tab strip takes one Tab stop, and arrow keys move within it.

Style the selected tab from the attribute, so the markup stays the source of truth:

```css
[role="tab"][aria-selected="true"] {
  border-bottom: 2px solid currentColor;
}
```

## Notes

### Accessibility

The markup follows the [ARIA tabs pattern](https://www.w3.org/WAI/ARIA/apg/patterns/tabs/): `role="tablist"`, `role="tab"`, `aria-controls`, `aria-selected`, `role="tabpanel"`, and a roving `tabindex`.

The pattern also expects the arrow keys to move between tabs. Put one handler on the tab strip:

```html
<div role="tablist"
     hx-on:keydown="let tabs = [...this.querySelectorAll('[role=tab]')];
                    let i = tabs.indexOf(document.activeElement);
                    let k = event.key;
                    let n = k == 'ArrowRight' ? i + 1 : k == 'ArrowLeft' ? i - 1
                          : k == 'Home' ? 0 : k == 'End' ? tabs.length - 1 : -1;
                    if (i < 0 || n < 0) return;
                    event.preventDefault();
                    let next = tabs[(n + tabs.length) % tabs.length];
                    next.focus();
                    next.click();">
```

The demo above uses it. Left and Right wrap around, and Home and End jump to the ends.
