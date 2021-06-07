.. _faq:

**************************
Frequently Asked Questions
**************************

A collection of frequently asked questions and their answers.

How should I report issues?
---------------------------

Issues with pyansys such as bugs, feature requests, and documentation errors
can be reported on the `GitHub page <https://github.com/pyansys/PyMAPDL/issues>`_ as new issues.

If you wish to ask more open-ended questions or wish to pick the brains of the community
you can visit the `Discussions section <https://github.com/pyansys/PyMAPDL/discussions>`_ of our GitHub repository.


What are the pros and cons of pyansys vs Ansys ACT?
---------------------------------------------------

It depends on your pipeline and software approach. Ansys Act is a workbench dependent approach where
extensions are built from within the ACT App Builder and then run from within Ansys Mechanical.
If you intend to vary parameters, you'll then need to use Ansys optiSLang to vary those parameters
and batch your solutions.

The main advantages that PyAnsys has over Ansys ACT are:

 * Tight integration with python tools and open source modules alongside Ansys software.
 * Scripts are written in python. ACT uses .net and you can call IronPython, and potentially
   other tools available within Ansys Mechanical.
 * Being outside of Ansys Mechanical means that you can call our application workflow without
   opening up the GUI for user interaction. Should you desire a GUI, you can create your own via PyQt,
   or just output plots via matplotlib or vtk.
 * It is compatible with modern Python (3), whereas ACT is only compatible with IronPython (Python 2)

The best approach will depend on your workflow needs and how you'd like to develop software.
