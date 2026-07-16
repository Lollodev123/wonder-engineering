#!/usr/bin/env python3
"""Replicate API helper — generate, poll, download.

Usage:
  scripts/replicate.py image  <prompt>  <output-path>  [--model schnell|dev|pro]  [--ar 16:9|1:1|9:16]
  scripts/replicate.py video  <prompt>  <output-path>  [--model hunyuan|ltx|mochi]
  scripts/replicate.py rembg  <input-path>  <output-path>

Reads REPLICATE_API_TOKEN from .env in repo root.
"""
import json, os, sys, time, urllib.request, urllib.error, urllib.parse, argparse, mimetypes
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ENV  = REPO / ".env"
API  = "https://api.replicate.com/v1"

MODELS = {
    "image": {
        "schnell": "black-forest-labs/flux-schnell",
        "dev":     "black-forest-labs/flux-dev",
        "pro":     "black-forest-labs/flux-1.1-pro",
    },
    "video": {
        # Hunyuan Video — open-source, ~$0.10–0.30/clip, ~5s
        "hunyuan": "tencent/hunyuan-video",
        # LTX Video — fast, very cheap
        "ltx":     "lightricks/ltx-video",
        # Mochi-1 — high quality, more expensive
        "mochi":   "genmoai/mochi-1",
    },
    "rembg":  "lucataco/remove-bg",
}

def load_token():
    if ENV.exists():
        for line in ENV.read_text().splitlines():
            if line.startswith("REPLICATE_API_TOKEN="):
                return line.split("=", 1)[1].strip()
    return os.environ.get("REPLICATE_API_TOKEN", "")

def http(method, url, headers=None, body=None):
    headers = headers or {}
    headers.setdefault("Content-Type", "application/json")
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        try: return e.code, json.loads(e.read().decode())
        except Exception: return e.code, {"error": str(e)}

def predict(model, inputs, token):
    h = {"Authorization": f"Bearer {token}"}
    status, body = http("POST", f"{API}/models/{model}/predictions", h,
                        {"input": inputs})
    if status >= 300:
        sys.stderr.write(f"ERROR {status}: {json.dumps(body, indent=2)}\n")
        sys.exit(1)
    pred_id = body["id"]
    sys.stderr.write(f"  prediction {pred_id} → polling…\n")

    while True:
        status, body = http("GET", body["urls"]["get"], h)
        st = body.get("status", "?")
        sys.stderr.write(f"    status={st}\n")
        if st in ("succeeded", "failed", "canceled"):
            break
        time.sleep(3)
    if st != "succeeded":
        sys.stderr.write(f"  prediction {st}: {body.get('error')}\n")
        sys.exit(2)
    out = body.get("output")
    if isinstance(out, list): out = out[0]
    return out, body.get("metrics", {})

def download(url, path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as r, open(path, "wb") as f:
        while chunk := r.read(65536):
            f.write(chunk)
    return os.path.getsize(path)

def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)

    pi = sub.add_parser("image")
    pi.add_argument("prompt")
    pi.add_argument("output")
    pi.add_argument("--model", default="schnell", choices=list(MODELS["image"].keys()))
    pi.add_argument("--ar",    default="16:9")

    pv = sub.add_parser("video")
    pv.add_argument("prompt")
    pv.add_argument("output")
    pv.add_argument("--model", default="ltx", choices=list(MODELS["video"].keys()))

    pr = sub.add_parser("rembg")
    pr.add_argument("input")
    pr.add_argument("output")

    a = p.parse_args()
    tok = load_token()
    if not tok:
        sys.stderr.write("FATAL: no REPLICATE_API_TOKEN in .env or env\n"); sys.exit(3)

    if a.cmd == "image":
        model = MODELS["image"][a.model]
        inputs = {
            "prompt": a.prompt,
            "aspect_ratio": a.ar,
            "num_outputs": 1,
            "output_format": "png",
            "go_fast": True,
        }
        if a.model == "schnell": inputs["num_inference_steps"] = 4
    elif a.cmd == "video":
        model = MODELS["video"][a.model]
        inputs = {"prompt": a.prompt}
        if a.model == "ltx":
            inputs.update({"num_frames": 121, "frame_rate": 24})  # ~5s
    else:
        model = MODELS["rembg"]
        ip = a.input
        # Upload local file as data URL or pass URL
        if ip.startswith("http"):
            inputs = {"image": ip}
        else:
            import base64
            mime = mimetypes.guess_type(ip)[0] or "image/png"
            data = base64.b64encode(Path(ip).read_bytes()).decode()
            inputs = {"image": f"data:{mime};base64,{data}"}

    sys.stderr.write(f"→ {model}: {a.prompt if a.cmd != 'rembg' else a.input}\n")
    out_url, metrics = predict(model, inputs, tok)
    sys.stderr.write(f"  ✓ done: {out_url[:80]}…\n")
    sys.stderr.write(f"  metrics: {metrics}\n")
    out_path = a.output if a.cmd == "rembg" else a.output
    size = download(out_url, out_path)
    sys.stderr.write(f"  ✓ saved {out_path} ({size//1024} KB)\n")
    print(out_path)

if __name__ == "__main__":
    main()
