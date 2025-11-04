from pythonforandroid.recipe import PyProjectRecipe

class Pybase64Recipe(PyProjectRecipe):
    
    version = 'v1.4.2'
    url = 'git+https://github.com/mayeut/pybase64'
    
    depends = ['setuptools']


recipe = Pybase64Recipe()
