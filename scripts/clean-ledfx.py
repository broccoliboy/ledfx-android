# Force full rebuild of ledfx by deleting all relevant build artifacts

import pathlib
import shutil

root = pathlib.Path(__file__).parent.parent.absolute()
build_root = root / '.buildozer'

modules = [
    'ledfx',
    # 'samplerate',
    # 'aubio'
]

for module in modules:

    patterns = [
        'android/app',
        f'android/platform/build-*/build/other_builds/{module}*',
        f'android/platform/build-*/build/python-installs/ledfx/*/{module}*',
        f'android/platform/build-*/packages/{module}*',
        'android/platform/build-*/dists'
    ]

    for p in patterns:
        for d in build_root.rglob(p):
            shutil.rmtree(d, ignore_errors=True)
