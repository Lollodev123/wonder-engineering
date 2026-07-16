"""Generate motion-concept previews + a contact sheet.

Run:  python3 generate.py [out_dir]
Produces, per primitive: <name>.mp4 (looping preview) and collects a hero frame
into contact-sheet.png. Also prints a collision-safety report.
"""
import sys
import os
import cv2
import numpy as np
import primitives as P
import preview as V

OUT = sys.argv[1] if len(sys.argv) > 1 else "out"
os.makedirs(OUT, exist_ok=True)
GAP_PREVIEW = V.GAP  # collision budget in preview units (pitch headroom)

report = []
heroes = []
order = ["traveling_wave", "ripple", "standing_wave", "column_cascade",
         "row_sweep", "elevator_reveal", "breathing", "gravity_settle"]

for name in order:
    fn, desc, kind = P.PRIMITIVES[name]
    amp = fn.__defaults__[0]
    ok, overlap = P.collision_safe(fn, amp, GAP_PREVIEW)
    # render preview
    label = f"{name}  ({kind})"
    frames = V.render_concept(name, f"{OUT}/{name}.mp4", n_frames=100, amp=amp, label=label)
    hero = frames[25].copy()
    # annotate hero with name + safety
    tag = "SAFE" if ok else f"OVERLAP {overlap:.0f}px"
    cv2.putText(hero, name, (24, V.H - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(hero, tag, (24, V.H - 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (120, 255, 120) if ok else (120, 120, 255), 1, cv2.LINE_AA)
    heroes.append(hero)
    report.append(f"  {name:16s} amp={amp:5.1f} {kind:11s} {'SAFE' if ok else 'OVERLAP %.0fpx'%overlap}  — {desc}")

# contact sheet: 2 cols x 4 rows of hero frames, scaled down
cell_w = V.W // 2
cell_h = V.H // 2
sheet = np.full((cell_h * 4, cell_w * 2, 3), 20, np.uint8)
for i, hero in enumerate(heroes):
    r, c = divmod(i, 2)
    small = cv2.resize(hero, (cell_w, cell_h))
    sheet[r * cell_h:(r + 1) * cell_h, c * cell_w:(c + 1) * cell_w] = small
cv2.imwrite(f"{OUT}/contact-sheet.png", sheet)

print("=== Motion-concept generation report ===")
print(f"8 concepts, 5x3 wall, Y-only, gap budget {GAP_PREVIEW}px (preview units)")
print("\n".join(report))
print(f"\ncontact-sheet.png + 8 .mp4 written to {OUT}/")
