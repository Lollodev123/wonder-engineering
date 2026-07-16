# Motion lab

A renderer-independent Python sandbox for the vertical motion of a 5×3 monitor wall.

## Components

- `primitives.py` — eight `dy(col, row, t, amp)` functions and a sampled vertical-clearance check.
- `compose.py` — four hand-authored choreography examples, crossfades, and synchronized content events.
- `preview.py` — fast OpenCV diagnostic renderer.
- `generate.py` — primitive videos, contact sheet, and sampled-clearance report.
- `to_cavalry.py` — optional bridge that samples one choreography into a higher-fidelity motion-design scene.

## Run

From the repository root:

```sh
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r motion-lab/requirements.txt

python3 motion-lab/generate.py motion-lab/out
python3 motion-lab/compose.py motion-lab/out
python3 -m unittest discover -s motion-lab/tests -v
```

## Choreography data

Each example contains motion beats and content events:

```python
{
    "beats": [
        {"primitive": "elevator_reveal", "t0": 0.0, "t1": 0.4, "amp": 40},
        {"primitive": "ripple", "t0": 0.4, "t1": 0.74, "amp": 16},
    ],
    "content": [
        {"kind": "highlight_pulse", "at_t": 0.2, "dur": 0.14, "tiles": "all"},
    ],
}
```

The examples are intentionally plain data, but they are not generated from arbitrary briefs today.

## What the clearance report means

`collision_safe()` samples 60 evenly spaced values of `t` by default. At each sample it compares vertically adjacent tiles in the same column and reports whether their relative displacement consumes the preview gap.

It does **not**:

- evaluate continuous time between samples;
- check lateral detach or zoom transitions in the HTML concept;
- model monitor thickness, motors, load, calibration, or emergency behavior;
- certify a physical rig.

The diagnostic is useful for rapid concept iteration. Hardware validation belongs to a separate engineering workflow.

## Known visual limitation

`gravity_settle` finishes with a deliberately quick reset. Its position is cyclic, but the reset can still read as a visible seam and must be judged in the rendered loop.
