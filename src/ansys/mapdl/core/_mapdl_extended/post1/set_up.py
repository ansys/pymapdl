"""POST1 setup command extensions."""

from functools import wraps

from ansys.mapdl.core.commands import CommandListingOutput
from ansys.mapdl.core.mapdl_core import _MapdlCore

from .. import _ExtendedMixinBase


class _ExtendedPostSetupMixin(_ExtendedMixinBase):
    """Extended POST1 setup commands."""
    @wraps(_MapdlCore.set)
    def set(
        self,
        lstep="",
        sbstep="",
        fact="",
        kimg="",
        time="",
        angle="",
        nset="",
        order="",
        **kwargs,
    ):
        """Wraps SET to return a Command listing

        Returns
        -------
        CommandListingOutput or str
            Command listing output when LIST is specified, otherwise MAPDL command output.
        """
        output = super().set(
            lstep, sbstep, fact, kimg, time, angle, nset, order, **kwargs
        )

        if (
            isinstance(lstep, str)
            and lstep.upper() == "LIST"
            and not sbstep
            and not fact
        ):
            return CommandListingOutput(
                output,
                magicwords=["SET", "TIME/FREQ"],
                columns_names=[
                    "SET",
                    "TIME/FREQ",
                    "LOAD STEP",
                    "SUBSTEP",
                    "CUMULATIVE",
                ],
            )
        else:
            return output
