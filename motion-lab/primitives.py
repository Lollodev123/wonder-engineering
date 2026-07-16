"""Motion-concept vocabulary for the kinetic monitor wall.

Each primitive is a pure function dy(col, row, t) -> vertical offset in px,
where t is the normalized loop position in [0, 1).

STRUCTURAL CONSTRAINTS:
  - Y-ONLY: primitives return a vertical offset only. There is no dx — the rig
    is vertical-rails, so lateral motion is impossible by design.
  - NO SCALE / NO DETACH: tiles keep size and grid membership; only position.y moves.
  - CYCLIC INPUT: most primitives return the same position at t=0 and t=1. The
    `gravity_settle` reset is intentionally fast and still needs visual inspection.
  - SAMPLED CLEARANCE: `collision_safe()` samples vertical neighbours. Amplitude
    defaults were chosen to pass that diagnostic for the preview geometry; they are
    not continuous-time or physical-rig guarantees.

The module provides reusable functions that a human-authored or future generated
choreography can compose and parameterize.
"""
import math

COLS, ROWS = 5, 3
CENTER_C, CENTER_R = (COLS - 1) / 2, (ROWS - 1) / 2


def _smoothstep(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def _raised_cos_pulse(x):
    """A smooth 0->1->0 bump over x in [0,1], 0 at the ends."""
    x = x % 1.0
    return 0.5 - 0.5 * math.cos(2 * math.pi * x)


# ── PHASED primitives ───────────────────────────────────────────────────────────

def traveling_wave(col, row, t, amp=16.0):
    """Classic sine that travels diagonally across the wall (the baseline gesture)."""
    phase = col * 0.12 + row * 0.06
    return amp * math.sin(2 * math.pi * (t - phase))


def ripple(col, row, t, amp=16.0):
    """Concentric rings radiating from the wall centre — a 'drop in water' feel."""
    dist = math.hypot(col - CENTER_C, row - CENTER_R)
    return amp * math.sin(2 * math.pi * (t - dist * 0.14))


def standing_wave(col, row, t, amp=16.0):
    """Nodes stay still, antinodes oscillate — a taut, resonant 'string' feel."""
    spatial = math.sin(math.pi * col / (COLS - 1) * 2)
    return amp * spatial * math.sin(2 * math.pi * t)


def column_cascade(col, row, t, amp=15.0):
    """Each column rises and falls in left-to-right sequence — a 'sweep' gesture."""
    return amp * _raised_cos_pulse(t - col * 0.10)


def row_sweep(col, row, t, amp=15.0):
    """Rows lift in top-to-bottom sequence — a vertical 'venetian blind' read."""
    return amp * _raised_cos_pulse(t - row * 0.16)


# ── UNISON / GROUPED primitives ─────────────────────────────────────────────────

def elevator_reveal(col, row, t, amp=40.0):
    """Whole wall rises, holds, then lowers with a slight per-column stagger."""
    stagger = col * 0.04
    tt = (t - stagger) % 1.0
    if tt < 0.30:
        return amp * _smoothstep(tt / 0.30)
    if tt < 0.70:
        return amp
    return amp * (1 - _smoothstep((tt - 0.70) / 0.30))


def breathing(col, row, t, amp=9.0):
    """Tiles above centre rise while the lower group sinks, then reverse."""
    direction = 1.0 if row <= CENTER_R else -1.0
    rank = abs(row - CENTER_R) + 0.4
    return amp * direction * rank * math.sin(2 * math.pi * t)


def gravity_settle(col, row, t, amp=46.0):
    """Tiles drop from above, bounce-settle, hold, then reset quickly."""
    stagger = col * 0.05 + row * 0.02
    tt = (t - stagger) % 1.0
    if tt < 0.70:
        p = tt / 0.70                      # 0..1 fall+bounce window
        fall = (1 - p)                      # starts high (1), lands (0)
        bounce = abs(math.sin(3 * math.pi * p)) * (1 - p) * 0.35
        return amp * (fall - bounce)
    # settle hold then quick reset back up
    if tt < 0.92:
        return 0.0
    return amp * _smoothstep((tt - 0.92) / 0.08)


# Registry: name -> (function, human description, default amp cap kind)
PRIMITIVES = {
    "traveling_wave": (traveling_wave, "Diagonal travelling sine", "phased"),
    "ripple":         (ripple,         "Concentric rings from the centre", "phased"),
    "standing_wave":  (standing_wave,  "Fixed nodes and moving antinodes", "phased"),
    "column_cascade": (column_cascade, "Columns rise from left to right", "grouped"),
    "row_sweep":      (row_sweep,      "Rows rise from top to bottom", "grouped"),
    "elevator_reveal":(elevator_reveal,"The wall rises, holds, and returns", "grouped"),
    "breathing":      (breathing,      "Upper and lower groups move apart", "grouped"),
    "gravity_settle": (gravity_settle, "Tiles drop, bounce, and reset", "grouped"),
}


def collision_safe(fn, amp_test, gap, n_t=60):
    """Sample vertically adjacent tiles for overlap across one normalized loop.

    Tiles are spaced by pitch = tile_h + gap. dy is upward-positive. The upper tile
    (smaller row index) and the lower tile (row+1) close their gap when the lower rises
    relative to the upper: sep_loss = dy_lower - dy_upper. Collision when sep_loss > gap.
    Returns (ok, max_overlap_px) where overlap = max sep_loss - gap (negative =
    sampled clearance). This is a diagnostic, not a continuous-time proof.
    """
    worst = 0.0
    for it in range(n_t):
        t = it / n_t
        for col in range(COLS):
            for row in range(ROWS - 1):
                dy_upper = fn(col, row, t, amp_test)
                dy_lower = fn(col, row + 1, t, amp_test)
                worst = max(worst, dy_lower - dy_upper)
    overlap = worst - gap
    return (overlap < 0, overlap)
