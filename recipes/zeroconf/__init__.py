from pythonforandroid.recipe import PyProjectRecipe


class ZeroconfRecipe(PyProjectRecipe):
    name = 'zeroconf'
    version = '0.148.0'
    url = 'https://github.com/jstasiak/python-zeroconf/archive/{version}.tar.gz'
    md5 = '569b21cb301815c5ebda8f41b4bdbd30'
    depends = ['setuptools', 'ifaddr']


recipe = ZeroconfRecipe()
