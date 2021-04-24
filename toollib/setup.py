from setuptools import setup, find_packages
from setuptools_rust import Binding, RustExtension


setup(
    name="minesweeper_toollib",
    version="1.0.4",
    rust_extensions=[RustExtension("minesweeper_toollib.minesweeper_toollib", binding=Binding.PyO3)],
    # packages=["hello_rust"],
    # rust extensions are not zip safe, just like C-extensions.
    zip_safe=False,


    url='https://github.com/eee555/Solvable-Minesweeper',  # Optional

    author='Wang Jianing',  # Optional

    keywords='minesweeper, solver, saolei, solvable',  # Optional

    package_dir={'': 'src'},  # Optional

    packages=find_packages(where='src'),  # Required

    python_requires='>=3.6, <4',
    classifiers=[  

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish
        'License :: OSI Approved :: GNU General Public License (GPL)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate you support Python 3. These classifiers are *not*
        # checked by 'pip install'. See instead 'python_requires' below.
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],

    project_urls={  # Optional
        'Bug Reports': 'https://github.com/eee555/Solvable-Minesweeper/issues',
        'Source': 'https://github.com/eee555/Solvable-Minesweeper/tree/master/toollib/src',
    },
)