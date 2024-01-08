.. _develop_on_codespaces:


Develop on Codespaces
=====================

`Codespaces <codespaces_features_>`_ is a virtual development environment provided by GitHub.
You can launch a container with all the required tools and start to work
in couple of minutes.
This is an easy way to get started with PyMAPDL development without going
through the process of setting up your environment.

.. warning:: `Codespaces <codespaces_features_>`_  are not free, but they have a generous
   free allowance per month.
   After that, you must pay according to `GitHub pricing <github_pricing_>`_.
   You can check your billing details in your `GitHub account settings` under
   *Billing and plans* and *Plans and usage*.


How to start
------------

To start a Codespace environment, go to the
`PyMAPDL repository <pymapdl_repo_>`_, click the green **Code** button,
and select the **Codespaces** tab.
Then, click the **+** button to open a default Codespace environment.

Alternatively, you can click the menu button and then select
**New with options**.

The next window shows you the configuration form. You can set these options: **Branch**,
**Dev container configuration**, **Region**, and **Machine type**.

The **Branch** option sets the PyMAPDL GitHub branch to load the configuration from.
The **Dev container configuration** option sets the Codespaces configuration.

Currently, there are three main configurations:

* :ref:`PyMAPDL-Codespaces-Developer <ref_codespaces_dev_welcome>`.
  This is the default configuration. It contains the OS and Python dependencies
  to develop and test PyMAPDL. For instance, it has ``xvfb``
  and ``pytest`` packages installed for testing.

  |Open a GitHub Codespaces for developers|

* :ref:`PyMAPDL-Codespaces-Documentation <ref_codespaces_docs_welcome>`.
  This configuration is specially set for people working with the documentation or examples. Thus,
  it includes the appropriate OS and Python dependencies.
  For instance, it includes ``sphinx`` and ``latex`` packages for building the documentation
  as HTML and PDF outputs.

  |Open a GitHub Codespaces for documentation|

* `PyMAPDL-DevContainer (Local) <pymapdl_codespaces_welcome_local_>`_ **[NOT RECOMMENDED]**. This is the
  configuration for launching a development container locally.
  This container is similar to the preceding configurations,
  but it is for use locally together with Visual Studio Code. Thus,
  you **must not** select it when creating your Codespaces environment.
  To get more information on how to launch a development container locally,
  see :ref:`develop_on_remote_containers`.

Lastly, the **Machine type** option allows you to choose the specifications of
the machine hosting the Codespace. The amount of your Codespace allowance
(free or paid) that consumed is proportional to the power of your machine.

.. warning:: If you choose **New with options**, building the Codespace
    might take longer (up to five minutes) than if you choose the default configuration.

How to use
==========

The usage of a in-browser Codespaces is very simple if you are
familiar with Visual Studio Code.
You can do almost anything that you can do in a Visual Studio Code instance
installed locally. For example, you can create, edit, and delete files, or you can install extensions.

You can connect to your Codespaces from your local IDE by opening the
**Command palette** (:kbd:`Ctr/⌘` + :kbd:`Shift` + :kbd:`P`) and selecting
**Open in** and the name of your IDE.

Alternatively, you can go to the PyMAPDL repository, click the **Code** button and **Codespaces** tab,
and then select the machine that you want to connect to.

.. note:: If you mistakenly close your browser window, your Codespace is still running.
   You can access it again from the PyMAPDL repository, by clicking the green **Code**
   button and then the **Codespaces** tab. You should see a list of your current
   (active and stopped) Codespace machine, where you can select the one that you want.

.. warning:: **Closing the browser window does not stop the Codespace
   from running**, which means you continue to be billed.

When you are not working with the Codespace virtual machine, you should stop it so you are not billed
for that time. You can stop the Codespace from the **Command palette**
(:kbd:`Ctr/⌘` + :kbd:`Shift` + :kbd:`P`) and then search for ``Stop current Codespace``.

When you have finished to work with the Codespace virtual machine and you can delete from 
your `personal Codespaces page <codespaces_>`_ there, click on the more button (**...**) of
the machine you want to dispose, and click on **Delete**.
Alternatively, you can delete them from the **Codespaces** tab under the **Code** button
in PyMAPDL repository. There you can see the running virtual machines and stop or delete
the one you prefer.

Limitations
===========

* Codespaces does not allow opening windows for plotting. However, you can plot to a file
  and then open it from the **File explorer** tab.
* When you open a Codespace from your local IDE, you might lose some configuration.
  For instance, you might find yourself in a different working directory, or you might see that the
  Python virtual environment is not properly activated.



.. |Open a GitHub Codespaces for developers| image:: https://github.com/codespaces/badge.svg
   :target: https://codespaces.new/ansys/pymapdl?quickstart=1&devcontainer_path=.devcontainer%2Fdevcontainer.json


.. |Open a GitHub Codespaces for documentation| image:: https://github.com/codespaces/badge.svg
   :target: https://codespaces.new/ansys/pymapdl?quickstart=1&devcontainer_path=.devcontainer%2Fcodespaces-docs%2Fdevcontainer.json