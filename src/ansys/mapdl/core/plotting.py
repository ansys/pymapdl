"""Plotting helper for MAPDL using pyvista"""
from warnings import warn

import numpy as np

from ansys.mapdl.core import _HAS_PYVISTA
from ansys.mapdl.core.misc import get_bounding_box, unique_rows

from .theme import MapdlTheme

# Supported labels
BC_D = [
    "TEMP",
    "UX",
    "UY",
    "UZ",
    "VOLT",  # "MAG"
]
BC_F = [
    "HEAT",
    "FX",
    "FY",
    "FZ",
    "AMPS",
    "CHRGS",
    # "FLUX",
    "CSGZ",
]  # TODO: Add moments MX, MY, MZ
FIELDS = {
    "MECHANICAL": ["UX", "UY", "UZ", "FX", "FY", "FZ"],
    "THERMAL": ["TEMP", "HEAT"],
    "ELECTRICAL": ["VOLT", "CHRGS", "AMPS"],
}


# All boundary conditions:
BCS = BC_D.copy()
BCS.extend(BC_F)

# Allowed entities to plot their boundary conditions
ALLOWED_TARGETS = ["NODES"]


if _HAS_PYVISTA:
    import pyvista as pv

    # Symbols for constrains
    TEMP = pv.Sphere(center=(0, 0, 0), radius=0.5)

    UX = pv.Arrow(
        start=(-1, 0, 0),
        direction=(1, 0, 0),
        tip_length=1,
        tip_radius=0.5,
        scale=1.0,
    )
    UY = pv.Arrow(
        start=(0, -1, 0),
        direction=(0, 1, 0),
        tip_length=1,
        tip_radius=0.5,
        scale=1.0,
    )

    UZ = pv.Arrow(
        start=(0, 0, -1),
        direction=(0, 0, 1),
        tip_length=1,
        tip_radius=0.5,
        scale=1.0,
    )

    FX = pv.Arrow(
        start=(-1, 0, 0),
        direction=(1, 0, 0),
        tip_length=0.5,
        tip_radius=0.25,
        scale=1.0,
    )
    FY = pv.Arrow(
        start=(0, -1, 0),
        direction=(0, 1, 0),
        tip_length=0.5,
        tip_radius=0.25,
        scale=1.0,
    )

    FZ = pv.Arrow(
        start=(0, 0, -1),
        direction=(0, 0, 1),
        tip_length=0.5,
        tip_radius=0.25,
        scale=1.0,
    )

    def get_VOLT():
        model_a = pv.Cylinder(
            center=(0, 0, 0), direction=(1, 0, 0), radius=0.2, height=2
        ).triangulate()

        model_b = pv.Cylinder(
            center=(0, 0, 0), direction=(0, 1, 0), radius=0.2, height=2
        ).triangulate()

        model_c = pv.Cylinder(
            center=(0, 0, 0), direction=(0, 0, 1), radius=0.2, height=2
        ).triangulate()

        result = model_a.merge(model_b).triangulate()
        result = result.merge(model_c)

        result.rotate_z(45.0, inplace=True)
        result.rotate_vector(
            vector=(1, -1, 0), angle=-45, point=(0, 0, 0), inplace=True
        )

        return result

    VOLT = get_VOLT()

    HEAT = pv.Cube(center=(0, 0, 0), x_length=1.0, y_length=1.0, z_length=1.0)

    BC_plot_settings = {
        "TEMP": {"color": "orange", "glyph": TEMP},
        "HEAT": {"color": "red", "glyph": HEAT},
        "UX": {"color": "red", "glyph": UX},
        "UY": {"color": "green", "glyph": UY},
        "UZ": {"color": "blue", "glyph": UZ},
        "VOLT": {"color": "yellow", "glyph": VOLT},
        "FX": {"color": "red", "glyph": FX},
        "FY": {"color": "green", "glyph": FY},
        "FZ": {"color": "blue", "glyph": FZ},
        "AMPS": {"color": "grey", "glyph": VOLT},
        "CHRGS": {"color": "grey", "glyph": VOLT},
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
    feature_angle=30.0,
    show_scalar_bar=None,
    split_sharp_edges=None,
    # labels kwargs
    font_size=None,
    font_family=None,
    text_color=None,
    theme=None,
    plotter=None,
    add_points_kwargs={},
    add_mesh_kwargs={},
    add_point_labels_kwargs={},
    plotter_kwargs={},
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
        enables ``off_screen``.

    show_bounds : bool, optional
        Shows mesh bounds when ``True``.

    show_axes : bool, optional
        Shows a vtk axes widget.  Enabled by default.

    savefig : str, optional
        Saves screenshot to a file path. If used, ``notebook`` and
        ``off_screen`` are evaluated to ``False`` and ``True``
        respectively.

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
        when ``style='points'``. Default ``5.0``

    line_width : float, optional
        Thickness of lines.  Only valid for wireframe and surface
        representations.  Default None.

    opacity : float, str, array-like
        Opacity of the mesh. If a single float value is given, it will be
        the global opacity of the mesh and uniformly applied everywhere
        should be between 0 and 1. A string can also be specified to map
        the scalars range to a predefined opacity transfer function
        (options include: ``'linear'``, ``'linear_r'``, ``'geom'``, or
        ``'geom_r'``).
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

    split_sharp_edges : bool, optional
        Split sharp edges exceeding 30 degrees when plotting with
        smooth shading.  Control the angle with the optional
        keyword argument ``feature_angle``.
        By default this is ``False``.

        .. note:: Note that enabling this will create a copy of
           the input mesh within the plotter.

    feature_angle : float, optional
        Angle to consider an edge a sharp edge. Default 30 degrees.

    theme : pyvista.DefaultTheme, optional
        PyVista theme. Defaults to `PyMAPDL theme <https://github
        .com/pyansys/pyansys-sphinx-theme>`_.

    plotter : pyvista.Plotter, optional
        If a :class:`pyvista.Plotter` not is provided, then creates its
        own plotter. If a :class:`pyvista.Plotter` is provided, the arguments
        ``notebook``, ``off_screen`` and ``theme`` are ignored, since
        they should be set when instantiated the provided plotter.
        Defaults to ``None`` (create the Plotter object).

    add_points_kwargs : dict
        This is a dict which is passed to all calls to
        :meth:`pyvista.Plotter.add_points` in
        :func:`ansys.mapdl.core.plotting.general_plotter`.
        This pyvista method is used to plot nodes for example.
        See examples section to learn more about its usage.

    add_mesh_kwargs : dict
        This is a dict which is passed to all calls to
        :meth:`pyvista.Plotter.add_mesh` in
        :func:`ansys.mapdl.core.plotting.general_plotter`.
        This pyvista method is used to plot elements for example.
        See examples section to learn more about its usage.

    add_point_labels_kwargs : dict
        This is a dict which is passed to all calls to
        :meth:`pyvista.Plotter.add_point_labels` in
        :func:`ansys.mapdl.core.plotting.general_plotter`.
        This pyvista method is used to plot node labels for example.
        See examples section to learn more about its usage.

    plotter_kwargs : dict
        This is a dict which is passed to the :class:`pyvista.Plotter`
        initializer in :func:`ansys.mapdl.core.plotting.general_plotter`.
        This pyvista class is used in all PyMAPDL plots.
        See examples section to learn more about its usage.

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

    Using ``add_mesh_kwargs`` to pass other arguments to ``add_mesh`` pyvista method.

    >>> mapdl.eplot(background='w', show_edges=True, add_mesh_kwargs = {"use_transparency": False})

    Using ``plotter_kwargs`` to pass other arguments to ``Plotter`` constructor.

    >>> mapdl.eplot(background='w', show_edges=True, plotter_kwargs = {"polygon_smoothing": False})

    """
    # Lazy import
    import pyvista as pv

    if theme is None:
        theme = MapdlTheme()

    if not (plotter is None or isinstance(plotter, pv.Plotter)):
        raise TypeError("The kwarg 'plotter' can only accept pv.Plotter objects.")

    if not plotter:
        plotter = pv.Plotter(
            off_screen=off_screen, notebook=notebook, theme=theme, **plotter_kwargs
        )
    else:
        if off_screen or notebook or theme:
            warn(
                "The kwargs 'off_screen', 'notebook' and 'theme' are ignored when using 'plotter' kwarg.",
                UserWarning,
            )

    if background:
        plotter.set_background(background)

    for point in points:
        plotter.add_points(
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
            **add_points_kwargs,
        )

    for mesh in meshes:
        plotter.add_mesh(
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
            **add_mesh_kwargs,
        )

    for label in labels:
        # verify points are not duplicates
        points, idx, _ = unique_rows(np.array(label["points"]))
        labels = np.array(label["labels"])[idx].tolist()

        plotter.add_point_labels(
            points,
            labels,
            show_points=False,
            shadow=False,
            font_size=font_size,
            font_family=font_family,
            text_color=text_color,
            **add_point_labels_kwargs,
        )

    if cpos:
        plotter.camera_position = cpos

    if show_bounds:
        plotter.show_bounds()

    if show_axes:
        plotter.show_axes()

    return plotter


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
    split_sharp_edges=None,
    # labels kwargs
    font_size=None,
    font_family=None,
    text_color=None,
    theme=None,
    return_plotter=False,
    return_cpos=False,
    mapdl=None,
    plot_bc=False,
    plot_bc_legend=None,
    plot_bc_labels=None,
    bc_labels=None,
    bc_target=None,
    bc_glyph_size=None,
    bc_labels_font_size=16,
    plotter=None,
    add_points_kwargs={},
    add_mesh_kwargs={},
    add_point_labels_kwargs={},
    plotter_kwargs={},
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

    edge_color : string or 3 item list, optional,
        The solid color to give the edges when ``show_edges=True``.
        Either a string, RGB list, or hex color string.
        Defaults to black.

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
        This overrides the ``return_cpos`` value.

    return_cpos : bool, optional
        Returns the camera position as an array. Default ``False``.

    mapdl : Mapdl instance, optional
        If you want to use `plot_bc` keyword, the MAPDL instance
        needs to be passed as argument. Defaults to ``None``

    plot_bc : bool, optional
        Activate the plotting of the boundary conditions.
        Defaults to ``False``.

        .. warning:: This is in alpha state.

    plot_bc_legend : bool, optional
        Shows the boundary conditions legend.
        Defaults to ``False``

    plot_bc_labels : bool, optional
        Shows the boundary conditions label per node.
        Defaults to ``False``.

    bc_labels : List[str], Tuple(str), optional
        List or tuple of strings with the boundary conditions
        to plot, i.e. ["UX", "UZ"].
        You can obtain the allowed boundary conditions by
        evaluating ``ansys.mapdl.core.plotting.BCS``.
        You can use also the following shortcuts:

        * **'mechanical'**
          To plot the following mechanical boundary conditions:
          'UX', 'UY', 'UZ', 'FX', 'FY', and 'FZ'.
          Rotational or momentum boundary conditions are not
          allowed.

        * **'thermal'**
          To plot the following boundary conditions: 'TEMP' and
          'HEAT'.

        * **'electrical'**
          To plot the following electrical boundary conditions:
          'VOLT', 'CHRGS', and 'AMPS'.

        Defaults to all the allowed boundary conditions present
        in the responses of :func:`ansys.mapdl.core.Mapdl.dlist`
        and :func:`ansys.mapdl.core.Mapdl.flist()`.

    bc_target : List[str], Tuple(str), optional
        Specify the boundary conditions target
        to plot, i.e. "Nodes", "Elements".
        You can obtain the allowed boundary conditions target by
        evaluating ``ansys.mapdl.core.plotting.ALLOWED_TARGETS``.
        Defaults to only ``Nodes``.

    bc_glyph_size : float, optional
        Specify the size of the glyph used for the boundary
        conditions plotting.
        By default is ratio of the bounding box dimensions.

    bc_labels_font_size : float, optional
        Size of the text on the boundary conditions labels.
        By default it is 16.

    plotter : pyvista.Plotter, optional
        If a :class:`pyvista.Plotter` is not provided, then creates its
        own plotter. If a :class:`pyvista.Plotter` is provided, the plotter
        is not shown (you need to issue :meth:`pyvista.Plotter.show` manually)
        and the arguments ``notebook``, ``off_screen`` and ``theme`` are ignored,
        since they should be set when instantiated the provided plotter.
        Defaults to ``None`` (create the Plotter object).

    add_points_kwargs : list[dict]
        This is a dict or list of dicts to be passed to all or just the
        correspondent :class:`pyvista.Plotter.add_points` call in
        :func:`ansys.mapdl.core.plotting.general_plotter`.
        This pyvista method is used to plot nodes for example.
        See examples section to learn more about its usage.

    add_mesh_kwargs : list[dict]
        This is a dict or list of dicts to be passed to all or just the
        correspondent :class:`pyvista.Plotter.add_mesh` call in
        :func:`ansys.mapdl.core.plotting.general_plotter`.
        This pyvista method is used to plot elements for example.
        See examples section to learn more about its usage.

    add_point_labels_kwargs : list[dict]
        This is a dict or list of dicts to be passed to all or just the
        correspondent :class:`pyvista.Plotter.add_point_labels` call in
        :func:`ansys.mapdl.core.plotting.general_plotter`.
        This pyvista method is used to plot node labels for example.
        See examples section to learn more about its usage.

    plotter_kwargs : dict
        This is a dict which is passed to the :class:`pyvista.Plotter`
        initializer in :func:`ansys.mapdl.core.plotting.general_plotter`.
        This pyvista class is used in all PyMAPDL plots.
        See examples section to learn more about its usage.

    Returns
    -------
    cpos or pyvista.Plotter or None
        Camera position or instance of ``pyvista.Plotter`` or ``None`` depending
        on ``return_plotter`` and ``return_cpos``.

    Notes
    -----
    Plotting boundary conditions is still under-development, so feel free to share feedback
    or suggestion in `PyMAPDL <https://github.com/pyansys/pymapdl>`_.
    At the moment only nodal boundary conditions can be shown (``bc_target='Nodes'``), and only
    the following types of boundary conditions:

    +------------+--------------------------------------+
    | Field      | Boundary conditions                  |
    +============+======================================+
    | MECHANICAL | ["UX", "UY", "UZ", "FX", "FY", "FZ"] |
    +------------+--------------------------------------+
    | THERMAL    | ["TEMP", "HEAT"]                     |
    +------------+--------------------------------------+
    | ELECTRICAL | ["VOLT", "CHRGS", "AMPS"]            |
    +------------+--------------------------------------+

    Examples
    --------
    Plot areas and modify the background color to ``'black'``

    >>> cpos = mapdl.aplot(background='black')

    Enable smooth_shading on an element plot.

    >>> cpos = mapdl.eplot(smooth_shading=True)

    Plot boundary conditions "UX" and "UZ" on the nodes:

    >>> mapdl.nplot(plot_bc=True, bc_labels=["UX", "UZ"], plot_bc_labels=True)

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

    Using ``add_mesh_kwargs`` to pass other arguments to ``add_mesh`` pyvista method.

    >>> mapdl.eplot(background='w', show_edges=True, add_mesh_kwargs = {"use_transparency": False})

    Using ``plotter_kwargs`` to pass other arguments to ``Plotter`` constructor.

    >>> mapdl.eplot(background='w', show_edges=True, plotter_kwargs = {"polygon_smoothing": False})
    """
    if notebook:
        off_screen = True  # pragma: no cover

    if savefig:
        off_screen = True
        notebook = False

    # Getting the plotter
    pl = _general_plotter(
        meshes,
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
        split_sharp_edges=split_sharp_edges,
        # labels kwargs
        font_size=font_size,
        font_family=font_family,
        text_color=text_color,
        theme=theme,
        plotter=plotter,
        add_points_kwargs=add_points_kwargs,
        add_mesh_kwargs=add_mesh_kwargs,
        add_point_labels_kwargs=add_point_labels_kwargs,
        plotter_kwargs=plotter_kwargs,
    )

    if plot_bc:
        if not mapdl:
            raise ValueError(
                "An instance of `ansys.mapdl.core.mapdl._MapdlCore` "
                "should be passed using `mapdl` keyword if you are aiming "
                "to plot the boundary conditions (`plot_bc` is `True`)."
            )
        pl = bc_plotter(
            pl,
            mapdl=mapdl,
            plot_bc_legend=plot_bc_legend,
            plot_bc_labels=plot_bc_labels,
            bc_labels=bc_labels,
            bc_target=bc_target,
            bc_glyph_size=bc_glyph_size,
            bc_labels_font_size=bc_labels_font_size,
        )

    if title:  # Added here to avoid labels overlapping title
        pl.add_title(title, color=text_color)

    if return_cpos and return_plotter:
        raise ValueError(
            "'return_cpos' and 'return_plotter' cannot be both 'True' at the same time."
        )

    # permit user to save the figure as a screenshot
    if savefig:
        pl.show(
            title=title,
            auto_close=False,
            window_size=window_size,
            screenshot=True,
        )
        pl.screenshot(savefig)

        # return unclosed plotter
        if return_plotter:
            return pl

        # if not returning plotter, close right away
        pl.close()

    else:
        if not return_plotter and not plotter:
            pl.show()

    if return_plotter:
        return pl
    elif return_cpos:
        return pl.camera_position
    else:
        return None


def bc_plotter(
    pl,
    mapdl=None,
    bc_labels=None,
    bc_target=None,
    plot_bc_labels=False,
    plot_bc_legend=None,
    bc_glyph_size=None,
    bc_labels_font_size=16,
):
    if bc_labels:
        bc_labels = _bc_labels_checker(bc_labels)
    else:
        bc_labels = _bc_labels_default(mapdl)

    if bc_target:
        bc_target = _bc_target_checker(bc_target)
    else:
        bc_target = ["NODES"]  # bc_target_default()

    # We need to scale the glyphs, otherwise, they will be plot sized 1.
    # We are going to calculate the distance between the closest points,
    # so we will scaled to a percentage of this distance.
    # This might create very small points in cases there are a concentration of points.
    #
    # Later can find a way to plot them and keep their size constant independent of the zoom.

    if bc_glyph_size is None:
        bc_glyph_size = get_bounding_box(mapdl.mesh.nodes)
        bc_glyph_size = bc_glyph_size[bc_glyph_size != 0]

        if bc_glyph_size.size != 0:
            bc_glyph_size = bc_glyph_size.mean() * 0.75 / 10
        else:  # Case were there is only one node
            bc_glyph_size = 1

    if not isinstance(bc_glyph_size, (int, float)):
        raise ValueError("The 'bc_glyph_size' parameter can be only an int or float.")

    if "NODES" in bc_target:
        pl = bc_nodes_plotter(
            mapdl,
            pl,
            bc_labels,
            plot_bc_labels=plot_bc_labels,
            bc_glyph_size=bc_glyph_size,
            plot_bc_legend=plot_bc_legend,
            bc_labels_font_size=bc_labels_font_size,
        )

    # Add next things
    if "ELEM" in bc_target:
        pass

    return pl


def bc_nodes_plotter(
    mapdl,
    pl,
    bc_labels,
    plot_bc_labels=False,
    bc_glyph_size=1,
    plot_bc_legend=None,
    bc_labels_font_size=16,
):
    """Plot nodes BC given a list of labels."""
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

        if bc.size == 0:  # There is no nodes with such label
            return pl

        bc_num = bc[:, 0].astype(int)
        bc_nodes = nodes_xyz[np.isin(nodes_num, bc_num), :]
        bc_values = bc[:, 1:].astype(float)
        bc_scale = abs(bc_values[:, 0])

        if bc_scale.max() != bc_scale.min():
            bc_scale = (bc_scale - bc_scale.min()) / (
                bc_scale.max() - bc_scale.min()
            ) + 0.5  # Normalization around 0.5
        else:
            bc_scale = (
                np.ones(bc_scale.shape) * 0.5
            )  # In case all the values are the same

        pcloud = pv.PolyData(bc_nodes)
        pcloud["scale"] = bc_scale * bc_glyph_size

        # Specify tolerance in terms of fraction of bounding box length.
        # Float value is between 0 and 1. Default is None.
        # If absolute is True then the tolerance can be an absolute distance.
        # If None, points merging as a preprocessing step is disabled.
        glyphs = pcloud.glyph(
            orient=False,
            scale="scale",
            # tolerance=0.05,
            geom=BC_plot_settings[each_label]["glyph"],
        )
        name_ = f"{each_label}"
        pl.add_mesh(
            glyphs,
            color=BC_plot_settings[each_label]["color"],
            style="surface",
            # style='wireframe',
            # edge_color=BC_plot_settings[each_label]['color'],
            # line_width=3,
            name=name_,
            label=name_,
        )

        if plot_bc_labels:
            if bc_point_labels is None:
                bc_point_labels = {each: "" for each in nodes_num}

            for id_, values in zip(bc_num, bc_values):
                if not bc_point_labels[id_]:
                    bc_point_labels[
                        id_
                    ] = f"Node: {id_}\n{each_label}: {values[0]:6.3f}, {values[1]:6.3f}"
                else:
                    bc_point_labels[
                        id_
                    ] = f"{bc_point_labels[id_]}\n{each_label}: {values[0]:6.3f}, {values[1]:6.3f}"

    if plot_bc_labels:
        pcloud = pv.PolyData(nodes_xyz)
        pcloud["labels"] = list(bc_point_labels.values())
        pl.add_point_labels(
            pcloud.points,
            pcloud["labels"],
            shape_opacity=0.25,
            font_size=bc_labels_font_size,
        )

    if plot_bc_legend:
        pl.add_legend(bcolor=None)

    return pl


def _bc_labels_checker(bc_labels):
    """Make sure we have allowed parameters and data types for ``bc_labels``"""
    if not isinstance(bc_labels, (str, list, tuple)):
        raise ValueError(
            "The parameter 'bc_labels' can be only a string, a list of strings or tuple of strings."
        )

    if isinstance(bc_labels, str):
        bc_labels = bc_labels.upper()
        if bc_labels not in BCS and bc_labels not in FIELDS:
            raise ValueError(
                f"The parameter '{bc_labels}' in 'bc_labels' is not supported.\n"
                "Please use any of the following:\n"
                f"{FIELDS}\nor any combination of:\n{BCS}"
            )
        bc_labels = [bc_labels]

    elif isinstance(bc_labels, (list, tuple)):
        if not all([isinstance(each, str) for each in bc_labels]):
            raise ValueError(
                "The parameter 'bc_labels' can be a list or tuple, but it should only contain strings inside them."
            )

        if not all([each.upper() in BCS for each in bc_labels]):
            raise ValueError(
                f"One or more parameters in 'bc_labels'({bc_labels}) are not supported.\n"
                f"Please use any combination of the following:\n{BCS}"
            )

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
        raise ValueError(
            "The parameter 'bc_target' can be only a string, a list of strings or tuple of strings."
        )

    if isinstance(bc_target, str):
        if bc_target.upper() not in ALLOWED_TARGETS:
            raise ValueError(
                f"The parameter '{bc_target}' in 'bc_target' is not supported.\n"
                f"At the moments only the following are supported:\n{ALLOWED_TARGETS}"
            )
        bc_target = [bc_target.upper()]

    if isinstance(bc_target, (list, tuple)):
        if not all([each.upper() in ALLOWED_TARGETS for each in bc_target]):
            raise ValueError(
                "One or more parameters in 'bc_target' are not supported.\n"
                f"Please use any combination of the following:\n{ALLOWED_TARGETS}"
            )
        if not all([isinstance(each, str) for each in bc_target]):
            raise ValueError(
                "The parameter 'bc_target' can be a list or tuple, but it should only contain strings inside them."
            )

        bc_target = [each.upper() for each in bc_target]

    return bc_target


def _bc_labels_default(mapdl):
    """Get the labels from the MAPDL database."""
    flist = list(
        set(
            [
                each[1].upper()
                for each in mapdl.get_nodal_loads()
                if each[1].upper() in BCS
            ]
        )
    )
    dlist = list(
        set(
            [
                each[1].upper()
                for each in mapdl.get_nodal_constrains()
                if each[1].upper() in BCS
            ]
        )
    )
    return flist + dlist
