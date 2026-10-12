# Lazy Load

> Load content after the page renders

## Basic usage

On the client, put a placeholder where the content will go.

```html
<div hx-get="/weather" hx-trigger="load">
  Loading...
</div>
```

- `hx-get`=`/weather` might query a database or call an external API.
- `hx-trigger`=`"load"` fires the request as soon as the element enters the DOM.

On the server, respond with the HTML content. htmx swaps it into the placeholder when it arrives.

```html
<div class="forecast">
  <h3>5-Day Forecast</h3>
  <p>Monday: 72° Sunny</p>
  <p>Tuesday: 68° Cloudy</p>
</div>
```

## Multiple sections

Each placeholder loads independently. Your page renders fast even if several sections are slow:

```html
<div hx-get="/dashboard/sales" hx-trigger="load">
  Loading sales...
</div>

<div hx-get="/dashboard/analytics" hx-trigger="load">
  Loading analytics...
</div>

<div hx-get="/dashboard/notifications" hx-trigger="load">
  Loading notifications...
</div>
```

All three requests fire in parallel when the page loads.

## Notes

### Layout shift

When the response swaps in, it can push content below it down. This is known as [Cumulative Layout Shift (CLS)](https://web.dev/articles/cls) and affects your [Lighthouse](https://developer.chrome.com/docs/lighthouse) score.

Reserve space with `min-height`:

```html
<div hx-get="/weather" hx-trigger="load" style="min-height: 200px">
  Loading...
</div>
```

The demo above does exactly this.

### Infinite loops

Be careful when including `hx-trigger="load"` in the server response.

```
load → GET /weather → response has hx-trigger="load" → load → GET /weather → …
```

If the response requests the same endpoint, it can create an infinite loop.
