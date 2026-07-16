# Prompt template — GSAP + Three.js monitor wall (primary)

The chrome-pilot pastes this template into Claude Design after the `_design-context-block.md` preamble, then fills the `<<SLOT: ...>>` markers from the brief + monitor map.

---

## Task

Generate a single self-contained HTML file that runs a 6-second looping animation implementing the kinetic monitor wall described in the design context block above. Use **GSAP timeline** to drive everything and **Three.js** to render the gallery 3D scene.

## Slots (filled by chrome-pilot per render)

```
<<SLOT: project>>            — e.g. "sports-tech demo"
<<SLOT: campaign>>           — e.g. "athlete analysis — live-event monitor wall"
<<SLOT: hero_headline>>      — e.g. "See movement from a new angle"
<<SLOT: brand_primary>>      — hex, e.g. "#4858D3"
<<SLOT: brand_secondary>>    — hex, e.g. "#CB395F"
<<SLOT: brand_tertiary>>     — hex, e.g. "#D86937" (optional)
<<SLOT: gradient_palette>>   — JSON array of [start, end] color pairs to populate idle GRADIENT tiles
<<SLOT: hero_image_prose>>   — e.g. "stylized 3D skeletal-pose silhouette" — drawn procedurally onto an off-screen canvas, sliced across IMAGE-SLICE tiles
<<SLOT: include_person>>     — boolean: render person silhouette or not
<<SLOT: monitor_map>>        — JSON, see schema in design-context-block.md
<<SLOT: stage3_quote>>       — { text, attrib } object, optional
```

## Implementation skeleton

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>kinetic monitor wall — <<SLOT: client>></title>
  <style>
    html, body { margin: 0; padding: 0; background: #1A1A1F; overflow: hidden; }
    canvas { display: block; }
    #replay { position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%);
              padding: 8px 16px; border-radius: 9999px; border: 0; cursor: pointer;
              background: rgba(255,255,255,0.08); color: #fff;
              font: 500 13px Inter, system-ui, sans-serif; }
    #replay:hover { background: rgba(255,255,255,0.16); }
  </style>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500&display=swap" rel="stylesheet" />
</head>
<body>
  <button id="replay">Explore →</button>

  <script src="https://cdn.jsdelivr.net/npm/three@0.160.1/build/three.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
  <script>
  /* ----- Constants from tokens.json ----- */
  const COLS = 5, ROWS = 3, GAP = 24, MON_ASPECT = 16/9;
  const AMP = 18, PERIOD = 4.0, PHASE_COL = 0.45, PHASE_ROW = 0.18;
  const ANCHORS = new Set(['1,1','2,1','3,1','2,0','2,2']);
  const STAGE = { IDLE_END: 2.5, TRANS_END: 4.0, REVEAL_END: 5.6, LOOP: 6.0 };
  const CINEMATIC = "cubic-bezier(0.16, 1, 0.3, 1)";
  gsap.registerEase('cinematic', t => 1 - Math.pow(1 - t, 4));  // approximation; close to (0.16, 1, 0.3, 1)

  /* ----- Slot data, filled per render ----- */
  const BRAND = { primary: '<<SLOT: brand_primary>>', secondary: '<<SLOT: brand_secondary>>', tertiary: '<<SLOT: brand_tertiary>>' };
  const GRAD = <<SLOT: gradient_palette>>;        // [[start,end], ...]
  const MAP = <<SLOT: monitor_map>>;              // { tiles, features, stage3_focus_order }
  const HERO_IMG_PROSE = `<<SLOT: hero_image_prose>>`;
  const INCLUDE_PERSON = <<SLOT: include_person>>;
  const QUOTE = <<SLOT: stage3_quote>>;

  /* ----- Three.js scene ----- */
  // Renderer, scene, camera, 3-point lighting rig, dark wall plane, ground plane with subtle reflection.
  // 15 PlaneGeometry meshes for monitors. Each has a CanvasTexture whose <canvas> we paint per frame.
  // Optional person silhouette mesh (extruded SVG path or PlaneGeometry + alpha texture).
  // Camera: PerspectiveCamera at fixed position looking head-on at the wall. NEVER moves (rule 2).

  /* ----- Per-tile canvas painter ----- */
  // function paintTile(ctx, tileSpec, t, state) { ... }
  // Reads tileSpec.idle.type, draws GRADIENT/IMAGE-SLICE/NUMBER/TEXT/ICON/CALLOUT.
  // Gradient angle = (t / 12) * 360deg.

  /* ----- GSAP timeline (6.0 s, repeats) ----- */
  const tl = gsap.timeline({ repeat: -1, defaults: { ease: 'cinematic' } });

  // Stage ① IDLE: 0 → 2.5  (no per-tile timeline entries — wave is driven each frame from clock)
  tl.addLabel('stage-1', 0);

  // Tap pulse at 2.5
  tl.addLabel('stage-2', STAGE.IDLE_END);
  tl.fromTo('#tap-pulse', { scale: 0, opacity: 0.45 },
                          { scale: 1.4, opacity: 0, duration: 0.20, ease: 'snappy' }, 'stage-2');

  // For each detaching tile: lift, travel, land
  for (const tile of MAP.tiles.filter(t => t.detach)) {
    const obj = monitorMeshes[`${tile.col},${tile.row}`].position;  // Three.js Vector3
    const land = computeLandingWorldPos(tile.detach.land);
    tl.to(obj, { y: obj.y + 0.05, duration: 0.45, ease: 'cinematic' }, 'stage-2');                  // lift
    tl.to(obj, { x: land.x, y: land.y, duration: 0.75, ease: 'cinematic' }, 'stage-2+=0.45');      // travel
    tl.to(monitorMeshes[`${tile.col},${tile.row}`].scale,
                            { x: 1.10, y: 1.10, z: 1.10, duration: 0.30, ease: 'cinematic' }, 'stage-2+=1.20'); // land
    // Content swap on land:
    tl.call(() => swapTileContent(tile, tile.detach.feature), [], 'stage-2+=1.50');
  }

  // Stage ③ REVEAL: 4.0 → 5.6
  tl.addLabel('stage-3', STAGE.TRANS_END);
  tl.call(() => pickFocus(currentLoopIndex()), [], 'stage-3');
  tl.to(focusedMesh.scale, { x: 4, y: 4, z: 4, duration: 1.6, ease: 'cinematic' }, 'stage-3');
  tl.to(focusedMesh.position, { x: 0, y: 0, duration: 1.6, ease: 'cinematic' }, 'stage-3');
  for (const tile of otherDetachedTiles) {
    tl.to(tile.scale, { x: 0.85, y: 0.85, z: 0.85, duration: 1.6, ease: 'cinematic' }, 'stage-3');
    tl.to(tile.material, { opacity: 0.30, duration: 1.6 }, 'stage-3');
  }
  // Anchor wave damping handled in updateWave() based on state.
  if (QUOTE) {
    tl.fromTo('#quote', { opacity: 0 }, { opacity: 1, duration: 0.4 }, 'stage-3+=1.2');
  }

  // Return: 5.6 → 6.0  reverse everything
  tl.addLabel('return', STAGE.REVEAL_END);
  tl.to([...allDetachedMeshes].map(m => m.position),
        { x: gsap.utils.snap(...), y: gsap.utils.snap(...), duration: 0.4, ease: 'cinematic' }, 'return');
  tl.to([...allDetachedMeshes].map(m => m.scale),
        { x: 1.0, y: 1.0, z: 1.0, duration: 0.4, ease: 'cinematic' }, 'return');

  /* ----- Render loop ----- */
  function tick(now) {
    const t = (now / 1000) % STAGE.LOOP;
    const state = stateFromT(t);
    updateWave(t, state);              // y-only sine for non-detached, non-focused tiles
    repaintTileCanvases(t, state);      // gradient drift, content per tile
    renderer.render(scene, camera);
    requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);

  /* ----- Public hooks for the preview/critic ----- */
  window.replayLoop = () => tl.restart();
  window.setLoopT   = (t) => tl.seek(t);
  window.captureLoop = async (seconds = 6.0) => {
    tl.restart();
    const stream = renderer.domElement.captureStream(60);
    const mime = MediaRecorder.isTypeSupported('video/webm;codecs=vp9') ? 'video/webm;codecs=vp9' : 'video/webm';
    const rec = new MediaRecorder(stream, { mimeType: mime, videoBitsPerSecond: 8_000_000 });
    return new Promise((resolve, reject) => {
      const chunks = [];
      rec.ondataavailable = e => e.data.size && chunks.push(e.data);
      rec.onstop = () => resolve(new Blob(chunks, { type: 'video/webm' }));
      rec.onerror = reject;
      rec.start();
      setTimeout(() => rec.stop(), seconds * 1000);
    });
  };

  document.getElementById('replay').addEventListener('click', () => tl.seek(STAGE.IDLE_END));
  </script>
</body>
</html>
```

The above is the **scaffold**. You must implement the missing pieces:

- `setupScene()` — Three.js scene, camera at `(0, 0, 5)` looking at origin, three lights per tokens, dark wall plane behind, ground plane below with `MeshPhysicalMaterial` reflectivity. Optional person silhouette mesh.
- `monitorMeshes` — 15 `Mesh(PlaneGeometry(monitorW, monitorH), MeshBasicMaterial({ map: tileTexture }))` keyed by `'col,row'`.
- `tileTexture` per tile — `THREE.CanvasTexture` wrapping a per-tile `<canvas>` painted by `paintTile(ctx, tileSpec, t, state)`.
- `paintTile(ctx, tileSpec, t, state)` — switch on `tileSpec.idle.type`:
  - `GRADIENT`: linear gradient with angle `t * 30` deg, colors from `GRAD[tileSpec.idle.gradientIdx]`.
  - `IMAGE-SLICE`: draw a portion of the procedurally-generated hero image; the slice is `tile.idle.imageSliceRect`.
  - `NUMBER`: fill text Inter 300, white or `BRAND.primary`, fontSize ~ 60% of height.
  - `TEXT`: headline 20 px + sub 13 px, white.
  - `ICON`: stroke-only glyph (chat, phone, etc.) centered.
  - `CALLOUT`: translucent black pill with white text, dashed connection line drawn from pill toward focused tile.
- `generateHeroImage(canvas, prose)` — procedural drawing routine. Switch on prose substring matches:
  - `"skeletal pose"` → stylized stick figure mid-air, brand-color stroke on a violet→cyan radial gradient.
  - `"molecule"` → hexagonal lattice with circle nodes.
  - `"chart"` → ascending line chart.
  - `"eyewear"` / default → simple silhouette of the named object.
  This image is then sliced for IMAGE-SLICE tiles.
- `updateWave(t, state)` — for each non-detaching, non-focused tile: `mesh.position.y = restingY + AMP * Math.sin(2π * t / PERIOD + col * PHASE_COL + row * PHASE_ROW)`. During REVEAL state, multiply AMP by 0.4 and PERIOD by 1.6 for anchor tiles.
- `validateMonitorMap(MAP)` at startup — check static positions and sampled detach paths. If a check fails, `console.error` and abort. Document the sampling interval; do not describe the check as a continuous-time proof.

## Don't

- Don't use OrbitControls — camera is locked (Rule 2).
- Don't use any Three.js helpers outside core (no `three/examples/*` aside from a single texture loader if needed).
- Don't add HTML elements other than the `#replay` button + an optional `#quote` overlay div.
- Don't deviate from the 6.0 s loop, 5×3 grid, anchors, or the three hard motion rules.
- Don't add comments explaining the obvious. Only comment a non-obvious *why*.

## Deliverable

Return the entire HTML file in a single fenced ```html code block. No prose around it.
