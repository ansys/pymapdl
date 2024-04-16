# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import pyvista as pv
from pyvista.core import _vtk_core as _vtk
from pyvista.core.utilities import translate
from pyvista.core.utilities.helpers import wrap
from pyvista.core.utilities.misc import no_new_attr

# I dont want to have to fix a very recent lower bound for pyvista.
# Hence I'm copying what I need from there.
# copied from pyvista source code:
# https://github.com/pyvista/pyvista/blob/35396c2e7645a6b57ad30d25ac1893f2141aab95/pyvista/core/utilities/geometric_sources.py#L2254


@no_new_attr
class ArrowSource(_vtk.vtkArrowSource):
    def __init__(
        self,
        tip_length=0.25,
        tip_radius=0.1,
        tip_resolution=20,
        shaft_radius=0.05,
        shaft_resolution=20,
    ):
        """Initialize source."""
        self.SetTipLength(tip_length)
        self.SetTipRadius(tip_radius)
        self.SetTipResolution(tip_resolution)
        self.SetShaftResolution(shaft_resolution)
        self.SetShaftRadius(shaft_radius)

    @property
    def output(self):
        """Get the output data object for a port on this algorithm.

        Returns
        -------
        pyvista.PolyData
            Plane mesh.
        """
        self.Update()
        return wrap(self.GetOutput())


# Symbols for constrains
class DefaultSymbol:
    # Class to store the symbols because of https://github.com/ansys/pymapdl/issues/2872
    # To solve that issue, we avoid having to load the pyvista attributes when the module is load.
    # Instead we set the parameters at calling

    def __init__(self):
        self._configured = False

    def __call__(self, name):
        if not self._configured:
            self._set_configuration()
            self._configured = True

        return getattr(self, name)

    def _set_configuration(self):
        self._point = pv.Sphere(center=(0, 0, 0), radius=0.5)
        self._cube = pv.Cube(center=(0, 0, 0), x_length=1, y_length=1, z_length=1)

        def _basic_arrow(
            start=(0.0, 0.0, 0.0),
            direction=(1.0, 0.0, 0.0),
            tip_length=0.5,
            tip_radius=0.25,
            tip_resolution=20,
            shaft_radius=0.05,
            shaft_resolution=20,
            invert=True,
        ):
            arrow = ArrowSource(
                tip_length=tip_length,
                tip_radius=tip_radius,
                tip_resolution=tip_resolution,
                shaft_radius=shaft_radius,
                shaft_resolution=shaft_resolution,
            )
            arrow.SetInvert(invert)
            surf = arrow.output

            translate(surf, start, direction)
            return surf

        def _arrow(*args, **kwargs):
            return _basic_arrow(*args, **kwargs)

        def _cone(start=(0, 0, 0), direction=None):
            return _basic_arrow(
                start=start,
                direction=direction,
                tip_length=1,
                tip_radius=0.5,
            )

        self.TEMP = {
            "color": "orange",
            "glyph": self._point,
        }

        self.HEAT = {"color": "red", "glyph": self._cube}

        self.UX = {"color": "red", "glyph": _cone(direction=(-1, 0, 0))}
        self.UY = {"color": "green", "glyph": _cone(direction=(0, -1, 0))}
        self.UZ = {"color": "blue", "glyph": _cone(direction=(0, 0, -1))}

        self.FX = {"color": "red", "glyph": _arrow(direction=(-1, 0, 0))}
        self.FY = {"color": "green", "glyph": _arrow(direction=(0, -1, 0))}
        self.FZ = {"color": "blue", "glyph": _arrow(direction=(0, 0, -1))}

        self.VOLT = {"color": "yellow", "glyph": self.cross_cylinders_3d()}

        self.AMPS = {"color": "red", "glyph": self.cross_cylinders_3d()}
        self.CHRG = {"color": "red", "glyph": self.cross_cylinders_3d()}

    @staticmethod
    def cross_cylinders_3d():
        model_a = pv.Cylinder(
            center=(0, 0, 0), direction=(1, 0, 0), radius=0.2, height=1.5
        ).triangulate()

        model_b = pv.Cylinder(
            center=(0, 0, 0), direction=(0, 1, 0), radius=0.2, height=1.5
        ).triangulate()

        model_c = pv.Cylinder(
            center=(0, 0, 0), direction=(0, 0, 1), radius=0.2, height=1.5
        ).triangulate()

        result = model_a.merge(model_b).triangulate()
        result = result.merge(model_c)

        result.rotate_z(45.0, inplace=True)
        result.rotate_vector(
            vector=(1, -1, 0), angle=-45, point=(0, 0, 0), inplace=True
        )

        return result
