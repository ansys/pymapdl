"""Installation file for ansys-mapdl-core"""
import os
import sys
from io import open as io_open

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext as _build_ext

try:
    import numpy as np
except ImportError:
    raise Exception('Please install numpy first with "pip install numpy"')


def check_cython():
    """Check if binaries exist and if not check if Cython is installed"""
    has_binary_reader = False
    for filename in os.listdir('ansys/mapdl/core'):
        if '_binary_reader' in filename:
            has_binary_reader = True

    if not has_binary_reader:
        # ensure cython is installed before trying to build
        try:
            import cython
        except ImportError:
            raise ImportError('\n\n\nTo build pyansys please install Cython with:\n\n'
                              'pip install cython\n\n') from None


check_cython()


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
    cmp_arg = ['-O3', '-w']
else:
    cmp_arg = ['/Ox', '-w']


# Get version from version info
__version__ = None
this_file = os.path.dirname(__file__)
version_file = os.path.join(this_file, 'ansys', 'mapdl', 'core', '_version.py')
with io_open(version_file, mode='r') as fd:
    # execute file from raw string
    exec(fd.read())

install_requires = ['numpy>=1.14.0',
                    'pyvista>=0.27.2',
                    'appdirs>=1.4.0',
                    'psutil>=5.0.0',
                    'pexpect>=4.8.0',
                    'tqdm>=4.45.0',
                    'pyiges>=0.1.2']


# Actual setup
setup(
    name='ansys-mapdl-core',
    packages=['ansys.mapdl.core', 'ansys.mapdl.core.examples'],

    # Version
    version=__version__,

    description='Pythonic interface to MAPDL',
    long_description=open('README.rst').read(),

    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],

    # Website
    url='https://github.com/akaszynski/pyansys',

    # Build cython modules
    cmdclass={'build_ext': build_ext},
    ext_modules=[
                 Extension('ansys.mapdl.core._reader',
                           ['ansys/mapdl/core/cython/_reader.pyx',
                            'ansys/mapdl/core/cython/reader.c',
                            'ansys/mapdl/core/cython/vtk_support.c'],
                           extra_compile_args=cmp_arg,
                           language='c',),

                 Extension("ansys.mapdl.core._relaxmidside",
                           ["ansys/mapdl/core/cython/_relaxmidside.pyx"],
                           extra_compile_args=cmp_arg,
                           language='c'),

                 Extension("ansys.mapdl.core._cellqual",
                           ["ansys/mapdl/core/cython/_cellqual.pyx"],
                           extra_compile_args=cmp_arg,
                           language='c'),

                 Extension("ansys.mapdl.core._binary_reader",
                           ["ansys/mapdl/core/cython/_binary_reader.pyx",
                            "ansys/mapdl/core/cython/binary_reader.cpp"],
                           extra_compile_args=cmp_arg,
                           language='c++'),
                 ],

    python_requires='>=3.6.*',
    keywords='vtk ANSYS cdb full rst',
    package_data={'ansys.mapdl.core.examples': ['TetBeam.cdb',
                                                'HexBeam.cdb',
                                                'hex_db_150.db',
                                                'hex_db_194.db',
                                                'file.rst',
                                                'file.full',
                                                'sector.rst',
                                                'sector.cdb']},

    install_requires=install_requires,
)
