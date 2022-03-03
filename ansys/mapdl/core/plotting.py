"""Plotting helper for MAPDL using pyvista"""
from functools import wraps
from stat import FILE_ATTRIBUTE_ARCHIVE
import pyvista as pv
import numpy as np

from ansys.mapdl.core.misc import unique_rows, approximate_minimum_distance_between_points, get_bounding_box
from .theme import MapdlTheme


# Supported labels
BC_D = ['TEMP', 'UX', 'UY', 'UZ', 'VOLT', 'MAG']
BC_F = ['HEAT', 'FX', 'FY', 'FZ', 'AMPS', 'CHRGS', 'FLUX', 'CSGZ'] #TODO: Add moments MX, MY, MZ
FIELDS = {
        'MECHANICAL': ['UX', 'UY', 'UZ', 'FX', 'FY', 'FZ'],
        'THERMAL': ['TEMP', 'FLUX'],
        'ELECTRICAL': ['VOLT', 'CHRGS']
        }




# All boundary conditions:
BCS = BC_D.copy()
BCS.extend(BC_F)

# Allowed entities to plot their boundary conditions
ALLOWED_TARGETS = ['NODES']

# Symbols for constrains
TEMP = pv.Sphere(center=(0, 0, 0),
                      radius=0.5)

UX = pv.Arrow(start=(-1, 0, 0),
                   direction=(1, 0, 0),
                   tip_length=1,
                   tip_radius=0.5,
                   scale=1.)
UY = pv.Arrow(start=(0, -1, 0),
                   direction=(0, 1, 0),
                   tip_length=1,
                   tip_radius=0.5,
                   scale=1.)

UZ = pv.Arrow(start=(0, 0, -1),
                   direction=(0, 0, 1),
                   tip_length=1,
                   tip_radius=0.5,
                   scale=1.)


FX = pv.Arrow(start=(-1, 0, 0),
                   direction=(1, 0, 0),
                   tip_length=0.5,
                   tip_radius=0.25,
                   scale=1.)
FY = pv.Arrow(start=(0, -1, 0),
                   direction=(0, 1, 0),
                   tip_length=0.5,
                   tip_radius=0.25,
                   scale=1.)

FZ = pv.Arrow(start=(0, 0, -1),
                   direction=(0, 0, 1),
                   tip_length=0.5,
                   tip_radius=0.25,
                   scale=1.)

def get_VOLT():
    model_a = pv.Cylinder(center=(0, 0, 0),
                    direction=(1, 0, 0),
                    radius=0.2,
                    height=2).triangulate()

    model_b = pv.Cylinder(center=(0, 0, 0),
                    direction=(0, 1, 0),
                    radius=0.2,
                    height=2).triangulate()

    model_c = pv.Cylinder(center=(0, 0, 0),
                    direction=(0, 0, 1),
                    radius=0.2,
                    height=2).triangulate()

    result = model_a.merge(model_b).triangulate()
    result = result.merge(model_c)

    result.rotate_z(45.0, inplace=True)
    result.rotate_vector(vector=(1, -1, 0), angle=-45, point=(0, 0, 0), inplace=True)

    return result

VOLT = get_VOLT()


HEAT = pv.Cube(center=(0, 0, 0),
                    x_length=1.0,
                    y_length=1.0,
                    z_length=1.0)

BC_plot_settings = {
    'TEMP': {
        'color': 'orange',
        'glyph': TEMP
    },
    'HEAT': {
        'color': 'red',
        'glyph': HEAT
    },
    'UX': {
        'color': 'red',
        'glyph': UX
    },
    'UY': {
        'color': 'green',
        'glyph': UY
    },
    'UZ': {
        'color': 'blue',
        'glyph': UZ
    },
    'VOLT': {
        'color': 'yellow',
        'glyph': VOLT
    },
    'FX': {
        'color': 'red',
        'glyph': FX
    },
    'FY': {
        'color': 'green',
        'glyph': FY
    },
    'FZ': {
        'color': 'blue',
        'glyph': FZ
    },
}

# Using * to force all the following arguments to be keyword only.
def _general_plotter(
    meshes,
    points,
    labels,
    *,
    cpos=None,
    show_bounds=False,
    show_axes=True,
    background=None,
    off_screen=None,
    notebook=None,
    # add_mesh kwargs:
    style=None,
    color="w",
    show_edges=None,
    edge_color=None,
    point_size=5.0,
    line_width=None,
    opacity=1.0,
    flip_scalars=False,
    lighting=None,
    n_colors=256,
    interpolate_before_map=True,
    cmap=None,
    render_points_as_spheres=False,
    render_lines_as_tubes=False,
    scalar_bar_args={},
    smooth_shading=None,
    show_scalar_bar=None,
    # labels kwargs
    font_size=None,
    font_family=None,
    text_color=None,
    theme=None
):
    """General pymapdl plotter for APDL geometry and meshes.

    Parameters
    ----------
    title : str, optional
        Add given title to plot.

    cpos : list(tuple(floats)), str
        The camera position to use.  You can either use a saved camera
        position or specify one of the following strings:

        - ``"xy"``
        - ``"xz"``
        - ``"yz"``
        - ``"yx"``
        - ``"zx"``
        - ``"zy"``
        - ``"iso"``

    off_screen : bool, optional
        Renders off screen when ``True``.  Useful for automated
        screenshots.

    window_size : list, optional
        Window size in pixels.  Defaults to ``[1024, 768]``

    notebook : bool, optional
        When True, the resulting plot is placed inline a jupyter
        notebook.  Assumes a jupyter console is active.  Automatically
        enables off_screen.

    show_bounds : bool, optional
        Shows mesh bounds when ``True``.

    show_axes : bool, optional
        Shows a vtk axes widget.  Enabled by default.

    savefig : str, optional
        Saves screenshot to a file path.

    style : string, optional
        Visualization style of the mesh.  One of the following:
        ``style='surface'``, ``style='wireframe'``,
        ``style='points'``.  Defaults to ``'surface'``. Note that
        ``'wireframe'`` only shows a wireframe of the outer geometry.

    color : string or 3 item list, optional
        Use to make the entire mesh have a single solid color.  Either
        a string, RGB list, or hex color string.  For example:
        ``color='white'``, ``color='w'``, ``color=[1, 1, 1]``, or
        ``color='#FFFFFF'``. Color will be overridden if scalars are
        specified.

    show_edges : bool, optional
        Shows the edges of a mesh.  Does not apply to a wireframe
        representation.

    edge_color : string or 3 item list, optional, defaults to black
        The solid color to give the edges when ``show_edges=True``.
        Either a string, RGB list, or hex color string.

    point_size : float, optional
        Point size of any nodes in the dataset plotted. Also applicable
        when style='points'. Default ``5.0``

    line_width : float, optional
        Thickness of lines.  Only valid for wireframe and surface
        representations.  Default None.

    opacity : float, str, array-like
        Opacity of the mesh. If a single float value is given, it will be
        the global opacity of the mesh and uniformly applied everywhere -
        should be between 0 and 1. A string can also be specified to map
        the scalars range to a predefined opacity transfer function
        (options include: 'linear', 'linear_r', 'geom', 'geom_r').
        A string could also be used to map a scalars array from the mesh to
        the opacity (must have same number of elements as the
        ``scalars`` argument). Or you can pass a custom made transfer
        function that is an array either ``n_colors`` in length or shorter.

    n_colors : int, optional
        Number of colors to use when displaying scalars. Defaults to 256.
        The scalar bar will also have this many colors.

    cmap : str, list, optional
       Name of the Matplotlib colormap to us when mapping the
       ``scalars``.  See available Matplotlib colormaps.  Only
       applicable for when displaying ``scalars``. Requires Matplotlib
       to be installed.  ``colormap`` is also an accepted alias for
       this. If ``colorcet`` or ``cmocean`` are installed, their
       colormaps can be specified by name.

        You can also specify a list of colors to override an
        existing colormap with a custom one.  For example, to
        create a three color colormap you might specify
        ``['green', 'red', 'blue']``

    render_points_as_spheres : bool, optional
        Render points as spheres.

    render_lines_as_tubes : bool, optional
        Renders lines as tubes.

    smooth_shading : bool, optional
        Smoothly render curved surfaces when plotting.  Not helpful
        for all meshes.

    theme : pyvista.DefaultTheme, optional
        PyVista theme.  Defaults to PyMAPDL theme.

    Returns
    -------
    pyvista.Plotter
        Instance of ``pyvista.Plotter``.

    Examples
    --------
    Plot areas and modify the background color to ``'black'``

    >>> p = mapdl.aplot(background='black')

    Enable smooth_shading on an element plot.

    >>> p = mapdl.eplot(smooth_shading=True)

    Return the plotting instance, modify it, and display the plot.

    >>> pl = mapdl.aplot()
    >>> pl.show_bounds()
    >>> pl.set_background('black')
    >>> pl.add_text('my text')
    >>> pl.show()

    Save a screenshot to disk without showing the plot.

    >>> mapdl.eplot(background='w', show_edges=True, smooth_shading=True,
                    window_size=[1920, 1080], savefig='screenshot.png',
                    off_screen=True)

    """
    if notebook:
        off_screen = True

    if theme is None:
        theme = MapdlTheme()

    pl = pv.Plotter(off_screen=off_screen, notebook=notebook, theme=theme)

    if background:
        pl.set_background(background)

    for point in points:
        pl.add_points(
            point["points"],
            scalars=point.get("scalars", None),
            color=color,
            show_edges=show_edges,
            edge_color=edge_color,
            point_size=point_size,
            line_width=line_width,
            opacity=opacity,
            flip_scalars=flip_scalars,
            lighting=lighting,
            n_colors=n_colors,
            interpolate_before_map=interpolate_before_map,
            cmap=cmap,
            render_points_as_spheres=render_points_as_spheres,
            render_lines_as_tubes=render_lines_as_tubes,
        )

    for mesh in meshes:
        pl.add_mesh(
            mesh["mesh"],
            scalars=mesh.get("scalars"),
            scalar_bar_args=scalar_bar_args,
            color=mesh.get("color", color),
            style=mesh.get("style", style),
            show_edges=show_edges,
            edge_color=edge_color,
            smooth_shading=smooth_shading,
            point_size=point_size,
            line_width=line_width,
            show_scalar_bar=show_scalar_bar,
            opacity=opacity,
            flip_scalars=flip_scalars,
            lighting=lighting,
            n_colors=n_colors,
            interpolate_before_map=interpolate_before_map,
            cmap=cmap,
            render_points_as_spheres=render_points_as_spheres,
            render_lines_as_tubes=render_lines_as_tubes,
        )

    for label in labels:
        # verify points are not duplicates
        points, idx, _ = unique_rows(np.array(label["points"]))
        labels = np.array(label["labels"])[idx].tolist()

        pl.add_point_labels(
            points,
            labels,
            show_points=False,
            shadow=False,
            font_size=font_size,
            font_family=font_family,
            text_color=text_color,
        )

    if cpos:
        pl.camera_position = cpos

    if show_bounds:
        pl.show_bounds()

    if show_axes:
        pl.show_axes()

    return pl

# Using * to force all the following arguments to be keyword only.
def general_plotter(
        meshes,
        points,
        labels,
        *,
        title="",
        cpos=None,
        show_bounds=False,
        show_axes=True,
        background=None,
        off_screen=None,
        savefig=None,
        window_size=None,
        notebook=None,
        # add_mesh kwargs:
        style=None,
        color="w",
        show_edges=None,
        edge_color=None,
        point_size=5.0,
        line_width=None,
        opacity=1.0,
        flip_scalars=False,
        lighting=None,
        n_colors=256,
        interpolate_before_map=True,
        cmap=None,
        render_points_as_spheres=False,
        render_lines_as_tubes=False,
        scalar_bar_args={},
        smooth_shading=None,
        show_scalar_bar=None,
        # labels kwargs
        font_size=None,
        font_family=None,
        text_color=None,
        theme=None,
        return_plotter=False,
        return_cpos=False,
        mapdl=None,
        plot_bc = False,
        plot_bc_legend=None,
        plot_labels=None,
        bc_labels = None,
        bc_target = None
        ):
    """General pymapdl plotter for APDL geometry and meshes.

    Parameters
    ----------
    title : str, optional
        Add given title to plot.

    cpos : list(tuple(floats)), str
        The camera position to use.  You can either use a saved camera
        position or specify one of the following strings:

        - ``"xy"``
        - ``"xz"``
        - ``"yz"``
        - ``"yx"``
        - ``"zx"``
        - ``"zy"``
        - ``"iso"``

    off_screen : bool, optional
        Renders off screen when ``True``.  Useful for automated
        screenshots.

    window_size : list, optional
        Window size in pixels.  Defaults to ``[1024, 768]``

    notebook : bool, optional
        When True, the resulting plot is placed inline a jupyter
        notebook.  Assumes a jupyter console is active.  Automatically
        enables off_screen.

    show_bounds : bool, optional
        Shows mesh bounds when ``True``.

    show_axes : bool, optional
        Shows a vtk axes widget.  Enabled by default.

    savefig : str, optional
        Saves screenshot to a file path.

    style : string, optional
        Visualization style of the mesh.  One of the following:
        ``style='surface'``, ``style='wireframe'``,
        ``style='points'``.  Defaults to ``'surface'``. Note that
        ``'wireframe'`` only shows a wireframe of the outer geometry.

    color : string or 3 item list, optional
        Use to make the entire mesh have a single solid color.  Either
        a string, RGB list, or hex color string.  For example:
        ``color='white'``, ``color='w'``, ``color=[1, 1, 1]``, or
        ``color='#FFFFFF'``. Color will be overridden if scalars are
        specified.

    show_edges : bool, optional
        Shows the edges of a mesh.  Does not apply to a wireframe
        representation.

    edge_color : string or 3 item list, optional, defaults to black
        The solid color to give the edges when ``show_edges=True``.
        Either a string, RGB list, or hex color string.

    point_size : float, optional
        Point size of any nodes in the dataset plotted. Also applicable
        when style='points'. Default ``5.0``

    line_width : float, optional
        Thickness of lines.  Only valid for wireframe and surface
        representations.  Default None.

    opacity : float, str, array-like
        Opacity of the mesh. If a single float value is given, it will be
        the global opacity of the mesh and uniformly applied everywhere -
        should be between 0 and 1. A string can also be specified to map
        the scalars range to a predefined opacity transfer function
        (options include: 'linear', 'linear_r', 'geom', 'geom_r').
        A string could also be used to map a scalars array from the mesh to
        the opacity (must have same number of elements as the
        ``scalars`` argument). Or you can pass a custom made transfer
        function that is an array either ``n_colors`` in length or shorter.

    n_colors : int, optional
        Number of colors to use when displaying scalars. Defaults to 256.
        The scalar bar will also have this many colors.

    cmap : str, list, optional
       Name of the Matplotlib colormap to us when mapping the
       ``scalars``.  See available Matplotlib colormaps.  Only
       applicable for when displaying ``scalars``. Requires Matplotlib
       to be installed.  ``colormap`` is also an accepted alias for
       this. If ``colorcet`` or ``cmocean`` are installed, their
       colormaps can be specified by name.

        You can also specify a list of colors to override an
        existing colormap with a custom one.  For example, to
        create a three color colormap you might specify
        ``['green', 'red', 'blue']``

    render_points_as_spheres : bool, optional
        Render points as spheres.

    render_lines_as_tubes : bool, optional
        Renders lines as tubes.

    smooth_shading : bool, optional
        Smoothly render curved surfaces when plotting.  Not helpful
        for all meshes.

    theme : pyvista.DefaultTheme, optional
        PyVista theme.  Defaults to PyMAPDL theme.

    return_plotter : bool, optional
        Return the plotting object rather than showing the plot and
        returning the camera position.  Default ``False``.

    return_cpos : bool, optional
        Returns the camera position as an array. Default ``False``.

    Returns
    -------
    cpos or pyvista.Plotter
        Camera position or instance of ``pyvista.Plotter`` depending
        on ``return_plotter``.

    Examples
    --------
    Plot areas and modify the background color to ``'black'``

    >>> cpos = mapdl.aplot(background='black')

    Enable smooth_shading on an element plot.

    >>> cpos = mapdl.eplot(smooth_shading=True)

    Return the plotting instance, modify it, and display the plot.

    >>> pl = mapdl.aplot(return_plotter=True)
    >>> pl.show_bounds()
    >>> pl.set_background('black')
    >>> pl.add_text('my text')
    >>> pl.show()

    Save a screenshot to disk without showing the plot.

    >>> mapdl.eplot(background='w', show_edges=True, smooth_shading=True,
                    window_size=[1920, 1080], savefig='screenshot.png',
                    off_screen=True)

    """

    # Getting the plotter
    pl = _general_plotter(meshes,
        points,
        labels,
        cpos=cpos,
        show_bounds=show_bounds,
        show_axes=show_axes,
        background=background,
        off_screen=off_screen,
        notebook=notebook,
        # add_mesh kwargs:
        style=style,
        color=color,
        show_edges=show_edges,
        edge_color=edge_color,
        point_size=point_size,
        line_width=line_width,
        opacity=opacity,
        flip_scalars=flip_scalars,
        lighting=lighting,
        n_colors=n_colors,
        interpolate_before_map=interpolate_before_map,
        cmap=cmap,
        render_points_as_spheres=render_points_as_spheres,
        render_lines_as_tubes=render_lines_as_tubes,
        scalar_bar_args=scalar_bar_args,
        smooth_shading=smooth_shading,
        show_scalar_bar=show_scalar_bar,
        # labels kwargs
        font_size=font_size,
        font_family=font_family,
        text_color=text_color,
        theme=theme)

    if plot_bc:
        if not mapdl:
            raise ValueError("An instance of `ansys.mapdl.core.mapdl._MapdlCore` "
                             "should be passed using `mapdl` keyword if you are aiming "
                             "to plot the boundary conditions (`plot_bc` is `True`).")
        pl = bc_plotter(pl,
                        mapdl=mapdl,
                        plot_bc_legend=plot_bc_legend,
                        plot_labels=plot_labels,
                        bc_labels=bc_labels,
                        bc_target=bc_target)

    if title:  #Added here to avoid labels overlapping title
        pl.add_title(title)

    returns_parameter = []
    if return_plotter:
        returns_parameter.append(pl)
    if return_cpos:
        returns_parameter.append(pl.camera_position)

    if not returns_parameter:
        returns_parameter = None
    else:
        if len(returns_parameter) == 1:
            returns_parameter = returns_parameter[0]
        else:
            returns_parameter = tuple(returns_parameter)  # We should return a tuple if possible.

    # permit user to save the figure as a screenshot
    if savefig:
        pl.show(title=title, auto_close=False, window_size=window_size, screenshot=True)
        pl.screenshot(savefig)

        # return unclosed plotter
        if return_plotter:
            return returns_parameter

        # if not returning plotter, close right away
        pl.close()

    elif return_plotter:
        return returns_parameter
    else:
        pl.show()

    return returns_parameter


def bc_plotter(pl,
               mapdl =None,
               bc_labels=None,
               bc_target=None,
               plot_labels=False,
               plot_bc_legend=None
               ):

    if bc_labels:
        bc_labels = _bc_labels_checker(bc_labels)
    else:
        bc_labels = _bc_labels_default(mapdl)

    if bc_target:
        bc_target = _bc_target_checker(bc_target)
    else:
        bc_target = ['NODES']  # bc_target_default()

    # We need to scale the glyphs, otherwise, they will be plot sized 1.
    # We are going to calculate the distance between the closest points,
    # so we will scaled to a percentage of this distance.
    # This might create very small points in cases there are a concentration of points.
    #
    # Later can find a way to plot them and keep their size constant independent of the zoom.

    # min_dist = approximate_minimum_distance_between_points(mapdl.mesh.nodes)
    # min_dist = 0.00001
    min_dist = get_bounding_box(mapdl.mesh.nodes)
    min_dist = min_dist[min_dist != 0].mean()*0.75/10

    if 'NODES' in bc_target:
        pl = bc_nodes_plotter(mapdl, pl, bc_labels, 
                              plot_labels=plot_labels,
                              min_dist=min_dist,
                              plot_bc_legend=plot_bc_legend)

    return pl


def bc_nodes_plotter(mapdl, pl, bc_labels,
                     plot_labels=False,
                     min_dist=1,
                     plot_bc_legend=None):
    """Plot nodes BC given a list of labels"""
    nodes_xyz = mapdl.mesh.nodes
    nodes_num = mapdl.mesh.nnum

    bc_point_labels = None

    for each_label in bc_labels:
        if each_label in BC_D:
            bc = mapdl.get_nodal_constrains(each_label)

        elif each_label in BC_F:
            bc = mapdl.get_nodal_loads(each_label)

        else:
            raise Exception(f"The label '{each_label}' is not supported.")

        bc_num = bc[:, 0].astype(int)
        bc_nodes = nodes_xyz[np.isin(nodes_num, bc_num), :]
        bc_values = bc[:, 1:].astype(float)
        bc_scale = abs(bc_values[:, 0])

        if bc_scale.max() != bc_scale.min():
            bc_scale = (bc_scale - bc_scale.min()) / \
                (bc_scale.max() - bc_scale.min())+0.5  # Normalization around 0.5
        else:
            bc_scale = np.ones(bc_scale.shape)*0.5  # In case all the values are the same

        pcloud = pv.PolyData(bc_nodes)
        pcloud["scale"] = bc_scale*min_dist

        # Specify tolerance in terms of fraction of bounding box length.
        # Float value is between 0 and 1. Default is None.
        # If absolute is True then the tolerance can be an absolute distance.
        # If None, points merging as a preprocessing step is disabled.
        glyphs = pcloud.glyph(scale="scale",
                            # tolerance=0.05,
                            geom=BC_plot_settings[each_label]['glyph'])
        name_ = f"{each_label}"
        pl.add_mesh(
            glyphs,
            color=BC_plot_settings[each_label]['color'],
            style='surface',
            # style='wireframe',
            # edge_color=BC_plot_settings[each_label]['color'],
            # line_width=3,
            name = name_,
            label=name_)

        if plot_labels:
            if bc_point_labels is None:
                bc_point_labels = {each: '' for each in nodes_num}

            for id, values in zip(bc_num, bc_values):
                if not bc_point_labels[id]:
                    bc_point_labels[id] = f"Node: {id}\n{each_label}: {values[0]:6.3f}, {values[1]:6.3f}"
                else:
                    bc_point_labels[id] = f"{bc_point_labels[id]}\n{each_label}: {values[0]:6.3f}, {values[1]:6.3f}"

    if plot_labels:
        pcloud = pv.PolyData(nodes_xyz)
        pcloud["labels"] = list(bc_point_labels.values())
        pl.add_point_labels(pcloud.points, pcloud["labels"],
                            shape_opacity=0.25)

    if plot_bc_legend:
        pl.add_legend(bcolor=None)

    return pl


def _bc_labels_checker(bc_labels):
    """Make sure we have allowed parameters and data types for ``bc_labels``"""

    if not isinstance(bc_labels, (str, list, tuple)):
        raise ValueError("The parameter 'bc_labels' can be only a string, a list of strings or tuple of strings.")

    if isinstance(bc_labels, str):
        bc_labels = bc_labels.upper()
        if bc_labels not in BCS and bc_labels not in FIELDS:
            raise ValueError(f"The parameter '{bc_labels}' in 'bc_labels' is not supported.\n"
                             "Please use any of the following:\n"
                             f"{FIELDS}\nor any combination of:\n{BCS}")
        bc_labels = [bc_labels]

    elif isinstance(bc_labels, (list, tuple)):
        if not all([isinstance(each, str) for each in bc_labels]):
            raise ValueError("The parameter 'bc_labels' can be a list or tuple, but it should only contain strings inside them.")

        if not all([each.upper() in BCS for each in bc_labels]):
            raise ValueError(f"One or more parameters in 'bc_labels'({bc_labels}) are not supported.\n"
                             f"Please use any combination of the following:\n{BCS}")

        bc_labels = [each.upper() for each in set(bc_labels)]  # Removing duplicates too

    # Replacing field by equivalent fields.
    for each_field in FIELDS:
        if each_field in bc_labels:
            bc_labels.remove(each_field)
            bc_labels.extend(FIELDS[each_field])

    return bc_labels


def _bc_target_checker(bc_target):
    """Make sure we have allowed parameters and data types for ``bc_labels``"""

    if not isinstance(bc_target, (str, list, tuple)):
        raise ValueError("The parameter 'bc_target' can be only a string, a list of strings or tuple of strings.")

    if isinstance(bc_target, str):
        if bc_target not in ALLOWED_TARGETS:
            raise ValueError(f"The parameter '{bc_target}' in 'bc_target' is not supported.\n"
                             f"At the moments only the following are supported:\n{ALLOWED_TARGETS}")
        bc_target = [bc_target.upper()]

    if isinstance(bc_target, (list, tuple)):
        if not all([each.upper() in ALLOWED_TARGETS for each in bc_target]):
            raise ValueError("One or more parameters in 'bc_target' are not supported.\n"
                             f"Please use any combination of the following:\n{ALLOWED_TARGETS}")
        if not all([isinstance(each, str) for each in bc_target]):
            raise ValueError("The parameter 'bc_target' can be a list or tuple, but it should only contain strings inside them.")

        bc_target = [each.upper() for each in bc_target]

    return bc_target

def _bc_labels_default(mapdl):
    """Get the labels from the MAPDL database."""
    flist = list(set([each[1].upper() for each in mapdl.get_nodal_loads() if each[1].upper() in BCS]))
    dlist = list(set([each[1].upper() for each in mapdl.get_nodal_constrains() if each[1].upper() in BCS]))
    return flist + dlist
