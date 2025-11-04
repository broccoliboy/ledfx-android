from pythonforandroid.recipe import PyProjectRecipe

class SamplerateRecipe(PyProjectRecipe):
    
    version = 'v0.2.1'
    url = 'git+https://github.com/tuxu/python-samplerate'
    
    depends = ['setuptools', 'numpy']
    
    def get_recipe_env(self, arch, **kwargs):
        env = super().get_recipe_env(arch, **kwargs)
        
        env['CMAKE_ARGS'] = ' '.join([
            env.get('CMAKE_ARGS', ''),  # existing CMAKE_ARGS, if any
            '-DCMAKE_SYSTEM_NAME=Android',  # tell cmake to cross compile for Android
            f'-DCMAKE_ANDROID_ARCH_ABI={arch.arch}',  # set ABI version
            f'-DCMAKE_ANDROID_NDK={self.ctx.ndk_dir}',  # set NDK path
            f'-DPYTHON_EXECUTABLE={self.ctx.python_recipe.python_exe}',  # needed for pybind11
            f'-DPYTHON_INCLUDE_DIRS={self.ctx.python_recipe.include_root(arch.arch)}'  # needed for pybind11
        ])
        return env


recipe = SamplerateRecipe()
