from pythonforandroid.recipe import PyProjectRecipe


class AubioRecipe(PyProjectRecipe):
    
    # v0.5.0-alpha
    version = "5461304"  # use commit hash because no v0.5 tag exists at this point
    url = "https://github.com/aubio/aubio/archive/{version}.zip"
    md5 = "4191c693e4944dfe49e7340b5be4e692"
    depends = ["numpy", "setuptools"]
    patches = [
        'remove-external-deps.patch'  # removes macos platform specific cmake configs so cross compilation works from macos
    ]


recipe = AubioRecipe()
