"""
LedFX recipe for python-for-android
A few changes are required to use LedFX on Android:
  - All requirements must be listed in this recipe file because python-for-android doesn't install them from setup.py by default
  - Requirements that are not pure python need their own recipes to tell python-for-android how to compile it on android. Aubio is one example.
"""
from pythonforandroid.recipe import PyProjectRecipe


class LedFxRecipe(PyProjectRecipe):
    """
    This recipe instructs python-for-android how to build LedFx. The LedFx source is expected to be already located in deps/ledfx
    """
    name = 'ledfx'

    depends = [
        'numpy',
        'aiohttp',
        'aubio',
        'zeroconf',
        'pybase64',
        'pillow',
        'samplerate',
        'requests',
        'netifaces'
    ]
    
    python_depends = [
        'multidict>=6.4.3,<7',
        'sacn>=1.9.0,<2',
        'python-osc>=1.9.3,<2',
        'stupidartnet>=1.4.0,<2',
        'openrgb-python>=0.2.15,<1',
        'flux-led>=1.2.0,<2',
        'aiohttp-cors>=0.8.1,<1',
        'voluptuous>=0.14.1,<1',
        'paho-mqtt>=1.6.1,<2',
        'psutil>=5.9.7,<6',
        'pyserial>=3.5,<4',
        'icmplib>=3.0.4,<4',
        'certifi>=2025.4.26,<2026',
        'python-dotenv>=1.1.0,<2',
        'vnoise>=0.1.0,<1',
        'webcolors>=24,<25',
    ]


recipe = LedFxRecipe()
