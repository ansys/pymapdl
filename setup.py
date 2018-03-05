"""
Installation file for pyansys
"""
import os
import sys
from io import open as io_open

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext as _build_ext


class build_ext(_build_ext):
    """ build class that includes numpy directory """
    def finalize_options(self):
        _build_ext.finalize_options(self)
        # Prevent numpy from thinking it is still in its setup process:
        __builtins__.__NUMPY_SETUP__ = False
        import numpy
        self.include_dirs.append(numpy.get_include())


def compilerName():
    """ Check compiler and assign compile arguments accordingly """
    import re
    import distutils.ccompiler
    comp = distutils.ccompiler.get_default_compiler()
    getnext = False

    for a in sys.argv[2:]:
        if getnext:
            comp = a
            getnext = False
            continue
        # separated by space
        if a == '--compiler' or re.search('^-[a-z]*c$', a):
            getnext = True
            continue
        # without space
        m = re.search('^--compiler=(.+)', a)
        if m is None:
            m = re.search('^-[a-z]*c(.+)', a)
            if m:
                comp = m.group(1)

    return comp


# Assign arguments based on compiler
compiler = compilerName()
if compiler == 'unix':
    cmp_arg = ['-O3']
else:
    cmp_arg = ['/Ox']


# Get version from version info
__version__ = None
version_file = os.path.join(
    os.path.dirname(__file__),
    'pyansys',
    '_version.py')
with io_open(version_file, mode='r') as fd:
    # execute file from raw string
    exec(fd.read())


# Actual setup
setup(
    name='pyansys',
    packages=['pyansys', 'pyansys.examples'],

    # Version
    version=__version__,

    description='Pythonic interface to ANSYS binary files',
    long_description=open('README.rst').read(),

    # Author details
    author='Alex Kaszynski',
    author_email='akascap@gmail.com',

    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    # Website
    url='https://github.com/akaszynski/pyansys',

    # Build cython modules
    cmdclass={'build_ext': build_ext},
    ext_modules=[Extension("pyansys._parsefull",
                           ['pyansys/cython/_parsefull.pyx',
                            'pyansys/cython/parsefull.c'],
                           extra_compile_args=cmp_arg,
                           language='c'),

                 Extension("pyansys._parser",
                           ["pyansys/cython/_parser.pyx"],
                           extra_compile_args=cmp_arg,
                           language='c'),

                 Extension('pyansys._reader',
                           ['pyansys/cython/_reader.pyx',
                            'pyansys/cython/reader.c'],
                           extra_compile_args=cmp_arg,
                           language='c',),

                 Extension("pyansys._relaxmidside",
                           ["pyansys/cython/_relaxmidside.pyx"],
                           extra_compile_args=cmp_arg,
                           language='c'),

                 # cell quality module
                 Extension("pyansys._cellqual",
                           ["pyansys/cython/_cellqual.pyx"],
                           extra_compile_args=cmp_arg,
                           language='c'),

                 # cell quality module
                 Extension("pyansys._cellqualfloat",
                           ["pyansys/cython/_cellqualfloat.pyx"],
                           extra_compile_args=cmp_arg,
                           language='c'),

                 Extension("pyansys._rstHelper",
                           ["pyansys/cython/_rstHelper.pyx"],
                           extra_compile_args=cmp_arg,
                           language='c'),

                 ],

    keywords='vtk ANSYS cdb full rst',
    package_data={'pyansys.examples': ['TetBeam.cdb', 'HexBeam.cdb',
                                       'file.rst', 'file.full']},

    # Might work with earlier versions
    install_requires=['numpy>1.9.3', 'cython>0.23.1', 'vtkInterface>=0.4.0']

)
