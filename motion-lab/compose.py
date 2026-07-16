"""compose.py - data-driven choreography examples.

A brief's narrative beats become a SEQUENCE of motion primitives with per-beat
parameters, smooth crossfades, and synced content events (moment_sync). This is what
makes it possible to render different sequences without rewriting the renderer.

A choreography is plain data and could be emitted by a future brief-to-plan step:
    beats:   [{primitive, t0, t1, amp, label}, ...]   (the rig motion over the loop)
    content: [{kind, at_t, dur, tiles}, ...]           (moment_sync: pixels respond to motion)

Renders Cavalry-free via preview.render_dy. Chosen choreography → Cavalry for hi-fi.
"""
import sys
import os
import cv2
import numpy as np
import primitives as P
import preview as V

XFADE = 0.05  # crossfade half-width (in global t) between adjacent beats


def _clamp01(x):
    return 0.0 if x < 0 else (1.0 if x > 1 else x)


def _smoothstep(x):
    x = _clamp01(x)
    return x * x * (3 - 2 * x)


# Four hand-authored examples. They exercise the same data structure with different
# primitive sequences; automatic planning from an arbitrary brief is not implemented.
CHOREOS = {
    "sports-tech (athlete reveal)": {
        "beats": [
            {"primitive": "elevator_reveal", "t0": 0.00, "t1": 0.40, "amp": 40, "label": "ATHLETE - reveal"},
            {"primitive": "ripple",          "t0": 0.40, "t1": 0.74, "amp": 16, "label": "FEATURE - pulse"},
            {"primitive": "gravity_settle",  "t0": 0.74, "t1": 1.00, "amp": 44, "label": "BRAND - land"},
        ],
        "content": [
            {"kind": "highlight_pulse", "at_t": 0.20, "dur": 0.14, "tiles": "all"},
            {"kind": "text_reveal",     "at_t": 0.50, "dur": 0.10, "tile": [2, 1], "text": "33", "color": (0, 215, 255)},   # gold "33" in centre tile (feature beat)
            {"kind": "highlight_pulse", "at_t": 0.57, "dur": 0.10, "tiles": "center"},
            {"kind": "color_shift",     "at_t": 0.76, "dur": 0.12, "tiles": "all", "to": (244, 133, 66)},                    # navy→electric-blue
        ],
    },
    "wellness (calm restorative)": {
        "beats": [
            {"primitive": "breathing",      "t0": 0.00, "t1": 0.45, "amp": 9,  "label": "INHALE - settle"},
            {"primitive": "standing_wave",  "t0": 0.45, "t1": 0.78, "amp": 14, "label": "RESONANCE"},
            {"primitive": "breathing",      "t0": 0.78, "t1": 1.00, "amp": 9,  "label": "EXHALE - release"},
        ],
        "content": [
            {"kind": "highlight_pulse", "at_t": 0.22, "dur": 0.20, "tiles": "all"},
            {"kind": "highlight_pulse", "at_t": 0.88, "dur": 0.12, "tiles": "center"},
        ],
    },
    "high-energy (drop + sweep)": {
        "beats": [
            {"primitive": "gravity_settle", "t0": 0.00, "t1": 0.38, "amp": 46, "label": "DROP"},
            {"primitive": "column_cascade", "t0": 0.38, "t1": 0.72, "amp": 15, "label": "SWEEP"},
            {"primitive": "ripple",         "t0": 0.72, "t1": 1.00, "amp": 16, "label": "BURST"},
        ],
        "content": [
            {"kind": "highlight_pulse", "at_t": 0.10, "dur": 0.08, "tiles": "all"},
            {"kind": "highlight_pulse", "at_t": 0.55, "dur": 0.06, "tiles": "all"},
            {"kind": "highlight_pulse", "at_t": 0.85, "dur": 0.10, "tiles": "center"},
        ],
    },
    "tech-reveal (product launch)": {
        "beats": [
            {"primitive": "elevator_reveal", "t0": 0.00, "t1": 0.42, "amp": 40, "label": "RISE"},
            {"primitive": "ripple",          "t0": 0.42, "t1": 0.70, "amp": 15, "label": "SCAN"},
            {"primitive": "row_sweep",       "t0": 0.70, "t1": 1.00, "amp": 15, "label": "SPECS"},
        ],
        "content": [
            {"kind": "dim",             "at_t": 0.08, "dur": 0.08, "tiles": "all"},
            {"kind": "highlight_pulse", "at_t": 0.25, "dur": 0.12, "tiles": "center"},
            {"kind": "highlight_pulse", "at_t": 0.82, "dur": 0.10, "tiles": "all"},
        ],
    },
}

# Back-compat default
CHOREO = CHOREOS["sports-tech (athlete reveal)"]

CENTER = {(1, 1), (2, 1), (3, 1), (2, 0), (2, 2)}


def _beat_dy(beat, col, row, T):
    fn = P.PRIMITIVES[beat["primitive"]][0]
    dur = max(1e-6, beat["t1"] - beat["t0"])
    local = _clamp01((T - beat["t0"]) / dur)
    return fn(col, row, local, beat["amp"])


def compose_dy(col, row, T, choreo=CHOREO):
    beats = choreo["beats"]
    # active beat
    act = beats[-1]
    for b in beats:
        if b["t0"] <= T < b["t1"]:
            act = b
            break
    dy = _beat_dy(act, col, row, T)
    # crossfade near the boundary into the next beat
    for i, b in enumerate(beats[:-1]):
        nb = beats[i + 1]
        edge = b["t1"]
        if edge - XFADE <= T <= edge + XFADE:
            w = _smoothstep((T - (edge - XFADE)) / (2 * XFADE))
            dy = (1 - w) * _beat_dy(b, col, row, T) + w * _beat_dy(nb, col, row, T)
    return dy


def _pulse(x):
    x = _clamp01(x)
    return np.sin(np.pi * x)  # 0→1→0


def _in_set(ev, col, row):
    sel = ev.get("tiles", "all")
    return sel == "all" or (sel == "center" and (col, row) in CENTER)


def compose_content(col, row, T, choreo=CHOREO):
    """Return a per-tile content struct for moment_sync events:
      highlight_pulse/dim → brightness ;  color_shift → palette tint (ramp+hold) ;
      text_reveal → KPI text inside one tile (fade-in+hold)."""
    out = {"bright": 1.0, "tint": None, "tint_amt": 0.0, "text": None, "text_alpha": 0.0}
    for ev in choreo["content"]:
        kind = ev["kind"]
        if kind in ("highlight_pulse", "dim"):
            if not (ev["at_t"] - ev["dur"] <= T <= ev["at_t"] + ev["dur"]) or not _in_set(ev, col, row):
                continue
            amt = float(_pulse((T - (ev["at_t"] - ev["dur"])) / (2 * ev["dur"])))
            out["bright"] *= (1.0 + 0.6 * amt) if kind == "highlight_pulse" else (1.0 - 0.45 * amt)
        elif kind == "color_shift":
            if T < ev["at_t"] or not _in_set(ev, col, row):
                continue
            amt = _smoothstep((T - ev["at_t"]) / ev["dur"])   # ramp then hold
            out["tint"], out["tint_amt"] = ev["to"], max(out["tint_amt"], amt)
        elif kind == "text_reveal":
            if (col, row) != tuple(ev["tile"]) or T < ev["at_t"]:
                continue
            out["text"] = ev["text"]
            out["text_color"] = tuple(ev.get("color", (255, 255, 255)))
            out["text_alpha"] = _smoothstep((T - ev["at_t"]) / ev["dur"])
    return out


def beat_label(T, choreo=CHOREO):
    for b in choreo["beats"]:
        if b["t0"] <= T < b["t1"]:
            return b["label"]
    return choreo["beats"][-1]["label"]


def _slug(name):
    return name.split(" ")[0].replace("(", "").replace(")", "")


def render_choreo(name, choreo, out, n_frames=150):
    frames = V.render_dy(
        lambda c, r, t: compose_dy(c, r, t, choreo),
        f"{out}/choreo-{_slug(name)}.mp4",
        content_fn=lambda c, r, t: compose_content(c, r, t, choreo),
        n_frames=n_frames, fps=25,
        label=name,
        beat_label_fn=lambda t: beat_label(t, choreo),
    )
    # one frame at each beat midpoint
    cells = []
    for b in choreo["beats"]:
        mid = (b["t0"] + b["t1"]) / 2
        f = frames[int(mid * len(frames))].copy()
        cv2.putText(f, b["label"], (20, V.H - 18), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
        cells.append(cv2.resize(f, (V.W // 3, V.H // 3)))
    return np.hstack(cells)   # one row = this brief's 3 beats


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "out"
    os.makedirs(out, exist_ok=True)
    rows = []
    for name, choreo in CHOREOS.items():
        seq = " → ".join(b["primitive"] for b in choreo["beats"])
        print(f"composing '{name}': {seq}")
        row = render_choreo(name, choreo, out)
        # brief-name banner above the row
        banner = np.full((30, row.shape[1], 3), 18, np.uint8)
        cv2.putText(banner, name, (12, 21), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (120, 230, 255), 1, cv2.LINE_AA)
        rows.append(np.vstack([banner, row]))
    sheet = np.vstack(rows)
    cv2.imwrite(f"{out}/variety-sheet.png", sheet)
    print(f"\n{len(CHOREOS)} distinct choreographies → {out}/variety-sheet.png + per-brief MP4s")
