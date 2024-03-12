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

# Symbols for constrains


class DefaultSymbol:
    # Class to store the symbols because of https://github.com/ansys/pymapdl/issues/2872
    # To solve that issue, we avoid having to load the pyvista attributes when the module is load.
    # Instead we set the parameters at calling

    def __init__(self):
        self._configured = False
        pass

    def __call__(self, name):
        if not self._configured:
            self._set_configuration()

        return getattr(self, name)

    def _set_configuration(self):
        # Setting the
        self.TEMP = {
            "color": "orange",
            "glyph": pv.Sphere(center=(0, 0, 0), radius=0.5),
        }

        self.HEAT = {
            "color": "red",
            "glyph": pv.Arrow(
                start=(-1, 0, 0),
                direction=(1, 0, 0),
                tip_length=1,
                tip_radius=0.5,
                scale=1.0,
            ),
        }

        self.UX = {
            "color": "red",
            "glyph": pv.Arrow(
                start=(0, -1, 0),
                direction=(0, 1, 0),
                tip_length=1,
                tip_radius=0.5,
                scale=1.0,
            ),
        }

        self.UY = {
            "color": "green",
            "glyph": pv.Arrow(
                start=(0, 0, -1),
                direction=(0, 0, 1),
                tip_length=1,
                tip_radius=0.5,
                scale=1.0,
            ),
        }

        self.UZ = {
            "color": "blue",
            "glyph": pv.Arrow(
                start=(-1, 0, 0),
                direction=(1, 0, 0),
                tip_length=0.5,
                tip_radius=0.25,
                scale=1.0,
            ),
        }

        self.VOLT = {
            "color": "yellow",
            "glyph": pv.Arrow(
                start=(0, -1, 0),
                direction=(0, 1, 0),
                tip_length=0.5,
                tip_radius=0.25,
                scale=1.0,
            ),
        }

        self.FX = {
            "color": "red",
            "glyph": pv.Arrow(
                start=(0, 0, -1),
                direction=(0, 0, 1),
                tip_length=0.5,
                tip_radius=0.25,
                scale=1.0,
            ),
        }

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

        self.FY = {"color": "green", "glyph": get_VOLT()}

        self.FZ = {
            "color": "blue",
            "glyph": pv.Cube(
                center=(0, 0, 0), x_length=1.0, y_length=1.0, z_length=1.0
            ),
        }

        self.AMPS = {"color": "grey", "glyph": get_VOLT()}
        self.CHRGS = {"color": "grey", "glyph": get_VOLT()}
