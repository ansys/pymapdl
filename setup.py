"""
Setup.py for pyansys
"""

from setuptools import setup, Extension
from Cython.Distutils import build_ext

import numpy

setup(
    name='pyansys',
    packages = ['pyansys', 'pyansys.Tests'],

    # Version
    version='0.10',

    description='Pythonic interface to ANSYS binary files',
    long_description=open('README.rst').read(),

    # Author details
    author='Alex Kaszynski',
    author_email='akascap@gmail.com',

    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',

        # Target audience
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Information Analysis',

        # MIT License
        'License :: OSI Approved :: MIT License',

        # Will work for other python 3 versions
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
    ],

    # Website
    url = 'https://github.com/akaszynski/pyansys',

    # Build cython modules
    cmdclass={'build_ext': build_ext},
    ext_modules=[Extension("pyansys._parsefull", 
                           ['pyansys/cython/_parsefull.pyx',
                            'pyansys/cython/parsefull.c'],
                           language='c'),

                ],
                           
    keywords='vtk ANSYS cdb full rst',                           
                           
    include_dirs=[numpy.get_include()],
                  
    package_data={'pyansys.Tests': ['HexBeam.cdb', 'file.rst', 'file.full']},

    # Might work with earlier versions (untested)
    install_requires=['numpy>1.9.3', 'ANSYScdb>=0.12.1', 'cython>0.23.1']

)
