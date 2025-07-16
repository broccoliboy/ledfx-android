"""Build AIOHTTP"""
from pythonforandroid.recipe import CppCompiledComponentsPythonRecipe, CythonRecipe


class AIOHTTPRecipe(CppCompiledComponentsPythonRecipe):  # type: ignore # pylint: disable=R0903
    version = "3.11.14"
    url = "https://pypi.python.org/packages/source/a/aiohttp/aiohttp-{version}.tar.gz"
    name = "aiohttp"
    depends = ["setuptools"]
    call_hostpython_via_targetpython = False
    install_in_hostpython = True

    def get_recipe_env(self, arch):
        env = super().get_recipe_env(arch)
        env['LDFLAGS'] += ' -lc++_shared'
        return env

    python_depends = [
        'aiohappyeyeballs >= 2.3.0',
        'aiosignal >=1.1.2,<1.4',
        'async-timeout >= 4.0, <6.0 ; python_version<"3.11"',
        'attrs >= 17.3.0',
        'frozenlist >= 1.1.1',
        'multidict >=4.5, < 7.0',
        'propcache >= 0.2.0',
        'yarl >= 1.17.0, < 2.0',
    ]


recipe = AIOHTTPRecipe()
