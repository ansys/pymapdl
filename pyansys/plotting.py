"""Plotting helper for MAPDL using pyvista"""
import pyvista as pv

def general_plotter(title, meshes, points, labels,
                    cpos=None,
                    show_bounds=False, show_axes=False,
                    background=None, off_screen=False,
                    screenshot=False,
                    window_size=None,
                    # add_mesh kwargs:
                    color='w',
                    show_edges=None, edge_color=None, point_size=5.0,
                    line_width=None, opacity=1.0, flip_scalars=False,
                    lighting=None, n_colors=256,
                    interpolate_before_map=True, cmap=None,
                    render_points_as_spheres=False, render_lines_as_tubes=False,
                    stitle=None,
                    smooth_shading=None,
                    # labels kwargs
                    font_size=None,
                    font_family=None,
                    text_color=None):
    """General APDL plotter"""
    pl = pv.Plotter(off_screen=off_screen)

    if background:
        pl.set_background(background)

    for point in points:
        pl.add_points(point['points'],
                      scalars=point.get('scalars', None),
                      color=color,
                      show_edges=show_edges, edge_color=edge_color,
                      point_size=point_size, line_width=line_width,
                      opacity=opacity, flip_scalars=flip_scalars,
                      lighting=lighting, n_colors=n_colors,
                      interpolate_before_map=interpolate_before_map,
                      cmap=cmap, render_points_as_spheres=render_points_as_spheres,
                      render_lines_as_tubes=render_lines_as_tubes)

    for mesh in meshes:
        pl.add_mesh(mesh['mesh'],
                    scalars=mesh.get('scalars', None),
                    color=mesh.get('color', color),
                    show_edges=show_edges, edge_color=edge_color,
                    smooth_shading=smooth_shading,
                    point_size=point_size, line_width=line_width,
                    opacity=opacity, flip_scalars=flip_scalars,
                    lighting=lighting, n_colors=n_colors,
                    interpolate_before_map=interpolate_before_map,
                    cmap=cmap, render_points_as_spheres=render_points_as_spheres,
                    render_lines_as_tubes=render_lines_as_tubes)

    for label in labels:
        pl.add_point_labels(label['points'],
                            label['labels'],
                            show_points=False, shadow=False,
                            font_size=font_size,
                            font_family=font_family,
                            text_color=text_color)

    if stitle is not None:
        pl.add_scalar_bar(title=stitle)

    if cpos:
        pl.camera_position = cpos

    if show_bounds:
        pl.show_bounds()

    if show_axes:
        pl.show_axes()

    if screenshot:
        pl.show(title=title, auto_close=False, window_size=window_size)
        pl.screenshot(screenshot)
    else:
        pl.show()

    return pl.camera_position
