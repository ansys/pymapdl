.. _ref_hpc:


.. toctree::
   :maxdepth: 1
   :hidden:

   introduction
   pymapdl
   mapdl
   troubleshooting

********************************
High performance computing (HPC)
********************************

This page provides an overview on how to use PyMAPDL in HPC clusters.
While it only considers the SLURM scheduler, many of the assumptions for this scheduler might apply to other schedulers, such as PBS, SGE, or LSF.


.. grid:: 2 2 2 2
    :gutter: 1 2 3 3
    :padding: 1 2 3 3

    .. grid-item-card:: Introduction to SLURM
       :link: ref_hpc_slurm
       :link-type: ref

       Short and basic introduction on how SLURM clusters work.
       How to submit, list and cancel jobs is explained briefly.


    .. grid-item-card:: PyMAPDL on SLURM HPC clusters
       :link: ref_hpc_pymapdl
       :link-type: ref

       How to use PyMAPDL on a SLURM cluster, from
       managing the Python virtual environment to job submission.


    .. grid-item-card:: MAPDL on SLURM HPC clusters
       :link: ref_hpc_mapdl
       :link-type: ref

       How launch MAPDL jobs on a SLURM cluster across
       one or multiple nodes.


    .. grid-item-card:: Troubleshooting
       :link: ref_hpc_troubleshooting
       :link-type: ref

       Most common issues when running PyMAPDL on a cluster are
       listed here with their solutions.

