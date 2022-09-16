This example demonstrates using pyMapdl with Dash.

Dash 
	a low-code framework for building data apps. 
	Dash apps are rendered in the web browser.
For Dash documentation , 
	refer to: https://dash.plotly.com/
	https://dash-bootstrap-components.opensource.faculty.ai/docs/components/

--------------------------------------------------------

For this example, install modules as needed:
	dash
	dash_bootstrap_components
	plotly.express 
	webbrowser
	pandas

--------------------------------------------------------

Go through the functions in the python file  and the assets folder :

Sidebar
	3 Navigation Links : Description, Simulation, Data
	Define Layout(contents) for each using components
2 Callback functions:
	render_page_content : 
		Event : Click on the any of the three links of the sidebar
		Return: Renders page content for the respective link
	start_pymapdl (for page2 of Simulation) : 
		Event : Click on submit button
		Do: Launches pyMapdl , Solves 
		Return : a value (tip deflection) and a plot image(tip deflection)
	1 more function 
		to point to a csv file for data wrangling

--------------------------------------------------------

Run  the py file 
This should launch the app in your default browser 

Description page : 
	Read the problem statement 
Simulation Page  : 
	Change the input values 
	Solve.Wait to finish.
	Notice the displacement and plot
Data Page : 
	Notice the data included in the table and graph 

