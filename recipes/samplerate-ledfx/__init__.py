from os.path import join
from pythonforandroid.recipe import PyProjectRecipe


class SamplerateLedfxRecipe(PyProjectRecipe):

    version = 'v0.2.3'
    url = 'git+https://github.com/ledfx/python-samplerate-ledfx'

    depends = ['numpy']

    def get_recipe_env(self, arch, **kwargs):
        env = super().get_recipe_env(arch, **kwargs)
        
        env['CMAKE_ARGS'] = ' '.join([
            env.get('CMAKE_ARGS', ''),  # existing CMAKE_ARGS, if any
            '-DCMAKE_SYSTEM_NAME=Android',  # tell cmake to cross compile for Android
            f'-DCMAKE_ANDROID_ARCH_ABI={arch.arch}',  # set ABI version
            f'-DCMAKE_ANDROID_NDK={self.ctx.ndk_dir}',  # set NDK path
            '-DPYBIND11_USE_CROSSCOMPILING=ON',  # tell pybind11 we're cross compiling
            '-DPYBIND11_FINDPYTHON=OFF',  # disable pybind11's FindPython
            f'-DPYTHON_INCLUDE_DIRS={self.ctx.python_recipe.include_root(arch.arch)}'  # tell pybind11 where to find Python
        ])
        
        return env


recipe = SamplerateLedfxRecipe()
