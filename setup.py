from setuptools.command.sdist import sdist as _sdist
from setuptools import setup, find_packages, Extension


try:
    from Cython.Distutils import build_ext
except ImportError:
    use_cython = False
else:
    use_cython = True

cmdclass = {}
ext_modules = []

if use_cython:
    from Cython.Build import cythonize
    ext_modules = cythonize(['syx/_speedups.pyx'])

    class sdist(_sdist):
        def run(self):
            # Make sure the compiled Cython files in the distribution
            # are up-to-date
            cythonize(['syx/_speedups.pyx'])
            _sdist.run(self)
    cmdclass['sdist'] = sdist
    cmdclass.update({
        'build_ext': build_ext
    })
else:
    ext_modules += [
        Extension(
            "syx._speedups",
            ["syx/_speedups.c"],
            extra_compile_args=["-O3"]),
    ]

__version__ = '0.4.0'


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='syx',
    version=__version__,
    description="Python 2 and 3 compatability library",
    long_description=readme(),
    url='www.github.com/lyft/syx',
    maintainer='Roy Willams',
    maintainer_email='rwilliams@lyft.com',
    packages=find_packages(exclude=['tests*']),
    license='apache2',
    dependency_links=[],
    install_requires=[
        'six>=1.1.0, <2.0.0'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    cmdclass=cmdclass,
    ext_modules=ext_modules,
)
