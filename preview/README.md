# Preview server

Static host for concept artifacts. Serves the **repo root** so that the iframe at `/preview/index.html?concept=<slug>` can load `/concepts/<slug>/artifact.html` cleanly via a relative path.

## Run

```sh
# from repo root, no install needed
bunx serve -l 4173 .
# or
npx serve -l 4173 .
# or once-installed
cd preview && npm install && npm run dev
```

Then open:

```
http://localhost:4173/preview/index.html?concept=_example-sports-tech
```

## Capture a loop video

The preview UI has a **`Capture loop.webm ↗`** button that records 6.0 s at 60 fps and triggers a browser download named `<slug>__loop.webm`. Move the file into `concepts/<slug>/loop.webm` and run `/ship <slug>` to convert to MP4 via ffmpeg.

The capture helper (`capture.js`) prefers the artifact's own `window.captureLoop(seconds)` if exposed; otherwise it falls back to recording the `<canvas>` directly via `canvas.captureStream(60)`.

## Manual replay

The **`Replay ↻`** button calls `window.replayLoop()` inside the artifact iframe (if defined), otherwise hard-reloads the iframe. Use it to inspect the choreography after edits.
