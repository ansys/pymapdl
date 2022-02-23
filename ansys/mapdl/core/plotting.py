"""Plotting helper for MAPDL using pyvista"""
import pyvista as pv
import numpy as np

from ansys.mapdl.core.misc import unique_rows
from .theme import MapdlTheme


def general_plotter(
    meshes,
    points,
    labels,
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
    split_sharp_edges=None,
    feature_angle=30.0,
    show_scalar_bar=None,
    # labels kwargs
    font_size=None,
    font_family=None,
    text_color=None,
    theme=None,
    return_plotter=False,
    return_cpos=False,
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

    split_sharp_edge : bool, optional
        Split sharp edges exceeding 30 degrees when plotting with
        smooth shading.  Control the angle with the optional
        keyword argument ``feature_angle``.
        By default this is ``False``.

        .. note:: Note that enabling this will create a copy of
        the input mesh within the plotter.

    feature_angle : float, optional
        Angle to consider an edge a sharp edge. Default 30 degrees.

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
            split_sharp_edges=split_sharp_edges,
            feature_angle=feature_angle,
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

    def return_from_plotter():
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
        return returns_parameter

    returns_parameter = return_from_plotter()

    # permit user to save the figure as a screenshot
    if savefig:
        pl.show(title=title, auto_close=False, window_size=window_size, screenshot=True)
        pl.screenshot(savefig)

        # return unclosed plotter
        if returns_parameter:
            return returns_parameter

        # if not returning plotter, close right away
        pl.close()

    else:
        pl.show()

    # Recreating "returns" to update cpos
    returns_parameter = return_from_plotter()

    return returns_parameter
