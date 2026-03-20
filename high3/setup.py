from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import subprocess
import os
import sys

class RustExtension(Extension):
    def __init__(self, name, path):
        super().__init__(name, sources=[])
        self.path = path

class RustBuild(build_ext):
    def run(self):
        for ext in self.extensions:
            if isinstance(ext, RustExtension):
                self.build_rust(ext)
        super().run()

    def build_rust(self, ext):
        cwd = ext.path
        target = os.environ.get('CARGO_BUILD_TARGET', None)
        args = ['cargo', 'build', '--release', '--lib']
        if target:
            args += ['--target', target]
        print(f"Building Rust library in {cwd}")
        subprocess.check_call(args, cwd=cwd)
        # Copy the built library to the extension output directory
        # This is a simplified version; in a real scenario you'd locate the .so/.dll
        # and copy it to self.build_lib.

# The actual extension is just a placeholder; the real library is built by cargo.
extensions = [
    RustExtension('sieve._sieve', path='./rust'),
]

setup(
    name='sieve-rs',
    version='0.1.0',
    description='Fast Sieve of Eratosthenes implemented in Rust with Python bindings',
    long_description=open('README.md').read() if os.path.exists('README.md') else '',
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='you@example.com',
    url='https://github.com/example/sieve',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Rust',
    ],
    python_requires='>=3.7',
    packages=['sieve'],
    package_dir={'sieve': 'python'},
    ext_modules=extensions,
    cmdclass={'build_ext': RustBuild},
    zip_safe=False,
)