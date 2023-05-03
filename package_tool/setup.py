from distutils.core import setup
from Cython.Build import cythonize

setup(ext_modules=cythonize(r"../src/metaminesweeper_checksum.py"))