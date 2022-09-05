"""
.. _ref_dpf_basic_example:

Basic DPF-Core Usage with PyMAPDL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This example is adapted from `Basic DPF-Core Usage Example <https://dpf.docs.pyansys.com/examples/00-basic/00-basic_example.html>`_
and it shows how to open a result file and do some
basic postprocessing.

If you have Ansys 2021 R1 installed, starting DPF is quite easy
as DPF-Core takes care of launching all the services that
are required for postprocessing Ansys files.

First, import the DPF-Core module as ``dpf_core`` and import the
included examples file.


"""
import tempfile

from ansys.dpf import core as dpf

from ansys.mapdl.core import launch_mapdl
from ansys.mapdl.core.examples import vmfiles

###############################################################################
# ## Model creation
# Running a verification manual example in MAPDL
#
mapdl = launch_mapdl()

vm5 = vmfiles["vm5"]
output = mapdl.input(vm5)

print(output)

# If you are working locally, you don't need to perform the following steps
temp_directory = tempfile.gettempdir()
# Downloading RST file to the current folder
rst_path = mapdl.download_result(temp_directory)

###############################################################################
# Next, open the generated RST file and print out the ``model`` object.  The
# ``Model`` class helps to organize access methods for the result by
# keeping track of the operators and data sources used by the result
# file.
#
# Printing the model displays:
#
# - Analysis type
# - Available results
# - Size of the mesh
# - Number of results
#
# Also, note that the first time you create a DPF object, Python
# automatically attempts to start the server in the background.  If you
# want to connect to an existing server (either local or remote), use
# :func:`dpf.connect_to_server`.

model = dpf.Model(rst_path)
print(model)

###############################################################################
# Model Metadata
# ~~~~~~~~~~~~~~
# Specific metadata can be extracted from the model by referencing the
# model's ``metadata`` property.  For example, to print only the
# ``result_info``:

metadata = model.metadata
print(metadata.result_info)

###############################################################################
# To print the mesh region:

print(metadata.meshed_region)

###############################################################################
# To print the time or frequency of the results:

print(metadata.time_freq_support)

###############################################################################
# Extracting Displacement Results
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# All results of the model can be accessed through the ``results``
# property, which returns the :class:`ansys.dpf.core.results.Results`
# class. This class contains the DPF result operators available to a
# specific result file, which are listed when printing the object with
# ``print(results)``.
#
# Here, the ``'U'`` operator is connected with ``data_sources``, which
# takes place automatically when running ``results.displacement()``.
# By default, the ``'U'`` operator is connected to the first result set,
# which for this static result is the only result.
results = model.results
displacements = results.displacement()
fields = displacements.outputs.fields_container()

# Finally, extract the data of the displacement field:
disp = fields[0].data
disp

###############################################################################
# ## Plot displacements
#

model.metadata.meshed_region.plot(fields, cpos="xy")


###############################################################################
# ## Clean up
#
# Stop mapdl
mapdl.exit()
