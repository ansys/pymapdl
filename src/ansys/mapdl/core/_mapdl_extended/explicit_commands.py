# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
# Copyright (C) 2016 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
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


"""The explicit commands MAPDL extended mixin."""

from functools import wraps

from ansys.mapdl.core.errors import CommandDeprecated
from ansys.mapdl.core.mapdl_core import _MapdlCore

from . import _ExtendedMixinBase


class _ExtendedExplicitCommandsMixin(_ExtendedMixinBase):
    """Static responsibility mixin for the extended MAPDL facade."""

    @wraps(_MapdlCore.edasmp)
    def edasmp(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edasmp()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edasmp(*args, **kwargs)

    @wraps(_MapdlCore.edbound)
    def edbound(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edbound()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edbound(*args, **kwargs)

    @wraps(_MapdlCore.edbx)
    def edbx(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edbx()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edbx(*args, **kwargs)

    @wraps(_MapdlCore.edcgen)
    def edcgen(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edcgen()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edcgen(*args, **kwargs)

    @wraps(_MapdlCore.edclist)
    def edclist(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edclist()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edclist(*args, **kwargs)

    @wraps(_MapdlCore.edcmore)
    def edcmore(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edcmore()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edcmore(*args, **kwargs)

    @wraps(_MapdlCore.edcnstr)
    def edcnstr(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edcnstr()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edcnstr(*args, **kwargs)

    @wraps(_MapdlCore.edcontact)
    def edcontact(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edcontact()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edcontact(*args, **kwargs)

    @wraps(_MapdlCore.edcrb)
    def edcrb(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edcrb()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edcrb(*args, **kwargs)

    @wraps(_MapdlCore.edcurve)
    def edcurve(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edcurve()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edcurve(*args, **kwargs)

    @wraps(_MapdlCore.eddbl)
    def eddbl(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.eddbl()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().eddbl(*args, **kwargs)

    @wraps(_MapdlCore.eddc)
    def eddc(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.eddc()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().eddc(*args, **kwargs)

    @wraps(_MapdlCore.edipart)
    def edipart(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edipart()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edipart(*args, **kwargs)

    @wraps(_MapdlCore.edlcs)
    def edlcs(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edlcs()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edlcs(*args, **kwargs)

    @wraps(_MapdlCore.edmp)
    def edmp(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edmp()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edmp(*args, **kwargs)

    @wraps(_MapdlCore.ednb)
    def ednb(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.ednb()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().ednb(*args, **kwargs)

    @wraps(_MapdlCore.edndtsd)
    def edndtsd(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edndtsd()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edndtsd(*args, **kwargs)

    @wraps(_MapdlCore.ednrot)
    def ednrot(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.ednrot()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().ednrot(*args, **kwargs)

    @wraps(_MapdlCore.edpart)
    def edpart(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edpart()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edpart(*args, **kwargs)

    @wraps(_MapdlCore.edpc)
    def edpc(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edpc()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edpc(*args, **kwargs)

    @wraps(_MapdlCore.edsp)
    def edsp(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edsp()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edsp(*args, **kwargs)

    @wraps(_MapdlCore.edweld)
    def edweld(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edweld()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edweld(*args, **kwargs)

    @wraps(_MapdlCore.edadapt)
    def edadapt(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edadapt()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edadapt(*args, **kwargs)

    @wraps(_MapdlCore.edale)
    def edale(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edale()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edale(*args, **kwargs)

    @wraps(_MapdlCore.edbvis)
    def edbvis(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edbvis()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edbvis(*args, **kwargs)

    @wraps(_MapdlCore.edcadapt)
    def edcadapt(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edcadapt()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edcadapt(*args, **kwargs)

    @wraps(_MapdlCore.edcpu)
    def edcpu(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edcpu()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edcpu(*args, **kwargs)

    @wraps(_MapdlCore.edcsc)
    def edcsc(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edcsc()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edcsc(*args, **kwargs)

    @wraps(_MapdlCore.edcts)
    def edcts(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edcts()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edcts(*args, **kwargs)

    @wraps(_MapdlCore.eddamp)
    def eddamp(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.eddamp()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().eddamp(*args, **kwargs)

    @wraps(_MapdlCore.eddrelax)
    def eddrelax(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.eddrelax()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().eddrelax(*args, **kwargs)

    @wraps(_MapdlCore.eddump)
    def eddump(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.eddump()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().eddump(*args, **kwargs)

    @wraps(_MapdlCore.edenergy)
    def edenergy(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edenergy()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edenergy(*args, **kwargs)

    @wraps(_MapdlCore.edfplot)
    def edfplot(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edfplot()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edfplot(*args, **kwargs)

    @wraps(_MapdlCore.edgcale)
    def edgcale(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edgcale()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edgcale(*args, **kwargs)

    @wraps(_MapdlCore.edhgls)
    def edhgls(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edhgls()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edhgls(*args, **kwargs)

    @wraps(_MapdlCore.edhist)
    def edhist(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edhist()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edhist(*args, **kwargs)

    @wraps(_MapdlCore.edhtime)
    def edhtime(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edhtime()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edhtime(*args, **kwargs)

    @wraps(_MapdlCore.edint)
    def edint(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edint()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edint(*args, **kwargs)

    @wraps(_MapdlCore.edis)
    def edis(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edis()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edis(*args, **kwargs)

    @wraps(_MapdlCore.edload)
    def edload(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edload()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edload(*args, **kwargs)

    @wraps(_MapdlCore.edopt)
    def edopt(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edopt()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edopt(*args, **kwargs)

    @wraps(_MapdlCore.edout)
    def edout(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edout()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edout(*args, **kwargs)

    @wraps(_MapdlCore.edpl)
    def edpl(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edpl()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edpl(*args, **kwargs)

    @wraps(_MapdlCore.edpvel)
    def edpvel(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edpvel()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edpvel(*args, **kwargs)

    @wraps(_MapdlCore.edrc)
    def edrc(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edrc()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edrc(*args, **kwargs)

    @wraps(_MapdlCore.edrd)
    def edrd(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edrd()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edrd(*args, **kwargs)

    @wraps(_MapdlCore.edri)
    def edri(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edri()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edri(*args, **kwargs)

    @wraps(_MapdlCore.edrst)
    def edrst(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edrst()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edrst(*args, **kwargs)

    @wraps(_MapdlCore.edrun)
    def edrun(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edrun()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edrun(*args, **kwargs)

    @wraps(_MapdlCore.edshell)
    def edshell(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edshell()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edshell(*args, **kwargs)

    @wraps(_MapdlCore.edsolv)
    def edsolv(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edsolv()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edsolv(*args, **kwargs)

    @wraps(_MapdlCore.edstart)
    def edstart(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edstart()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edstart(*args, **kwargs)

    @wraps(_MapdlCore.edterm)
    def edterm(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edterm()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edterm(*args, **kwargs)

    @wraps(_MapdlCore.edtp)
    def edtp(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edtp()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edtp(*args, **kwargs)

    @wraps(_MapdlCore.edvel)
    def edvel(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edvel()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edvel(*args, **kwargs)

    @wraps(_MapdlCore.edwrite)
    def edwrite(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edwrite()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edwrite(*args, **kwargs)

    @wraps(_MapdlCore.rexport)
    def rexport(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.rexport()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().rexport(*args, **kwargs)
