# Motion libraries — what to use and why

The visual target is a cinematic motion-graphics render rather than a rough canvas sketch. To approach that quality on the web, the prototype uses timeline-driven, GPU-accelerated tools.

## Recommendation, in order

### 1. **GSAP timeline + Three.js + CSS/DOM tiles** — *default for our concepts*

- **GSAP** (GreenSock) is the industry standard for cinematic timeline animation. Its `gsap.timeline()` is exactly the abstraction we want: one timeline drives all 15 tiles + camera + UI through Stages ① ② ③ with absolute time control, easing, labels, and seamless looping. ~78 KB.
- **Three.js** renders the dark gallery 3D space — back wall, lighting rig, ground plane reflection, optional person silhouette. The 15 monitors become 15 `Mesh` planes with a shader that paints their screen content. This gives the *gallery scale* the videos sell.
- **CSS/DOM tiles** are an alternative when 3D is overkill: same GSAP timeline driving CSS `transform: translate3d()` on `<div>` tiles. Faster to iterate, looks crisp, no WebGL bring-up. Use when the brief is "talking-head wall" rather than "physical exhibit render".

**Trade-off accepted:** larger bundle, more setup. Worth it because the deliverable is a sales asset; quality > weight.

### 2. **Theatre.js** — *when designer-friendly editing matters*

- Built for cinematic motion graphics; ships a visual timeline editor that runs in-page. You can hand the URL to a teammate who scrubs and tweaks the easing without touching code.
- Drives DOM, SVG, and Three.js objects through the same timeline.
- Strong fit for a workflow where the user wants to *adjust* a generated concept rather than re-render it. Add as a second-pass edit layer over a GSAP-generated baseline.

### 3. **Rive** — *when shipping the same animation everywhere*

- State-machine native: idle / transitioning / reveal / returning is exactly Rive's mental model. GPU-accelerated, 120 fps on a budget phone.
- Used broadly for production-grade interactive animation.
- Cost: requires the Rive editor (desktop app) to author. Not a fit when we want code-only generation via Claude Design.
- Future option if we move from "one-pitch pre-vis" to "ship the same loop on the client's brand site too".

### 4. **p5.js** — *only for fast prototypes*

- Friendly, immediate-mode, easy to generate. Good for a first sketch when we don't yet know what the choreography wants to be.
- Weaknesses for our use case: no built-in timeline (we hand-roll a state machine), 2D-only DOM canvas (no real 3D scene), motion easing is fiddly (must implement cubic-bezier by hand).
- Keep as a fallback when the user explicitly wants a single-file p5 sketch.

### 5. **Anime.js / Motion (Framer Motion) / Lottie** — *not recommended for this repo*

- **Anime.js** — lightweight, fine for staggered UI but lacks the timeline depth of GSAP.
- **Motion** — React-first; we're not in React.
- **Lottie** — for After-Effects-exported motion. Powerful but requires AE in the loop, breaks the all-code-via-Claude-Design workflow.

## How this maps to our pipeline

| Brief intent | Recommended stack | tech-router output |
|---|---|---|
| Default monitor-wall pitch (like our seed) | GSAP timeline + Three.js gallery + shader-painted tiles | `gsap-three` |
| Talking-head / data-dashboard wall (no 3D needed) | GSAP timeline + DOM/CSS tiles | `gsap-dom` |
| User explicitly wants "single-file p5 sketch" | p5.js with hand-rolled state machine | `p5` |
| Iterating on a baseline; designer wants to tweak timing | GSAP baseline + Theatre.js studio overlay | `gsap-theatre` |
| Production-shipped to client brand site | Rive (out of repo scope; flag for handoff) | `rive` (handoff) |

## CDN-loadable defaults (chrome-pilot pastes these into Claude Design prompts)

```
GSAP        https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js
Three.js    https://cdn.jsdelivr.net/npm/three@0.160.1/build/three.min.js
Lil-GUI     https://cdn.jsdelivr.net/npm/three@0.160.1/examples/jsm/libs/lil-gui.module.min.js  (debug)
Theatre.js  https://cdn.jsdelivr.net/npm/@theatre/core@0.7.0/dist/index.min.js
            https://cdn.jsdelivr.net/npm/@theatre/studio@0.7.0/dist/index.min.js  (dev only)
p5.js       https://cdn.jsdelivr.net/npm/p5@1.9.4/lib/p5.min.js
```

All single-file, single-script-tag — important so the artifact stays self-contained.

## Why not Framer's own runtime

The reference site is a Framer build, but Framer's runtime ships only as part of a Framer-hosted page; you can't load it as a library and hand-author. We approximate the same motion fidelity with GSAP + Three.js, which we *can* hand-author into a single HTML file via Claude Design.
