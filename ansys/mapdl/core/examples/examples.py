"""pymapdl examples"""
import os

# get location of this folder and the example files
dir_path = os.path.dirname(os.path.realpath(__file__))

# add any files you'd like to import here.  For example:
wing_model = os.path.join(dir_path, 'wing.dat')

# be sure to add the input file directly in this directory
# This way, files can be loaded with:
# from ansys.mapdl.core import examples
# examples.wing_model
