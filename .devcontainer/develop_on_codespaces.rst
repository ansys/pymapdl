.. _develop_on_codespaces:


Develop on Codespaces
=====================

`Codespaces <codespaces_>`_ is a virtual development environment provided by GitHub.
You can launch a container which all the required tools and start to work
in couple of minutes.
This is an easy way to get started with PyMAPDL development without going
through the process of setting your environment.

.. warning:: `Codespaces <codespaces_>`_  are not free, but they have a generous
   free allowance per month.
   After that, you must pay according to `GitHub pricing <github_pricing_>`_.
   You can check your billing details in your `GitHub account settings` under
   `Billing and plans` and `Plans and usage`.


How to start
------------

To start a Codespace environment you must go to the repository page
`PyMAPDL <pymapdl_repo_>`_, and click on the `<> Code` green button,
and select the tab `Codespaces`.
There you can click on `+` to open a default Codespace environment.

Alternatively, you can click on the `...` button and then click on
`New with options`.
The next window shows you the configuration form. You can choose the `branch`,
the `Dev container configuration`, the `Region` and the `Machine type`.
The `branch` refers to the PyMAPDL Github branch from which the
configuration is load from.
The `Dev container configuration` refers to the Codespaces configuration.
Currently, there are 3 main configurations:

* **PyMAPDL-Codespaces-Developer**. This is the default configuration.
  It contains the OS and Python dependencies
  to develop and test PyMAPDL. For instance, it has installed `xvfb`
  and `python pytest` for testing.
* **PyMAPDL-Codespaces-Documentation**. This configuration is specially
  set for people working with the documentation or examples, and hence
  it includes the appropriate OS and Python dependencies.
  For instance, it includes `sphinx` and `latex` to build the documentation
  as HTML and PDF.
* **PyMAPDL-DevContainer (Local) [NOT RECOMMENDED]**. This is the
  configuration for launching a development container locally.
  This container follow similar steps to the preceding configurations,
  but it is for use locally together with Visual Code, hence
  you **must not** select it when creating your Codespaces environment.
  To get more information about how to launch a devcontainer locally,
  visit :ref:`develop_on_remote_containers`.

Last, the `Machine type` allows you to choose the specifications of
the machine hosting the Codespace. 

.. warning:: If you choose `New with options`, building the Codespace
    might take longer (up to 5 minutes) than using the default configuration.

How to use
==========

The usage of a in-browser Codespaces is very simple if you are
familiar with Visual Code.
You can do almost anything that you can do in a Visual Code instance
installed locally. Create, edit and delete files, install extensions, etc.

You can connect to your Codespaces from your local IDE, by opening the
`Command palette` (:kbd:`Ctr/⌘` + :kbd:`Shift` + :kbd:`P`) and selecting
`Open in` and the name of your IDE.
Alternatively, you can also go to the PyMAPDL repository, click on 
`<> Code` button, `Codespaces` tab and then in the machine you want
to connect to.

.. note:: If by mistake you close your browser window, your Codespace is still running.
    You can access it again from the PyMAPDL repository, by clicking on the `<> Code`
    button and then `Codespaces` tab. Then you should see a list of your current
    (active and stopped) Codespaces. Just select the one you want.

.. warning:: Closing the browser window does not stop the Codespace
    from running, and hence from billing you.
    You can stop the Codespace environment from the
    `Command palette` (:kbd:`Ctr/⌘` + :kbd:`Shift` + :kbd:`P`), and then search
    for `Stop current Codespace`.

Limitations
===========

* Codespaces does not allow opening windows for plotting. However you can plot to a file,
  and open it with the `File explorer`.
* When you open a Codespace from your local IDE, you might lose some configuration.
  For instance, you might find yourself in a different working directory, or that the
  python virtual environment is not properly activated.
