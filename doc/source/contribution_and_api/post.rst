.. _post_processing_api:


Post-Processing
===============

This class contains an API to post-process directly from MAPDL.
Should you wish to post-process MAPDL result files outside of PyMAPDL,
you can use one of the following packages:

* `DPF-Core <_dpf_core_docs>`_ : Post-Processing using the Data Processing Framework (DPF).  More complex yet and more powerful post-processing APIs.
* `DPF-Post <dpf_post_docs>`_ : Streamlined and simplified DPF Post Processing.  Higher level package and uses ``DPF-Core``.
* `Legacy PyMAPDL Reader <legacy_reader_docs>`_: Legacy result file reader.  Supports result files from MAPDL v14.5 to the current release.

.. currentmodule:: ansys.mapdl.core

.. autosummary::
   :toctree: _autosummary

   post.PostProcessing
