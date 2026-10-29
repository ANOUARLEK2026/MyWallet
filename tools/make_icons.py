#!/usr/bin/env python3
"""Generate every launcher/PWA icon from App.png (run from the project root).
Output: android-res/ (copied into the Android project by scripts/android-customize.sh)
        www/icons/icon-192.png, www/icons/icon-512.png"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "App.png")
OUT = os.path.join(ROOT, "android-res")

im = Image.open(SRC).convert("RGB")
a = np.array(im).astype(np.int16)

# 1) squircle = clearly blue pixels (the PNG has a white frame around the rounded square)
core = (a[:, :, 0] < 120) & (a[:, :, 2] > 100)
core = ndi.binary_fill_holes(core)
core = ndi.binary_erosion(core, iterations=4)           # drop anti-aliased fringe
ys, xs = np.where(core)
x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
sq_w = x1 - x0 + 1                                       # width of the usable art

# 2) fill everything outside the squircle with the nearest interior colour (seam-free full-bleed)
idx = ndi.distance_transform_edt(~core, return_distances=False, return_indices=True)
filled = a[idx[0], idx[1]].astype(np.uint8)
# soften the streaks only in the filled area
blur = np.array(Image.fromarray(filled).filter(__import__("PIL.ImageFilter", fromlist=["x"]).GaussianBlur(18)))
m = core[:, :, None]
full = np.where(m, filled, blur).astype(np.uint8)
full_img = Image.fromarray(full)

def full_bleed(size, art_fraction):
    """Square canvas where the (eroded) squircle spans `art_fraction` of the width; margins are edge-extended."""
    canvas_px = int(round(sq_w / art_fraction))
    H, W = full.shape[:2]
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    left, top = int(round(cx - canvas_px / 2)), int(round(cy - canvas_px / 2))
    pad = max(0, -left, -top, left + canvas_px - W, top + canvas_px - H)
    arr = np.pad(full, ((pad, pad), (pad, pad), (0, 0)), mode="edge") if pad else full
    c = Image.fromarray(arr).crop((left + pad, top + pad, left + pad + canvas_px, top + pad + canvas_px))
    return c.resize((size, size), Image.LANCZOS)

def squircle_rgba(size, scale):
    """Squircle art with transparent corners, scaled to `scale` of a size x size canvas (legacy icons)."""
    h = core.copy()
    rgba = np.dstack([full, (ndi.binary_dilation(h, iterations=3) * 255).astype(np.uint8)])
    s = Image.fromarray(rgba).crop((x0 - 3, y0 - 3, x1 + 4, y1 + 4))
    # soft alpha edge
    al = s.split()[3].filter(__import__("PIL.ImageFilter", fromlist=["x"]).GaussianBlur(1.6))
    s.putalpha(al)
    t = int(round(size * scale))
    s = s.resize((t, t), Image.LANCZOS)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(s, ((size - t) // 2, (size - t) // 2), s)
    return out

def circle(img):
    sz = img.size[0]
    mask = Image.new("L", (sz * 4, sz * 4), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, sz * 4 - 1, sz * 4 - 1), fill=255)
    mask = mask.resize((sz, sz), Image.LANCZOS)
    out = Image.new("RGBA", (sz, sz), (0, 0, 0, 0))
    out.paste(img.convert("RGBA"), (0, 0), mask)
    return out

DENS = {"mdpi": 1, "hdpi": 1.5, "xhdpi": 2, "xxhdpi": 3, "xxxhdpi": 4}
for d, f in DENS.items():
    folder = os.path.join(OUT, f"mipmap-{d}")
    os.makedirs(folder, exist_ok=True)
    # adaptive foreground (108dp): full-bleed art, wallet kept inside the 66dp safe zone
    full_bleed(int(108 * f), 0.70).save(os.path.join(folder, "ic_launcher_foreground.png"))
    # legacy square + round icons (48dp)
    legacy = int(48 * f)
    squircle_rgba(legacy, 0.96).save(os.path.join(folder, "ic_launcher.png"))
    circle(full_bleed(legacy, 0.90)).save(os.path.join(folder, "ic_launcher_round.png"))

# PWA / favicon icons: full-bleed, maskable-safe
wd = os.path.join(ROOT, "www", "icons")
os.makedirs(wd, exist_ok=True)
for s in (192, 512):
    full_bleed(s, 0.78).convert("RGB").save(os.path.join(wd, f"icon-{s}.png"), optimize=True)
# Play-store style 512 preview (not shipped in the APK)
squircle_rgba(512, 0.98).save(os.path.join(OUT, "preview-squircle.png"))
print("art", x0, x1, y0, y1, "width", sq_w)
