#!/usr/bin/env python3
"""Resize and recompress oversized images listed in an inventory CSV, in place.

Usage:
  python3 scripts/optimize-images.py --csv inventory.csv [--apply] [--root DIR]
  (default is a dry run: same table, nothing written; --root defaults to the
  parent of scripts/)

CSV header: path,bytes,width,height,max_display_w,max_display_h,lightbox,og_image,referenced,pages,notes

Skipped (reported, untouched): .svg, assets/logos/*, non-image extensions, .gif,
missing files, referenced=no, and rows with no display size, no lightbox, no og_image.

Target width: scale = 2 * max(display_w/width, display_h/height) (whichever are
present), target_w = round(width*scale); lightbox=yes -> 2000; og_image=yes ->
at least 1200; capped at 2000; never upscaled (target >= natural -> no resize).
Aspect ratio kept, LANCZOS resampling. Natural size is measured from the file
after EXIF orientation is applied (the CSV width/height are not trusted for this).

Encoding: EXIF orientation applied (tag not written back), ICC profile kept.
JPEG q80 optimized progressive (RGBA/P/LA flattened on white); PNG lossless
optimize=True (P -> RGBA, saved as RGB if fully opaque); WEBP q80 method 6.
Written to a temp file in the same directory, then os.replace (atomic).
Without a resize, the file is replaced only if the output is >=10% smaller; if a
resize produced a larger file, the original is kept.
Exit code 0 unless an unexpected error occurred (other files still processed).
"""
import argparse
import csv
import os
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageOps

MAX_W = 2000
OG_MIN_W = 1200
MIN_SAVING = 0.10
JPEG_EXT = {".jpg", ".jpeg"}
IMAGE_EXT = JPEG_EXT | {".png", ".webp", ".gif"}


def yes(v):
    return (v or "").strip().lower() == "yes"


def num(v):
    try:
        return float((v or "").strip())
    except ValueError:
        return None


def skip_reason(row, root):
    rel = row["path"].strip()
    ext = Path(rel).suffix.lower()
    if ext == ".svg":
        return "svg"
    if rel.replace("\\", "/").startswith("assets/logos/"):
        return "logo"
    if ext == ".gif":
        return "gif skipped"
    if ext not in IMAGE_EXT:
        return "not an image"
    if not (root / rel).is_file():
        return "file not found"
    if not yes(row.get("referenced")):
        return "not referenced"
    dw, dh = num(row.get("max_display_w")), num(row.get("max_display_h"))
    if dw is None and dh is None and not yes(row.get("lightbox")) and not yes(row.get("og_image")):
        return "no display size known"
    return None


def target_width(row, w, h):
    dw, dh = num(row.get("max_display_w")), num(row.get("max_display_h"))
    ratios = [d / n for d, n in ((dw, w), (dh, h)) if d]
    tw = round(w * 2 * max(ratios)) if ratios else 0
    if yes(row.get("lightbox")):
        tw = MAX_W
    if yes(row.get("og_image")):
        tw = max(tw, OG_MIN_W)
    return min(tw, MAX_W)


def encode(im, ext, path, icc):
    kw = {"icc_profile": icc} if icc else {}
    if ext in JPEG_EXT:
        if im.mode in ("RGBA", "LA", "P"):
            im = im.convert("RGBA")
            bg = Image.new("RGB", im.size, (255, 255, 255))
            bg.paste(im, mask=im.getchannel("A"))
            im = bg
        elif im.mode not in ("RGB", "L", "CMYK"):
            im = im.convert("RGB")
        im.save(path, "JPEG", quality=80, optimize=True, progressive=True, **kw)
    elif ext == ".png":
        if im.mode == "RGBA" and im.getchannel("A").getextrema()[0] == 255:
            im = im.convert("RGB")
        im.save(path, "PNG", optimize=True, **kw)
    else:
        im.save(path, "WEBP", quality=80, method=6, **kw)


def process(row, root, apply):
    """Return (before_wh, after_wh, before_bytes, after_bytes, action)."""
    rel = row["path"].strip()
    path = root / rel
    ext = path.suffix.lower()
    before_b = path.stat().st_size
    with Image.open(path) as src:
        src.load()
        icc = src.info.get("icc_profile")
        if ext == ".png" and src.mode == "P":
            src = src.convert("RGBA")
        im = ImageOps.exif_transpose(src)
        w, h = im.size
        tw = target_width(row, w, h)
        resized = 0 < tw < w
        if resized:
            th = max(1, round(h * tw / w))
            im = im.resize((tw, th), Image.LANCZOS)
        out_wh = im.size
        fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".opt-", suffix=ext)
        os.close(fd)
        try:
            encode(im, ext, tmp, icc)
            after_b = os.path.getsize(tmp)
            if resized:
                ok = after_b <= before_b
                action = "resized" if ok else "kept (resized output larger)"
            else:
                ok = after_b <= before_b * (1 - MIN_SAVING)
                action = "recompressed" if ok else "kept"
            if ok and apply:
                os.replace(tmp, path)
                tmp = None
        finally:
            if tmp and os.path.exists(tmp):
                os.remove(tmp)
    if not ok:
        return (w, h), (w, h), before_b, before_b, action
    return (w, h), out_wh, before_b, after_b, action


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--csv", required=True)
    ap.add_argument("--apply", action="store_true", help="write changes (default: dry run)")
    ap.add_argument("--root", default=str(Path(__file__).resolve().parent.parent))
    args = ap.parse_args()
    root = Path(args.root).resolve()

    with open(args.csv, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    hdr = ("path", "before WxH", "after WxH", "before KB", "after KB", "saved %", "action")
    table, errors = [], []
    changed = tb = ta = 0
    for row in rows:
        rel = (row.get("path") or "").strip()
        if not rel:
            continue
        try:
            row["path"] = rel
            reason = skip_reason(row, root)
            if reason:
                size = (root / rel).stat().st_size if (root / rel).is_file() else 0
                table.append((rel, "-", "-", f"{size/1024:.0f}" if size else "-", "-", "-", f"skipped:{reason}"))
                continue
            bwh, awh, bb, ab, action = process(row, root, args.apply)
            did = action in ("resized", "recompressed")
            changed += did
            tb += bb
            ta += ab if did else bb
            pct = f"{100 * (bb - ab) / bb:.1f}" if bb else "0.0"
            table.append((rel, "%dx%d" % bwh, "%dx%d" % awh, f"{bb/1024:.0f}", f"{ab/1024:.0f}", pct, action))
        except Exception as e:  # keep going, report at the end
            errors.append((rel, repr(e)))
            table.append((rel, "-", "-", "-", "-", "-", "ERROR"))

    widths = [max(len(str(r[i])) for r in [hdr] + table) for i in range(len(hdr))]
    for r in [hdr] + table:
        print(" | ".join(str(c).ljust(widths[i]) for i, c in enumerate(r)))
    mb = 1024 * 1024
    print(f"\n{'APPLIED' if args.apply else 'DRY RUN (nothing written)'}: {changed} file(s) changed; "
          f"{tb/mb:.2f} MB before, {ta/mb:.2f} MB after, {(tb-ta)/mb:.2f} MB saved "
          f"(totals cover processed, non-skipped files)")
    for rel, err in errors:
        print(f"ERROR {rel}: {err}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
