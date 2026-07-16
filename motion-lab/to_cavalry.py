"""Port a motion-lab choreography into a real Cavalry render via Stallion.

Bridges the Cavalry-free generator (primitives + composer) to the high-fidelity tool:
emits Cavalry JS that builds the 5x3 wall with per-tile gradients and position.y
keyframes sampled from a chosen choreography, then renders a PNG sequence. This shows
how the motion data transfers into a higher-fidelity renderer — the
designer then finishes from here.

Usage: python3 to_cavalry.py            # builds + emits JS to /tmp/cav-build.js
       (the script then POSTs it to Stallion on localhost:8080 and polls the render)
"""
import json
import urllib.request
import time
import os
import glob
import math
import primitives as P
import compose as C

COLS, ROWS = 5, 3
TW, TH, GAP = 280, 160, 32
PITCHX, PITCHY = TW + GAP, TH + GAP
COMP_W, COMP_H = 1920, 1080
NFR = 100                     # frames (4s @ 25)
KF_STEP = 5                   # keyframe every N frames
SCALE = 50
SEQ = "/tmp/cav-dump/seq"
CHOREO = C.CHOREOS["sports-tech (athlete reveal)"]

PAL_HEX = [
    ["#A82AFF", "#C875FF", "#E5BFE8"],
    ["#1B47E5", "#5A8CFF", "#9B9DFF"],
    ["#5EEAD4", "#A7F3D0", "#ECFDF5"],
    ["#1B47E5", "#9B9DFF", "#E5BFE8"],
]


def base_xy(col, row):
    x = (col - (COLS - 1) / 2) * PITCHX
    y = ((ROWS - 1) / 2 - row) * PITCHY   # Cavalry +y is up; top row (row0) highest
    return x, y


def build_js():
    L = []
    L.append('api.writeToFile("/tmp/cav-build-log.txt","start",true);')
    L.append('var comp = api.getActiveComp();')
    L.append(f'api.set(comp, {{"resolution.x": {COMP_W}, "resolution.y": {COMP_H}}});')
    L.append('try {')
    # dark background FIRST (this scene draws last-created on top, so bg must be first
    # to sit behind the tiles)
    L.append(f"""
  (function(){{
    var bg = api.primitive("rectangle","BG");
    api.set(bg, {{"generator.dimensions":{{x:{COMP_W*2},y:{COMP_H*2}}},
                  "position":{{x:0,y:0,z:0}}}});
    var bm = api.create("colorMaterial","BGmat");
    api.set(bm, {{"materialColor.r":26,"materialColor.g":26,"materialColor.b":31,"materialColor.a":255}});
    api.connect(bm,"id",bg,"material",true);
  }})();""")
    # content events (moment_sync) parsed from the choreography
    color_evs = [e for e in CHOREO["content"] if e["kind"] == "color_shift"]
    text_evs = [e for e in CHOREO["content"] if e["kind"] == "text_reveal"]

    def in_set(ev, col, row):
        sel = ev.get("tiles", "all")
        return sel == "all" or (sel == "center" and (col, row) in C.CENTER)

    # tiles (created after bg → render on top of it)
    for row in range(ROWS):
        for col in range(COLS):
            bx, by = base_xy(col, row)
            stops = json.dumps(PAL_HEX[(col + row) % len(PAL_HEX)])
            rot = (col * 30 + row * 45) % 360
            kfs, ov_kfs = [], []
            for f in range(0, NFR + 1, KF_STEP):
                t = f / NFR
                dy = C.compose_dy(col, row, t, CHOREO)
                kfs.append(f'api.keyframe(r,{f},{{"position.y":{by + dy:.2f}}});')
                ov_kfs.append((f, by + dy))
            kf_js = "\n    ".join(kfs)
            L.append(f"""
  (function(){{
    var r = api.primitive("rectangle","Tile_{col}_{row}");
    api.set(r, {{"generator.dimensions":{{x:{TW},y:{TH}}},"generator.cornerRadius":6,
                 "position":{{x:{bx:.1f},y:{by:.1f},z:0}}}});
    var g = api.create("gradientShader","Grad_{col}_{row}");
    api.setGradientFromColors(g,"generator.gradient",{stops});
    api.set(g,{{"gradientMode":0,"generator.rotation":{rot}}});
    api.connect(g,"id",r,"material.colorShaders",true);
    {kf_js}
  }})();""")
            # color_shift overlay: a flat target-colour rect that follows the tile and
            # fades in on its beat (created after the tile → on top of it)
            for ev in color_evs:
                if not in_set(ev, col, row):
                    continue
                b, gr, rd = ev["to"]                       # ev["to"] is (B,G,R)
                op_kfs = []
                for f, yv in ov_kfs:
                    t = f / NFR
                    op = 0.0 if t < ev["at_t"] else min(1.0, (t - ev["at_t"]) / ev["dur"]) * 82
                    op_kfs.append(f'api.keyframe(o,{f},{{"position.y":{yv:.2f},"opacity":{op:.1f}}});')
                op_js = "\n    ".join(op_kfs)
                L.append(f"""
  (function(){{
    var o = api.primitive("rectangle","Shift_{col}_{row}");
    api.set(o, {{"generator.dimensions":{{x:{TW},y:{TH}}},"generator.cornerRadius":6,
                 "position":{{x:{bx:.1f},y:{by:.1f},z:0}}}});
    var m = api.create("colorMaterial","ShiftMat_{col}_{row}");
    api.set(m,{{"materialColor.r":{rd},"materialColor.g":{gr},"materialColor.b":{b},"materialColor.a":255}});
    api.connect(m,"id",o,"material",true);
    {op_js}
  }})();""")
    # text_reveal: KPI text inside a tile, fading in on its beat (created last = on top)
    for ev in text_evs:
        tcol, trow = ev["tile"]
        bx, by = base_xy(tcol, trow)
        b, gr, rd = ev.get("color", (255, 255, 255))      # (B,G,R)
        t_kfs = []
        for f in range(0, NFR + 1, KF_STEP):
            t = f / NFR
            dy = C.compose_dy(tcol, trow, t, CHOREO)
            op = 0.0 if t < ev["at_t"] else min(1.0, (t - ev["at_t"]) / ev["dur"]) * 100
            t_kfs.append(f'api.keyframe(tx,{f},{{"position.y":{by + dy - 30:.2f},"opacity":{op:.1f}}});')
        t_js = "\n    ".join(t_kfs)
        L.append(f"""
  (function(){{
    var tx = api.create("textShape","KPI_{tcol}_{trow}");
    api.set(tx, {{"text.text":{json.dumps(ev["text"])},"fontSize":96,
                  "font":{{"font":"Helvetica Neue","style":"Bold"}},
                  "material.materialColor":{{r:{rd},g:{gr},b:{b},a:255}},
                  "position":{{x:{bx - 40:.1f},y:{by - 30:.1f},z:0}}}});
    {t_js}
  }})();""")
    # render loop
    L.append(f"""
  for (var f=0; f<={NFR}; f++) {{
    api.setFrame(f);
    api.renderPNGFrame("{SEQ}/f_"+("000"+f).slice(-4)+".png", {SCALE});
  }}
  api.writeToFile("/tmp/cav-build-log.txt","OK rendered="+({NFR}+1),true);
}} catch(e) {{ api.writeToFile("/tmp/cav-build-log.txt","FAIL: "+e.toString(),true); }}""")
    return "\n".join(L)


def post(js):
    payload = json.dumps({"type": "script", "code": js}).encode()
    req = urllib.request.Request("http://localhost:8080/post", data=payload,
                                 headers={"Content-Type": "application/json"}, method="POST")
    return urllib.request.urlopen(req, timeout=300).read().decode()[:40]


if __name__ == "__main__":
    os.makedirs(SEQ, exist_ok=True)
    for f in glob.glob(f"{SEQ}/*.png"):
        os.remove(f)
    js = build_js()
    open("/tmp/cav-build.js", "w").write(js)
    print("JS bytes:", len(js), "| posting to Stallion…")
    print("HTTP", post(js))
