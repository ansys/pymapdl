# Import all the necessary libraries

import csv
import os
import shutil
from threading import Timer
import webbrowser

import dash
from dash import dash_table, dcc, html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

from ansys.mapdl.core import launch_mapdl

JNAME = "my_new_vm"
FINAL_IMAGE_PATH = "assets/cylinder.png"


def pyMapdl_vm35(L, t, T1, T2, e1, e2, c1, c2):
    """1. Deletes old image file if it exists
    2. Creates a new csv file if needed
    3. Starts fresh mapdl run
    4. Returns new image file and deformation value
    """
    try:
        cwd = os.getcwd()
        mydir = os.path.join(cwd, "assets")
        for item in os.listdir(mydir):
            if item.endswith(".png") and item.startswith("cyl"):
                os.remove(os.path.join(mydir, item))
    except:
        print("[older png file deletion not necessary]")

    # Create a new csv file if not available
    try:
        needed_file = os.path.join(os.getcwd(), "assets", "data.csv")
        needed_file_exists_check = os.path.exists(needed_file)
        col_names = [
            "Length",
            "Thickness",
            "Tref",
            "Tamb",
            "e1",
            "CTE1",
            "E2",
            "CTE2",
            "deflection",
            "LT_Ratio",
            "Temp_Diff",
        ]

        if not needed_file_exists_check:
            with open(needed_file, "w", newline="\n") as f:
                writer = csv.writer(f, lineterminator="\n")
                writer.writerow(col_names)
    except:
        print("[csv file already exists]")

    # Launch
    mapdl, my_wdirnow = my_mapdl_launch(JNAME)

    # Solve
    solve_vm_35(mapdl, L, t, e1, c1, e2, c2, T1, T2)

    # postprocess
    r = mapdl.result
    png_path = os.path.join(my_wdirnow, "tempname.png")
    r.plot_nodal_displacement(
        0,
        comp="Z",
        screenshot=png_path,
        interactive=False,
        show_displacement=True,
        overlay_wireframe=True,
        show_edges=True,
        add_text=False,
    )
    q = mapdl.queries
    tip_node = q.node(L, 0, 0)
    uz = q.uz(tip_node)
    # Exit
    mapdl.exit()

    # Update the csv file
    r = ""
    fields = [
        L,
        t,
        T1,
        T2,
        e1,
        c1,
        e2,
        c2,
        round(uz, 3),
        round(L / t, 2),
        round((T1 - T2), 2),
    ]
    data_file = os.path.join(os.getcwd(), "assets", "data.csv")
    with open(data_file, "a", newline="\n") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(fields)

    return [png_path, round(uz, 3)]


def my_mapdl_launch(my_job_name):
    """launch an mapdl instance"""

    mapdl = launch_mapdl(jobname=my_job_name, nproc=4, override=True)
    print("mapdl working directory : ", mapdl.directory)
    return mapdl, mapdl.directory


def solve_vm_35(
    mapdl, length, thickness, ex_mat1, cte_mat1, ex_mat2, cte_mat2, my_t_ref, my_t_amb
):
    """the mapdl run"""

    mapdl.clear("NOSTART")
    mapdl.prep7()
    mapdl.units("BIN")  # SI - International system (m, kg, s, K).
    mapdl.prep7()
    mapdl.title("VM35 BIMETALLIC LAYERED CANTILEVER PLATE WITH THERMAL LOADING")
    mapdl.antype("STATIC")
    mapdl.et(1, "SHELL281")
    mapdl.sectype(1, "SHELL")
    mapdl.secdata(thickness / 2, 1, 0)  # LAYER 1: 0.05 THICK, MAT'L 1, THETA 0
    mapdl.secdata(thickness / 2, 2, 0)  # LAYER 2: 0.05 THICK, MAT'L 2, THETA 0,
    mapdl.mp("EX", 1, ex_mat1)  # MATERIAL PROPERTIES
    mapdl.mp("EX", 2, ex_mat2)
    mapdl.mp("ALPX", 1, cte_mat1)
    mapdl.mp("ALPX", 2, cte_mat2)
    mapdl.mp("NUXY", 1, 0)
    mapdl.mp("NUXY", 2, 0)
    mapdl.n(1)  # DEFINE GEOMETRY
    mapdl.n(12, "", 1)
    mapdl.n(22, length, 1)
    mapdl.n(11, length)
    mapdl.fill(1, 11, 9, 2, 1)
    mapdl.fill(12, 22, 9, 13, 1)
    for ii in range(0, 6):
        mapdl.fill(ii * 2 + 1, (ii + 1) * 2 + 10, 1, ii + 23)
    for jj in range(0, 5):
        mapdl.e(
            jj * 2 + 1,
            (jj + 1) * 2 + 10,
            (jj + 1) * 2 + 12,
            jj * 2 + 3,
            jj + 23,
            jj * 2 + 13,
            jj + 24,
            jj * 2 + 2,
        )
    mapdl.nsel("S", "LOC", "X")
    mapdl.nsel("R", "LOC", "Y", 0.5)
    mapdl.d("ALL", "ALL")  # FIX ONE END OF CANTILEVER
    mapdl.nsel("S", "LOC", "Y", 0.5)
    mapdl.dsym("SYMM", "Y")  # SYMMETRY PLANE DOWN CENTERLINE
    mapdl.nsel("ALL")
    mapdl.tref(my_t_ref)
    mapdl.bfunif("TEMP", my_t_amb)  # DEFINE UNIFORM TEMPERATURE
    mapdl.finish()
    mapdl.run("/SOLU")
    mapdl.outpr("NSOL", 1)
    mapdl.outpr("RSOL", 1)
    mapdl.solve()


# Define Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.SIMPLEX],
    suppress_callback_exceptions=True,
)

# Other Themes from https://bootswatch.com/ that you can try : BOOTSTRAP, CERULEAN, COSMO, CYBORG etc.


# Define first part of Dash App : The  Layout
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "15rem",
    "padding": "2rem 1rem",
}

CONTENT_STYLE0 = {
    "margin-left": "12rem",
    "margin-right": "1rem",
    "padding": "2rem 1rem",
}

CONTENT_STYLE1 = {
    "margin-left": "6rem",
    "margin-right": "1rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("VM 35", className="display-4"),
        html.Hr(),
        html.P(
            "Bimetallic Layered Cantilever Plate with Thermal Loading", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Description", href="/", active="exact", id="description"),
                dbc.NavLink(
                    "Simulation", href="/page-1", active="exact", id="simulation"
                ),
                dbc.NavLink("Data", href="/page-2", active="exact", id="data"),
            ],
            vertical=True,
            pills=True,
            id="pages",
        ),
    ],
    style=SIDEBAR_STYLE,
)

# actual content goes into children later
content = html.Div(id="page-content", children=[], style=CONTENT_STYLE0)

# Build Page0 Layout
top_card1 = dbc.Card(
    [
        dbc.CardImg(src="/assets/input_image.png", top=True, className="card-body"),
        dbc.CardBody(html.P("")),
    ],
    style={"width": "36rem"},
)

top_card2 = dbc.Card(
    [
        dbc.CardBody(
            html.P(
                "A cantilever beam of length  L , width w, and thickness t is built from two equal thickness layers "
                "of different metals. "
                "The beam is stress free at Tref. The beam is fixed at the centerline of one end (X = 0, Y = w/2), "
                "and subjected to a uniform temperature Ta. "
                "Determine the deflection at the centerline of the free end (X =  ) of the cantilever and the outer "
                "fiber bending stress at the fixed end.",
                className="card-title",
            )
        ),
    ],
    style={"width": "36rem"},
)

mycontent_page0 = dbc.Row(
    [
        dbc.Col(top_card2, width="auto"),
        html.Br(),
        html.Br(),
        html.Br(),
        dbc.Col(top_card1, width="auto"),
    ],
    style=CONTENT_STYLE0,
)

# Build Page1 Layout
mycontent_page1 = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.H1(" Inputs ", className="text-center text-primary mb-4 "),
                    width=12,
                )
            ]
        ),
        dbc.Row(
            [
                # first column
                dbc.Col(
                    [
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("Length"),
                                dbc.Input(
                                    id="length",
                                    value="10",
                                    type="number",
                                    style={"textAlign": "center"},
                                ),
                                dbc.InputGroupText("in"),
                            ],
                            className="mb-3",
                        ),
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("Thickness"),
                                dbc.Input(
                                    id="thickness",
                                    value="0.1",
                                    type="number",
                                    style={"textAlign": "center"},
                                ),
                                dbc.InputGroupText("in"),
                            ],
                            className="mb-3",
                        ),
                        html.Br(),
                        dcc.Slider(
                            0,
                            200,
                            1,
                            value=70,
                            marks=None,
                            id="tref",
                            tooltip={"placement": "top", "always_visible": True},
                        ),
                        html.Br(),
                        dcc.Slider(
                            0,
                            200,
                            1,
                            value=170,
                            marks=None,
                            id="tamb",
                            tooltip={"placement": "bottom", "always_visible": True},
                            className="mb-6",
                        ),
                    ],
                    width=4,
                ),
                dbc.Col(
                    [
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("Tref (F)"),
                            ],
                            className="mb-1",
                        ),
                        html.Br(),
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("Tamb (F)"),
                            ],
                            className="mb-1",
                        ),
                    ]
                ),
                dbc.Col(
                    [
                        html.Br(),
                    ],
                ),
                dbc.Col(
                    [
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("Material1 - Young's Modulus"),
                                dbc.Input(
                                    id="e1",
                                    value="3e7",
                                    type="number",
                                    style={"textAlign": "center"},
                                ),
                                dbc.InputGroupText("psi"),
                            ],
                            className="mb-3",
                        ),
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("Material2 - Young's Modulus"),
                                dbc.Input(
                                    id="e2",
                                    value="3e7",
                                    type="number",
                                    style={"textAlign": "center"},
                                ),
                                dbc.InputGroupText("psi"),
                            ],
                            className="mb-3",
                        ),
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("Material1 - CTE"),
                                dbc.Input(
                                    id="c1",
                                    value="1e-5",
                                    type="number",
                                    style={"textAlign": "center"},
                                ),
                                dbc.InputGroupText("/degF"),
                            ],
                            className="mb-3",
                        ),
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("Material2 - CTE"),
                                dbc.Input(
                                    id="c2",
                                    value="2e-5",
                                    type="number",
                                    style={"textAlign": "center"},
                                ),
                                dbc.InputGroupText("/degF"),
                            ],
                            className="mb-3",
                        ),
                    ],
                    width=4,
                ),
                # blank  column, width 1 . column 4
                dbc.Col(html.H1("  "), width=1),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Button(
                            "Solve",
                            size="lg",
                            className="me-1 ",
                            id="input-group-button",
                            disabled=False,
                            n_clicks=0,
                        )
                    ],
                    className="d-grid gap-2 col-6 mx-auto",
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.H1(" Outputs", className="text-center text-primary mb-4 "),
                    width=12,
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [html.Br()],
                ),
            ]
        ),
        # ===============
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Spinner(
                            children=[
                                dbc.InputGroup(
                                    [
                                        dbc.InputGroupText("Free End Deflection"),
                                        dbc.Input(
                                            id="displacement",
                                            value={},
                                            type="number",
                                            disabled=True,
                                        ),
                                        dbc.InputGroupText("in"),
                                    ],
                                    className="mb-3",
                                )
                            ],
                            size="lg",
                            color="danger",
                            type="border",
                            fullscreen=False,
                            spinner_style={"width": "5rem", "height": "5rem"},
                        ),
                    ],
                    width=4,
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [html.Br(), html.Br(), html.Br()],
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Spinner(
                            children=[
                                dbc.Card(
                                    [
                                        html.Div(id="image-id"),
                                    ],
                                )
                            ],
                            size="lg",
                            color="success",
                            type="border",
                            fullscreen=False,
                            spinner_style={"width": "5rem", "height": "5rem"},
                        )
                    ],
                    width=12,
                ),
            ]
        ),
    ],
    style=CONTENT_STYLE1,
)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


def find_csv_file_and_create_df():
    """find the right file to populate page 2"""
    # find the right file
    default_file = os.path.join(os.getcwd(), "assets", "initial.csv")
    needed_file = os.path.join(os.getcwd(), "assets", "data.csv")
    needed_file_exists_check = os.path.exists(needed_file)

    if needed_file_exists_check:
        use_file = needed_file
    else:
        use_file = default_file
    df = pd.read_csv(use_file)
    return df


def open_browser():
    """Opens the app in default web browser"""
    webbrowser.open_new("http://127.0.0.1:8061/")


# When the page is loaded , it renders two different html pages
# for "description" and "simulation" sidebar pages

# Define second  part of Dash App : The  Callbacks
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return [html.H1("Description", style={"textAlign": "center"}), mycontent_page0]

    elif pathname == "/page-1":

        return [html.H1("Simulation", style={"textAlign": "center"}), mycontent_page1]

    elif pathname == "/page-2":
        df = find_csv_file_and_create_df()
        # data cleanup : remove duplicates and round the values
        df = df.drop_duplicates()
        df["LT_Ratio"] = df["Length"] / df["Thickness"]
        df["Temp_Diff"] = pd.Series.abs(df["Tref"] - df["Tamb"])
        df["LT_Ratio"] = df["LT_Ratio"].apply(lambda x: round(x, 2))
        df["Temp_Diff"] = df["Temp_Diff"].apply(lambda x: round(x, 2))
        df["abs_deflection"] = df["deflection"].abs()

        fig = px.scatter(
            df,
            x="Temp_Diff",
            y="abs_deflection",
            size="LT_Ratio",
            color="Thickness",
            template="plotly_dark",
            title=" Absolute Tip Deflection (size: LT_Ratio) ",
            color_continuous_scale=px.colors.sequential.Oryel,
        )
        mycontent_page2_2 = dcc.Graph(figure=fig)

        mycontent_page2_1 = dash_table.DataTable(
            data=df.to_dict("records"),
            columns=[{"name": i, "id": i} for i in df.columns],
            style_as_list_view=True,
            sort_action="native",
            column_selectable="single",
            style_cell={"padding": "5px"},
            style_header={
                "backgroundColor": "rgb(210, 210, 210)",
                "color": "black",
                "fontWeight": "bold",
                "text-align": "center",
            },
            style_data={
                "backgroundColor": "rgb(50, 50, 50)",
                "color": "white",
                "text-align": "center",
            },
            style_data_conditional=(
                [
                    {
                        "if": {
                            "filter_query": "{{Thickness}} = {}".format(i),
                            "column_id": "Thickness",
                        },
                        "backgroundColor": "#7FDBFF",
                        "color": "black",
                    }
                    for i in df["Thickness"].nsmallest(2)
                ]
                + [
                    {
                        "if": {
                            "filter_query": "{{abs_deflection}} = {}".format(i),
                            "column_id": "abs_deflection",
                        },
                        "backgroundColor": "#0074D9",
                        "color": "white",
                    }
                    for i in df["abs_deflection"].nlargest(2)
                ]
                + [
                    {
                        "if": {
                            "filter_query": "{{Length}} = {}".format(i),
                            "column_id": "Length",
                        },
                        "backgroundColor": "#0074D9",
                        "color": "white",
                    }
                    for i in df["Length"].nlargest(2)
                ]
                + [
                    {
                        "if": {
                            "filter_query": "{{LT_Ratio}} = {}".format(i),
                            "column_id": "LT_Ratio",
                        },
                        "backgroundColor": "#0074D9",
                        "color": "white",
                    }
                    for i in df["LT_Ratio"].nlargest(2)
                ]
                + [
                    {
                        "if": {
                            "filter_query": "{{Temp_Diff}} = {}".format(i),
                            "column_id": "Temp_Diff",
                        },
                        "backgroundColor": "#0074D9",
                        "color": "white",
                    }
                    for i in df["Temp_Diff"].nlargest(2)
                ]
            ),
        )

        mycontent_page2 = dbc.Container(
            [
                dbc.Row(
                    [
                        mycontent_page2_1,
                    ],
                    style=CONTENT_STYLE0,
                ),
                dbc.Row(
                    [
                        mycontent_page2_2,
                    ],
                    style=CONTENT_STYLE0,
                ),
            ]
        )

        return [html.H1("Data", style={"textAlign": "center"}), mycontent_page2]

    else:
        return None


# When Solve button is clicked ,
# the inputs are used to trigger the pyMapdl run
# the outputs are disp result and disp image
@app.callback(
    Output("displacement", "value"),
    Output("image-id", "children"),
    Input("length", "value"),
    Input("thickness", "value"),
    Input("tref", "value"),
    Input("tamb", "value"),
    Input("e1", "value"),
    Input("e2", "value"),
    Input("c1", "value"),
    Input("c2", "value"),
    Input("input-group-button", "n_clicks"),
)
def start_pymapdl(L, t, tr, ta, e1, e2, c1, c2, n_clicks):
    """enables multiple clicks on the solve button"""
    triggered = dash.callback_context.triggered
    triggered_id = triggered[0]["prop_id"].split(".")[0]
    if triggered_id == "input-group-button" and n_clicks > 0:
        p_run = pyMapdl_vm35(
            float(L),
            float(t),
            float(tr),
            float(ta),
            float(e1),
            float(e2),
            float(c1),
            float(c2),
        )
        print(".......Run Complete.......")
        image = ""
        shutil.move(p_run[0], FINAL_IMAGE_PATH)

        import time

        timestr = time.strftime("%Y%m%d-%H%M%S")
        newname = FINAL_IMAGE_PATH.split("/")[0] + r"/cyl_" + timestr + ".png"
        os.rename(FINAL_IMAGE_PATH, newname)

        image = FINAL_IMAGE_PATH
        usum = p_run[1]
        print(image)
        print(usum)
        print(n_clicks)
        return str(usum), dbc.CardImg(
            id="image_result", src=newname, className="card-body"
        )
    else:
        raise PreventUpdate


if __name__ == "__main__":
    Timer(1, open_browser).start()
    # Run the server that launches the app  :
    app.run_server(debug=False, port=8061)
