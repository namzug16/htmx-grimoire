# Progress Bar

> Show progress bar during background job

## Basic usage

On the client, a button starts the job.

```html
<button hx-post="/start" hx-swap="outerMorph">
  Start Job
</button>
```

On the server, respond with a container that polls for progress:

```html
<div hx-trigger="every 400ms"
     hx-get="/job/progress"
     hx-swap="outerMorph">
  ...progress bar...
</div>
```

- `hx-trigger`=`"every 400ms"` polls the server on an interval.
- `outerMorph` morphs the element in place, so CSS transitions on `transform` animate smoothly.

Each poll returns updated progress. When done, the server responds with markup that omits `hx-trigger`, so the morph tears down the polling interval and polling stops.

## Notes

### Use `transform` instead of `width`

Animating `width` causes [layout recalculation](https://web.dev/articles/avoid-large-complex-layouts-and-layout-thrashing). Use `transform: scaleX()` instead ([GPU-composited](https://web.dev/articles/stick-to-compositor-only-properties-and-manage-layer-count), no layout thrashing):

```css
.bar {
  width: 100%;
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 400ms ease-in-out;
}
```

The server returns `style="transform: scaleX(0.65)"` instead of `style="width: 65%"`. Same look, no layout thrashing. The demo above uses this approach.
