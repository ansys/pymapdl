"""Plotting helper for MAPDL using pyvista"""
from functools import wraps
import pyvista as pv
import numpy as np

from ansys.mapdl.core.misc import unique_rows, approximate_minimum_distance_between_points
from .theme import MapdlTheme


# Supported labels
BC_D = ['TEMP', 'UX', 'UY', 'UZ', 'VOLT', 'MAG']
BC_F = ['HEAT', 'FX', 'FY', 'FZ', 'AMPS', 'CHRGS', 'FLUX', 'CSGZ'] #TODO: Add moments MX, MY, MZ
FIELDS = ['MECHANICAL', 'THERMAL', 'ELECTRICAL']

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

VOLT = pv.Cube(center=(0, 0, 0),
                    x_length=1.0,
                    y_length=1.0,
                    z_length=1.0)


BC_plot_settings = {
    'TEMP': {
        'color': 'red',
        'arrow': TEMP
    },
    'UX': {
        'color': 'grey',
        'arrow': UX
    },
    'UY': {
        'color': 'grey',
        'arrow': UY
    },
    'UZ': {
        'color': 'grey',
        'arrow': UZ
    },
    'VOLT': {
        'color': 'yellow',
        'arrow': VOLT
    }
}

# Using * to force all the following arguments to be keyword only.
def _general_plotter(
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
    plot_BC = None,
    BC_labels = None,
    BC_target = None
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
    if title:
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
            returns_parameter = tuple(returns_parameter)

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


def general_plotter(*args, **kwargs):
    """Wraps the general plotter, to add BC plots."""

    mapdl = kwargs.get('mapdl', None)
    plot_BC = kwargs.get('plot_BC', False)
    BC_labels = kwargs.get('BC_labels', None)
    BC_target = kwargs.get('BC_target', ['NODES'])

    if not plot_BC:
        return _general_plotter(*args, **kwargs)

    # Getting the inputs values
    return_plotter = kwargs.get('return_plotter', False)
    return_cpos = kwargs.get('return_cpos', False)

    # Overwritting the return plotter
    kwargs['return_plotter'] = True

    # Getting the plotter
    pl, cpos = general_plotter(*args, **kwargs)

    pl = bc_plotter(pl, **kwargs)

    if not return_plotter and not return_cpos:
        return
    elif return_plotter and return_cpos:
        return pl, cpos
    else:
        return pl if return_plotter else cpos


def bc_plotter(pl, mapdl =None, BC_labels=None, BC_target=None, **kwargs):

    BC_labels = _bc_labels_checker(BC_labels)
    BC_target = _bc_target_checker(BC_target)

    # We need to scale the glyphs, otherwise, they will be plot sized 1.
    # We are going to calculate the distance between the closest points, so we will scaled to a percetange of this distance.
    # This might create very small points in cases there are a concentration of points.
    #
    # Later can find a way to plot them and keep their size constant independent of the zoom.

    min_dist = approximate_minimum_distance_between_points(mapdl.mesh.nodes)

    if not BC_labels:
        BC_labels = True

    if not BC_target:
        BC_target = ['NODES']

    if 'NODES' in BC_target:
        pl = bc_nodes_plotter(mapdl, pl, BC_labels, min_dist=min_dist)

    return pl


def bc_nodes_plotter(mapdl, pl, BC_labels, plot_labels=False, min_dist=1):
    """Plot nodes BC given a list of labels"""
    nodes_xyz = mapdl.mesh.nodes
    nodes_num = mapdl.mesh.nnum

    for each_label in BC_labels:
        if each_label in BC_D:
            bc = mapdl.get_nodal_constrains(each_label)

            bc_num = bc[:, 0].astype(int)
            bc_nodes = nodes_xyz[np.isin(nodes_num, bc_num), :]
            bc_values = bc[:, 1:]
            bc_scale = abs(bc_values[:, 0])

            if bc_scale.max() != bc_scale.min():
                bc_scale = (bc_scale - bc_scale.min()) / \
                    (bc_scale.max() - bc_scale.min())+0.5  # Normalization around 0.5
            else:
                bc_scale = np.ones(bc_scale.shape)*0.5  # In case all the values are the same

            pcloud = pv.PolyData(bc_nodes)
            pcloud["scale"] = bc_scale*min_dist

            glyphs = pcloud.glyph(scale="scale",
                                tolerance=0.05,
                                geom=BC_plot_settings[each_label]['arrow'])

            pl.add_mesh(
                glyphs, color=BC_plot_settings[each_label]['color'], style='surface')

            if plot_labels:
                bc_labels = [f"{id} ({each_label}: {values[0]:6.3f}, {values[1]:6.3f})" for id,
                        values in zip(bc_num, bc_values)]
                pcloud["labels"] = bc_labels
                pl.add_point_labels(pcloud.points, pcloud["labels"])

        elif each_label in BC_F:
            # To implement later
            raise Exception(f"The label '{each_label}' is not implemented yet.")
        else:
            raise Exception(f"The label '{each_label}' is not supported.")

    return pl


def _bc_labels_checker(BC_labels):
    """Make sure we have allowed parameters and data types for ``BC_labels``"""

    if not isinstance(BC_labels, (str, list, tuple)):
        raise ValueError("The parameter 'BC_labels' can be only a string, a list of strings or tuple of strings.")

    if isinstance(BC_labels, str):
        if BC_labels not in BCS or BC_labels not in FIELDS:
            raise ValueError(f"The parameter '{BC_labels}' in 'BC_labels' is not supported.\n"
                             "Please use any of the following:\n"
                             f"{FIELDS}\nor any combination of:\n{BCS}")
        BC_labels = [BC_labels.upper()]

    if isinstance(BC_labels, (list, tuple)):
        if not all([each.upper() in BCS for each in BC_labels]):
            raise ValueError("One or more parameters in 'BC_labels' are not supported.\n"
                             f"Please use any combination of the following:\n{BCS}")
        if not all([isinstance(each, str) for each in BC_labels]):
            raise ValueError("The parameter 'BC_labels' can be a list or tuple, but it should only contain strings inside them.")

        BC_labels = [each.upper() for each in BC_labels]

    return BC_labels


def _bc_target_checker(BC_target):
    """Make sure we have allowed parameters and data types for ``BC_labels``"""

    if not isinstance(BC_target, (str, list, tuple)):
        raise ValueError("The parameter 'BC_target' can be only a string, a list of strings or tuple of strings.")

    if isinstance(BC_target, str):
        if BC_target not in ALLOWED_TARGETS:
            raise ValueError(f"The parameter '{BC_target}' in 'BC_target' is not supported.\n"
                             f"At the moments only the following are supported:\n{ALLOWED_TARGETS}")
        BC_target = [BC_target.upper()]

    if isinstance(BC_target, (list, tuple)):
        if not all([each.upper() in ALLOWED_TARGETS for each in BC_target]):
            raise ValueError("One or more parameters in 'BC_target' are not supported.\n"
                             f"Please use any combination of the following:\n{ALLOWED_TARGETS}")
        if not all([isinstance(each, str) for each in BC_target]):
            raise ValueError("The parameter 'BC_target' can be a list or tuple, but it should only contain strings inside them.")

        BC_target = [each.upper() for each in BC_target]

    return BC_target
