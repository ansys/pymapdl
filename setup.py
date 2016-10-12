"""
Setup.py for ANSYScdb
"""

from setuptools import setup


setup(
    name='pyansys',
    packages = ['pyansys', 'pyansys.Tests'],

    # Version
    version='0.10',

    description='Pythonic interface to ANSYS and ANSYS files',
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

        # Tested with with just Python 2.7 (so far)
        'Programming Language :: Python :: 2.7',
#        'Programming Language :: Python :: 3.5',
    ],

    # Website
    url = 'https://github.com/akaszynski/pyansys',

    # Build cython modules
                           
    keywords='vtk ANSYS cdb',                           
                           
#    include_dirs=[numpy.get_include()],
                  
    package_data={'pyansys.Tests': ['HexBeam.cdb', 'file.rst']},

    # Might work with earlier versions (untested)
    install_requires=['numpy>1.9.3', 'ANSYScdb>=0.12.1']

)
