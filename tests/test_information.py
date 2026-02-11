# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
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

"""Test the information module"""

import inspect

import pytest

from ansys.mapdl.core.information import UnitsDict


def test_units_dict_parsing():
    """Test UnitsDict parsing and access without requiring MAPDL."""
    # Sample units string similar to what MAPDL returns
    units_string = """MKS UNITS SPECIFIED FOR INTERNAL    
  LENGTH        (l)  = METER (M)
  MASS          (M)  = KILOGRAM (KG)
  TIME          (t)  = SECOND (SEC)
  TEMPERATURE   (T)  = CELSIUS (C)
  TOFFSET            = 273.0
  CHARGE        (Q)  = COULOMB
  FORCE         (f)  = NEWTON (N) (KG-M/SEC2)
  HEAT               = JOULE (N-M)

  PRESSURE           = PASCAL (NEWTON/M**2)
  ENERGY        (W)  = JOULE (N-M)
  POWER         (P)  = WATT (N-M/SEC)
  CURRENT       (i)  = AMPERE (COULOMBS/SEC)
  CAPACITANCE   (C)  = FARAD
  INDUCTANCE    (L)  = HENRY
  MAGNETIC FLUX      = WEBER
  RESISTANCE    (R)  = OHM
  ELECTRIC POTENTIAL = VOLT"""
    
    units = UnitsDict(units_string)
    
    # Test access by full name (case-insensitive)
    assert units['CHARGE'] == 'coulomb'
    assert units['charge'] == 'coulomb'
    assert units['Charge'] == 'coulomb'
    
    # Test access by short name
    assert units['Q'] == 'coulomb'
    assert units['q'] == 'coulomb'
    
    # Test length access
    assert units['LENGTH'] == 'meter'
    assert units['length'] == 'meter'
    assert units['l'] == 'meter'  # short name
    
    # Test mass access
    assert units['MASS'] == 'kilogram'
    assert units['mass'] == 'kilogram'
    assert units['M'] == 'kilogram'  # short name
    assert units['m'] == 'kilogram'
    
    # Test numeric value
    assert units['TOFFSET'] == '273.0'
    assert units['toffset'] == '273.0'
    
    # Test __str__ and __repr__ return original string
    assert str(units) == units_string
    assert repr(units) == units_string
    
    # Test __contains__
    assert 'charge' in units
    assert 'CHARGE' in units
    assert 'q' in units
    assert 'nonexistent' not in units
    
    # Test get method with default
    assert units.get('charge') == 'coulomb'
    assert units.get('nonexistent', 'default') == 'default'


def test_units_dict_short_name_collision():
    """Test that when short names collide, the first occurrence is kept."""
    # Test case where 'L' appears as short name for both LENGTH and INDUCTANCE
    # Only the first (LENGTH) should be kept as 'l'
    units_string = """TEST UNITS
  LENGTH        (l)  = METER (M)
  INDUCTANCE    (L)  = HENRY"""
    
    units = UnitsDict(units_string)
    
    # 'l' should map to the first occurrence (meter), not the second (henry)
    assert units['l'] == 'meter'
    assert units['L'] == 'meter'
    
    # But the full names should still work correctly
    assert units['length'] == 'meter'
    assert units['inductance'] == 'henry'


def test_mapdl_info(mapdl, cleared, capfd):
    info = mapdl.info
    for attr, value in inspect.getmembers(info):
        if not attr.startswith("_") and attr not in ["title", "stitles", "units"]:
            assert isinstance(value, str)

            with pytest.raises(AttributeError):
                setattr(info, attr, "any_value")

    assert "PyMAPDL" in mapdl.info.__repr__()
    out = info.__str__()

    assert "ansys" in out.lower()
    assert "Product" in out
    assert "MAPDL Version" in out
    assert "UPDATE" in out


def test_info_title(mapdl, cleared):
    title = "this is my title"
    mapdl.info.title = title
    assert title == mapdl.info.title


def test_info_stitle(mapdl, cleared):
    info = mapdl.info

    assert all([not each for each in info.stitles])
    stitles = ["asfd", "qwer", "zxcv", "jkl"]
    info.stitles = "\n".join(stitles)

    assert stitles == info.stitles

    stitles = stitles[::-1]

    info.stitles = stitles
    assert stitles == info.stitles

    info.stitles = None
    assert all([not each for each in info.stitles])


def test_title(mapdl, cleared):
    """Test the title property of the MapdlInfo class."""
    title = "This is a test title"
    mapdl.info.title = title
    assert mapdl.info.title == title

    stitles = ["Subtitle 1", "Subtitle 2", "Subtitle 3", "Subtitle 4"]
    mapdl.info.stitles = stitles
    assert mapdl.info.stitles == stitles


def test_units(mapdl, cleared):
    """Test the units property returns a UnitsDict with proper functionality."""
    from ansys.mapdl.core.information import UnitsDict
    
    units = mapdl.info.units
    
    # Check that it's a UnitsDict instance
    assert isinstance(units, UnitsDict)
    
    # Check that it's also a dict
    assert isinstance(units, dict)
    
    # Check __str__ and __repr__ return the original formatted string
    units_str = str(units)
    units_repr = repr(units)
    
    assert "UNITS SPECIFIED" in units_str
    assert "UNITS SPECIFIED" in units_repr
    
    # Check that we can access units by their full name (case-insensitive)
    # These assertions might vary depending on what units are set, so we test
    # if the dict is not empty and has expected structure
    assert len(units) > 0
    
    # Try to access some common unit keys (if they exist)
    # The actual keys present depend on the MAPDL unit system
    # So we just verify the case-insensitive access works
    for key in list(units.keys())[:1]:  # Test with the first key
        # Test case insensitive access
        value = units[key]
        assert value == units[key.upper()]
        assert value == units[key.lower()]
        
    # Test that invalid keys raise KeyError
    with pytest.raises(KeyError):
        _ = units["NONEXISTENT_UNIT_KEY_12345"]

