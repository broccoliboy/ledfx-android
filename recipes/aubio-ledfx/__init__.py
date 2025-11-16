from pythonforandroid.recipe import MesonRecipe


class AubioLedfxRecipe(MesonRecipe):
    
    meson_version = "1.9.1"

    version = "v0.4.11"
    url = "https://github.com/ledfx/aubio-ledfx/archive/{version}.zip"
    depends = ["numpy"]


recipe = AubioLedfxRecipe()
