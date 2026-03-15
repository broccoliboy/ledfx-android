
#!/usr/bin/env python3
# Script to resize banner.png for Android TV, maintaining aspect ratio and centering.
import shutil

from PIL import Image, ImageOps
from pathlib import Path


def main():
    project_root = Path(__file__).parent.parent
    res_base = project_root / 'src' / 'res'

    # Copy tray.png to res directory
    tray_src = (project_root / 'deps' / 'ledfx' / 'ledfx_assets' / 'tray.png').resolve()
    tray_dst = res_base / 'tray.png'
    if tray_src.exists():
        tray_dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(tray_src, tray_dst)
        print(f'Copied: {tray_src} -> {tray_dst}')
    else:
        raise FileNotFoundError(f'tray.png not found at {tray_src}')

    # Copy banner.png to res directory
    src = (project_root / 'deps' / 'ledfx' / 'ledfx_assets' / 'banner.png').resolve()
    if not src.exists():
        raise FileNotFoundError(f'banner.png not found at {src}')
    banner_dst = res_base / 'banner.png'
    banner_dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, banner_dst)
    print(f'Copied: {src} -> {banner_dst}')

    sizes = [
        (160, 90, 'mipmap-mdpi'),
        (240, 135, 'mipmap-hdpi'),
        (320, 180, 'mipmap-xhdpi'),
        (480, 270, 'mipmap-xxhdpi'),
        (640, 360, 'mipmap-xxxhdpi'),
    ]
    img = Image.open(str(src))
    for w, h, d in sizes:
        outdir = res_base / d
        outdir.mkdir(parents=True, exist_ok=True)
        outpath = outdir / 'banner.png'
        padded = ImageOps.pad(img, (w, h), color=(0, 0, 0, 0), centering=(0.5, 0.5))
        padded.save(str(outpath))
        print(f'Saved: {outpath}')

if __name__ == '__main__':
    main()
