.. _dash_example:

Use Dash to build a PyMAPDL web app
===================================

This example shows how to use Dash to build a web app for a simple FEA problem.

Dash is a low-code framework for building data apps which are rendered in a web browser. 
For Dash documentation, refer to: https://dash.plotly.com/


Required modules
----------------

For this example, install modules as needed:

* ``dash``
* ``dash_bootstrap_components``
* ``plotly.express``
* ``webbrowser``
* ``pandas``

Structure
---------

* Description page. Read the problem statement 
* Simulation Page. 
  Allow to change the input values, solve the problem and plot the results.
* Data Page : 
	Allow to plot data in a table and graph


Usage
-----

Download the zip file from the link below and unzip it to a folder.
Run the Python file ``BimetallicStrip.py`` which launches the app in your default browser.

:download:`ANSYS Licensing Guide <dash-vm35.zip>`
