"""Lightweight, Cavalry-free preview renderer for motion concepts.

Draws the 5x3 kinetic wall in a dark gallery and animates each tile's position.y
via a motion primitive. NOT production fidelity — its job is to make a *new motion
concept* visible instantly so the design loop can compare and judge choreographies
without the heavy Cavalry round-trip. The chosen concept then gets a high-fidelity
finish in Cavalry by the designer.
"""
import cv2
import numpy as np
import math
import primitives as P

W, H = 960, 540
COLS, ROWS = P.COLS, P.ROWS
TILE_W, TILE_H, GAP = 150, 84, 18          # preview-scaled; pitch = TILE_H + GAP
PITCH_X, PITCH_Y = TILE_W + GAP, TILE_H + GAP
BG = (31, 26, 26)                          # #1A1A1F-ish (BGR)

# Per-tile gradient palettes (BGR top, BGR bottom) — high-contrast screen colors
_PALETTES = [
    ((255, 117, 200), (232, 42, 168)),   # magenta→violet
    ((255, 156, 90),  (229, 71, 27)),    # blue→cyan-ish (BGR)
    ((122, 217, 93),  (240, 191, 155)),  # amber/teal mix
    ((229, 140, 90),  (155, 157, 255)),  # blue→lavender
]


def _vgrad(w, h, top_bgr, bot_bgr):
    grad = np.zeros((h, w, 3), np.uint8)
    for c in range(3):
        grad[:, :, c] = np.linspace(top_bgr[c], bot_bgr[c], h, dtype=np.uint8)[:, None].repeat(w, 1)
    return grad


def _rounded_tile(canvas, x, y, w, h, top_bgr, bot_bgr, alpha=1.0, bright=1.0,
                  tint_bgr=None, tint_amt=0.0):
    """Blit a vertical-gradient tile with a subtle bezel at (x,y) top-left.
    Content-event hooks:
      `bright`   — brightness multiplier (<1 dim, >1 glow). highlight_pulse / dim.
      `tint_bgr`+`tint_amt` — blend the gradient toward a flat target colour
                   (color_shift, e.g. navy→electric-blue). tint_amt in [0,1]."""
    x0, y0 = int(x), int(y)
    x1, y1 = x0 + w, y0 + h
    if x1 <= 0 or y1 <= 0 or x0 >= W or y0 >= H:
        return
    cx0, cy0, cx1, cy1 = max(0, x0), max(0, y0), min(W, x1), min(H, y1)
    grad = _vgrad(w, h, top_bgr, bot_bgr).astype(np.float32)
    if tint_bgr is not None and tint_amt > 0:
        target = np.array(tint_bgr, np.float32)
        grad = grad * (1 - tint_amt) + target * tint_amt
    if bright != 1.0:
        grad = grad * bright
    grad = np.clip(grad, 0, 255).astype(np.uint8)
    gx0, gy0 = cx0 - x0, cy0 - y0
    sub = grad[gy0:gy0 + (cy1 - cy0), gx0:gx0 + (cx1 - cx0)]
    if alpha >= 1.0:
        canvas[cy0:cy1, cx0:cx1] = sub
    else:
        roi = canvas[cy0:cy1, cx0:cx1]
        cv2.addWeighted(sub, alpha, roi, 1 - alpha, 0, roi)
    cv2.rectangle(canvas, (cx0, cy0), (cx1 - 1, cy1 - 1), (12, 10, 10), 1)


def _silhouette(canvas):
    """A simple person silhouette on the right, for scale."""
    cx, base = int(W * 0.84), int(H * 0.92)
    col = (14, 12, 12)
    cv2.ellipse(canvas, (cx, base - 150), (26, 70), 0, 0, 360, col, -1)   # torso
    cv2.circle(canvas, (cx, base - 230), 22, col, -1)                     # head
    cv2.ellipse(canvas, (cx, base - 60), (34, 90), 0, 0, 360, col, -1)    # legs/base


def render_concept(primitive_name, out_mp4, n_frames=100, fps=25, amp=None, label=None):
    fn, desc, kind = P.PRIMITIVES[primitive_name]
    if amp is None:
        amp = fn.__defaults__[0]
    grid_w = COLS * PITCH_X - GAP
    grid_h = ROWS * PITCH_Y - GAP
    ox = (W - grid_w) // 2 - 60        # shift left, leave room for silhouette
    oy = (H - grid_h) // 2

    vw = cv2.VideoWriter(out_mp4, cv2.VideoWriter_fourcc(*"mp4v"), fps, (W, H))
    frames = []
    for fi in range(n_frames):
        t = fi / n_frames
        canvas = np.full((H, W, 3), BG, np.uint8)
        # faint radial vignette
        # floor reflection (drawn first, faint, flipped) + tiles
        for reflect in (True, False):
            for row in range(ROWS):
                for col in range(COLS):
                    dy = fn(col, row, t, amp)                  # up-positive
                    bx = ox + col * PITCH_X
                    by = oy + row * PITCH_Y - dy                # screen y-down → subtract up-offset
                    pal = _PALETTES[(col + row) % len(_PALETTES)]
                    if reflect:
                        ry = oy + grid_h + 40 + (grid_h - (row * PITCH_Y)) + dy
                        _rounded_tile(canvas, bx, ry, TILE_W, TILE_H, pal[1], pal[0], alpha=0.10)
                    else:
                        _rounded_tile(canvas, bx, by, TILE_W, TILE_H, pal[0], pal[1])
        _silhouette(canvas)
        if label:
            cv2.putText(canvas, label, (24, 34), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (230, 230, 230), 2, cv2.LINE_AA)
        vw.write(canvas)
        frames.append(canvas)
    vw.release()
    return frames


def hero_frame(primitive_name, fi_frac=0.25, n_frames=100, amp=None):
    frames = render_concept(primitive_name, "/tmp/_throwaway.mp4", n_frames=n_frames, amp=amp)
    return frames[int(fi_frac * n_frames)]


def render_dy(dy_fn, out_mp4, content_fn=None, n_frames=150, fps=25,
              label=None, beat_label_fn=None):
    """Render an arbitrary choreography.

    dy_fn(col, row, t) -> vertical offset px (amp already baked in).
    content_fn(col, row, t) -> brightness multiplier (default 1.0) — the content-event
        layer (highlight_pulse / color_shift read as brightness here in preview).
    beat_label_fn(t) -> str shown bottom-left (which narrative beat is active).
    """
    grid_w = COLS * PITCH_X - GAP
    grid_h = ROWS * PITCH_Y - GAP
    ox = (W - grid_w) // 2 - 60
    oy = (H - grid_h) // 2
    def _norm(c):
        if c is None:
            return {}
        if isinstance(c, (int, float)):
            return {"bright": float(c)}
        return c

    vw = cv2.VideoWriter(out_mp4, cv2.VideoWriter_fourcc(*"mp4v"), fps, (W, H))
    frames = []
    for fi in range(n_frames):
        t = fi / n_frames
        canvas = np.full((H, W, 3), BG, np.uint8)
        text_draws = []
        for reflect in (True, False):
            for row in range(ROWS):
                for col in range(COLS):
                    dy = dy_fn(col, row, t)
                    cnt = _norm(content_fn(col, row, t)) if content_fn else {}
                    bx = ox + col * PITCH_X
                    by = oy + row * PITCH_Y - dy
                    pal = _PALETTES[(col + row) % len(_PALETTES)]
                    if reflect:
                        ry = oy + grid_h + 40 + (grid_h - row * PITCH_Y) + dy
                        _rounded_tile(canvas, bx, ry, TILE_W, TILE_H, pal[1], pal[0], alpha=0.10)
                    else:
                        _rounded_tile(canvas, bx, by, TILE_W, TILE_H, pal[0], pal[1],
                                      bright=cnt.get("bright", 1.0),
                                      tint_bgr=cnt.get("tint"), tint_amt=cnt.get("tint_amt", 0.0))
                        if cnt.get("text") and cnt.get("text_alpha", 0) > 0.02:
                            text_draws.append((bx + TILE_W // 2, by + TILE_H // 2,
                                               cnt["text"], cnt.get("text_color", (255, 255, 255)),
                                               cnt["text_alpha"]))
        # text-reveal drawn on top of all tiles
        for tx, ty, txt, color, a in text_draws:
            scale = 1.1
            (tw, th), _ = cv2.getTextSize(txt, cv2.FONT_HERSHEY_SIMPLEX, scale, 2)
            overlay = canvas.copy()
            cv2.putText(overlay, txt, (int(tx - tw / 2), int(ty + th / 2)),
                        cv2.FONT_HERSHEY_SIMPLEX, scale, color, 2, cv2.LINE_AA)
            cv2.addWeighted(overlay, a, canvas, 1 - a, 0, canvas)
        _silhouette(canvas)
        if label:
            cv2.putText(canvas, label, (24, 34), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (230, 230, 230), 2, cv2.LINE_AA)
        if beat_label_fn:
            cv2.putText(canvas, beat_label_fn(t), (24, H - 24), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (120, 230, 255), 2, cv2.LINE_AA)
        vw.write(canvas)
        frames.append(canvas)
    vw.release()
    return frames
