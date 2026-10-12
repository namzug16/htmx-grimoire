# htmax

> htmx bundled with the most popular extensions in a single file.

The `htmax.js` file bundles htmx with the most popular extensions in a single file:

* `hx-sse`
* `hx-ws`
* `hx-preload`
* `hx-browser-indicator`
* `hx-download`
* `hx-pending`
* `hx-targets`
* `hx-live`
* `hx-upsert`
* `hx-alpine-compat`
* `hx-history-cache` _(included but disabled by default)_

The extensions are automatically available, you can just use their attributes directly (e.g. `hx-sse:connect`, `hx-ws:connect`).

```html
<script src="/js/htmax.min.js"></script>
```

To enable history caching, opt in via the meta tag:

```html
<meta name="htmx-config" content='{"historyCache": {"disable": false}}'>
```
