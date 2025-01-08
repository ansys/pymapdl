# Copyright (C) 2016 - 2025 ANSYS, Inc. and/or its affiliates.
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

from functools import wraps
import re
from typing import Callable, List, Optional
import weakref

from ansys.mapdl import core as pymapdl
from ansys.mapdl.core.errors import MapdlExitedError


def update_information_first(update: bool = False) -> Callable:
    """
    Decorator to wrap :class:`Information <ansys.mapdl.core.misc.Information>`
    methods to force update the fields when accessed.

    Parameters
    ----------
    update : bool, optional
        If ``True``, the class information is updated by calling ``/STATUS``
        before accessing the methods. By default ``False``
    """

    def decorator(function):
        @wraps(function)
        def wrapper(self, *args, **kwargs):
            if update or not self._stats:
                self._update()
            return function(self, *args, **kwargs)

        return wrapper

    return decorator


class Information:
    """
    This class provide some MAPDL information from ``/STATUS`` MAPDL command.

    It is also the object that is called when you issue ``print(mapdl)``,
    which means ``print`` calls ``mapdl.info.__str__()``.

    Notes
    -----
    You cannot directly modify the values of this class.

    Some of the results are cached for later calls.

    Examples
    --------
    >>> mapdl.info
    Product:             Ansys Mechanical Enterprise
    MAPDL Version:       24.1
    ansys.mapdl Version: 0.68.0

    >>> print(mapdl)
    Product:             Ansys Mechanical Enterprise
    MAPDL Version:       24.1
    ansys.mapdl Version: 0.68.0

    >>> mapdl.info.product
    'Ansys Mechanical Enterprise'

    >>> info = mapdl.info
    >>> info.mapdl_version
    'RELEASE  2021 R2           BUILD 21.2      UPDATE 20210601'

    """

    def __init__(self, mapdl: "Mapdl") -> None:
        """Class Initializer"""
        from ansys.mapdl.core.mapdl import MapdlBase  # lazy import to avoid circular

        if not isinstance(mapdl, MapdlBase):  # pragma: no cover
            raise TypeError("Must be implemented from MAPDL class")

        self._mapdl_weakref = weakref.ref(mapdl)
        self._stats = None
        self._repr_keys = {
            "Product": "product",
            "MAPDL Version": "mapdl_version",
            "PyMAPDL Version": "pymapdl_version",
        }

    @property
    def _mapdl(self) -> "Mapdl":
        """Return the weakly referenced MAPDL instance."""
        return self._mapdl_weakref()

    def _update(self) -> None:
        """We might need to do more calls if we implement properties
        that change over the MAPDL session."""
        try:
            if self._mapdl._exited:  # pragma: no cover
                raise MapdlExitedError("Information class: MAPDL exited")

            stats = self._mapdl.slashstatus("ALL")
        except Exception:  # pragma: no cover
            self._stats = None
            raise MapdlExitedError("Information class: MAPDL exited")

        stats = stats.replace("\n ", "\n")  # Bit of formatting
        self._stats = stats
        self._mapdl._log.debug("Information class: Updated")

    def __repr__(self) -> str:
        if self._mapdl.is_console and self._mapdl.exited:
            return "MAPDL exited"

        if not self._stats:
            self._update()

        return "\n".join(
            [
                f"{each_name}:".ljust(25) + f"{getattr(self, each_attr)}".ljust(25)
                for each_name, each_attr in self._repr_keys.items()
            ]
        )

    @property
    @update_information_first(False)
    def product(self) -> str:
        """Retrieve the product from the MAPDL instance."""
        return self._get_product()

    @property
    @update_information_first(False)
    def mapdl_version(self) -> str:
        """Retrieve the MAPDL version from the MAPDL instance."""
        return self._get_mapdl_version()

    @property
    @update_information_first(False)
    def mapdl_version_release(self) -> str:
        """Retrieve the MAPDL version release from the MAPDL instance."""
        st = self._get_mapdl_version()
        return self._get_between("RELEASE", "BUILD", st).strip()

    @property
    @update_information_first(False)
    def mapdl_version_build(self) -> str:
        """Retrieve the MAPDL version build from the MAPDL instance."""
        st = self._get_mapdl_version()
        return self._get_between("BUILD", "UPDATE", st).strip()

    @property
    @update_information_first(False)
    def mapdl_version_update(self) -> str:
        """Retrieve the MAPDL version update from the MAPDL instance."""
        st = self._get_mapdl_version()
        return self._get_between("UPDATE", "", st).strip()

    @property
    @update_information_first(False)
    def pymapdl_version(self) -> str:
        """Retrieve the PyMAPDL version from the MAPDL instance."""
        return self._get_pymapdl_version()

    @property
    @update_information_first(False)
    def products(self) -> str:
        """Retrieve the products from the MAPDL instance."""
        return self._get_products()

    @property
    @update_information_first(False)
    def preprocessing_capabilities(self) -> str:
        """Retrieve the preprocessing capabilities from the MAPDL instance."""
        return self._get_preprocessing_capabilities()

    @property
    @update_information_first(False)
    def aux_capabilities(self) -> str:
        """Retrieve the aux capabilities from the MAPDL instance."""
        return self._get_aux_capabilities()

    @property
    @update_information_first(True)
    def solution_options(self) -> str:
        """Retrieve the solution options from the MAPDL instance."""
        return self._get_solution_options()

    @property
    @update_information_first(False)
    def post_capabilities(self) -> str:
        """Retrieve the post capabilities from the MAPDL instance."""
        return self._get_post_capabilities()

    @property
    @update_information_first(True)
    def titles(self) -> str:
        """Retrieve the titles from the MAPDL instance."""
        return self._get_titles()

    @property
    @update_information_first(True)
    def title(self) -> str:
        """Retrieve and set the title from the MAPDL instance."""
        return self._mapdl.inquire("", "title")

    @title.setter
    def title(self, title) -> str:
        return self._mapdl.run(f"/TITLE, {title}")

    @property
    @update_information_first(True)
    def stitles(self, i: int = None) -> str:
        """Retrieve or set the value for the MAPDL stitle (subtitles).

        If 'stitle' includes newline characters (`\\n`), then each line
        is assigned to one STITLE.

        If 'stitle' is equals ``None``, the stitles are reset.

        If ``i`` is supplied, only set the stitle number i.

        Starting from 0 up to 3 (Python indexing).
        """
        if not i:
            return self._get_stitles()
        else:
            return self._get_stitles()[i]

    @stitles.setter
    def stitles(self, stitle: str, i: int = None) -> None:
        if stitle is None:
            # Case to empty
            stitle = ["", "", "", ""]

        if not isinstance(stitle, (str, list)):
            raise ValueError("Only str or list are allowed for stitle")

        if isinstance(stitle, str):
            if "\n" in stitle:
                stitle = stitle.splitlines()
            else:
                stitle = "\n".join(
                    [stitle[ii : ii + 70] for ii in range(0, len(stitle), 70)]
                )

        if any([len(each) > 70 for each in stitle]):
            raise ValueError("The number of characters per subtitle is limited to 70.")

        if not i:
            for each_index, each_stitle in zip(range(1, 5), stitle):
                self._mapdl.stitle(each_index, each_stitle)
        else:
            self._mapdl.stitle(i, stitle)

    @property
    @update_information_first(True)
    def units(self) -> str:
        """Retrieve the units from the MAPDL instance."""
        return self._get_units()

    @property
    @update_information_first(True)
    def scratch_memory_status(self) -> str:
        """Retrieve the scratch memory status from the MAPDL instance."""
        return self._get_scratch_memory_status()

    @property
    @update_information_first(True)
    def database_status(self) -> str:
        """Retrieve the database status from the MAPDL instance."""
        return self._get_database_status()

    @property
    @update_information_first(True)
    def config_values(self) -> str:
        """Retrieve the config values from the MAPDL instance."""
        return self._get_config_values()

    @property
    @update_information_first(True)
    def global_status(self) -> str:
        """Retrieve the global status from the MAPDL instance."""
        return self._get_global_status()

    @property
    @update_information_first(True)
    def job_information(self) -> str:
        """Retrieve the job information from the MAPDL instance."""
        return self._get_job_information()

    @property
    @update_information_first(True)
    def model_information(self) -> str:
        """Retrieve the model information from the MAPDL instance."""
        return self._get_model_information()

    @property
    @update_information_first(True)
    def boundary_condition_information(self) -> str:
        """Retrieve the boundary condition information from the MAPDL instance."""
        return self._get_boundary_condition_information()

    @property
    @update_information_first(True)
    def routine_information(self) -> str:
        """Retrieve the routine information from the MAPDL instance."""
        return self._get_routine_information()

    @property
    @update_information_first(True)
    def solution_options_configuration(self) -> str:
        """Retrieve the solution options configuration from the MAPDL instance."""
        return self._get_solution_options_configuration()

    @property
    @update_information_first(True)
    def load_step_options(self) -> str:
        """Retrieve the load step options from the MAPDL instance."""
        return self._get_load_step_options()

    def _get_between(
        self,
        init_string: str,
        end_string: Optional[str] = None,
        string: Optional[str] = None,
    ) -> str:
        if not string:
            self._update()
            string = self._stats

        st = string.find(init_string) + len(init_string)

        if not end_string:
            en = None
        else:
            en = string.find(end_string)
        return "\n".join(string[st:en].splitlines()).strip()

    def _get_product(self) -> str:
        return self._get_products().splitlines()[0]

    def _get_mapdl_version(self) -> str:
        titles_ = self._get_titles()
        st = titles_.find("RELEASE")
        en = titles_.find("INITIAL", st)
        return titles_[st:en].split("CUSTOMER")[0].strip()

    def _get_pymapdl_version(self) -> str:
        return pymapdl.__version__

    def _get_title(self) -> str:
        match = re.match(r"TITLE=(.*)$", self._get_titles())
        if match:
            return match.groups(1)[0].strip()

    def _get_stitles(self) -> List[str]:
        return [
            (
                re.search(f"SUBTITLE  {i}=(.*)", self._get_titles())
                .groups(1)[0]
                .strip()
                if re.search(f"SUBTITLE  {i}=(.*)", self._get_titles())
                else ""
            )
            for i in range(1, 5)
        ]

    def _get_products(self) -> str:
        init_ = "*** Products ***"
        end_string = "*** PreProcessing Capabilities ***"
        return self._get_between(init_, end_string)

    def _get_preprocessing_capabilities(self) -> str:
        init_ = "*** PreProcessing Capabilities ***"
        end_string = "*** Aux Capabilities ***"
        return self._get_between(init_, end_string)

    def _get_aux_capabilities(self) -> str:
        init_ = "*** Aux Capabilities ***"
        end_string = "*** Solution Options ***"
        return self._get_between(init_, end_string)

    def _get_solution_options(self) -> str:
        init_ = "*** Solution Options ***"
        end_string = "*** Post Capabilities ***"
        return self._get_between(init_, end_string)

    def _get_post_capabilities(self) -> str:
        init_ = "*** Post Capabilities ***"
        end_string = "***** TITLES *****"
        return self._get_between(init_, end_string)

    def _get_titles(self) -> str:
        init_ = "***** TITLES *****"
        end_string = "***** UNITS *****"
        return self._get_between(init_, end_string)

    def _get_units(self) -> str:
        init_ = "***** UNITS *****"
        end_string = "***** SCRATCH MEMORY STATUS *****"
        return self._get_between(init_, end_string)

    def _get_scratch_memory_status(self) -> str:
        init_ = "***** SCRATCH MEMORY STATUS *****"
        end_string = "*****    DATABASE STATUS    *****"
        return self._get_between(init_, end_string)

    def _get_database_status(self) -> str:
        init_ = "*****    DATABASE STATUS    *****"
        end_string = "***** CONFIG VALUES *****"
        return self._get_between(init_, end_string)

    def _get_config_values(self) -> str:
        init_ = "***** CONFIG VALUES *****"
        end_string = "G L O B A L   S T A T U S"
        return self._get_between(init_, end_string)

    def _get_global_status(self) -> str:
        init_ = "G L O B A L   S T A T U S"
        end_string = "J O B   I N F O R M A T I O N"
        return self._get_between(init_, end_string)

    def _get_job_information(self) -> str:
        init_ = "J O B   I N F O R M A T I O N"
        end_string = "M O D E L   I N F O R M A T I O N"
        return self._get_between(init_, end_string)

    def _get_model_information(self) -> str:
        init_ = "M O D E L   I N F O R M A T I O N"
        end_string = "B O U N D A R Y   C O N D I T I O N   I N F O R M A T I O N"
        return self._get_between(init_, end_string)

    def _get_boundary_condition_information(self) -> str:
        init_ = "B O U N D A R Y   C O N D I T I O N   I N F O R M A T I O N"
        end_string = "R O U T I N E   I N F O R M A T I O N"
        return self._get_between(init_, end_string)

    def _get_routine_information(self) -> str:
        init_ = "R O U T I N E   I N F O R M A T I O N"
        end_string = None
        return self._get_between(init_, end_string)

    def _get_solution_options_configuration(self) -> str:
        init_ = "S O L U T I O N   O P T I O N S"
        end_string = "L O A D   S T E P   O P T I O N S"
        return self._get_between(init_, end_string)

    def _get_load_step_options(self) -> str:
        init_ = "L O A D   S T E P   O P T I O N S"
        end_string = None
        return self._get_between(init_, end_string)
