from pythonforandroid.recipe import PyProjectRecipe

class VnoiseRecipe(PyProjectRecipe):
    '''vnoise is pure python but latest version on pypi uses pkg_resources, which is 
    deprecated and throws an exception in latest python versions. We can use this fork until
    the issue is resolved upstream.
    '''
    
    version = 'ff10442'
    url = 'https://github.com/broccoliboy/vnoise/archive/{version}.zip'

recipe = VnoiseRecipe()
