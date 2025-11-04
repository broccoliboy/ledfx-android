from pythonforandroid.recipe import PythonRecipe, PyProjectRecipe


class RequestsRecipe(PyProjectRecipe):
    name = 'requests'
    version = 'v2.32.5'
    url = 'https://github.com/psf/requests/archive/{version}.tar.gz'
    depends = ['setuptools']

    python_depends = [
        # "charset_normalizer>=2,<4",  # probably needs dedicated recipe to use this, but chardet seems to work fine
        "chardet>=5,<6",
        "idna>=2.5,<4",
        "urllib3>=1.21.1,<3",
        "certifi>=2017.4.17",
    ]


recipe = RequestsRecipe()
