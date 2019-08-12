import warnings

class _DeprecCommands(object):
    """Contains all decpreciated functions for the mapdl interface.
    Will be removed in the future.
    """

    def Dalist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Dalist" decpreciated.  Use "dalist" instead'))
        return self.dalist(*args, **kwargs)

    def Space(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Space" decpreciated.  Use "space" instead'))
        return self.space(*args, **kwargs)

    def Sfbeam(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sfbeam" decpreciated.  Use "sfbeam" instead'))
        return self.sfbeam(*args, **kwargs)

    def Mopt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mopt" decpreciated.  Use "mopt" instead'))
        return self.mopt(*args, **kwargs)

    def Dv3d(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Dv3d" decpreciated.  Use "dv3d" instead'))
        return self.dv3d(*args, **kwargs)

    def Define(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Define" decpreciated.  Use "define" instead'))
        return self.define(*args, **kwargs)

    def Meshing(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Meshing" decpreciated.  Use "meshing" instead'))
        return self.meshing(*args, **kwargs)

    def Aplot(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Aplot" decpreciated.  Use "aplot" instead'))
        return self.aplot(*args, **kwargs)

    def Resp(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Resp" decpreciated.  Use "resp" instead'))
        return self.resp(*args, **kwargs)

    def Datadef(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Datadef" decpreciated.  Use "datadef" instead'))
        return self.datadef(*args, **kwargs)

    def Combine(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Combine" decpreciated.  Use "combine" instead'))
        return self.combine(*args, **kwargs)

    def Get(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Get" decpreciated.  Use "get" instead'))
        return self.get(*args, **kwargs)

    def Hbc(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Hbc" decpreciated.  Use "hbc" instead'))
        return self.hbc(*args, **kwargs)

    def Dfswave(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Dfswave" decpreciated.  Use "dfswave" instead'))
        return self.dfswave(*args, **kwargs)

    def Mptemp(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mptemp" decpreciated.  Use "mptemp" instead'))
        return self.mptemp(*args, **kwargs)

    def User(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"User" decpreciated.  Use "user" instead'))
        return self.user(*args, **kwargs)

    def Exprofile(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Exprofile" decpreciated.  Use "exprofile" instead'))
        return self.exprofile(*args, **kwargs)

    def Ulib(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ulib" decpreciated.  Use "ulib" instead'))
        return self.ulib(*args, **kwargs)

    def Gcdef(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Gcdef" decpreciated.  Use "gcdef" instead'))
        return self.gcdef(*args, **kwargs)

    def Sfa(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sfa" decpreciated.  Use "sfa" instead'))
        return self.sfa(*args, **kwargs)

    def Kfill(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Kfill" decpreciated.  Use "kfill" instead'))
        return self.kfill(*args, **kwargs)

    def Dsum(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Dsum" decpreciated.  Use "dsum" instead'))
        return self.dsum(*args, **kwargs)

    def Dist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Dist" decpreciated.  Use "dist" instead'))
        return self.dist(*args, **kwargs)

    def Endrelease(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Endrelease" decpreciated.  Use "endrelease" instead'))
        return self.endrelease(*args, **kwargs)

    def Ekill(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ekill" decpreciated.  Use "ekill" instead'))
        return self.ekill(*args, **kwargs)

    def Cp(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cp" decpreciated.  Use "cp" instead'))
        return self.cp(*args, **kwargs)

    def Outaero(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Outaero" decpreciated.  Use "outaero" instead'))
        return self.outaero(*args, **kwargs)

    def Point(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Point" decpreciated.  Use "point" instead'))
        return self.point(*args, **kwargs)

    def Fllist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Fllist" decpreciated.  Use "fllist" instead'))
        return self.fllist(*args, **kwargs)

    def Bss2(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Bss2" decpreciated.  Use "bss2" instead'))
        return self.bss2(*args, **kwargs)

    def Atype(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Atype" decpreciated.  Use "atype" instead'))
        return self.atype(*args, **kwargs)

    def Lplot(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lplot" decpreciated.  Use "lplot" instead'))
        return self.lplot(*args, **kwargs)

    def Afun(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Afun" decpreciated.  Use "afun" instead'))
        return self.afun(*args, **kwargs)

    def Dsys(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Dsys" decpreciated.  Use "dsys" instead'))
        return self.dsys(*args, **kwargs)

    def Mplist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mplist" decpreciated.  Use "mplist" instead'))
        return self.mplist(*args, **kwargs)

    def Vfquery(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vfquery" decpreciated.  Use "vfquery" instead'))
        return self.vfquery(*args, **kwargs)

    def Cqc(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cqc" decpreciated.  Use "cqc" instead'))
        return self.cqc(*args, **kwargs)

    def Vedit(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vedit" decpreciated.  Use "vedit" instead'))
        return self.vedit(*args, **kwargs)

    def Undelete(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Undelete" decpreciated.  Use "undelete" instead'))
        return self.undelete(*args, **kwargs)

    def Vglue(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vglue" decpreciated.  Use "vglue" instead'))
        return self.vglue(*args, **kwargs)

    def Mp(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mp" decpreciated.  Use "mp" instead'))
        return self.mp(*args, **kwargs)

    def Pdanl(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pdanl" decpreciated.  Use "pdanl" instead'))
        return self.pdanl(*args, **kwargs)

    def M(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"M" decpreciated.  Use "m" instead'))
        return self.m(*args, **kwargs)

    def Avres(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Avres" decpreciated.  Use "avres" instead'))
        return self.avres(*args, **kwargs)

    def Sueval(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sueval" decpreciated.  Use "sueval" instead'))
        return self.sueval(*args, **kwargs)

    def Ltran(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ltran" decpreciated.  Use "ltran" instead'))
        return self.ltran(*args, **kwargs)

    def Cint(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cint" decpreciated.  Use "cint" instead'))
        return self.cint(*args, **kwargs)

    def Mstole(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mstole" decpreciated.  Use "mstole" instead'))
        return self.mstole(*args, **kwargs)

    def Rmporder(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rmporder" decpreciated.  Use "rmporder" instead'))
        return self.rmporder(*args, **kwargs)

    def Edstart(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edstart" decpreciated.  Use "edstart" instead'))
        return self.edstart(*args, **kwargs)

    def Vrotat(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vrotat" decpreciated.  Use "vrotat" instead'))
        return self.vrotat(*args, **kwargs)

    def Icdele(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Icdele" decpreciated.  Use "icdele" instead'))
        return self.icdele(*args, **kwargs)

    def Nwpave(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Nwpave" decpreciated.  Use "nwpave" instead'))
        return self.nwpave(*args, **kwargs)

    def Bucopt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Bucopt" decpreciated.  Use "bucopt" instead'))
        return self.bucopt(*args, **kwargs)

    def Pstatus(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pstatus" decpreciated.  Use "pstatus" instead'))
        return self.pstatus(*args, **kwargs)

    def Lsclear(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lsclear" decpreciated.  Use "lsclear" instead'))
        return self.lsclear(*args, **kwargs)

    def Rmaster(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rmaster" decpreciated.  Use "rmaster" instead'))
        return self.rmaster(*args, **kwargs)

    def Vmask(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vmask" decpreciated.  Use "vmask" instead'))
        return self.vmask(*args, **kwargs)

    def Prvect(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Prvect" decpreciated.  Use "prvect" instead'))
        return self.prvect(*args, **kwargs)

    def Sfalist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sfalist" decpreciated.  Use "sfalist" instead'))
        return self.sfalist(*args, **kwargs)

    def Ldrag(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ldrag" decpreciated.  Use "ldrag" instead'))
        return self.ldrag(*args, **kwargs)

    def Fl(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Fl" decpreciated.  Use "fl" instead'))
        return self.fl(*args, **kwargs)

    def Angle(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Angle" decpreciated.  Use "angle" instead'))
        return self.angle(*args, **kwargs)

    def Slashtype(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Slashtype" decpreciated.  Use "slashtype" instead'))
        return self.slashtype(*args, **kwargs)

    def Sfcum(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sfcum" decpreciated.  Use "sfcum" instead'))
        return self.sfcum(*args, **kwargs)

    def Smult(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Smult" decpreciated.  Use "smult" instead'))
        return self.smult(*args, **kwargs)

    def Menu(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Menu" decpreciated.  Use "menu" instead'))
        return self.menu(*args, **kwargs)

    def Prerr(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Prerr" decpreciated.  Use "prerr" instead'))
        return self.prerr(*args, **kwargs)

    def Exp(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Exp" decpreciated.  Use "exp" instead'))
        return self.exp(*args, **kwargs)

    def Mfinter(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mfinter" decpreciated.  Use "mfinter" instead'))
        return self.mfinter(*args, **kwargs)

    def Ftsize(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ftsize" decpreciated.  Use "ftsize" instead'))
        return self.ftsize(*args, **kwargs)

    def Mfconv(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mfconv" decpreciated.  Use "mfconv" instead'))
        return self.mfconv(*args, **kwargs)

    def Spline(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Spline" decpreciated.  Use "spline" instead'))
        return self.spline(*args, **kwargs)

    def Kgen(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Kgen" decpreciated.  Use "kgen" instead'))
        return self.kgen(*args, **kwargs)

    def Secmodif(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Secmodif" decpreciated.  Use "secmodif" instead'))
        return self.secmodif(*args, **kwargs)

    def Eplot(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Eplot" decpreciated.  Use "eplot" instead'))
        return self.eplot(*args, **kwargs)

    def Aux15(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Aux15" decpreciated.  Use "aux15" instead'))
        return self.aux15(*args, **kwargs)

    def Dkdele(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Dkdele" decpreciated.  Use "dkdele" instead'))
        return self.dkdele(*args, **kwargs)

    def Edload(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edload" decpreciated.  Use "edload" instead'))
        return self.edload(*args, **kwargs)

    def Sedlist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sedlist" decpreciated.  Use "sedlist" instead'))
        return self.sedlist(*args, **kwargs)

    def Esurf(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Esurf" decpreciated.  Use "esurf" instead'))
        return self.esurf(*args, **kwargs)

    def Starvget(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Starvget" decpreciated.  Use "starvget" instead'))
        return self.starvget(*args, **kwargs)

    def Fileaux2(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Fileaux2" decpreciated.  Use "fileaux2" instead'))
        return self.fileaux2(*args, **kwargs)

    def Form(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Form" decpreciated.  Use "form" instead'))
        return self.form(*args, **kwargs)

    def Fklist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Fklist" decpreciated.  Use "fklist" instead'))
        return self.fklist(*args, **kwargs)

    def Dynopt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Dynopt" decpreciated.  Use "dynopt" instead'))
        return self.dynopt(*args, **kwargs)

    def Dmpext(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Dmpext" decpreciated.  Use "dmpext" instead'))
        return self.dmpext(*args, **kwargs)

    def Askin(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Askin" decpreciated.  Use "askin" instead'))
        return self.askin(*args, **kwargs)

    def Pwedge(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pwedge" decpreciated.  Use "pwedge" instead'))
        return self.pwedge(*args, **kwargs)

    def Vmesh(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vmesh" decpreciated.  Use "vmesh" instead'))
        return self.vmesh(*args, **kwargs)

    def Ask(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ask" decpreciated.  Use "ask" instead'))
        return self.ask(*args, **kwargs)

    def Csdele(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Csdele" decpreciated.  Use "csdele" instead'))
        return self.csdele(*args, **kwargs)

    def Uimp(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Uimp" decpreciated.  Use "uimp" instead'))
        return self.uimp(*args, **kwargs)

    def Omega(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Omega" decpreciated.  Use "omega" instead'))
        return self.omega(*args, **kwargs)

    def Lcomb(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lcomb" decpreciated.  Use "lcomb" instead'))
        return self.lcomb(*args, **kwargs)

    def Plchist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Plchist" decpreciated.  Use "plchist" instead'))
        return self.plchist(*args, **kwargs)

    def Gopr(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Gopr" decpreciated.  Use "gopr" instead'))
        return self.gopr(*args, **kwargs)

    def Supr(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Supr" decpreciated.  Use "supr" instead'))
        return self.supr(*args, **kwargs)

    def Czdel(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Czdel" decpreciated.  Use "czdel" instead'))
        return self.czdel(*args, **kwargs)

    def Powerh(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Powerh" decpreciated.  Use "powerh" instead'))
        return self.powerh(*args, **kwargs)

    def Suget(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Suget" decpreciated.  Use "suget" instead'))
        return self.suget(*args, **kwargs)

    def Aux12(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Aux12" decpreciated.  Use "aux12" instead'))
        return self.aux12(*args, **kwargs)

    def Lcsl(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lcsl" decpreciated.  Use "lcsl" instead'))
        return self.lcsl(*args, **kwargs)

    def Sdelete(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sdelete" decpreciated.  Use "sdelete" instead'))
        return self.sdelete(*args, **kwargs)

    def Pltrac(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pltrac" decpreciated.  Use "pltrac" instead'))
        return self.pltrac(*args, **kwargs)

    def Vlist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vlist" decpreciated.  Use "vlist" instead'))
        return self.vlist(*args, **kwargs)

    def Tsres(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Tsres" decpreciated.  Use "tsres" instead'))
        return self.tsres(*args, **kwargs)

    def Upgeom(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Upgeom" decpreciated.  Use "upgeom" instead'))
        return self.upgeom(*args, **kwargs)

    def Operate(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Operate" decpreciated.  Use "operate" instead'))
        return self.operate(*args, **kwargs)

    def Couple(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Couple" decpreciated.  Use "couple" instead'))
        return self.couple(*args, **kwargs)

    def Prpath(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Prpath" decpreciated.  Use "prpath" instead'))
        return self.prpath(*args, **kwargs)

    def Adgl(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Adgl" decpreciated.  Use "adgl" instead'))
        return self.adgl(*args, **kwargs)

    def Esort(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Esort" decpreciated.  Use "esort" instead'))
        return self.esort(*args, **kwargs)

    def Tbdata(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Tbdata" decpreciated.  Use "tbdata" instead'))
        return self.tbdata(*args, **kwargs)

    def Rpr4(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rpr4" decpreciated.  Use "rpr4" instead'))
        return self.rpr4(*args, **kwargs)

    def Yrange(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Yrange" decpreciated.  Use "yrange" instead'))
        return self.yrange(*args, **kwargs)

    def Pdcmat(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pdcmat" decpreciated.  Use "pdcmat" instead'))
        return self.pdcmat(*args, **kwargs)

    def Pmlopt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pmlopt" decpreciated.  Use "pmlopt" instead'))
        return self.pmlopt(*args, **kwargs)

    def Vfact(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vfact" decpreciated.  Use "vfact" instead'))
        return self.vfact(*args, **kwargs)

    def Rock(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rock" decpreciated.  Use "rock" instead'))
        return self.rock(*args, **kwargs)

    def Aux2(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Aux2" decpreciated.  Use "aux2" instead'))
        return self.aux2(*args, **kwargs)

    def Bste(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Bste" decpreciated.  Use "bste" instead'))
        return self.bste(*args, **kwargs)

    def Mfiter(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mfiter" decpreciated.  Use "mfiter" instead'))
        return self.mfiter(*args, **kwargs)

    def Bf(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Bf" decpreciated.  Use "bf" instead'))
        return self.bf(*args, **kwargs)

    def Octype(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Octype" decpreciated.  Use "octype" instead'))
        return self.octype(*args, **kwargs)

    def Lcase(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lcase" decpreciated.  Use "lcase" instead'))
        return self.lcase(*args, **kwargs)

    def Amesh(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Amesh" decpreciated.  Use "amesh" instead'))
        return self.amesh(*args, **kwargs)

    def Lines(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lines" decpreciated.  Use "lines" instead'))
        return self.lines(*args, **kwargs)

    def Psf(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Psf" decpreciated.  Use "psf" instead'))
        return self.psf(*args, **kwargs)

    def Mpread(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mpread" decpreciated.  Use "mpread" instead'))
        return self.mpread(*args, **kwargs)

    def Comp(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Comp" decpreciated.  Use "comp" instead'))
        return self.comp(*args, **kwargs)

    def Toper(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Toper" decpreciated.  Use "toper" instead'))
        return self.toper(*args, **kwargs)

    def Andscl(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Andscl" decpreciated.  Use "andscl" instead'))
        return self.andscl(*args, **kwargs)

    def Bfcum(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Bfcum" decpreciated.  Use "bfcum" instead'))
        return self.bfcum(*args, **kwargs)

    def Segen(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Segen" decpreciated.  Use "segen" instead'))
        return self.segen(*args, **kwargs)

    def Sfscale(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sfscale" decpreciated.  Use "sfscale" instead'))
        return self.sfscale(*args, **kwargs)

    def Mpchg(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mpchg" decpreciated.  Use "mpchg" instead'))
        return self.mpchg(*args, **kwargs)

    def Smooth(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Smooth" decpreciated.  Use "smooth" instead'))
        return self.smooth(*args, **kwargs)

    def Modmsh(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Modmsh" decpreciated.  Use "modmsh" instead'))
        return self.modmsh(*args, **kwargs)

    def Cycle(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cycle" decpreciated.  Use "cycle" instead'))
        return self.cycle(*args, **kwargs)

    def V2dopt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"V2dopt" decpreciated.  Use "v2dopt" instead'))
        return self.v2dopt(*args, **kwargs)

    def Perturb(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Perturb" decpreciated.  Use "perturb" instead'))
        return self.perturb(*args, **kwargs)

    def Timp(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Timp" decpreciated.  Use "timp" instead'))
        return self.timp(*args, **kwargs)

    def Psdcom(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Psdcom" decpreciated.  Use "psdcom" instead'))
        return self.psdcom(*args, **kwargs)

    def Dcgomg(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Dcgomg" decpreciated.  Use "dcgomg" instead'))
        return self.dcgomg(*args, **kwargs)

    def Cgloc(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cgloc" decpreciated.  Use "cgloc" instead'))
        return self.cgloc(*args, **kwargs)

    def Vlen(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vlen" decpreciated.  Use "vlen" instead'))
        return self.vlen(*args, **kwargs)

    def Spread(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Spread" decpreciated.  Use "spread" instead'))
        return self.spread(*args, **kwargs)

    def Selm(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Selm" decpreciated.  Use "selm" instead'))
        return self.selm(*args, **kwargs)

    def Edopt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edopt" decpreciated.  Use "edopt" instead'))
        return self.edopt(*args, **kwargs)

    def Spower(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Spower" decpreciated.  Use "spower" instead'))
        return self.spower(*args, **kwargs)

    def Tbtemp(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Tbtemp" decpreciated.  Use "tbtemp" instead'))
        return self.tbtemp(*args, **kwargs)

    def Uis(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Uis" decpreciated.  Use "uis" instead'))
        return self.uis(*args, **kwargs)

    def Resvec(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Resvec" decpreciated.  Use "resvec" instead'))
        return self.resvec(*args, **kwargs)

    def Boptn(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Boptn" decpreciated.  Use "boptn" instead'))
        return self.boptn(*args, **kwargs)

    def Fplist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Fplist" decpreciated.  Use "fplist" instead'))
        return self.fplist(*args, **kwargs)

    def Rmrplot(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rmrplot" decpreciated.  Use "rmrplot" instead'))
        return self.rmrplot(*args, **kwargs)

    def Cntr(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cntr" decpreciated.  Use "cntr" instead'))
        return self.cntr(*args, **kwargs)

    def Pdwrite(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pdwrite" decpreciated.  Use "pdwrite" instead'))
        return self.pdwrite(*args, **kwargs)

    def Rcon(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rcon" decpreciated.  Use "rcon" instead'))
        return self.rcon(*args, **kwargs)

    def Eddrelax(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Eddrelax" decpreciated.  Use "eddrelax" instead'))
        return self.eddrelax(*args, **kwargs)

    def Secfunction(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Secfunction" decpreciated.  Use "secfunction" instead'))
        return self.secfunction(*args, **kwargs)

    def Sfe(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sfe" decpreciated.  Use "sfe" instead'))
        return self.sfe(*args, **kwargs)

    def Esel(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Esel" decpreciated.  Use "esel" instead'))
        return self.esel(*args, **kwargs)

    def Swadd(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Swadd" decpreciated.  Use "swadd" instead'))
        return self.swadd(*args, **kwargs)

    def Export(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Export" decpreciated.  Use "export" instead'))
        return self.export(*args, **kwargs)

    def Mdele(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mdele" decpreciated.  Use "mdele" instead'))
        return self.mdele(*args, **kwargs)

    def Bfint(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Bfint" decpreciated.  Use "bfint" instead'))
        return self.bfint(*args, **kwargs)

    def Veorient(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Veorient" decpreciated.  Use "veorient" instead'))
        return self.veorient(*args, **kwargs)

    def Plsect(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Plsect" decpreciated.  Use "plsect" instead'))
        return self.plsect(*args, **kwargs)

    def Nforce(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Nforce" decpreciated.  Use "nforce" instead'))
        return self.nforce(*args, **kwargs)

    def Edread(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edread" decpreciated.  Use "edread" instead'))
        return self.edread(*args, **kwargs)

    def Rimport(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rimport" decpreciated.  Use "rimport" instead'))
        return self.rimport(*args, **kwargs)

    def Mapsolve(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mapsolve" decpreciated.  Use "mapsolve" instead'))
        return self.mapsolve(*args, **kwargs)

    def Vitrp(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vitrp" decpreciated.  Use "vitrp" instead'))
        return self.vitrp(*args, **kwargs)

    def Race(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Race" decpreciated.  Use "race" instead'))
        return self.race(*args, **kwargs)

    def Mffr(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mffr" decpreciated.  Use "mffr" instead'))
        return self.mffr(*args, **kwargs)

    def Sspm(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sspm" decpreciated.  Use "sspm" instead'))
        return self.sspm(*args, **kwargs)

    def Iclwid(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Iclwid" decpreciated.  Use "iclwid" instead'))
        return self.iclwid(*args, **kwargs)

    def Xvar(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Xvar" decpreciated.  Use "xvar" instead'))
        return self.xvar(*args, **kwargs)

    def Nrefine(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Nrefine" decpreciated.  Use "nrefine" instead'))
        return self.nrefine(*args, **kwargs)

    def Cpsgen(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cpsgen" decpreciated.  Use "cpsgen" instead'))
        return self.cpsgen(*args, **kwargs)

    def Bool(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Bool" decpreciated.  Use "bool" instead'))
        return self.bool(*args, **kwargs)

    def Path(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Path" decpreciated.  Use "path" instead'))
        return self.path(*args, **kwargs)

    def Rescombine(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rescombine" decpreciated.  Use "rescombine" instead'))
        return self.rescombine(*args, **kwargs)

    def Kcalc(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Kcalc" decpreciated.  Use "kcalc" instead'))
        return self.kcalc(*args, **kwargs)

    def Cgrow(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cgrow" decpreciated.  Use "cgrow" instead'))
        return self.cgrow(*args, **kwargs)

    def Svplot(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Svplot" decpreciated.  Use "svplot" instead'))
        return self.svplot(*args, **kwargs)

    def Plfar(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Plfar" decpreciated.  Use "plfar" instead'))
        return self.plfar(*args, **kwargs)

    def Mode(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mode" decpreciated.  Use "mode" instead'))
        return self.mode(*args, **kwargs)

    def Prnear(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Prnear" decpreciated.  Use "prnear" instead'))
        return self.prnear(*args, **kwargs)

    def Sf(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sf" decpreciated.  Use "sf" instead'))
        return self.sf(*args, **kwargs)

    def Awave(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Awave" decpreciated.  Use "awave" instead'))
        return self.awave(*args, **kwargs)

    def Llist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Llist" decpreciated.  Use "llist" instead'))
        return self.llist(*args, **kwargs)

    def Cisol(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cisol" decpreciated.  Use "cisol" instead'))
        return self.cisol(*args, **kwargs)

    def Antime(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Antime" decpreciated.  Use "antime" instead'))
        return self.antime(*args, **kwargs)

    def List(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"List" decpreciated.  Use "list" instead'))
        return self.list(*args, **kwargs)

    def Sfldele(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sfldele" decpreciated.  Use "sfldele" instead'))
        return self.sfldele(*args, **kwargs)

    def Nrlsum(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Nrlsum" decpreciated.  Use "nrlsum" instead'))
        return self.nrlsum(*args, **kwargs)

    def End(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"End" decpreciated.  Use "end" instead'))
        return self.end(*args, **kwargs)

    def Fslist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Fslist" decpreciated.  Use "fslist" instead'))
        return self.fslist(*args, **kwargs)

    def Lclear(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lclear" decpreciated.  Use "lclear" instead'))
        return self.lclear(*args, **kwargs)

    def Mfsorder(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mfsorder" decpreciated.  Use "mfsorder" instead'))
        return self.mfsorder(*args, **kwargs)

    def Numoff(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Numoff" decpreciated.  Use "numoff" instead'))
        return self.numoff(*args, **kwargs)

    def Perbc2d(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Perbc2d" decpreciated.  Use "perbc2d" instead'))
        return self.perbc2d(*args, **kwargs)

    def Shrink(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Shrink" decpreciated.  Use "shrink" instead'))
        return self.shrink(*args, **kwargs)

    def Biot(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Biot" decpreciated.  Use "biot" instead'))
        return self.biot(*args, **kwargs)

    def Nusort(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Nusort" decpreciated.  Use "nusort" instead'))
        return self.nusort(*args, **kwargs)

    def Devdisp(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Devdisp" decpreciated.  Use "devdisp" instead'))
        return self.devdisp(*args, **kwargs)

    def Triad(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Triad" decpreciated.  Use "triad" instead'))
        return self.triad(*args, **kwargs)

    def Alphad(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Alphad" decpreciated.  Use "alphad" instead'))
        return self.alphad(*args, **kwargs)

    def Psdunit(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Psdunit" decpreciated.  Use "psdunit" instead'))
        return self.psdunit(*args, **kwargs)

    def Paput(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Paput" decpreciated.  Use "paput" instead'))
        return self.paput(*args, **kwargs)

    def Ansol(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ansol" decpreciated.  Use "ansol" instead'))
        return self.ansol(*args, **kwargs)

    def Move(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Move" decpreciated.  Use "move" instead'))
        return self.move(*args, **kwargs)

    def Synchro(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Synchro" decpreciated.  Use "synchro" instead'))
        return self.synchro(*args, **kwargs)

    def Lgen(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lgen" decpreciated.  Use "lgen" instead'))
        return self.lgen(*args, **kwargs)

    def Seclock(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Seclock" decpreciated.  Use "seclock" instead'))
        return self.seclock(*args, **kwargs)

    def Sumtype(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sumtype" decpreciated.  Use "sumtype" instead'))
        return self.sumtype(*args, **kwargs)

    def Spdamp(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Spdamp" decpreciated.  Use "spdamp" instead'))
        return self.spdamp(*args, **kwargs)

    def Nsol(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Nsol" decpreciated.  Use "nsol" instead'))
        return self.nsol(*args, **kwargs)

    def Eread(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Eread" decpreciated.  Use "eread" instead'))
        return self.eread(*args, **kwargs)

    def Fccheck(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Fccheck" decpreciated.  Use "fccheck" instead'))
        return self.fccheck(*args, **kwargs)

    def Vsbw(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vsbw" decpreciated.  Use "vsbw" instead'))
        return self.vsbw(*args, **kwargs)

    def Seccontrol(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Seccontrol" decpreciated.  Use "seccontrol" instead'))
        return self.seccontrol(*args, **kwargs)

    def Kwplan(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Kwplan" decpreciated.  Use "kwplan" instead'))
        return self.kwplan(*args, **kwargs)

    def Anorm(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Anorm" decpreciated.  Use "anorm" instead'))
        return self.anorm(*args, **kwargs)

    def Vsla(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vsla" decpreciated.  Use "vsla" instead'))
        return self.vsla(*args, **kwargs)

    def Vimp(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vimp" decpreciated.  Use "vimp" instead'))
        return self.vimp(*args, **kwargs)

    def Edlcs(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edlcs" decpreciated.  Use "edlcs" instead'))
        return self.edlcs(*args, **kwargs)

    def Mptres(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mptres" decpreciated.  Use "mptres" instead'))
        return self.mptres(*args, **kwargs)

    def Mkdir(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mkdir" decpreciated.  Use "mkdir" instead'))
        return self.mkdir(*args, **kwargs)

    def Tb(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Tb" decpreciated.  Use "tb" instead'))
        return self.tb(*args, **kwargs)

    def Vstat(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vstat" decpreciated.  Use "vstat" instead'))
        return self.vstat(*args, **kwargs)

    def Clog(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Clog" decpreciated.  Use "clog" instead'))
        return self.clog(*args, **kwargs)

    def Spval(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Spval" decpreciated.  Use "spval" instead'))
        return self.spval(*args, **kwargs)

    def Plopts(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Plopts" decpreciated.  Use "plopts" instead'))
        return self.plopts(*args, **kwargs)

    def Sesymm(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sesymm" decpreciated.  Use "sesymm" instead'))
        return self.sesymm(*args, **kwargs)

    def Pcircle(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pcircle" decpreciated.  Use "pcircle" instead'))
        return self.pcircle(*args, **kwargs)

    def Bfllist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Bfllist" decpreciated.  Use "bfllist" instead'))
        return self.bfllist(*args, **kwargs)

    def Anharm(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Anharm" decpreciated.  Use "anharm" instead'))
        return self.anharm(*args, **kwargs)

    def Et(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Et" decpreciated.  Use "et" instead'))
        return self.et(*args, **kwargs)

    def Slashdelete(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Slashdelete" decpreciated.  Use "slashdelete" instead'))
        return self.slashdelete(*args, **kwargs)

    def Linp(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Linp" decpreciated.  Use "linp" instead'))
        return self.linp(*args, **kwargs)

    def Psdspl(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Psdspl" decpreciated.  Use "psdspl" instead'))
        return self.psdspl(*args, **kwargs)

    def Lcoper(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lcoper" decpreciated.  Use "lcoper" instead'))
        return self.lcoper(*args, **kwargs)

    def Aoffst(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Aoffst" decpreciated.  Use "aoffst" instead'))
        return self.aoffst(*args, **kwargs)

    def Cmedit(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cmedit" decpreciated.  Use "cmedit" instead'))
        return self.cmedit(*args, **kwargs)

    def Plnsol(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Plnsol" decpreciated.  Use "plnsol" instead'))
        return self.plnsol(*args, **kwargs)

    def Circle(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Circle" decpreciated.  Use "circle" instead'))
        return self.circle(*args, **kwargs)

    def Save(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Save" decpreciated.  Use "save" instead'))
        return self.save(*args, **kwargs)

    def Cbte(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cbte" decpreciated.  Use "cbte" instead'))
        return self.cbte(*args, **kwargs)

    def Pmap(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pmap" decpreciated.  Use "pmap" instead'))
        return self.pmap(*args, **kwargs)

    def Bflist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Bflist" decpreciated.  Use "bflist" instead'))
        return self.bflist(*args, **kwargs)

    def Cyl4(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cyl4" decpreciated.  Use "cyl4" instead'))
        return self.cyl4(*args, **kwargs)

    def Aux3(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Aux3" decpreciated.  Use "aux3" instead'))
        return self.aux3(*args, **kwargs)

    def Vscfun(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vscfun" decpreciated.  Use "vscfun" instead'))
        return self.vscfun(*args, **kwargs)

    def Hpgl(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Hpgl" decpreciated.  Use "hpgl" instead'))
        return self.hpgl(*args, **kwargs)

    def Smat(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Smat" decpreciated.  Use "smat" instead'))
        return self.smat(*args, **kwargs)

    def Edhgls(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edhgls" decpreciated.  Use "edhgls" instead'))
        return self.edhgls(*args, **kwargs)

    def Eddbl(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Eddbl" decpreciated.  Use "eddbl" instead'))
        return self.eddbl(*args, **kwargs)

    def Rexport(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rexport" decpreciated.  Use "rexport" instead'))
        return self.rexport(*args, **kwargs)

    def Arsym(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Arsym" decpreciated.  Use "arsym" instead'))
        return self.arsym(*args, **kwargs)

    def Secwrite(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Secwrite" decpreciated.  Use "secwrite" instead'))
        return self.secwrite(*args, **kwargs)

    def Emtgen(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Emtgen" decpreciated.  Use "emtgen" instead'))
        return self.emtgen(*args, **kwargs)

    def Dim(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Dim" decpreciated.  Use "dim" instead'))
        return self.dim(*args, **kwargs)

    def Line(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Line" decpreciated.  Use "line" instead'))
        return self.line(*args, **kwargs)

    def Emunit(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Emunit" decpreciated.  Use "emunit" instead'))
        return self.emunit(*args, **kwargs)

    def Lextnd(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lextnd" decpreciated.  Use "lextnd" instead'))
        return self.lextnd(*args, **kwargs)

    def Soluopt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Soluopt" decpreciated.  Use "soluopt" instead'))
        return self.soluopt(*args, **kwargs)

    def Ngen(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ngen" decpreciated.  Use "ngen" instead'))
        return self.ngen(*args, **kwargs)

    def Term(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Term" decpreciated.  Use "term" instead'))
        return self.term(*args, **kwargs)

    def Units(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Units" decpreciated.  Use "units" instead'))
        return self.units(*args, **kwargs)

    def Fp(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Fp" decpreciated.  Use "fp" instead'))
        return self.fp(*args, **kwargs)

    def Small(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Small" decpreciated.  Use "small" instead'))
        return self.small(*args, **kwargs)

    def Sload(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sload" decpreciated.  Use "sload" instead'))
        return self.sload(*args, **kwargs)

    def Lsla(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lsla" decpreciated.  Use "lsla" instead'))
        return self.lsla(*args, **kwargs)

    def Cat5in(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cat5in" decpreciated.  Use "cat5in" instead'))
        return self.cat5in(*args, **kwargs)

    def Ftwrite(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ftwrite" decpreciated.  Use "ftwrite" instead'))
        return self.ftwrite(*args, **kwargs)

    def Facet(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Facet" decpreciated.  Use "facet" instead'))
        return self.facet(*args, **kwargs)

    def Damorph(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Damorph" decpreciated.  Use "damorph" instead'))
        return self.damorph(*args, **kwargs)

    def Do(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Do" decpreciated.  Use "do" instead'))
        return self.do(*args, **kwargs)

    def Keyw(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Keyw" decpreciated.  Use "keyw" instead'))
        return self.keyw(*args, **kwargs)

    def Dnsol(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Dnsol" decpreciated.  Use "dnsol" instead'))
        return self.dnsol(*args, **kwargs)

    def Bsplin(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Bsplin" decpreciated.  Use "bsplin" instead'))
        return self.bsplin(*args, **kwargs)

    def Fs(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Fs" decpreciated.  Use "fs" instead'))
        return self.fs(*args, **kwargs)

    def Gresume(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Gresume" decpreciated.  Use "gresume" instead'))
        return self.gresume(*args, **kwargs)

    def Mstart(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mstart" decpreciated.  Use "mstart" instead'))
        return self.mstart(*args, **kwargs)

    def Lptn(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lptn" decpreciated.  Use "lptn" instead'))
        return self.lptn(*args, **kwargs)

    def Mrep(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mrep" decpreciated.  Use "mrep" instead'))
        return self.mrep(*args, **kwargs)

    def Edmp(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edmp" decpreciated.  Use "edmp" instead'))
        return self.edmp(*args, **kwargs)

    def Vext(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vext" decpreciated.  Use "vext" instead'))
        return self.vext(*args, **kwargs)

    def Aptn(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Aptn" decpreciated.  Use "aptn" instead'))
        return self.aptn(*args, **kwargs)

    def Outpr(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Outpr" decpreciated.  Use "outpr" instead'))
        return self.outpr(*args, **kwargs)

    def Mshmid(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mshmid" decpreciated.  Use "mshmid" instead'))
        return self.mshmid(*args, **kwargs)

    def Plpath(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Plpath" decpreciated.  Use "plpath" instead'))
        return self.plpath(*args, **kwargs)

    def Dscale(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Dscale" decpreciated.  Use "dscale" instead'))
        return self.dscale(*args, **kwargs)

    def Pdresu(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pdresu" decpreciated.  Use "pdresu" instead'))
        return self.pdresu(*args, **kwargs)

    def Allsel(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Allsel" decpreciated.  Use "allsel" instead'))
        return self.allsel(*args, **kwargs)

    def Lcfile(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lcfile" decpreciated.  Use "lcfile" instead'))
        return self.lcfile(*args, **kwargs)

    def Nopr(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Nopr" decpreciated.  Use "nopr" instead'))
        return self.nopr(*args, **kwargs)

    def Psdgraph(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Psdgraph" decpreciated.  Use "psdgraph" instead'))
        return self.psdgraph(*args, **kwargs)

    def Wmid(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Wmid" decpreciated.  Use "wmid" instead'))
        return self.wmid(*args, **kwargs)

    def Plmap(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Plmap" decpreciated.  Use "plmap" instead'))
        return self.plmap(*args, **kwargs)

    def Ctype(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ctype" decpreciated.  Use "ctype" instead'))
        return self.ctype(*args, **kwargs)

    def Nerr(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Nerr" decpreciated.  Use "nerr" instead'))
        return self.nerr(*args, **kwargs)

    def Numexp(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Numexp" decpreciated.  Use "numexp" instead'))
        return self.numexp(*args, **kwargs)

    def Aslv(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Aslv" decpreciated.  Use "aslv" instead'))
        return self.aslv(*args, **kwargs)

    def Target(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Target" decpreciated.  Use "target" instead'))
        return self.target(*args, **kwargs)

    def Pduser(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pduser" decpreciated.  Use "pduser" instead'))
        return self.pduser(*args, **kwargs)

    def Lvscale(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lvscale" decpreciated.  Use "lvscale" instead'))
        return self.lvscale(*args, **kwargs)

    def Eqslv(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Eqslv" decpreciated.  Use "eqslv" instead'))
        return self.eqslv(*args, **kwargs)

    def Cycopt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cycopt" decpreciated.  Use "cycopt" instead'))
        return self.cycopt(*args, **kwargs)

    def Plcfreq(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Plcfreq" decpreciated.  Use "plcfreq" instead'))
        return self.plcfreq(*args, **kwargs)

    def Nslv(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Nslv" decpreciated.  Use "nslv" instead'))
        return self.nslv(*args, **kwargs)

    def Larc(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Larc" decpreciated.  Use "larc" instead'))
        return self.larc(*args, **kwargs)

    def Sfllist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sfllist" decpreciated.  Use "sfllist" instead'))
        return self.sfllist(*args, **kwargs)

    def Fjlist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Fjlist" decpreciated.  Use "fjlist" instead'))
        return self.fjlist(*args, **kwargs)

    def Nsort(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Nsort" decpreciated.  Use "nsort" instead'))
        return self.nsort(*args, **kwargs)

    def Pcopy(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pcopy" decpreciated.  Use "pcopy" instead'))
        return self.pcopy(*args, **kwargs)

    def Cycphase(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cycphase" decpreciated.  Use "cycphase" instead'))
        return self.cycphase(*args, **kwargs)

    def Einfin(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Einfin" decpreciated.  Use "einfin" instead'))
        return self.einfin(*args, **kwargs)

    def Lesize(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lesize" decpreciated.  Use "lesize" instead'))
        return self.lesize(*args, **kwargs)

    def Rename(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rename" decpreciated.  Use "rename" instead'))
        return self.rename(*args, **kwargs)

    def Edcsc(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edcsc" decpreciated.  Use "edcsc" instead'))
        return self.edcsc(*args, **kwargs)

    def Madapt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Madapt" decpreciated.  Use "madapt" instead'))
        return self.madapt(*args, **kwargs)

    def Mflcomm(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mflcomm" decpreciated.  Use "mflcomm" instead'))
        return self.mflcomm(*args, **kwargs)

    def Ednrot(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ednrot" decpreciated.  Use "ednrot" instead'))
        return self.ednrot(*args, **kwargs)

    def Lsbac(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lsbac" decpreciated.  Use "lsbac" instead'))
        return self.lsbac(*args, **kwargs)

    def Prnsol(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Prnsol" decpreciated.  Use "prnsol" instead'))
        return self.prnsol(*args, **kwargs)

    def Pscr(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pscr" decpreciated.  Use "pscr" instead'))
        return self.pscr(*args, **kwargs)

    def Stargo(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Stargo" decpreciated.  Use "stargo" instead'))
        return self.stargo(*args, **kwargs)

    def Resume(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Resume" decpreciated.  Use "resume" instead'))
        return self.resume(*args, **kwargs)

    def Mfanalysis(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mfanalysis" decpreciated.  Use "mfanalysis" instead'))
        return self.mfanalysis(*args, **kwargs)

    def Coriolis(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Coriolis" decpreciated.  Use "coriolis" instead'))
        return self.coriolis(*args, **kwargs)

    def Taxis(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Taxis" decpreciated.  Use "taxis" instead'))
        return self.taxis(*args, **kwargs)

    def Replot(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Replot" decpreciated.  Use "replot" instead'))
        return self.replot(*args, **kwargs)

    def Mail(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mail" decpreciated.  Use "mail" instead'))
        return self.mail(*args, **kwargs)

    def Elem(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Elem" decpreciated.  Use "elem" instead'))
        return self.elem(*args, **kwargs)

    def Sectype(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sectype" decpreciated.  Use "sectype" instead'))
        return self.sectype(*args, **kwargs)

    def Prod(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Prod" decpreciated.  Use "prod" instead'))
        return self.prod(*args, **kwargs)

    def Fitem(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Fitem" decpreciated.  Use "fitem" instead'))
        return self.fitem(*args, **kwargs)

    def Expand(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Expand" decpreciated.  Use "expand" instead'))
        return self.expand(*args, **kwargs)

    def Bioopt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Bioopt" decpreciated.  Use "bioopt" instead'))
        return self.bioopt(*args, **kwargs)

    def Rappnd(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rappnd" decpreciated.  Use "rappnd" instead'))
        return self.rappnd(*args, **kwargs)

    def Sph5(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sph5" decpreciated.  Use "sph5" instead'))
        return self.sph5(*args, **kwargs)

    def Pcalc(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pcalc" decpreciated.  Use "pcalc" instead'))
        return self.pcalc(*args, **kwargs)

    def Rcyc(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rcyc" decpreciated.  Use "rcyc" instead'))
        return self.rcyc(*args, **kwargs)

    def Kpscale(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Kpscale" decpreciated.  Use "kpscale" instead'))
        return self.kpscale(*args, **kwargs)

    def Vfopt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vfopt" decpreciated.  Use "vfopt" instead'))
        return self.vfopt(*args, **kwargs)

    def Wrk(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Wrk" decpreciated.  Use "wrk" instead'))
        return self.wrk(*args, **kwargs)

    def Fill(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Fill" decpreciated.  Use "fill" instead'))
        return self.fill(*args, **kwargs)

    def Vsymm(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vsymm" decpreciated.  Use "vsymm" instead'))
        return self.vsymm(*args, **kwargs)

    def Nscale(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Nscale" decpreciated.  Use "nscale" instead'))
        return self.nscale(*args, **kwargs)

    def Sptopt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sptopt" decpreciated.  Use "sptopt" instead'))
        return self.sptopt(*args, **kwargs)

    def Plvect(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Plvect" decpreciated.  Use "plvect" instead'))
        return self.plvect(*args, **kwargs)

    def Master(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Master" decpreciated.  Use "master" instead'))
        return self.master(*args, **kwargs)

    def Dl(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Dl" decpreciated.  Use "dl" instead'))
        return self.dl(*args, **kwargs)

    def Presol(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Presol" decpreciated.  Use "presol" instead'))
        return self.presol(*args, **kwargs)

    def Rmroptions(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rmroptions" decpreciated.  Use "rmroptions" instead'))
        return self.rmroptions(*args, **kwargs)

    def Finish(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Finish" decpreciated.  Use "finish" instead'))
        return self.finish(*args, **kwargs)

    def Data(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Data" decpreciated.  Use "data" instead'))
        return self.data(*args, **kwargs)

    def Desol(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Desol" decpreciated.  Use "desol" instead'))
        return self.desol(*args, **kwargs)

    def Emid(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Emid" decpreciated.  Use "emid" instead'))
        return self.emid(*args, **kwargs)

    def Sucr(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sucr" decpreciated.  Use "sucr" instead'))
        return self.sucr(*args, **kwargs)

    def Mfbucket(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mfbucket" decpreciated.  Use "mfbucket" instead'))
        return self.mfbucket(*args, **kwargs)

    def Toffst(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Toffst" decpreciated.  Use "toffst" instead'))
        return self.toffst(*args, **kwargs)

    def Eddump(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Eddump" decpreciated.  Use "eddump" instead'))
        return self.eddump(*args, **kwargs)

    def Gauge(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Gauge" decpreciated.  Use "gauge" instead'))
        return self.gauge(*args, **kwargs)

    def Psdfrq(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Psdfrq" decpreciated.  Use "psdfrq" instead'))
        return self.psdfrq(*args, **kwargs)

    def Gcmd(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Gcmd" decpreciated.  Use "gcmd" instead'))
        return self.gcmd(*args, **kwargs)

    def Remesh(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Remesh" decpreciated.  Use "remesh" instead'))
        return self.remesh(*args, **kwargs)

    def Etchg(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Etchg" decpreciated.  Use "etchg" instead'))
        return self.etchg(*args, **kwargs)

    def Ksll(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ksll" decpreciated.  Use "ksll" instead'))
        return self.ksll(*args, **kwargs)

    def Gsum(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Gsum" decpreciated.  Use "gsum" instead'))
        return self.gsum(*args, **kwargs)

    def Polygon(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Polygon" decpreciated.  Use "polygon" instead'))
        return self.polygon(*args, **kwargs)

    def Geom(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Geom" decpreciated.  Use "geom" instead'))
        return self.geom(*args, **kwargs)

    def Gmface(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Gmface" decpreciated.  Use "gmface" instead'))
        return self.gmface(*args, **kwargs)

    def Cutcontrol(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cutcontrol" decpreciated.  Use "cutcontrol" instead'))
        return self.cutcontrol(*args, **kwargs)

    def Xflist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Xflist" decpreciated.  Use "xflist" instead'))
        return self.xflist(*args, **kwargs)

    def Use(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Use" decpreciated.  Use "use" instead'))
        return self.use(*args, **kwargs)

    def Abextract(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Abextract" decpreciated.  Use "abextract" instead'))
        return self.abextract(*args, **kwargs)

    def Pstres(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pstres" decpreciated.  Use "pstres" instead'))
        return self.pstres(*args, **kwargs)

    def Showdisp(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Showdisp" decpreciated.  Use "showdisp" instead'))
        return self.showdisp(*args, **kwargs)

    def Ltan(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ltan" decpreciated.  Use "ltan" instead'))
        return self.ltan(*args, **kwargs)

    def Nwrite(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Nwrite" decpreciated.  Use "nwrite" instead'))
        return self.nwrite(*args, **kwargs)

    def Pdplot(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pdplot" decpreciated.  Use "pdplot" instead'))
        return self.pdplot(*args, **kwargs)

    def Partsel(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Partsel" decpreciated.  Use "partsel" instead'))
        return self.partsel(*args, **kwargs)

    def Campbell(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Campbell" decpreciated.  Use "campbell" instead'))
        return self.campbell(*args, **kwargs)

    def Rmrgenerate(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rmrgenerate" decpreciated.  Use "rmrgenerate" instead'))
        return self.rmrgenerate(*args, **kwargs)

    def Expsol(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Expsol" decpreciated.  Use "expsol" instead'))
        return self.expsol(*args, **kwargs)

    def Vptn(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vptn" decpreciated.  Use "vptn" instead'))
        return self.vptn(*args, **kwargs)

    def Vcum(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vcum" decpreciated.  Use "vcum" instead'))
        return self.vcum(*args, **kwargs)

    def En(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"En" decpreciated.  Use "en" instead'))
        return self.en(*args, **kwargs)

    def Lccat(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lccat" decpreciated.  Use "lccat" instead'))
        return self.lccat(*args, **kwargs)

    def Cplgen(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cplgen" decpreciated.  Use "cplgen" instead'))
        return self.cplgen(*args, **kwargs)

    def Nooffset(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Nooffset" decpreciated.  Use "nooffset" instead'))
        return self.nooffset(*args, **kwargs)

    def Edbound(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edbound" decpreciated.  Use "edbound" instead'))
        return self.edbound(*args, **kwargs)

    def Starvplot(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Starvplot" decpreciated.  Use "starvplot" instead'))
        return self.starvplot(*args, **kwargs)

    def Rpsd(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rpsd" decpreciated.  Use "rpsd" instead'))
        return self.rpsd(*args, **kwargs)

    def Da(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Da" decpreciated.  Use "da" instead'))
        return self.da(*args, **kwargs)

    def Dvmorph(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Dvmorph" decpreciated.  Use "dvmorph" instead'))
        return self.dvmorph(*args, **kwargs)

    def Enersol(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Enersol" decpreciated.  Use "enersol" instead'))
        return self.enersol(*args, **kwargs)

    def Mfexter(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mfexter" decpreciated.  Use "mfexter" instead'))
        return self.mfexter(*args, **kwargs)

    def Ematwrite(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ematwrite" decpreciated.  Use "ematwrite" instead'))
        return self.ematwrite(*args, **kwargs)

    def Spec(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Spec" decpreciated.  Use "spec" instead'))
        return self.spec(*args, **kwargs)

    def Edge(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edge" decpreciated.  Use "edge" instead'))
        return self.edge(*args, **kwargs)

    def Input(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Input" decpreciated.  Use "input" instead'))
        return self.input(*args, **kwargs)

    def Bfdele(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Bfdele" decpreciated.  Use "bfdele" instead'))
        return self.bfdele(*args, **kwargs)

    def Wstart(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Wstart" decpreciated.  Use "wstart" instead'))
        return self.wstart(*args, **kwargs)

    def Afsurf(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Afsurf" decpreciated.  Use "afsurf" instead'))
        return self.afsurf(*args, **kwargs)

    def Transfer(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Transfer" decpreciated.  Use "transfer" instead'))
        return self.transfer(*args, **kwargs)

    def Kmesh(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Kmesh" decpreciated.  Use "kmesh" instead'))
        return self.kmesh(*args, **kwargs)

    def Lsrestore(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lsrestore" decpreciated.  Use "lsrestore" instead'))
        return self.lsrestore(*args, **kwargs)

    def Copy(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Copy" decpreciated.  Use "copy" instead'))
        return self.copy(*args, **kwargs)

    def Stat(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Stat" decpreciated.  Use "stat" instead'))
        return self.stat(*args, **kwargs)

    def Mfun(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mfun" decpreciated.  Use "mfun" instead'))
        return self.mfun(*args, **kwargs)

    def Prvar(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Prvar" decpreciated.  Use "prvar" instead'))
        return self.prvar(*args, **kwargs)

    def Syp(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Syp" decpreciated.  Use "syp" instead'))
        return self.syp(*args, **kwargs)

    def Lglue(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lglue" decpreciated.  Use "lglue" instead'))
        return self.lglue(*args, **kwargs)

    def Suvect(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Suvect" decpreciated.  Use "suvect" instead'))
        return self.suvect(*args, **kwargs)

    def Fj(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Fj" decpreciated.  Use "fj" instead'))
        return self.fj(*args, **kwargs)

    def Frqscl(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Frqscl" decpreciated.  Use "frqscl" instead'))
        return self.frqscl(*args, **kwargs)

    def Prtime(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Prtime" decpreciated.  Use "prtime" instead'))
        return self.prtime(*args, **kwargs)

    def Directory(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Directory" decpreciated.  Use "directory" instead'))
        return self.directory(*args, **kwargs)

    def Slashlarc(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Slashlarc" decpreciated.  Use "slashlarc" instead'))
        return self.slashlarc(*args, **kwargs)

    def Sys(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sys" decpreciated.  Use "sys" instead'))
        return self.sys(*args, **kwargs)

    def Help(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Help" decpreciated.  Use "help" instead'))
        return self.help(*args, **kwargs)

    def Pdcdf(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pdcdf" decpreciated.  Use "pdcdf" instead'))
        return self.pdcdf(*args, **kwargs)

    def Vtran(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vtran" decpreciated.  Use "vtran" instead'))
        return self.vtran(*args, **kwargs)

    def Lcwrite(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lcwrite" decpreciated.  Use "lcwrite" instead'))
        return self.lcwrite(*args, **kwargs)

    def Pngr(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pngr" decpreciated.  Use "pngr" instead'))
        return self.pngr(*args, **kwargs)

    def Vcross(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vcross" decpreciated.  Use "vcross" instead'))
        return self.vcross(*args, **kwargs)

    def Com(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Com" decpreciated.  Use "com" instead'))
        return self.com(*args, **kwargs)

    def Tchg(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Tchg" decpreciated.  Use "tchg" instead'))
        return self.tchg(*args, **kwargs)

    def Psdres(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Psdres" decpreciated.  Use "psdres" instead'))
        return self.psdres(*args, **kwargs)

    def Pause(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pause" decpreciated.  Use "pause" instead'))
        return self.pause(*args, **kwargs)

    def Anflow(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Anflow" decpreciated.  Use "anflow" instead'))
        return self.anflow(*args, **kwargs)

    def Append(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Append" decpreciated.  Use "append" instead'))
        return self.append(*args, **kwargs)

    def Qdval(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Qdval" decpreciated.  Use "qdval" instead'))
        return self.qdval(*args, **kwargs)

    def Mdamp(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mdamp" decpreciated.  Use "mdamp" instead'))
        return self.mdamp(*args, **kwargs)

    def Larea(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Larea" decpreciated.  Use "larea" instead'))
        return self.larea(*args, **kwargs)

    def Ncnv(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ncnv" decpreciated.  Use "ncnv" instead'))
        return self.ncnv(*args, **kwargs)

    def Ioptn(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ioptn" decpreciated.  Use "ioptn" instead'))
        return self.ioptn(*args, **kwargs)

    def Lssolve(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lssolve" decpreciated.  Use "lssolve" instead'))
        return self.lssolve(*args, **kwargs)

    def Ftype(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ftype" decpreciated.  Use "ftype" instead'))
        return self.ftype(*args, **kwargs)

    def Spgraph(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Spgraph" decpreciated.  Use "spgraph" instead'))
        return self.spgraph(*args, **kwargs)

    def Prscontrol(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Prscontrol" decpreciated.  Use "prscontrol" instead'))
        return self.prscontrol(*args, **kwargs)

    def Pdcfld(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pdcfld" decpreciated.  Use "pdcfld" instead'))
        return self.pdcfld(*args, **kwargs)

    def Wsort(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Wsort" decpreciated.  Use "wsort" instead'))
        return self.wsort(*args, **kwargs)

    def Lsymm(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lsymm" decpreciated.  Use "lsymm" instead'))
        return self.lsymm(*args, **kwargs)

    def Edvel(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edvel" decpreciated.  Use "edvel" instead'))
        return self.edvel(*args, **kwargs)

    def Prrsol(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Prrsol" decpreciated.  Use "prrsol" instead'))
        return self.prrsol(*args, **kwargs)

    def Tbeo(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Tbeo" decpreciated.  Use "tbeo" instead'))
        return self.tbeo(*args, **kwargs)

    def Dowhile(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Dowhile" decpreciated.  Use "dowhile" instead'))
        return self.dowhile(*args, **kwargs)

    def Esln(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Esln" decpreciated.  Use "esln" instead'))
        return self.esln(*args, **kwargs)

    def Wplane(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Wplane" decpreciated.  Use "wplane" instead'))
        return self.wplane(*args, **kwargs)

    def Lrefine(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lrefine" decpreciated.  Use "lrefine" instead'))
        return self.lrefine(*args, **kwargs)

    def Tintp(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Tintp" decpreciated.  Use "tintp" instead'))
        return self.tintp(*args, **kwargs)

    def Bstq(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Bstq" decpreciated.  Use "bstq" instead'))
        return self.bstq(*args, **kwargs)

    def Setfgap(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Setfgap" decpreciated.  Use "setfgap" instead'))
        return self.setfgap(*args, **kwargs)

    def Engen(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Engen" decpreciated.  Use "engen" instead'))
        return self.engen(*args, **kwargs)

    def Cone(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cone" decpreciated.  Use "cone" instead'))
        return self.cone(*args, **kwargs)

    def Dot(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Dot" decpreciated.  Use "dot" instead'))
        return self.dot(*args, **kwargs)

    def Rsplot(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rsplot" decpreciated.  Use "rsplot" instead'))
        return self.rsplot(*args, **kwargs)

    def For2d(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"For2d" decpreciated.  Use "for2d" instead'))
        return self.for2d(*args, **kwargs)

    def Tspec(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Tspec" decpreciated.  Use "tspec" instead'))
        return self.tspec(*args, **kwargs)

    def Lmatrix(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lmatrix" decpreciated.  Use "lmatrix" instead'))
        return self.lmatrix(*args, **kwargs)

    def Lstr(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lstr" decpreciated.  Use "lstr" instead'))
        return self.lstr(*args, **kwargs)

    def Rmndisp(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rmndisp" decpreciated.  Use "rmndisp" instead'))
        return self.rmndisp(*args, **kwargs)

    def Vfun(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vfun" decpreciated.  Use "vfun" instead'))
        return self.vfun(*args, **kwargs)

    def Lsba(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lsba" decpreciated.  Use "lsba" instead'))
        return self.lsba(*args, **kwargs)

    def Coval(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Coval" decpreciated.  Use "coval" instead'))
        return self.coval(*args, **kwargs)

    def Lfsurf(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lfsurf" decpreciated.  Use "lfsurf" instead'))
        return self.lfsurf(*args, **kwargs)

    def Bfvdele(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Bfvdele" decpreciated.  Use "bfvdele" instead'))
        return self.bfvdele(*args, **kwargs)

    def Check(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Check" decpreciated.  Use "check" instead'))
        return self.check(*args, **kwargs)

    def Rmore(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rmore" decpreciated.  Use "rmore" instead'))
        return self.rmore(*args, **kwargs)

    def Mfvolume(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mfvolume" decpreciated.  Use "mfvolume" instead'))
        return self.mfvolume(*args, **kwargs)

    def Hropt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Hropt" decpreciated.  Use "hropt" instead'))
        return self.hropt(*args, **kwargs)

    def Starlist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Starlist" decpreciated.  Use "starlist" instead'))
        return self.starlist(*args, **kwargs)

    def Anum(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Anum" decpreciated.  Use "anum" instead'))
        return self.anum(*args, **kwargs)

    def Shade(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Shade" decpreciated.  Use "shade" instead'))
        return self.shade(*args, **kwargs)

    def Seltol(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Seltol" decpreciated.  Use "seltol" instead'))
        return self.seltol(*args, **kwargs)

    def Timerange(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Timerange" decpreciated.  Use "timerange" instead'))
        return self.timerange(*args, **kwargs)

    def Lsel(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lsel" decpreciated.  Use "lsel" instead'))
        return self.lsel(*args, **kwargs)

    def Grid(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Grid" decpreciated.  Use "grid" instead'))
        return self.grid(*args, **kwargs)

    def Suresu(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Suresu" decpreciated.  Use "suresu" instead'))
        return self.suresu(*args, **kwargs)

    def Asub(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Asub" decpreciated.  Use "asub" instead'))
        return self.asub(*args, **kwargs)

    def Sort(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sort" decpreciated.  Use "sort" instead'))
        return self.sort(*args, **kwargs)

    def Secjoint(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Secjoint" decpreciated.  Use "secjoint" instead'))
        return self.secjoint(*args, **kwargs)

    def Eorient(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Eorient" decpreciated.  Use "eorient" instead'))
        return self.eorient(*args, **kwargs)

    def Mfclear(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mfclear" decpreciated.  Use "mfclear" instead'))
        return self.mfclear(*args, **kwargs)

    def Paget(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Paget" decpreciated.  Use "paget" instead'))
        return self.paget(*args, **kwargs)

    def Vgen(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vgen" decpreciated.  Use "vgen" instead'))
        return self.vgen(*args, **kwargs)

    def Txtre(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Txtre" decpreciated.  Use "txtre" instead'))
        return self.txtre(*args, **kwargs)

    def Cmplot(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cmplot" decpreciated.  Use "cmplot" instead'))
        return self.cmplot(*args, **kwargs)

    def Nsubst(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Nsubst" decpreciated.  Use "nsubst" instead'))
        return self.nsubst(*args, **kwargs)

    def Kclear(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Kclear" decpreciated.  Use "kclear" instead'))
        return self.kclear(*args, **kwargs)

    def Slashgo(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Slashgo" decpreciated.  Use "slashgo" instead'))
        return self.slashgo(*args, **kwargs)

    def Dmat(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Dmat" decpreciated.  Use "dmat" instead'))
        return self.dmat(*args, **kwargs)

    def Fecons(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Fecons" decpreciated.  Use "fecons" instead'))
        return self.fecons(*args, **kwargs)

    def Vovlap(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vovlap" decpreciated.  Use "vovlap" instead'))
        return self.vovlap(*args, **kwargs)

    def Header(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Header" decpreciated.  Use "header" instead'))
        return self.header(*args, **kwargs)

    def Ddoption(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ddoption" decpreciated.  Use "ddoption" instead'))
        return self.ddoption(*args, **kwargs)

    def Elbow(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Elbow" decpreciated.  Use "elbow" instead'))
        return self.elbow(*args, **kwargs)

    def Domega(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Domega" decpreciated.  Use "domega" instead'))
        return self.domega(*args, **kwargs)

    def Keypts(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Keypts" decpreciated.  Use "keypts" instead'))
        return self.keypts(*args, **kwargs)

    def Nrrang(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Nrrang" decpreciated.  Use "nrrang" instead'))
        return self.nrrang(*args, **kwargs)

    def Gplist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Gplist" decpreciated.  Use "gplist" instead'))
        return self.gplist(*args, **kwargs)

    def Lrotat(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lrotat" decpreciated.  Use "lrotat" instead'))
        return self.lrotat(*args, **kwargs)

    def Lsbl(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lsbl" decpreciated.  Use "lsbl" instead'))
        return self.lsbl(*args, **kwargs)

    def Nread(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Nread" decpreciated.  Use "nread" instead'))
        return self.nread(*args, **kwargs)

    def Lsread(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lsread" decpreciated.  Use "lsread" instead'))
        return self.lsread(*args, **kwargs)

    def Rectng(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rectng" decpreciated.  Use "rectng" instead'))
        return self.rectng(*args, **kwargs)

    def Bfkdele(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Bfkdele" decpreciated.  Use "bfkdele" instead'))
        return self.bfkdele(*args, **kwargs)

    def Nang(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Nang" decpreciated.  Use "nang" instead'))
        return self.nang(*args, **kwargs)

    def Flst(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Flst" decpreciated.  Use "flst" instead'))
        return self.flst(*args, **kwargs)

    def Sread(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sread" decpreciated.  Use "sread" instead'))
        return self.sread(*args, **kwargs)

    def Bfunif(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Bfunif" decpreciated.  Use "bfunif" instead'))
        return self.bfunif(*args, **kwargs)

    def Subopt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Subopt" decpreciated.  Use "subopt" instead'))
        return self.subopt(*args, **kwargs)

    def Vinp(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vinp" decpreciated.  Use "vinp" instead'))
        return self.vinp(*args, **kwargs)

    def Mffname(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mffname" decpreciated.  Use "mffname" instead'))
        return self.mffname(*args, **kwargs)

    def Pdhist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pdhist" decpreciated.  Use "pdhist" instead'))
        return self.pdhist(*args, **kwargs)

    def Set(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Set" decpreciated.  Use "set" instead'))
        return self.set(*args, **kwargs)

    def Elist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Elist" decpreciated.  Use "elist" instead'))
        return self.elist(*args, **kwargs)

    def Cpcyc(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cpcyc" decpreciated.  Use "cpcyc" instead'))
        return self.cpcyc(*args, **kwargs)

    def Irlf(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Irlf" decpreciated.  Use "irlf" instead'))
        return self.irlf(*args, **kwargs)

    def Free(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Free" decpreciated.  Use "free" instead'))
        return self.free(*args, **kwargs)

    def Lwplan(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lwplan" decpreciated.  Use "lwplan" instead'))
        return self.lwplan(*args, **kwargs)

    def Mpamod(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mpamod" decpreciated.  Use "mpamod" instead'))
        return self.mpamod(*args, **kwargs)

    def Local(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Local" decpreciated.  Use "local" instead'))
        return self.local(*args, **kwargs)

    def Aclear(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Aclear" decpreciated.  Use "aclear" instead'))
        return self.aclear(*args, **kwargs)

    def Rssims(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rssims" decpreciated.  Use "rssims" instead'))
        return self.rssims(*args, **kwargs)

    def Gsave(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Gsave" decpreciated.  Use "gsave" instead'))
        return self.gsave(*args, **kwargs)

    def Contour(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Contour" decpreciated.  Use "contour" instead'))
        return self.contour(*args, **kwargs)

    def Monitor(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Monitor" decpreciated.  Use "monitor" instead'))
        return self.monitor(*args, **kwargs)

    def Fe(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Fe" decpreciated.  Use "fe" instead'))
        return self.fe(*args, **kwargs)

    def C(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"C" decpreciated.  Use "c" instead'))
        return self.c(*args, **kwargs)

    def Layplot(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Layplot" decpreciated.  Use "layplot" instead'))
        return self.layplot(*args, **kwargs)

    def Psmesh(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Psmesh" decpreciated.  Use "psmesh" instead'))
        return self.psmesh(*args, **kwargs)

    def Edbvis(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edbvis" decpreciated.  Use "edbvis" instead'))
        return self.edbvis(*args, **kwargs)

    def Dllist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Dllist" decpreciated.  Use "dllist" instead'))
        return self.dllist(*args, **kwargs)

    def Xfrm(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Xfrm" decpreciated.  Use "xfrm" instead'))
        return self.xfrm(*args, **kwargs)

    def Lang(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lang" decpreciated.  Use "lang" instead'))
        return self.lang(*args, **kwargs)

    def Vcol(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vcol" decpreciated.  Use "vcol" instead'))
        return self.vcol(*args, **kwargs)

    def Pdef(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pdef" decpreciated.  Use "pdef" instead'))
        return self.pdef(*args, **kwargs)

    def Crplim(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Crplim" decpreciated.  Use "crplim" instead'))
        return self.crplim(*args, **kwargs)

    def Lcdef(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lcdef" decpreciated.  Use "lcdef" instead'))
        return self.lcdef(*args, **kwargs)

    def Dklist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Dklist" decpreciated.  Use "dklist" instead'))
        return self.dklist(*args, **kwargs)

    def Cfwrite(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cfwrite" decpreciated.  Use "cfwrite" instead'))
        return self.cfwrite(*args, **kwargs)

    def Filedisp(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Filedisp" decpreciated.  Use "filedisp" instead'))
        return self.filedisp(*args, **kwargs)

    def Pdscat(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pdscat" decpreciated.  Use "pdscat" instead'))
        return self.pdscat(*args, **kwargs)

    def Sfdele(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sfdele" decpreciated.  Use "sfdele" instead'))
        return self.sfdele(*args, **kwargs)

    def Hbmat(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Hbmat" decpreciated.  Use "hbmat" instead'))
        return self.hbmat(*args, **kwargs)

    def Rmmrange(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rmmrange" decpreciated.  Use "rmmrange" instead'))
        return self.rmmrange(*args, **kwargs)

    def Tvar(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Tvar" decpreciated.  Use "tvar" instead'))
        return self.tvar(*args, **kwargs)

    def Vadd(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vadd" decpreciated.  Use "vadd" instead'))
        return self.vadd(*args, **kwargs)

    def Gropt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Gropt" decpreciated.  Use "gropt" instead'))
        return self.gropt(*args, **kwargs)

    def Prim(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Prim" decpreciated.  Use "prim" instead'))
        return self.prim(*args, **kwargs)

    def Asifile(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Asifile" decpreciated.  Use "asifile" instead'))
        return self.asifile(*args, **kwargs)

    def Vclear(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vclear" decpreciated.  Use "vclear" instead'))
        return self.vclear(*args, **kwargs)

    def Hrcplx(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Hrcplx" decpreciated.  Use "hrcplx" instead'))
        return self.hrcplx(*args, **kwargs)

    def Tbcopy(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Tbcopy" decpreciated.  Use "tbcopy" instead'))
        return self.tbcopy(*args, **kwargs)

    def Djdele(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Djdele" decpreciated.  Use "djdele" instead'))
        return self.djdele(*args, **kwargs)

    def Vfill(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vfill" decpreciated.  Use "vfill" instead'))
        return self.vfill(*args, **kwargs)

    def Rmanl(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rmanl" decpreciated.  Use "rmanl" instead'))
        return self.rmanl(*args, **kwargs)

    def Compress(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Compress" decpreciated.  Use "compress" instead'))
        return self.compress(*args, **kwargs)

    def Lfillt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lfillt" decpreciated.  Use "lfillt" instead'))
        return self.lfillt(*args, **kwargs)

    def Vabs(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vabs" decpreciated.  Use "vabs" instead'))
        return self.vabs(*args, **kwargs)

    def Torus(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Torus" decpreciated.  Use "torus" instead'))
        return self.torus(*args, **kwargs)

    def Afillt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Afillt" decpreciated.  Use "afillt" instead'))
        return self.afillt(*args, **kwargs)

    def Imesh(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Imesh" decpreciated.  Use "imesh" instead'))
        return self.imesh(*args, **kwargs)

    def Cbmd(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cbmd" decpreciated.  Use "cbmd" instead'))
        return self.cbmd(*args, **kwargs)

    def Real(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Real" decpreciated.  Use "real" instead'))
        return self.real(*args, **kwargs)

    def Etlist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Etlist" decpreciated.  Use "etlist" instead'))
        return self.etlist(*args, **kwargs)

    def Expass(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Expass" decpreciated.  Use "expass" instead'))
        return self.expass(*args, **kwargs)

    def Vinv(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vinv" decpreciated.  Use "vinv" instead'))
        return self.vinv(*args, **kwargs)

    def Fctyp(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Fctyp" decpreciated.  Use "fctyp" instead'))
        return self.fctyp(*args, **kwargs)

    def Alist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Alist" decpreciated.  Use "alist" instead'))
        return self.alist(*args, **kwargs)

    def Erase(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Erase" decpreciated.  Use "erase" instead'))
        return self.erase(*args, **kwargs)

    def Gmarker(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Gmarker" decpreciated.  Use "gmarker" instead'))
        return self.gmarker(*args, **kwargs)

    def Cerig(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cerig" decpreciated.  Use "cerig" instead'))
        return self.cerig(*args, **kwargs)

    def Cmdomega(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cmdomega" decpreciated.  Use "cmdomega" instead'))
        return self.cmdomega(*args, **kwargs)

    def Esll(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Esll" decpreciated.  Use "esll" instead'))
        return self.esll(*args, **kwargs)

    def Thopt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Thopt" decpreciated.  Use "thopt" instead'))
        return self.thopt(*args, **kwargs)

    def Ratio(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ratio" decpreciated.  Use "ratio" instead'))
        return self.ratio(*args, **kwargs)

    def Edis(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edis" decpreciated.  Use "edis" instead'))
        return self.edis(*args, **kwargs)

    def Ernorm(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ernorm" decpreciated.  Use "ernorm" instead'))
        return self.ernorm(*args, **kwargs)

    def Rdec(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rdec" decpreciated.  Use "rdec" instead'))
        return self.rdec(*args, **kwargs)

    def Vardel(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vardel" decpreciated.  Use "vardel" instead'))
        return self.vardel(*args, **kwargs)

    def Sqrt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sqrt" decpreciated.  Use "sqrt" instead'))
        return self.sqrt(*args, **kwargs)

    def Krefine(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Krefine" decpreciated.  Use "krefine" instead'))
        return self.krefine(*args, **kwargs)

    def Assign(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Assign" decpreciated.  Use "assign" instead'))
        return self.assign(*args, **kwargs)

    def Cfclos(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cfclos" decpreciated.  Use "cfclos" instead'))
        return self.cfclos(*args, **kwargs)

    def Edrst(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edrst" decpreciated.  Use "edrst" instead'))
        return self.edrst(*args, **kwargs)

    def Edpvel(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edpvel" decpreciated.  Use "edpvel" instead'))
        return self.edpvel(*args, **kwargs)

    def Lina(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lina" decpreciated.  Use "lina" instead'))
        return self.lina(*args, **kwargs)

    def Pcgopt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pcgopt" decpreciated.  Use "pcgopt" instead'))
        return self.pcgopt(*args, **kwargs)

    def Hrocean(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Hrocean" decpreciated.  Use "hrocean" instead'))
        return self.hrocean(*args, **kwargs)

    def Gfile(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Gfile" decpreciated.  Use "gfile" instead'))
        return self.gfile(*args, **kwargs)

    def Edpl(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edpl" decpreciated.  Use "edpl" instead'))
        return self.edpl(*args, **kwargs)

    def Msg(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Msg" decpreciated.  Use "msg" instead'))
        return self.msg(*args, **kwargs)

    def Ptxy(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ptxy" decpreciated.  Use "ptxy" instead'))
        return self.ptxy(*args, **kwargs)

    def Pdsens(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pdsens" decpreciated.  Use "pdsens" instead'))
        return self.pdsens(*args, **kwargs)

    def Numvar(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Numvar" decpreciated.  Use "numvar" instead'))
        return self.numvar(*args, **kwargs)

    def Pdprob(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pdprob" decpreciated.  Use "pdprob" instead'))
        return self.pdprob(*args, **kwargs)

    def Cmsfile(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cmsfile" decpreciated.  Use "cmsfile" instead'))
        return self.cmsfile(*args, **kwargs)

    def Rsurf(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rsurf" decpreciated.  Use "rsurf" instead'))
        return self.rsurf(*args, **kwargs)

    def Anisos(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Anisos" decpreciated.  Use "anisos" instead'))
        return self.anisos(*args, **kwargs)

    def Rlist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rlist" decpreciated.  Use "rlist" instead'))
        return self.rlist(*args, **kwargs)

    def Noorder(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Noorder" decpreciated.  Use "noorder" instead'))
        return self.noorder(*args, **kwargs)

    def Edcmore(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edcmore" decpreciated.  Use "edcmore" instead'))
        return self.edcmore(*args, **kwargs)

    def Sucalc(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sucalc" decpreciated.  Use "sucalc" instead'))
        return self.sucalc(*args, **kwargs)

    def Smbc(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Smbc" decpreciated.  Use "smbc" instead'))
        return self.smbc(*args, **kwargs)

    def Map(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Map" decpreciated.  Use "map" instead'))
        return self.map(*args, **kwargs)

    def Senergy(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Senergy" decpreciated.  Use "senergy" instead'))
        return self.senergy(*args, **kwargs)

    def Sfedele(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sfedele" decpreciated.  Use "sfedele" instead'))
        return self.sfedele(*args, **kwargs)

    def Edhtime(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edhtime" decpreciated.  Use "edhtime" instead'))
        return self.edhtime(*args, **kwargs)

    def Spctemp(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Spctemp" decpreciated.  Use "spctemp" instead'))
        return self.spctemp(*args, **kwargs)

    def Mfelem(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mfelem" decpreciated.  Use "mfelem" instead'))
        return self.mfelem(*args, **kwargs)

    def Lmesh(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lmesh" decpreciated.  Use "lmesh" instead'))
        return self.lmesh(*args, **kwargs)

    def Cmrotate(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cmrotate" decpreciated.  Use "cmrotate" instead'))
        return self.cmrotate(*args, **kwargs)

    def Rgb(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rgb" decpreciated.  Use "rgb" instead'))
        return self.rgb(*args, **kwargs)

    def Reorder(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Reorder" decpreciated.  Use "reorder" instead'))
        return self.reorder(*args, **kwargs)

    def Bfscale(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Bfscale" decpreciated.  Use "bfscale" instead'))
        return self.bfscale(*args, **kwargs)

    def Format(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Format" decpreciated.  Use "format" instead'))
        return self.format(*args, **kwargs)

    def Bfelist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Bfelist" decpreciated.  Use "bfelist" instead'))
        return self.bfelist(*args, **kwargs)

    def File(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"File" decpreciated.  Use "file" instead'))
        return self.file(*args, **kwargs)

    def Stitle(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Stitle" decpreciated.  Use "stitle" instead'))
        return self.stitle(*args, **kwargs)

    def Rsprnt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rsprnt" decpreciated.  Use "rsprnt" instead'))
        return self.rsprnt(*args, **kwargs)

    def Lreverse(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lreverse" decpreciated.  Use "lreverse" instead'))
        return self.lreverse(*args, **kwargs)

    def Mgen(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mgen" decpreciated.  Use "mgen" instead'))
        return self.mgen(*args, **kwargs)

    def Mfwrite(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mfwrite" decpreciated.  Use "mfwrite" instead'))
        return self.mfwrite(*args, **kwargs)

    def Gapf(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Gapf" decpreciated.  Use "gapf" instead'))
        return self.gapf(*args, **kwargs)

    def Edfplot(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edfplot" decpreciated.  Use "edfplot" instead'))
        return self.edfplot(*args, **kwargs)

    def Ancut(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ancut" decpreciated.  Use "ancut" instead'))
        return self.ancut(*args, **kwargs)

    def Torqc2d(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Torqc2d" decpreciated.  Use "torqc2d" instead'))
        return self.torqc2d(*args, **kwargs)

    def Al(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Al" decpreciated.  Use "al" instead'))
        return self.al(*args, **kwargs)

    def Wpoffs(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Wpoffs" decpreciated.  Use "wpoffs" instead'))
        return self.wpoffs(*args, **kwargs)

    def Fmagbc(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Fmagbc" decpreciated.  Use "fmagbc" instead'))
        return self.fmagbc(*args, **kwargs)

    def Voffst(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Voffst" decpreciated.  Use "voffst" instead'))
        return self.voffst(*args, **kwargs)

    def Batch(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Batch" decpreciated.  Use "batch" instead'))
        return self.batch(*args, **kwargs)

    def K(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"K" decpreciated.  Use "k" instead'))
        return self.k(*args, **kwargs)

    def Aglue(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Aglue" decpreciated.  Use "aglue" instead'))
        return self.aglue(*args, **kwargs)

    def Dspoption(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Dspoption" decpreciated.  Use "dspoption" instead'))
        return self.dspoption(*args, **kwargs)

    def Vdgl(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vdgl" decpreciated.  Use "vdgl" instead'))
        return self.vdgl(*args, **kwargs)

    def Tlabel(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Tlabel" decpreciated.  Use "tlabel" instead'))
        return self.tlabel(*args, **kwargs)

    def Starvput(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Starvput" decpreciated.  Use "starvput" instead'))
        return self.starvput(*args, **kwargs)

    def Subset(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Subset" decpreciated.  Use "subset" instead'))
        return self.subset(*args, **kwargs)

    def Geometry(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Geometry" decpreciated.  Use "geometry" instead'))
        return self.geometry(*args, **kwargs)

    def Rmnevec(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rmnevec" decpreciated.  Use "rmnevec" instead'))
        return self.rmnevec(*args, **kwargs)

    def Edsolv(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edsolv" decpreciated.  Use "edsolv" instead'))
        return self.edsolv(*args, **kwargs)

    def Adrag(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Adrag" decpreciated.  Use "adrag" instead'))
        return self.adrag(*args, **kwargs)

    def Init(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Init" decpreciated.  Use "init" instead'))
        return self.init(*args, **kwargs)

    def Nlopt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Nlopt" decpreciated.  Use "nlopt" instead'))
        return self.nlopt(*args, **kwargs)

    def Slashstatus(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Slashstatus" decpreciated.  Use "slashstatus" instead'))
        return self.slashstatus(*args, **kwargs)

    def Mprint(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mprint" decpreciated.  Use "mprint" instead'))
        return self.mprint(*args, **kwargs)

    def Shell(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Shell" decpreciated.  Use "shell" instead'))
        return self.shell(*args, **kwargs)

    def Lcsel(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lcsel" decpreciated.  Use "lcsel" instead'))
        return self.lcsel(*args, **kwargs)

    def Fcdele(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Fcdele" decpreciated.  Use "fcdele" instead'))
        return self.fcdele(*args, **kwargs)

    def Kcenter(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Kcenter" decpreciated.  Use "kcenter" instead'))
        return self.kcenter(*args, **kwargs)

    def Pfact(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pfact" decpreciated.  Use "pfact" instead'))
        return self.pfact(*args, **kwargs)

    def Edcpu(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edcpu" decpreciated.  Use "edcpu" instead'))
        return self.edcpu(*args, **kwargs)

    def Arefine(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Arefine" decpreciated.  Use "arefine" instead'))
        return self.arefine(*args, **kwargs)

    def Abbres(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Abbres" decpreciated.  Use "abbres" instead'))
        return self.abbres(*args, **kwargs)

    def Plorb(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Plorb" decpreciated.  Use "plorb" instead'))
        return self.plorb(*args, **kwargs)

    def Vddam(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vddam" decpreciated.  Use "vddam" instead'))
        return self.vddam(*args, **kwargs)

    def Poly(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Poly" decpreciated.  Use "poly" instead'))
        return self.poly(*args, **kwargs)

    def Timint(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Timint" decpreciated.  Use "timint" instead'))
        return self.timint(*args, **kwargs)

    def Ldread(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ldread" decpreciated.  Use "ldread" instead'))
        return self.ldread(*args, **kwargs)

    def Usrdof(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Usrdof" decpreciated.  Use "usrdof" instead'))
        return self.usrdof(*args, **kwargs)

    def Kbetw(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Kbetw" decpreciated.  Use "kbetw" instead'))
        return self.kbetw(*args, **kwargs)

    def Map2dto3d(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Map2dto3d" decpreciated.  Use "map2dto3d" instead'))
        return self.map2dto3d(*args, **kwargs)

    def View(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"View" decpreciated.  Use "view" instead'))
        return self.view(*args, **kwargs)

    def Fft(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Fft" decpreciated.  Use "fft" instead'))
        return self.fft(*args, **kwargs)

    def Cesgen(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cesgen" decpreciated.  Use "cesgen" instead'))
        return self.cesgen(*args, **kwargs)

    def Bfldele(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Bfldele" decpreciated.  Use "bfldele" instead'))
        return self.bfldele(*args, **kwargs)

    def Ldiv(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ldiv" decpreciated.  Use "ldiv" instead'))
        return self.ldiv(*args, **kwargs)

    def Show(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Show" decpreciated.  Use "show" instead'))
        return self.show(*args, **kwargs)

    def Hrout(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Hrout" decpreciated.  Use "hrout" instead'))
        return self.hrout(*args, **kwargs)

    def Tee(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Tee" decpreciated.  Use "tee" instead'))
        return self.tee(*args, **kwargs)

    def Febody(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Febody" decpreciated.  Use "febody" instead'))
        return self.febody(*args, **kwargs)

    def Rescontrol(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rescontrol" decpreciated.  Use "rescontrol" instead'))
        return self.rescontrol(*args, **kwargs)

    def Katt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Katt" decpreciated.  Use "katt" instead'))
        return self.katt(*args, **kwargs)

    def Antype(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Antype" decpreciated.  Use "antype" instead'))
        return self.antype(*args, **kwargs)

    def Cmgrp(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cmgrp" decpreciated.  Use "cmgrp" instead'))
        return self.cmgrp(*args, **kwargs)

    def Varnam(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Varnam" decpreciated.  Use "varnam" instead'))
        return self.varnam(*args, **kwargs)

    def Fkdele(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Fkdele" decpreciated.  Use "fkdele" instead'))
        return self.fkdele(*args, **kwargs)

    def Sftran(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sftran" decpreciated.  Use "sftran" instead'))
        return self.sftran(*args, **kwargs)

    def An3d(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"An3d" decpreciated.  Use "an3d" instead'))
        return self.an3d(*args, **kwargs)

    def Gthk(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Gthk" decpreciated.  Use "gthk" instead'))
        return self.gthk(*args, **kwargs)

    def Undo(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Undo" decpreciated.  Use "undo" instead'))
        return self.undo(*args, **kwargs)

    def Esym(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Esym" decpreciated.  Use "esym" instead'))
        return self.esym(*args, **kwargs)

    def Octable(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Octable" decpreciated.  Use "octable" instead'))
        return self.octable(*args, **kwargs)

    def Rstoff(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rstoff" decpreciated.  Use "rstoff" instead'))
        return self.rstoff(*args, **kwargs)

    def Fssparm(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Fssparm" decpreciated.  Use "fssparm" instead'))
        return self.fssparm(*args, **kwargs)

    def Pbf(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pbf" decpreciated.  Use "pbf" instead'))
        return self.pbf(*args, **kwargs)

    def Ucmd(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ucmd" decpreciated.  Use "ucmd" instead'))
        return self.ucmd(*args, **kwargs)

    def L2ang(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"L2ang" decpreciated.  Use "l2ang" instead'))
        return self.l2ang(*args, **kwargs)

    def Sph4(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sph4" decpreciated.  Use "sph4" instead'))
        return self.sph4(*args, **kwargs)

    def Ddaspec(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ddaspec" decpreciated.  Use "ddaspec" instead'))
        return self.ddaspec(*args, **kwargs)

    def Cylind(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cylind" decpreciated.  Use "cylind" instead'))
        return self.cylind(*args, **kwargs)

    def Vscale(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vscale" decpreciated.  Use "vscale" instead'))
        return self.vscale(*args, **kwargs)

    def Asba(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Asba" decpreciated.  Use "asba" instead'))
        return self.asba(*args, **kwargs)

    def Rbe3(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rbe3" decpreciated.  Use "rbe3" instead'))
        return self.rbe3(*args, **kwargs)

    def Filldata(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Filldata" decpreciated.  Use "filldata" instead'))
        return self.filldata(*args, **kwargs)

    def Con4(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Con4" decpreciated.  Use "con4" instead'))
        return self.con4(*args, **kwargs)

    def Ce(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ce" decpreciated.  Use "ce" instead'))
        return self.ce(*args, **kwargs)

    def Ceqn(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ceqn" decpreciated.  Use "ceqn" instead'))
        return self.ceqn(*args, **kwargs)

    def Bfe(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Bfe" decpreciated.  Use "bfe" instead'))
        return self.bfe(*args, **kwargs)

    def Ksln(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ksln" decpreciated.  Use "ksln" instead'))
        return self.ksln(*args, **kwargs)

    def Bfl(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Bfl" decpreciated.  Use "bfl" instead'))
        return self.bfl(*args, **kwargs)

    def Anstoaqwa(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Anstoaqwa" decpreciated.  Use "anstoaqwa" instead'))
        return self.anstoaqwa(*args, **kwargs)

    def Cplane(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cplane" decpreciated.  Use "cplane" instead'))
        return self.cplane(*args, **kwargs)

    def Areverse(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Areverse" decpreciated.  Use "areverse" instead'))
        return self.areverse(*args, **kwargs)

    def Snoption(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Snoption" decpreciated.  Use "snoption" instead'))
        return self.snoption(*args, **kwargs)

    def Lsdump(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lsdump" decpreciated.  Use "lsdump" instead'))
        return self.lsdump(*args, **kwargs)

    def Lcfact(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lcfact" decpreciated.  Use "lcfact" instead'))
        return self.lcfact(*args, **kwargs)

    def Tbmodif(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Tbmodif" decpreciated.  Use "tbmodif" instead'))
        return self.tbmodif(*args, **kwargs)

    def Prism(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Prism" decpreciated.  Use "prism" instead'))
        return self.prism(*args, **kwargs)

    def Immed(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Immed" decpreciated.  Use "immed" instead'))
        return self.immed(*args, **kwargs)

    def Wpave(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Wpave" decpreciated.  Use "wpave" instead'))
        return self.wpave(*args, **kwargs)

    def Wrfull(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Wrfull" decpreciated.  Use "wrfull" instead'))
        return self.wrfull(*args, **kwargs)

    def Psearch(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Psearch" decpreciated.  Use "psearch" instead'))
        return self.psearch(*args, **kwargs)

    def Window(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Window" decpreciated.  Use "window" instead'))
        return self.window(*args, **kwargs)

    def Dofsel(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Dofsel" decpreciated.  Use "dofsel" instead'))
        return self.dofsel(*args, **kwargs)

    def Rdele(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rdele" decpreciated.  Use "rdele" instead'))
        return self.rdele(*args, **kwargs)

    def Ocdelete(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ocdelete" decpreciated.  Use "ocdelete" instead'))
        return self.ocdelete(*args, **kwargs)

    def Autots(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Autots" decpreciated.  Use "autots" instead'))
        return self.autots(*args, **kwargs)

    def Agen(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Agen" decpreciated.  Use "agen" instead'))
        return self.agen(*args, **kwargs)

    def Slashexit(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Slashexit" decpreciated.  Use "slashexit" instead'))
        return self.slashexit(*args, **kwargs)

    def Eddamp(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Eddamp" decpreciated.  Use "eddamp" instead'))
        return self.eddamp(*args, **kwargs)

    def Slashreset(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Slashreset" decpreciated.  Use "slashreset" instead'))
        return self.slashreset(*args, **kwargs)

    def Nsel(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Nsel" decpreciated.  Use "nsel" instead'))
        return self.nsel(*args, **kwargs)

    def Igesout(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Igesout" decpreciated.  Use "igesout" instead'))
        return self.igesout(*args, **kwargs)

    def Sfadele(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sfadele" decpreciated.  Use "sfadele" instead'))
        return self.sfadele(*args, **kwargs)

    def Gslist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Gslist" decpreciated.  Use "gslist" instead'))
        return self.gslist(*args, **kwargs)

    def Normal(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Normal" decpreciated.  Use "normal" instead'))
        return self.normal(*args, **kwargs)

    def Slashline(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Slashline" decpreciated.  Use "slashline" instead'))
        return self.slashline(*args, **kwargs)

    def Susave(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Susave" decpreciated.  Use "susave" instead'))
        return self.susave(*args, **kwargs)

    def Edterm(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edterm" decpreciated.  Use "edterm" instead'))
        return self.edterm(*args, **kwargs)

    def Sfelist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sfelist" decpreciated.  Use "sfelist" instead'))
        return self.sfelist(*args, **kwargs)

    def Udoc(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Udoc" decpreciated.  Use "udoc" instead'))
        return self.udoc(*args, **kwargs)

    def Ptr(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ptr" decpreciated.  Use "ptr" instead'))
        return self.ptr(*args, **kwargs)

    def Cycexpand(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cycexpand" decpreciated.  Use "cycexpand" instead'))
        return self.cycexpand(*args, **kwargs)

    def Spunit(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Spunit" decpreciated.  Use "spunit" instead'))
        return self.spunit(*args, **kwargs)

    def Sudel(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sudel" decpreciated.  Use "sudel" instead'))
        return self.sudel(*args, **kwargs)

    def Calc(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Calc" decpreciated.  Use "calc" instead'))
        return self.calc(*args, **kwargs)

    def Accoption(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Accoption" decpreciated.  Use "accoption" instead'))
        return self.accoption(*args, **kwargs)

    def Sflist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sflist" decpreciated.  Use "sflist" instead'))
        return self.sflist(*args, **kwargs)

    def Repeat(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Repeat" decpreciated.  Use "repeat" instead'))
        return self.repeat(*args, **kwargs)

    def Emis(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Emis" decpreciated.  Use "emis" instead'))
        return self.emis(*args, **kwargs)

    def Fscale(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Fscale" decpreciated.  Use "fscale" instead'))
        return self.fscale(*args, **kwargs)

    def Cdwrite(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cdwrite" decpreciated.  Use "cdwrite" instead'))
        return self.cdwrite(*args, **kwargs)

    def Dmprat(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Dmprat" decpreciated.  Use "dmprat" instead'))
        return self.dmprat(*args, **kwargs)

    def Rmsmple(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rmsmple" decpreciated.  Use "rmsmple" instead'))
        return self.rmsmple(*args, **kwargs)

    def Cncheck(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cncheck" decpreciated.  Use "cncheck" instead'))
        return self.cncheck(*args, **kwargs)

    def Moper(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Moper" decpreciated.  Use "moper" instead'))
        return self.moper(*args, **kwargs)

    def Prcint(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Prcint" decpreciated.  Use "prcint" instead'))
        return self.prcint(*args, **kwargs)

    def Starprint(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Starprint" decpreciated.  Use "starprint" instead'))
        return self.starprint(*args, **kwargs)

    def Store(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Store" decpreciated.  Use "store" instead'))
        return self.store(*args, **kwargs)

    def Psmat(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Psmat" decpreciated.  Use "psmat" instead'))
        return self.psmat(*args, **kwargs)

    def Mpdele(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mpdele" decpreciated.  Use "mpdele" instead'))
        return self.mpdele(*args, **kwargs)

    def Cedele(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cedele" decpreciated.  Use "cedele" instead'))
        return self.cedele(*args, **kwargs)

    def Modopt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Modopt" decpreciated.  Use "modopt" instead'))
        return self.modopt(*args, **kwargs)

    def Rezone(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rezone" decpreciated.  Use "rezone" instead'))
        return self.rezone(*args, **kwargs)

    def Lsbv(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lsbv" decpreciated.  Use "lsbv" instead'))
        return self.lsbv(*args, **kwargs)

    def Lsdele(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lsdele" decpreciated.  Use "lsdele" instead'))
        return self.lsdele(*args, **kwargs)

    def Pbc(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pbc" decpreciated.  Use "pbc" instead'))
        return self.pbc(*args, **kwargs)

    def Dldele(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Dldele" decpreciated.  Use "dldele" instead'))
        return self.dldele(*args, **kwargs)

    def Slashexpand(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Slashexpand" decpreciated.  Use "slashexpand" instead'))
        return self.slashexpand(*args, **kwargs)

    def Ovcheck(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ovcheck" decpreciated.  Use "ovcheck" instead'))
        return self.ovcheck(*args, **kwargs)

    def Asll(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Asll" decpreciated.  Use "asll" instead'))
        return self.asll(*args, **kwargs)

    def Nlmesh(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Nlmesh" decpreciated.  Use "nlmesh" instead'))
        return self.nlmesh(*args, **kwargs)

    def Ndele(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ndele" decpreciated.  Use "ndele" instead'))
        return self.ndele(*args, **kwargs)

    def Csys(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Csys" decpreciated.  Use "csys" instead'))
        return self.csys(*args, **kwargs)

    def Aesize(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Aesize" decpreciated.  Use "aesize" instead'))
        return self.aesize(*args, **kwargs)

    def Nldiag(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Nldiag" decpreciated.  Use "nldiag" instead'))
        return self.nldiag(*args, **kwargs)

    def Gplot(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Gplot" decpreciated.  Use "gplot" instead'))
        return self.gplot(*args, **kwargs)

    def Abbr(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Abbr" decpreciated.  Use "abbr" instead'))
        return self.abbr(*args, **kwargs)

    def Slashsolu(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Slashsolu" decpreciated.  Use "slashsolu" instead'))
        return self.slashsolu(*args, **kwargs)

    def Post1(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Post1" decpreciated.  Use "post1" instead'))
        return self.post1(*args, **kwargs)

    def Tunif(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Tunif" decpreciated.  Use "tunif" instead'))
        return self.tunif(*args, **kwargs)

    def Midtol(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Midtol" decpreciated.  Use "midtol" instead'))
        return self.midtol(*args, **kwargs)

    def Type(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Type" decpreciated.  Use "type" instead'))
        return self.type(*args, **kwargs)

    def Rsymm(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rsymm" decpreciated.  Use "rsymm" instead'))
        return self.rsymm(*args, **kwargs)

    def Nropt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Nropt" decpreciated.  Use "nropt" instead'))
        return self.nropt(*args, **kwargs)

    def Swdel(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Swdel" decpreciated.  Use "swdel" instead'))
        return self.swdel(*args, **kwargs)

    def Cfact(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cfact" decpreciated.  Use "cfact" instead'))
        return self.cfact(*args, **kwargs)

    def Wfront(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Wfront" decpreciated.  Use "wfront" instead'))
        return self.wfront(*args, **kwargs)

    def Rmresume(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rmresume" decpreciated.  Use "rmresume" instead'))
        return self.rmresume(*args, **kwargs)

    def Parain(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Parain" decpreciated.  Use "parain" instead'))
        return self.parain(*args, **kwargs)

    def Padele(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Padele" decpreciated.  Use "padele" instead'))
        return self.padele(*args, **kwargs)

    def Morph(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Morph" decpreciated.  Use "morph" instead'))
        return self.morph(*args, **kwargs)

    def Irlist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Irlist" decpreciated.  Use "irlist" instead'))
        return self.irlist(*args, **kwargs)

    def Seclib(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Seclib" decpreciated.  Use "seclib" instead'))
        return self.seclib(*args, **kwargs)

    def Smrtsize(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Smrtsize" decpreciated.  Use "smrtsize" instead'))
        return self.smrtsize(*args, **kwargs)

    def Kplot(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Kplot" decpreciated.  Use "kplot" instead'))
        return self.kplot(*args, **kwargs)

    def Rmrstatus(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rmrstatus" decpreciated.  Use "rmrstatus" instead'))
        return self.rmrstatus(*args, **kwargs)

    def Edcgen(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edcgen" decpreciated.  Use "edcgen" instead'))
        return self.edcgen(*args, **kwargs)

    def Quot(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Quot" decpreciated.  Use "quot" instead'))
        return self.quot(*args, **kwargs)

    def Spoint(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Spoint" decpreciated.  Use "spoint" instead'))
        return self.spoint(*args, **kwargs)

    def Rsplit(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rsplit" decpreciated.  Use "rsplit" instead'))
        return self.rsplit(*args, **kwargs)

    def Essolv(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Essolv" decpreciated.  Use "essolv" instead'))
        return self.essolv(*args, **kwargs)

    def Smbody(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Smbody" decpreciated.  Use "smbody" instead'))
        return self.smbody(*args, **kwargs)

    def Aovlap(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Aovlap" decpreciated.  Use "aovlap" instead'))
        return self.aovlap(*args, **kwargs)

    def Dof(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Dof" decpreciated.  Use "dof" instead'))
        return self.dof(*args, **kwargs)

    def Secoffset(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Secoffset" decpreciated.  Use "secoffset" instead'))
        return self.secoffset(*args, **kwargs)

    def Helpdisp(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Helpdisp" decpreciated.  Use "helpdisp" instead'))
        return self.helpdisp(*args, **kwargs)

    def Priter(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Priter" decpreciated.  Use "priter" instead'))
        return self.priter(*args, **kwargs)

    def Starset(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Starset" decpreciated.  Use "starset" instead'))
        return self.starset(*args, **kwargs)

    def Slashmap(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Slashmap" decpreciated.  Use "slashmap" instead'))
        return self.slashmap(*args, **kwargs)

    def Sbclist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sbclist" decpreciated.  Use "sbclist" instead'))
        return self.sbclist(*args, **kwargs)

    def Psel(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Psel" decpreciated.  Use "psel" instead'))
        return self.psel(*args, **kwargs)

    def Stabilize(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Stabilize" decpreciated.  Use "stabilize" instead'))
        return self.stabilize(*args, **kwargs)

    def Plcplx(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Plcplx" decpreciated.  Use "plcplx" instead'))
        return self.plcplx(*args, **kwargs)

    def Xfenrich(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Xfenrich" decpreciated.  Use "xfenrich" instead'))
        return self.xfenrich(*args, **kwargs)

    def Nrotat(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Nrotat" decpreciated.  Use "nrotat" instead'))
        return self.nrotat(*args, **kwargs)

    def Rigresp(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rigresp" decpreciated.  Use "rigresp" instead'))
        return self.rigresp(*args, **kwargs)

    def Vsweep(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vsweep" decpreciated.  Use "vsweep" instead'))
        return self.vsweep(*args, **kwargs)

    def Pds(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pds" decpreciated.  Use "pds" instead'))
        return self.pds(*args, **kwargs)

    def Lovlap(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lovlap" decpreciated.  Use "lovlap" instead'))
        return self.lovlap(*args, **kwargs)

    def Edgcale(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edgcale" decpreciated.  Use "edgcale" instead'))
        return self.edgcale(*args, **kwargs)

    def Smfor(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Smfor" decpreciated.  Use "smfor" instead'))
        return self.smfor(*args, **kwargs)

    def Prorb(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Prorb" decpreciated.  Use "prorb" instead'))
        return self.prorb(*args, **kwargs)

    def Rforce(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rforce" decpreciated.  Use "rforce" instead'))
        return self.rforce(*args, **kwargs)

    def Seexp(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Seexp" decpreciated.  Use "seexp" instead'))
        return self.seexp(*args, **kwargs)

    def Secnum(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Secnum" decpreciated.  Use "secnum" instead'))
        return self.secnum(*args, **kwargs)

    def Cslist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cslist" decpreciated.  Use "cslist" instead'))
        return self.cslist(*args, **kwargs)

    def Volumes(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Volumes" decpreciated.  Use "volumes" instead'))
        return self.volumes(*args, **kwargs)

    def Nlog(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Nlog" decpreciated.  Use "nlog" instead'))
        return self.nlog(*args, **kwargs)

    def Anpres(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Anpres" decpreciated.  Use "anpres" instead'))
        return self.anpres(*args, **kwargs)

    def Nsvr(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Nsvr" decpreciated.  Use "nsvr" instead'))
        return self.nsvr(*args, **kwargs)

    def Felist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Felist" decpreciated.  Use "felist" instead'))
        return self.felist(*args, **kwargs)

    def Efacet(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Efacet" decpreciated.  Use "efacet" instead'))
        return self.efacet(*args, **kwargs)

    def Fluxv(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Fluxv" decpreciated.  Use "fluxv" instead'))
        return self.fluxv(*args, **kwargs)

    def Nodes(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Nodes" decpreciated.  Use "nodes" instead'))
        return self.nodes(*args, **kwargs)

    def Hfsym(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Hfsym" decpreciated.  Use "hfsym" instead'))
        return self.hfsym(*args, **kwargs)

    def Fssect(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Fssect" decpreciated.  Use "fssect" instead'))
        return self.fssect(*args, **kwargs)

    def Tblist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Tblist" decpreciated.  Use "tblist" instead'))
        return self.tblist(*args, **kwargs)

    def Sed(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sed" decpreciated.  Use "sed" instead'))
        return self.sed(*args, **kwargs)

    def V(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"V" decpreciated.  Use "v" instead'))
        return self.v(*args, **kwargs)

    def Desize(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Desize" decpreciated.  Use "desize" instead'))
        return self.desize(*args, **kwargs)

    def Mfrstart(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mfrstart" decpreciated.  Use "mfrstart" instead'))
        return self.mfrstart(*args, **kwargs)

    def Stef(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Stef" decpreciated.  Use "stef" instead'))
        return self.stef(*args, **kwargs)

    def Parres(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Parres" decpreciated.  Use "parres" instead'))
        return self.parres(*args, **kwargs)

    def Plcint(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Plcint" decpreciated.  Use "plcint" instead'))
        return self.plcint(*args, **kwargs)

    def Nora(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Nora" decpreciated.  Use "nora" instead'))
        return self.nora(*args, **kwargs)

    def Solve(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Solve" decpreciated.  Use "solve" instead'))
        return self.solve(*args, **kwargs)

    def Ssmt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ssmt" decpreciated.  Use "ssmt" instead'))
        return self.ssmt(*args, **kwargs)

    def Imagin(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Imagin" decpreciated.  Use "imagin" instead'))
        return self.imagin(*args, **kwargs)

    def Cbtmp(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cbtmp" decpreciated.  Use "cbtmp" instead'))
        return self.cbtmp(*args, **kwargs)

    def Areas(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Areas" decpreciated.  Use "areas" instead'))
        return self.areas(*args, **kwargs)

    def Wpstyl(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Wpstyl" decpreciated.  Use "wpstyl" instead'))
        return self.wpstyl(*args, **kwargs)

    def Catiain(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Catiain" decpreciated.  Use "catiain" instead'))
        return self.catiain(*args, **kwargs)

    def Dump(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Dump" decpreciated.  Use "dump" instead'))
        return self.dump(*args, **kwargs)

    def Output(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Output" decpreciated.  Use "output" instead'))
        return self.output(*args, **kwargs)

    def Hmagsolv(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Hmagsolv" decpreciated.  Use "hmagsolv" instead'))
        return self.hmagsolv(*args, **kwargs)

    def Reswrite(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Reswrite" decpreciated.  Use "reswrite" instead'))
        return self.reswrite(*args, **kwargs)

    def Esize(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Esize" decpreciated.  Use "esize" instead'))
        return self.esize(*args, **kwargs)

    def Cmacel(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cmacel" decpreciated.  Use "cmacel" instead'))
        return self.cmacel(*args, **kwargs)

    def Rmmselect(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rmmselect" decpreciated.  Use "rmmselect" instead'))
        return self.rmmselect(*args, **kwargs)

    def Pletab(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pletab" decpreciated.  Use "pletab" instead'))
        return self.pletab(*args, **kwargs)

    def Swlist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Swlist" decpreciated.  Use "swlist" instead'))
        return self.swlist(*args, **kwargs)

    def Arscale(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Arscale" decpreciated.  Use "arscale" instead'))
        return self.arscale(*args, **kwargs)

    def Acel(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Acel" decpreciated.  Use "acel" instead'))
        return self.acel(*args, **kwargs)

    def Sspd(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sspd" decpreciated.  Use "sspd" instead'))
        return self.sspd(*args, **kwargs)

    def Edrc(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edrc" decpreciated.  Use "edrc" instead'))
        return self.edrc(*args, **kwargs)

    def Layer(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Layer" decpreciated.  Use "layer" instead'))
        return self.layer(*args, **kwargs)

    def Layerp26(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Layerp26" decpreciated.  Use "layerp26" instead'))
        return self.layerp26(*args, **kwargs)

    def Celist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Celist" decpreciated.  Use "celist" instead'))
        return self.celist(*args, **kwargs)

    def Rmcap(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rmcap" decpreciated.  Use "rmcap" instead'))
        return self.rmcap(*args, **kwargs)

    def Clabel(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Clabel" decpreciated.  Use "clabel" instead'))
        return self.clabel(*args, **kwargs)

    def Sflex(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sflex" decpreciated.  Use "sflex" instead'))
        return self.sflex(*args, **kwargs)

    def Trans(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Trans" decpreciated.  Use "trans" instead'))
        return self.trans(*args, **kwargs)

    def Memm(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Memm" decpreciated.  Use "memm" instead'))
        return self.memm(*args, **kwargs)

    def Bsm1(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Bsm1" decpreciated.  Use "bsm1" instead'))
        return self.bsm1(*args, **kwargs)

    def Cmatrix(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cmatrix" decpreciated.  Use "cmatrix" instead'))
        return self.cmatrix(*args, **kwargs)

    def Bss1(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Bss1" decpreciated.  Use "bss1" instead'))
        return self.bss1(*args, **kwargs)

    def Eddc(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Eddc" decpreciated.  Use "eddc" instead'))
        return self.eddc(*args, **kwargs)

    def Werase(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Werase" decpreciated.  Use "werase" instead'))
        return self.werase(*args, **kwargs)

    def Paresu(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Paresu" decpreciated.  Use "paresu" instead'))
        return self.paresu(*args, **kwargs)

    def Nwplan(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Nwplan" decpreciated.  Use "nwplan" instead'))
        return self.nwplan(*args, **kwargs)

    def Shpp(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Shpp" decpreciated.  Use "shpp" instead'))
        return self.shpp(*args, **kwargs)

    def Opncontrol(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Opncontrol" decpreciated.  Use "opncontrol" instead'))
        return self.opncontrol(*args, **kwargs)

    def Dadele(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Dadele" decpreciated.  Use "dadele" instead'))
        return self.dadele(*args, **kwargs)

    def Ensym(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ensym" decpreciated.  Use "ensym" instead'))
        return self.ensym(*args, **kwargs)

    def Pdropt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pdropt" decpreciated.  Use "pdropt" instead'))
        return self.pdropt(*args, **kwargs)

    def Satin(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Satin" decpreciated.  Use "satin" instead'))
        return self.satin(*args, **kwargs)

    def Swgen(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Swgen" decpreciated.  Use "swgen" instead'))
        return self.swgen(*args, **kwargs)

    def Prfar(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Prfar" decpreciated.  Use "prfar" instead'))
        return self.prfar(*args, **kwargs)

    def Gformat(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Gformat" decpreciated.  Use "gformat" instead'))
        return self.gformat(*args, **kwargs)

    def Pcirc(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pcirc" decpreciated.  Use "pcirc" instead'))
        return self.pcirc(*args, **kwargs)

    def Pltime(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pltime" decpreciated.  Use "pltime" instead'))
        return self.pltime(*args, **kwargs)

    def Spcnod(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Spcnod" decpreciated.  Use "spcnod" instead'))
        return self.spcnod(*args, **kwargs)

    def Image(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Image" decpreciated.  Use "image" instead'))
        return self.image(*args, **kwargs)

    def Fileaux3(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Fileaux3" decpreciated.  Use "fileaux3" instead'))
        return self.fileaux3(*args, **kwargs)

    def Tshap(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Tshap" decpreciated.  Use "tshap" instead'))
        return self.tshap(*args, **kwargs)

    def Modify(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Modify" decpreciated.  Use "modify" instead'))
        return self.modify(*args, **kwargs)

    def Cval(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cval" decpreciated.  Use "cval" instead'))
        return self.cval(*args, **kwargs)

    def Cmlist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cmlist" decpreciated.  Use "cmlist" instead'))
        return self.cmlist(*args, **kwargs)

    def Proein(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Proein" decpreciated.  Use "proein" instead'))
        return self.proein(*args, **kwargs)

    def Eintf(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Eintf" decpreciated.  Use "eintf" instead'))
        return self.eintf(*args, **kwargs)

    def Plotting(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Plotting" decpreciated.  Use "plotting" instead'))
        return self.plotting(*args, **kwargs)

    def Auto(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Auto" decpreciated.  Use "auto" instead'))
        return self.auto(*args, **kwargs)

    def Rthick(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rthick" decpreciated.  Use "rthick" instead'))
        return self.rthick(*args, **kwargs)

    def Va(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Va" decpreciated.  Use "va" instead'))
        return self.va(*args, **kwargs)

    def Plpagm(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Plpagm" decpreciated.  Use "plpagm" instead'))
        return self.plpagm(*args, **kwargs)

    def Sabs(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sabs" decpreciated.  Use "sabs" instead'))
        return self.sabs(*args, **kwargs)

    def Psdval(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Psdval" decpreciated.  Use "psdval" instead'))
        return self.psdval(*args, **kwargs)

    def Wmore(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Wmore" decpreciated.  Use "wmore" instead'))
        return self.wmore(*args, **kwargs)

    def Cyccalc(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cyccalc" decpreciated.  Use "cyccalc" instead'))
        return self.cyccalc(*args, **kwargs)

    def Kdele(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Kdele" decpreciated.  Use "kdele" instead'))
        return self.kdele(*args, **kwargs)

    def Eigen(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Eigen" decpreciated.  Use "eigen" instead'))
        return self.eigen(*args, **kwargs)

    def Hfang(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Hfang" decpreciated.  Use "hfang" instead'))
        return self.hfang(*args, **kwargs)

    def Aina(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Aina" decpreciated.  Use "aina" instead'))
        return self.aina(*args, **kwargs)

    def Modcont(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Modcont" decpreciated.  Use "modcont" instead'))
        return self.modcont(*args, **kwargs)

    def Conjug(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Conjug" decpreciated.  Use "conjug" instead'))
        return self.conjug(*args, **kwargs)

    def Reset(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Reset" decpreciated.  Use "reset" instead'))
        return self.reset(*args, **kwargs)

    def Mpplot(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mpplot" decpreciated.  Use "mpplot" instead'))
        return self.mpplot(*args, **kwargs)

    def Print(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Print" decpreciated.  Use "print" instead'))
        return self.print(*args, **kwargs)

    def Rate(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rate" decpreciated.  Use "rate" instead'))
        return self.rate(*args, **kwargs)

    def Dval(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Dval" decpreciated.  Use "dval" instead'))
        return self.dval(*args, **kwargs)

    def Vget(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vget" decpreciated.  Use "vget" instead'))
        return self.vget(*args, **kwargs)

    def Page(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Page" decpreciated.  Use "page" instead'))
        return self.page(*args, **kwargs)

    def Ftcalc(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ftcalc" decpreciated.  Use "ftcalc" instead'))
        return self.ftcalc(*args, **kwargs)

    def Pddoel(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pddoel" decpreciated.  Use "pddoel" instead'))
        return self.pddoel(*args, **kwargs)

    def Dtran(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Dtran" decpreciated.  Use "dtran" instead'))
        return self.dtran(*args, **kwargs)

    def Nmodif(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Nmodif" decpreciated.  Use "nmodif" instead'))
        return self.nmodif(*args, **kwargs)

    def Wprota(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Wprota" decpreciated.  Use "wprota" instead'))
        return self.wprota(*args, **kwargs)

    def Magopt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Magopt" decpreciated.  Use "magopt" instead'))
        return self.magopt(*args, **kwargs)

    def Fsdele(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Fsdele" decpreciated.  Use "fsdele" instead'))
        return self.fsdele(*args, **kwargs)

    def Secplot(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Secplot" decpreciated.  Use "secplot" instead'))
        return self.secplot(*args, **kwargs)

    def Bfedele(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Bfedele" decpreciated.  Use "bfedele" instead'))
        return self.bfedele(*args, **kwargs)

    def Edshell(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edshell" decpreciated.  Use "edshell" instead'))
        return self.edshell(*args, **kwargs)

    def Plst(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Plst" decpreciated.  Use "plst" instead'))
        return self.plst(*args, **kwargs)

    def Extrem(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Extrem" decpreciated.  Use "extrem" instead'))
        return self.extrem(*args, **kwargs)

    def Flist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Flist" decpreciated.  Use "flist" instead'))
        return self.flist(*args, **kwargs)

    def Cpngen(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cpngen" decpreciated.  Use "cpngen" instead'))
        return self.cpngen(*args, **kwargs)

    def Realvar(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Realvar" decpreciated.  Use "realvar" instead'))
        return self.realvar(*args, **kwargs)

    def Fcum(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Fcum" decpreciated.  Use "fcum" instead'))
        return self.fcum(*args, **kwargs)

    def Edbx(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edbx" decpreciated.  Use "edbx" instead'))
        return self.edbx(*args, **kwargs)

    def Ugin(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ugin" decpreciated.  Use "ugin" instead'))
        return self.ugin(*args, **kwargs)

    def Lnsrch(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lnsrch" decpreciated.  Use "lnsrch" instead'))
        return self.lnsrch(*args, **kwargs)

    def Outres(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Outres" decpreciated.  Use "outres" instead'))
        return self.outres(*args, **kwargs)

    def Erefine(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Erefine" decpreciated.  Use "erefine" instead'))
        return self.erefine(*args, **kwargs)

    def Tbin(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Tbin" decpreciated.  Use "tbin" instead'))
        return self.tbin(*args, **kwargs)

    def Tread(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Tread" decpreciated.  Use "tread" instead'))
        return self.tread(*args, **kwargs)

    def Edrd(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edrd" decpreciated.  Use "edrd" instead'))
        return self.edrd(*args, **kwargs)

    def Vatt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vatt" decpreciated.  Use "vatt" instead'))
        return self.vatt(*args, **kwargs)

    def Eresx(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Eresx" decpreciated.  Use "eresx" instead'))
        return self.eresx(*args, **kwargs)

    def Seopt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Seopt" decpreciated.  Use "seopt" instead'))
        return self.seopt(*args, **kwargs)

    def Cswpla(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cswpla" decpreciated.  Use "cswpla" instead'))
        return self.cswpla(*args, **kwargs)

    def Amap(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Amap" decpreciated.  Use "amap" instead'))
        return self.amap(*args, **kwargs)

    def Exunit(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Exunit" decpreciated.  Use "exunit" instead'))
        return self.exunit(*args, **kwargs)

    def Ftran(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ftran" decpreciated.  Use "ftran" instead'))
        return self.ftran(*args, **kwargs)

    def Plzz(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Plzz" decpreciated.  Use "plzz" instead'))
        return self.plzz(*args, **kwargs)

    def Dj(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Dj" decpreciated.  Use "dj" instead'))
        return self.dj(*args, **kwargs)

    def Mat(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mat" decpreciated.  Use "mat" instead'))
        return self.mat(*args, **kwargs)

    def Vread(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vread" decpreciated.  Use "vread" instead'))
        return self.vread(*args, **kwargs)

    def Anmode(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Anmode" decpreciated.  Use "anmode" instead'))
        return self.anmode(*args, **kwargs)

    def Vsel(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vsel" decpreciated.  Use "vsel" instead'))
        return self.vsel(*args, **kwargs)

    def Mxpand(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mxpand" decpreciated.  Use "mxpand" instead'))
        return self.mxpand(*args, **kwargs)

    def Vcone(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vcone" decpreciated.  Use "vcone" instead'))
        return self.vcone(*args, **kwargs)

    def Pmore(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pmore" decpreciated.  Use "pmore" instead'))
        return self.pmore(*args, **kwargs)

    def Number(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Number" decpreciated.  Use "number" instead'))
        return self.number(*args, **kwargs)

    def Lsoper(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lsoper" decpreciated.  Use "lsoper" instead'))
        return self.lsoper(*args, **kwargs)

    def Gcgen(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Gcgen" decpreciated.  Use "gcgen" instead'))
        return self.gcgen(*args, **kwargs)

    def Lslk(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lslk" decpreciated.  Use "lslk" instead'))
        return self.lslk(*args, **kwargs)

    def Edpart(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edpart" decpreciated.  Use "edpart" instead'))
        return self.edpart(*args, **kwargs)

    def Cdread(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cdread" decpreciated.  Use "cdread" instead'))
        return self.cdread(*args, **kwargs)

    def Splot(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Splot" decpreciated.  Use "splot" instead'))
        return self.splot(*args, **kwargs)

    def Asbv(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Asbv" decpreciated.  Use "asbv" instead'))
        return self.asbv(*args, **kwargs)

    def Djlist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Djlist" decpreciated.  Use "djlist" instead'))
        return self.djlist(*args, **kwargs)

    def Zoom(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Zoom" decpreciated.  Use "zoom" instead'))
        return self.zoom(*args, **kwargs)

    def Dmpstr(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Dmpstr" decpreciated.  Use "dmpstr" instead'))
        return self.dmpstr(*args, **kwargs)

    def Andata(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Andata" decpreciated.  Use "andata" instead'))
        return self.andata(*args, **kwargs)

    def Msolve(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Msolve" decpreciated.  Use "msolve" instead'))
        return self.msolve(*args, **kwargs)

    def Vec(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vec" decpreciated.  Use "vec" instead'))
        return self.vec(*args, **kwargs)

    def Graphics(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Graphics" decpreciated.  Use "graphics" instead'))
        return self.graphics(*args, **kwargs)

    def Freq(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Freq" decpreciated.  Use "freq" instead'))
        return self.freq(*args, **kwargs)

    def Errang(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Errang" decpreciated.  Use "errang" instead'))
        return self.errang(*args, **kwargs)

    def Kmove(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Kmove" decpreciated.  Use "kmove" instead'))
        return self.kmove(*args, **kwargs)

    def Esla(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Esla" decpreciated.  Use "esla" instead'))
        return self.esla(*args, **kwargs)

    def Upcoord(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Upcoord" decpreciated.  Use "upcoord" instead'))
        return self.upcoord(*args, **kwargs)

    def Sspe(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sspe" decpreciated.  Use "sspe" instead'))
        return self.sspe(*args, **kwargs)

    def Secread(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Secread" decpreciated.  Use "secread" instead'))
        return self.secread(*args, **kwargs)

    def Cnvtol(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cnvtol" decpreciated.  Use "cnvtol" instead'))
        return self.cnvtol(*args, **kwargs)

    def Torq2d(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Torq2d" decpreciated.  Use "torq2d" instead'))
        return self.torq2d(*args, **kwargs)

    def Endif(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Endif" decpreciated.  Use "endif" instead'))
        return self.endif(*args, **kwargs)

    def Force(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Force" decpreciated.  Use "force" instead'))
        return self.force(*args, **kwargs)

    def Prep7(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Prep7" decpreciated.  Use "prep7" instead'))
        return self.prep7(*args, **kwargs)

    def Sphere(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sphere" decpreciated.  Use "sphere" instead'))
        return self.sphere(*args, **kwargs)

    def Accat(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Accat" decpreciated.  Use "accat" instead'))
        return self.accat(*args, **kwargs)

    def Edale(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edale" decpreciated.  Use "edale" instead'))
        return self.edale(*args, **kwargs)

    def Mfci(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mfci" decpreciated.  Use "mfci" instead'))
        return self.mfci(*args, **kwargs)

    def Cecmod(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cecmod" decpreciated.  Use "cecmod" instead'))
        return self.cecmod(*args, **kwargs)

    def Lspec(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lspec" decpreciated.  Use "lspec" instead'))
        return self.lspec(*args, **kwargs)

    def Plls(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Plls" decpreciated.  Use "plls" instead'))
        return self.plls(*args, **kwargs)

    def Fvmesh(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Fvmesh" decpreciated.  Use "fvmesh" instead'))
        return self.fvmesh(*args, **kwargs)

    def Pdpinv(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pdpinv" decpreciated.  Use "pdpinv" instead'))
        return self.pdpinv(*args, **kwargs)

    def Pmlsize(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pmlsize" decpreciated.  Use "pmlsize" instead'))
        return self.pmlsize(*args, **kwargs)

    def Mapvar(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mapvar" decpreciated.  Use "mapvar" instead'))
        return self.mapvar(*args, **kwargs)

    def Bftran(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Bftran" decpreciated.  Use "bftran" instead'))
        return self.bftran(*args, **kwargs)

    def Prnld(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Prnld" decpreciated.  Use "prnld" instead'))
        return self.prnld(*args, **kwargs)

    def Cwd(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cwd" decpreciated.  Use "cwd" instead'))
        return self.cwd(*args, **kwargs)

    def Source(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Source" decpreciated.  Use "source" instead'))
        return self.source(*args, **kwargs)

    def Seg(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Seg" decpreciated.  Use "seg" instead'))
        return self.seg(*args, **kwargs)

    def Tble(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Tble" decpreciated.  Use "tble" instead'))
        return self.tble(*args, **kwargs)

    def Asbw(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Asbw" decpreciated.  Use "asbw" instead'))
        return self.asbw(*args, **kwargs)

    def Mfsurface(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mfsurface" decpreciated.  Use "mfsurface" instead'))
        return self.mfsurface(*args, **kwargs)

    def Sbctran(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sbctran" decpreciated.  Use "sbctran" instead'))
        return self.sbctran(*args, **kwargs)

    def Lccalc(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lccalc" decpreciated.  Use "lccalc" instead'))
        return self.lccalc(*args, **kwargs)

    def Nkpt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Nkpt" decpreciated.  Use "nkpt" instead'))
        return self.nkpt(*args, **kwargs)

    def Nummrg(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Nummrg" decpreciated.  Use "nummrg" instead'))
        return self.nummrg(*args, **kwargs)

    def Grp(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Grp" decpreciated.  Use "grp" instead'))
        return self.grp(*args, **kwargs)

    def Parsav(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Parsav" decpreciated.  Use "parsav" instead'))
        return self.parsav(*args, **kwargs)

    def Gst(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Gst" decpreciated.  Use "gst" instead'))
        return self.gst(*args, **kwargs)

    def Kbc(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Kbc" decpreciated.  Use "kbc" instead'))
        return self.kbc(*args, **kwargs)

    def Nplot(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Nplot" decpreciated.  Use "nplot" instead'))
        return self.nplot(*args, **kwargs)

    def Blc4(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Blc4" decpreciated.  Use "blc4" instead'))
        return self.blc4(*args, **kwargs)

    def Mfcalc(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mfcalc" decpreciated.  Use "mfcalc" instead'))
        return self.mfcalc(*args, **kwargs)

    def Gsgdata(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Gsgdata" decpreciated.  Use "gsgdata" instead'))
        return self.gsgdata(*args, **kwargs)

    def Usrcal(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Usrcal" decpreciated.  Use "usrcal" instead'))
        return self.usrcal(*args, **kwargs)

    def Deltim(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Deltim" decpreciated.  Use "deltim" instead'))
        return self.deltim(*args, **kwargs)

    def Gmatrix(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Gmatrix" decpreciated.  Use "gmatrix" instead'))
        return self.gmatrix(*args, **kwargs)

    def Kwpave(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Kwpave" decpreciated.  Use "kwpave" instead'))
        return self.kwpave(*args, **kwargs)

    def Mwrite(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mwrite" decpreciated.  Use "mwrite" instead'))
        return self.mwrite(*args, **kwargs)

    def Post26(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Post26" decpreciated.  Use "post26" instead'))
        return self.post26(*args, **kwargs)

    def Edwrite(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edwrite" decpreciated.  Use "edwrite" instead'))
        return self.edwrite(*args, **kwargs)

    def Sspb(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sspb" decpreciated.  Use "sspb" instead'))
        return self.sspb(*args, **kwargs)

    def Vlscale(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vlscale" decpreciated.  Use "vlscale" instead'))
        return self.vlscale(*args, **kwargs)

    def Fatigue(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Fatigue" decpreciated.  Use "fatigue" instead'))
        return self.fatigue(*args, **kwargs)

    def Read(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Read" decpreciated.  Use "read" instead'))
        return self.read(*args, **kwargs)

    def Wtbcreate(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Wtbcreate" decpreciated.  Use "wtbcreate" instead'))
        return self.wtbcreate(*args, **kwargs)

    def Config(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Config" decpreciated.  Use "config" instead'))
        return self.config(*args, **kwargs)

    def Bfecum(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Bfecum" decpreciated.  Use "bfecum" instead'))
        return self.bfecum(*args, **kwargs)

    def Sffun(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sffun" decpreciated.  Use "sffun" instead'))
        return self.sffun(*args, **kwargs)

    def Edndtsd(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edndtsd" decpreciated.  Use "edndtsd" instead'))
        return self.edndtsd(*args, **kwargs)

    def Deriv(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Deriv" decpreciated.  Use "deriv" instead'))
        return self.deriv(*args, **kwargs)

    def Axpy(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Axpy" decpreciated.  Use "axpy" instead'))
        return self.axpy(*args, **kwargs)

    def Linv(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Linv" decpreciated.  Use "linv" instead'))
        return self.linv(*args, **kwargs)

    def Nsmooth(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Nsmooth" decpreciated.  Use "nsmooth" instead'))
        return self.nsmooth(*args, **kwargs)

    def Edcts(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edcts" decpreciated.  Use "edcts" instead'))
        return self.edcts(*args, **kwargs)

    def Sumap(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sumap" decpreciated.  Use "sumap" instead'))
        return self.sumap(*args, **kwargs)

    def Edweld(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edweld" decpreciated.  Use "edweld" instead'))
        return self.edweld(*args, **kwargs)

    def Eslv(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Eslv" decpreciated.  Use "eslv" instead'))
        return self.eslv(*args, **kwargs)

    def Plcamp(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Plcamp" decpreciated.  Use "plcamp" instead'))
        return self.plcamp(*args, **kwargs)

    def Ocdata(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ocdata" decpreciated.  Use "ocdata" instead'))
        return self.ocdata(*args, **kwargs)

    def Ancyc(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ancyc" decpreciated.  Use "ancyc" instead'))
        return self.ancyc(*args, **kwargs)

    def R(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"R" decpreciated.  Use "r" instead'))
        return self.r(*args, **kwargs)

    def Cvar(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cvar" decpreciated.  Use "cvar" instead'))
        return self.cvar(*args, **kwargs)

    def Vfsm(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vfsm" decpreciated.  Use "vfsm" instead'))
        return self.vfsm(*args, **kwargs)

    def Vdot(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vdot" decpreciated.  Use "vdot" instead'))
        return self.vdot(*args, **kwargs)

    def Linl(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Linl" decpreciated.  Use "linl" instead'))
        return self.linl(*args, **kwargs)

    def Lsfactor(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lsfactor" decpreciated.  Use "lsfactor" instead'))
        return self.lsfactor(*args, **kwargs)

    def Bfvlist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Bfvlist" decpreciated.  Use "bfvlist" instead'))
        return self.bfvlist(*args, **kwargs)

    def Pdmeth(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pdmeth" decpreciated.  Use "pdmeth" instead'))
        return self.pdmeth(*args, **kwargs)

    def Rmalist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rmalist" decpreciated.  Use "rmalist" instead'))
        return self.rmalist(*args, **kwargs)

    def Ic(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ic" decpreciated.  Use "ic" instead'))
        return self.ic(*args, **kwargs)

    def Msave(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Msave" decpreciated.  Use "msave" instead'))
        return self.msave(*args, **kwargs)

    def Staopt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Staopt" decpreciated.  Use "staopt" instead'))
        return self.staopt(*args, **kwargs)

    def Supl(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Supl" decpreciated.  Use "supl" instead'))
        return self.supl(*args, **kwargs)

    def Nlhist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Nlhist" decpreciated.  Use "nlhist" instead'))
        return self.nlhist(*args, **kwargs)

    def Outopt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Outopt" decpreciated.  Use "outopt" instead'))
        return self.outopt(*args, **kwargs)

    def Prcamp(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Prcamp" decpreciated.  Use "prcamp" instead'))
        return self.prcamp(*args, **kwargs)

    def Rprism(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rprism" decpreciated.  Use "rprism" instead'))
        return self.rprism(*args, **kwargs)

    def Trnopt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Trnopt" decpreciated.  Use "trnopt" instead'))
        return self.trnopt(*args, **kwargs)

    def Mftime(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mftime" decpreciated.  Use "mftime" instead'))
        return self.mftime(*args, **kwargs)

    def Pdclr(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pdclr" decpreciated.  Use "pdclr" instead'))
        return self.pdclr(*args, **kwargs)

    def Vwrite(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vwrite" decpreciated.  Use "vwrite" instead'))
        return self.vwrite(*args, **kwargs)

    def Wpcsys(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Wpcsys" decpreciated.  Use "wpcsys" instead'))
        return self.wpcsys(*args, **kwargs)

    def Itengine(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Itengine" decpreciated.  Use "itengine" instead'))
        return self.itengine(*args, **kwargs)

    def Spfreq(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Spfreq" decpreciated.  Use "spfreq" instead'))
        return self.spfreq(*args, **kwargs)

    def Ceintf(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ceintf" decpreciated.  Use "ceintf" instead'))
        return self.ceintf(*args, **kwargs)

    def Kmodif(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Kmodif" decpreciated.  Use "kmodif" instead'))
        return self.kmodif(*args, **kwargs)

    def Sv(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sv" decpreciated.  Use "sv" instead'))
        return self.sv(*args, **kwargs)

    def E(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"E" decpreciated.  Use "e" instead'))
        return self.e(*args, **kwargs)

    def Edrun(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edrun" decpreciated.  Use "edrun" instead'))
        return self.edrun(*args, **kwargs)

    def Avprin(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Avprin" decpreciated.  Use "avprin" instead'))
        return self.avprin(*args, **kwargs)

    def Prjsol(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Prjsol" decpreciated.  Use "prjsol" instead'))
        return self.prjsol(*args, **kwargs)

    def Bcsoption(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Bcsoption" decpreciated.  Use "bcsoption" instead'))
        return self.bcsoption(*args, **kwargs)

    def Fc(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Fc" decpreciated.  Use "fc" instead'))
        return self.fc(*args, **kwargs)

    def Setran(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Setran" decpreciated.  Use "setran" instead'))
        return self.setran(*args, **kwargs)

    def Inres(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Inres" decpreciated.  Use "inres" instead'))
        return self.inres(*args, **kwargs)

    def Ssum(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ssum" decpreciated.  Use "ssum" instead'))
        return self.ssum(*args, **kwargs)

    def Esys(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Esys" decpreciated.  Use "esys" instead'))
        return self.esys(*args, **kwargs)

    def Cyclic(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cyclic" decpreciated.  Use "cyclic" instead'))
        return self.cyclic(*args, **kwargs)

    def Naxis(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Naxis" decpreciated.  Use "naxis" instead'))
        return self.naxis(*args, **kwargs)

    def Cycfreq(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cycfreq" decpreciated.  Use "cycfreq" instead'))
        return self.cycfreq(*args, **kwargs)

    def Cmap(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cmap" decpreciated.  Use "cmap" instead'))
        return self.cmap(*args, **kwargs)

    def Pdcorr(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pdcorr" decpreciated.  Use "pdcorr" instead'))
        return self.pdcorr(*args, **kwargs)

    def Pred(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pred" decpreciated.  Use "pred" instead'))
        return self.pred(*args, **kwargs)

    def Pivcheck(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pivcheck" decpreciated.  Use "pivcheck" instead'))
        return self.pivcheck(*args, **kwargs)

    def Mdplot(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mdplot" decpreciated.  Use "mdplot" instead'))
        return self.mdplot(*args, **kwargs)

    def Harfrq(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Harfrq" decpreciated.  Use "harfrq" instead'))
        return self.harfrq(*args, **kwargs)

    def Kdist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Kdist" decpreciated.  Use "kdist" instead'))
        return self.kdist(*args, **kwargs)

    def Betad(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Betad" decpreciated.  Use "betad" instead'))
        return self.betad(*args, **kwargs)

    def Mfouri(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mfouri" decpreciated.  Use "mfouri" instead'))
        return self.mfouri(*args, **kwargs)

    def Physics(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Physics" decpreciated.  Use "physics" instead'))
        return self.physics(*args, **kwargs)

    def Curr2d(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Curr2d" decpreciated.  Use "curr2d" instead'))
        return self.curr2d(*args, **kwargs)

    def Cnkmod(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cnkmod" decpreciated.  Use "cnkmod" instead'))
        return self.cnkmod(*args, **kwargs)

    def Dset(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Dset" decpreciated.  Use "dset" instead'))
        return self.dset(*args, **kwargs)

    def Rpoly(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rpoly" decpreciated.  Use "rpoly" instead'))
        return self.rpoly(*args, **kwargs)

    def Aatt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Aatt" decpreciated.  Use "aatt" instead'))
        return self.aatt(*args, **kwargs)

    def Aadd(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Aadd" decpreciated.  Use "aadd" instead'))
        return self.aadd(*args, **kwargs)

    def Andyna(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Andyna" decpreciated.  Use "andyna" instead'))
        return self.andyna(*args, **kwargs)

    def Deact(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Deact" decpreciated.  Use "deact" instead'))
        return self.deact(*args, **kwargs)

    def Edcrb(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edcrb" decpreciated.  Use "edcrb" instead'))
        return self.edcrb(*args, **kwargs)

    def Numstr(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Numstr" decpreciated.  Use "numstr" instead'))
        return self.numstr(*args, **kwargs)

    def Xrange(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Xrange" decpreciated.  Use "xrange" instead'))
        return self.xrange(*args, **kwargs)

    def Lswrite(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lswrite" decpreciated.  Use "lswrite" instead'))
        return self.lswrite(*args, **kwargs)

    def Cpdele(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cpdele" decpreciated.  Use "cpdele" instead'))
        return self.cpdele(*args, **kwargs)

    def Digit(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Digit" decpreciated.  Use "digit" instead'))
        return self.digit(*args, **kwargs)

    def Ainp(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ainp" decpreciated.  Use "ainp" instead'))
        return self.ainp(*args, **kwargs)

    def Prange(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Prange" decpreciated.  Use "prange" instead'))
        return self.prange(*args, **kwargs)

    def Dk(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Dk" decpreciated.  Use "dk" instead'))
        return self.dk(*args, **kwargs)

    def Mfpsimul(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mfpsimul" decpreciated.  Use "mfpsimul" instead'))
        return self.mfpsimul(*args, **kwargs)

    def Annot(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Annot" decpreciated.  Use "annot" instead'))
        return self.annot(*args, **kwargs)

    def Ednb(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ednb" decpreciated.  Use "ednb" instead'))
        return self.ednb(*args, **kwargs)

    def Prenergy(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Prenergy" decpreciated.  Use "prenergy" instead'))
        return self.prenergy(*args, **kwargs)

    def Rmlvscale(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rmlvscale" decpreciated.  Use "rmlvscale" instead'))
        return self.rmlvscale(*args, **kwargs)

    def Edipart(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edipart" decpreciated.  Use "edipart" instead'))
        return self.edipart(*args, **kwargs)

    def Mshcopy(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mshcopy" decpreciated.  Use "mshcopy" instead'))
        return self.mshcopy(*args, **kwargs)

    def Anstoasas(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Anstoasas" decpreciated.  Use "anstoasas" instead'))
        return self.anstoasas(*args, **kwargs)

    def Dig(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Dig" decpreciated.  Use "dig" instead'))
        return self.dig(*args, **kwargs)

    def Color(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Color" decpreciated.  Use "color" instead'))
        return self.color(*args, **kwargs)

    def Starexit(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Starexit" decpreciated.  Use "starexit" instead'))
        return self.starexit(*args, **kwargs)

    def Escheck(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Escheck" decpreciated.  Use "escheck" instead'))
        return self.escheck(*args, **kwargs)

    def Plnear(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Plnear" decpreciated.  Use "plnear" instead'))
        return self.plnear(*args, **kwargs)

    def Inistate(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Inistate" decpreciated.  Use "inistate" instead'))
        return self.inistate(*args, **kwargs)

    def Secstop(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Secstop" decpreciated.  Use "secstop" instead'))
        return self.secstop(*args, **kwargs)

    def Ealive(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ealive" decpreciated.  Use "ealive" instead'))
        return self.ealive(*args, **kwargs)

    def Hrexp(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Hrexp" decpreciated.  Use "hrexp" instead'))
        return self.hrexp(*args, **kwargs)

    def Clear(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Clear" decpreciated.  Use "clear" instead'))
        return self.clear(*args, **kwargs)

    def Magsolv(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Magsolv" decpreciated.  Use "magsolv" instead'))
        return self.magsolv(*args, **kwargs)

    def Starstatus(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Starstatus" decpreciated.  Use "starstatus" instead'))
        return self.starstatus(*args, **kwargs)

    def Ancntr(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ancntr" decpreciated.  Use "ancntr" instead'))
        return self.ancntr(*args, **kwargs)

    def Tallow(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Tallow" decpreciated.  Use "tallow" instead'))
        return self.tallow(*args, **kwargs)

    def Fefor(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Fefor" decpreciated.  Use "fefor" instead'))
        return self.fefor(*args, **kwargs)

    def Rmuse(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rmuse" decpreciated.  Use "rmuse" instead'))
        return self.rmuse(*args, **kwargs)

    def Gap(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Gap" decpreciated.  Use "gap" instead'))
        return self.gap(*args, **kwargs)

    def Psymb(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Psymb" decpreciated.  Use "psymb" instead'))
        return self.psymb(*args, **kwargs)

    def Bsmd(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Bsmd" decpreciated.  Use "bsmd" instead'))
        return self.bsmd(*args, **kwargs)

    def Sscale(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sscale" decpreciated.  Use "sscale" instead'))
        return self.sscale(*args, **kwargs)

    def Large(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Large" decpreciated.  Use "large" instead'))
        return self.large(*args, **kwargs)

    def Grtyp(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Grtyp" decpreciated.  Use "grtyp" instead'))
        return self.grtyp(*args, **kwargs)

    def Tbft(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Tbft" decpreciated.  Use "tbft" instead'))
        return self.tbft(*args, **kwargs)

    def Edenergy(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edenergy" decpreciated.  Use "edenergy" instead'))
        return self.edenergy(*args, **kwargs)

    # def Del(self, *args, **kwargs):
    #     warnings.warn(DeprecationWarning('"Del" decpreciated.  Use "del" instead'))
    #     return self.del(*args, **kwargs)

    def Cm(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cm" decpreciated.  Use "cm" instead'))
        return self.cm(*args, **kwargs)

    def Cmsopt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cmsopt" decpreciated.  Use "cmsopt" instead'))
        return self.cmsopt(*args, **kwargs)

    def Sstate(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sstate" decpreciated.  Use "sstate" instead'))
        return self.sstate(*args, **kwargs)

    def Mcheck(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mcheck" decpreciated.  Use "mcheck" instead'))
        return self.mcheck(*args, **kwargs)

    def Mfimport(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mfimport" decpreciated.  Use "mfimport" instead'))
        return self.mfimport(*args, **kwargs)

    def Pdvar(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pdvar" decpreciated.  Use "pdvar" instead'))
        return self.pdvar(*args, **kwargs)

    def Edhist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edhist" decpreciated.  Use "edhist" instead'))
        return self.edhist(*args, **kwargs)

    def Nsym(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Nsym" decpreciated.  Use "nsym" instead'))
        return self.nsym(*args, **kwargs)

    def Asum(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Asum" decpreciated.  Use "asum" instead'))
        return self.asum(*args, **kwargs)

    def Blc5(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Blc5" decpreciated.  Use "blc5" instead'))
        return self.blc5(*args, **kwargs)

    def Gpdele(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Gpdele" decpreciated.  Use "gpdele" instead'))
        return self.gpdele(*args, **kwargs)

    def Egen(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Egen" decpreciated.  Use "egen" instead'))
        return self.egen(*args, **kwargs)

    def Cpmerge(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cpmerge" decpreciated.  Use "cpmerge" instead'))
        return self.cpmerge(*args, **kwargs)

    def Ereinf(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ereinf" decpreciated.  Use "ereinf" instead'))
        return self.ereinf(*args, **kwargs)

    def Dflx(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Dflx" decpreciated.  Use "dflx" instead'))
        return self.dflx(*args, **kwargs)

    def Pdot(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pdot" decpreciated.  Use "pdot" instead'))
        return self.pdot(*args, **kwargs)

    def Inrtia(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Inrtia" decpreciated.  Use "inrtia" instead'))
        return self.inrtia(*args, **kwargs)

    def Genopt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Genopt" decpreciated.  Use "genopt" instead'))
        return self.genopt(*args, **kwargs)

    def Extopt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Extopt" decpreciated.  Use "extopt" instead'))
        return self.extopt(*args, **kwargs)

    def Cbmx(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cbmx" decpreciated.  Use "cbmx" instead'))
        return self.cbmx(*args, **kwargs)

    def Trtime(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Trtime" decpreciated.  Use "trtime" instead'))
        return self.trtime(*args, **kwargs)

    def Aflist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Aflist" decpreciated.  Use "aflist" instead'))
        return self.aflist(*args, **kwargs)

    def Edout(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edout" decpreciated.  Use "edout" instead'))
        return self.edout(*args, **kwargs)

    def Qsopt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Qsopt" decpreciated.  Use "qsopt" instead'))
        return self.qsopt(*args, **kwargs)

    def Lcabs(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lcabs" decpreciated.  Use "lcabs" instead'))
        return self.lcabs(*args, **kwargs)

    def Slashdscale(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Slashdscale" decpreciated.  Use "slashdscale" instead'))
        return self.slashdscale(*args, **kwargs)

    def Vdele(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vdele" decpreciated.  Use "vdele" instead'))
        return self.vdele(*args, **kwargs)

    def Secdata(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Secdata" decpreciated.  Use "secdata" instead'))
        return self.secdata(*args, **kwargs)

    def Pdsave(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pdsave" decpreciated.  Use "pdsave" instead'))
        return self.pdsave(*args, **kwargs)

    def Mfoutput(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mfoutput" decpreciated.  Use "mfoutput" instead'))
        return self.mfoutput(*args, **kwargs)

    def L(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"L" decpreciated.  Use "l" instead'))
        return self.l(*args, **kwargs)

    def Wait(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Wait" decpreciated.  Use "wait" instead'))
        return self.wait(*args, **kwargs)

    def Edele(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edele" decpreciated.  Use "edele" instead'))
        return self.edele(*args, **kwargs)

    def Mflist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mflist" decpreciated.  Use "mflist" instead'))
        return self.mflist(*args, **kwargs)

    def Eof(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Eof" decpreciated.  Use "eof" instead'))
        return self.eof(*args, **kwargs)

    def Rmodif(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rmodif" decpreciated.  Use "rmodif" instead'))
        return self.rmodif(*args, **kwargs)

    def Sadd(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sadd" decpreciated.  Use "sadd" instead'))
        return self.sadd(*args, **kwargs)

    def Rmxport(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rmxport" decpreciated.  Use "rmxport" instead'))
        return self.rmxport(*args, **kwargs)

    def Demorph(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Demorph" decpreciated.  Use "demorph" instead'))
        return self.demorph(*args, **kwargs)

    def Prcplx(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Prcplx" decpreciated.  Use "prcplx" instead'))
        return self.prcplx(*args, **kwargs)

    def Lsengine(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lsengine" decpreciated.  Use "lsengine" instead'))
        return self.lsengine(*args, **kwargs)

    def Etdele(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Etdele" decpreciated.  Use "etdele" instead'))
        return self.etdele(*args, **kwargs)

    def Atan(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Atan" decpreciated.  Use "atan" instead'))
        return self.atan(*args, **kwargs)

    def Delete(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Delete" decpreciated.  Use "delete" instead'))
        return self.delete(*args, **kwargs)

    def Enorm(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Enorm" decpreciated.  Use "enorm" instead'))
        return self.enorm(*args, **kwargs)

    def Cpintf(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cpintf" decpreciated.  Use "cpintf" instead'))
        return self.cpintf(*args, **kwargs)

    def Mfmap(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mfmap" decpreciated.  Use "mfmap" instead'))
        return self.mfmap(*args, **kwargs)

    def Fluread(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Fluread" decpreciated.  Use "fluread" instead'))
        return self.fluread(*args, **kwargs)

    def Ssln(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ssln" decpreciated.  Use "ssln" instead'))
        return self.ssln(*args, **kwargs)

    def Time(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Time" decpreciated.  Use "time" instead'))
        return self.time(*args, **kwargs)

    def Cmomega(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cmomega" decpreciated.  Use "cmomega" instead'))
        return self.cmomega(*args, **kwargs)

    def Arclen(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Arclen" decpreciated.  Use "arclen" instead'))
        return self.arclen(*args, **kwargs)

    def Rose(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rose" decpreciated.  Use "rose" instead'))
        return self.rose(*args, **kwargs)

    def Eextrude(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Eextrude" decpreciated.  Use "eextrude" instead'))
        return self.eextrude(*args, **kwargs)

    def Lsum(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lsum" decpreciated.  Use "lsum" instead'))
        return self.lsum(*args, **kwargs)

    def Ainv(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ainv" decpreciated.  Use "ainv" instead'))
        return self.ainv(*args, **kwargs)

    def Lgwrite(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lgwrite" decpreciated.  Use "lgwrite" instead'))
        return self.lgwrite(*args, **kwargs)

    def Adapt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Adapt" decpreciated.  Use "adapt" instead'))
        return self.adapt(*args, **kwargs)

    def Gp(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Gp" decpreciated.  Use "gp" instead'))
        return self.gp(*args, **kwargs)

    def Laylist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Laylist" decpreciated.  Use "laylist" instead'))
        return self.laylist(*args, **kwargs)

    def Jpeg(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Jpeg" decpreciated.  Use "jpeg" instead'))
        return self.jpeg(*args, **kwargs)

    def Rmdir(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rmdir" decpreciated.  Use "rmdir" instead'))
        return self.rmdir(*args, **kwargs)

    def Vplot(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vplot" decpreciated.  Use "vplot" instead'))
        return self.vplot(*args, **kwargs)

    def Vsba(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vsba" decpreciated.  Use "vsba" instead'))
        return self.vsba(*args, **kwargs)

    def Pri2(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pri2" decpreciated.  Use "pri2" instead'))
        return self.pri2(*args, **kwargs)

    def Btol(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Btol" decpreciated.  Use "btol" instead'))
        return self.btol(*args, **kwargs)

    def Fesurf(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Fesurf" decpreciated.  Use "fesurf" instead'))
        return self.fesurf(*args, **kwargs)

    def Plesol(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Plesol" decpreciated.  Use "plesol" instead'))
        return self.plesol(*args, **kwargs)

    def Iclist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Iclist" decpreciated.  Use "iclist" instead'))
        return self.iclist(*args, **kwargs)

    def Emagerr(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Emagerr" decpreciated.  Use "emagerr" instead'))
        return self.emagerr(*args, **kwargs)

    def Mshape(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mshape" decpreciated.  Use "mshape" instead'))
        return self.mshape(*args, **kwargs)

    def Sspa(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sspa" decpreciated.  Use "sspa" instead'))
        return self.sspa(*args, **kwargs)

    def Dflab(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Dflab" decpreciated.  Use "dflab" instead'))
        return self.dflab(*args, **kwargs)

    def Nsle(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Nsle" decpreciated.  Use "nsle" instead'))
        return self.nsle(*args, **kwargs)

    def Plf2d(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Plf2d" decpreciated.  Use "plf2d" instead'))
        return self.plf2d(*args, **kwargs)

    def Thexpand(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Thexpand" decpreciated.  Use "thexpand" instead'))
        return self.thexpand(*args, **kwargs)

    def Nolist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Nolist" decpreciated.  Use "nolist" instead'))
        return self.nolist(*args, **kwargs)

    def Ddele(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ddele" decpreciated.  Use "ddele" instead'))
        return self.ddele(*args, **kwargs)

    def Ndsurf(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ndsurf" decpreciated.  Use "ndsurf" instead'))
        return self.ndsurf(*args, **kwargs)

    def Ksum(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ksum" decpreciated.  Use "ksum" instead'))
        return self.ksum(*args, **kwargs)

    def Rstmac(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rstmac" decpreciated.  Use "rstmac" instead'))
        return self.rstmac(*args, **kwargs)

    def Psdwav(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Psdwav" decpreciated.  Use "psdwav" instead'))
        return self.psdwav(*args, **kwargs)

    def Mfcmmand(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mfcmmand" decpreciated.  Use "mfcmmand" instead'))
        return self.mfcmmand(*args, **kwargs)

    def Nldpost(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Nldpost" decpreciated.  Use "nldpost" instead'))
        return self.nldpost(*args, **kwargs)

    def Ascres(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ascres" decpreciated.  Use "ascres" instead'))
        return self.ascres(*args, **kwargs)

    def Pddmcs(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pddmcs" decpreciated.  Use "pddmcs" instead'))
        return self.pddmcs(*args, **kwargs)

    def Kesize(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Kesize" decpreciated.  Use "kesize" instead'))
        return self.kesize(*args, **kwargs)

    def Tbdele(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Tbdele" decpreciated.  Use "tbdele" instead'))
        return self.tbdele(*args, **kwargs)

    def Emsym(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Emsym" decpreciated.  Use "emsym" instead'))
        return self.emsym(*args, **kwargs)

    def Cplist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cplist" decpreciated.  Use "cplist" instead'))
        return self.cplist(*args, **kwargs)

    def Edcurve(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edcurve" decpreciated.  Use "edcurve" instead'))
        return self.edcurve(*args, **kwargs)

    def Etcontrol(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Etcontrol" decpreciated.  Use "etcontrol" instead'))
        return self.etcontrol(*args, **kwargs)

    def Gsbdata(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Gsbdata" decpreciated.  Use "gsbdata" instead'))
        return self.gsbdata(*args, **kwargs)

    def Kl(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Kl" decpreciated.  Use "kl" instead'))
        return self.kl(*args, **kwargs)

    def Arotat(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Arotat" decpreciated.  Use "arotat" instead'))
        return self.arotat(*args, **kwargs)

    def Title(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Title" decpreciated.  Use "title" instead'))
        return self.title(*args, **kwargs)

    def Cecyc(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cecyc" decpreciated.  Use "cecyc" instead'))
        return self.cecyc(*args, **kwargs)

    def Pretab(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pretab" decpreciated.  Use "pretab" instead'))
        return self.pretab(*args, **kwargs)

    def Aremesh(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Aremesh" decpreciated.  Use "aremesh" instead'))
        return self.aremesh(*args, **kwargs)

    def Lumpm(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lumpm" decpreciated.  Use "lumpm" instead'))
        return self.lumpm(*args, **kwargs)

    def Lczero(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lczero" decpreciated.  Use "lczero" instead'))
        return self.lczero(*args, **kwargs)

    def Bfa(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Bfa" decpreciated.  Use "bfa" instead'))
        return self.bfa(*args, **kwargs)

    def Bsax(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Bsax" decpreciated.  Use "bsax" instead'))
        return self.bsax(*args, **kwargs)

    def Lsymbol(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lsymbol" decpreciated.  Use "lsymbol" instead'))
        return self.lsymbol(*args, **kwargs)

    def Adele(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Adele" decpreciated.  Use "adele" instead'))
        return self.adele(*args, **kwargs)

    def Plgeom(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Plgeom" decpreciated.  Use "plgeom" instead'))
        return self.plgeom(*args, **kwargs)

    def Spmwrite(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Spmwrite" decpreciated.  Use "spmwrite" instead'))
        return self.spmwrite(*args, **kwargs)

    def Prsect(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Prsect" decpreciated.  Use "prsect" instead'))
        return self.prsect(*args, **kwargs)

    def Elseif(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Elseif" decpreciated.  Use "elseif" instead'))
        return self.elseif(*args, **kwargs)

    def Sfgrad(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sfgrad" decpreciated.  Use "sfgrad" instead'))
        return self.sfgrad(*args, **kwargs)

    def Nrm(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Nrm" decpreciated.  Use "nrm" instead'))
        return self.nrm(*args, **kwargs)

    def Rsys(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rsys" decpreciated.  Use "rsys" instead'))
        return self.rsys(*args, **kwargs)

    def Nocolor(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Nocolor" decpreciated.  Use "nocolor" instead'))
        return self.nocolor(*args, **kwargs)

    def Abbsav(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Abbsav" decpreciated.  Use "abbsav" instead'))
        return self.abbsav(*args, **kwargs)

    def Dsym(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Dsym" decpreciated.  Use "dsym" instead'))
        return self.dsym(*args, **kwargs)

    def Detab(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Detab" decpreciated.  Use "detab" instead'))
        return self.detab(*args, **kwargs)

    def Fjdele(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Fjdele" decpreciated.  Use "fjdele" instead'))
        return self.fjdele(*args, **kwargs)

    def Mlist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mlist" decpreciated.  Use "mlist" instead'))
        return self.mlist(*args, **kwargs)

    def Nslk(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Nslk" decpreciated.  Use "nslk" instead'))
        return self.nslk(*args, **kwargs)

    def Cdopt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cdopt" decpreciated.  Use "cdopt" instead'))
        return self.cdopt(*args, **kwargs)

    def Bfklist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Bfklist" decpreciated.  Use "bfklist" instead'))
        return self.bfklist(*args, **kwargs)

    def Bfk(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Bfk" decpreciated.  Use "bfk" instead'))
        return self.bfk(*args, **kwargs)

    def Mpwrite(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mpwrite" decpreciated.  Use "mpwrite" instead'))
        return self.mpwrite(*args, **kwargs)

    def Lsscale(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lsscale" decpreciated.  Use "lsscale" instead'))
        return self.lsscale(*args, **kwargs)

    def Fsum(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Fsum" decpreciated.  Use "fsum" instead'))
        return self.fsum(*args, **kwargs)

    def Oclist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Oclist" decpreciated.  Use "oclist" instead'))
        return self.oclist(*args, **kwargs)

    def Lsbw(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lsbw" decpreciated.  Use "lsbw" instead'))
        return self.lsbw(*args, **kwargs)

    def Pcross(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pcross" decpreciated.  Use "pcross" instead'))
        return self.pcross(*args, **kwargs)

    def Edcadapt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edcadapt" decpreciated.  Use "edcadapt" instead'))
        return self.edcadapt(*args, **kwargs)

    def Trpoin(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Trpoin" decpreciated.  Use "trpoin" instead'))
        return self.trpoin(*args, **kwargs)

    def Nlist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Nlist" decpreciated.  Use "nlist" instead'))
        return self.nlist(*args, **kwargs)

    def Cmwrite(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cmwrite" decpreciated.  Use "cmwrite" instead'))
        return self.cmwrite(*args, **kwargs)

    def Display(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Display" decpreciated.  Use "display" instead'))
        return self.display(*args, **kwargs)

    def Dcum(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Dcum" decpreciated.  Use "dcum" instead'))
        return self.dcum(*args, **kwargs)

    def L2tan(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"L2tan" decpreciated.  Use "l2tan" instead'))
        return self.l2tan(*args, **kwargs)

    def Cecheck(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cecheck" decpreciated.  Use "cecheck" instead'))
        return self.cecheck(*args, **kwargs)

    def Focus(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Focus" decpreciated.  Use "focus" instead'))
        return self.focus(*args, **kwargs)

    def Inquire(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Inquire" decpreciated.  Use "inquire" instead'))
        return self.inquire(*args, **kwargs)

    def Gssol(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Gssol" decpreciated.  Use "gssol" instead'))
        return self.gssol(*args, **kwargs)

    def Light(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Light" decpreciated.  Use "light" instead'))
        return self.light(*args, **kwargs)

    def Mftol(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mftol" decpreciated.  Use "mftol" instead'))
        return self.mftol(*args, **kwargs)

    def Tbfield(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Tbfield" decpreciated.  Use "tbfield" instead'))
        return self.tbfield(*args, **kwargs)

    def Etype(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Etype" decpreciated.  Use "etype" instead'))
        return self.etype(*args, **kwargs)

    def Mpcopy(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mpcopy" decpreciated.  Use "mpcopy" instead'))
        return self.mpcopy(*args, **kwargs)

    def Pasave(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pasave" decpreciated.  Use "pasave" instead'))
        return self.pasave(*args, **kwargs)

    def Golist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Golist" decpreciated.  Use "golist" instead'))
        return self.golist(*args, **kwargs)

    def Eshape(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Eshape" decpreciated.  Use "eshape" instead'))
        return self.eshape(*args, **kwargs)

    def Dmpoption(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Dmpoption" decpreciated.  Use "dmpoption" instead'))
        return self.dmpoption(*args, **kwargs)

    def Anmres(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Anmres" decpreciated.  Use "anmres" instead'))
        return self.anmres(*args, **kwargs)

    def Vup(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vup" decpreciated.  Use "vup" instead'))
        return self.vup(*args, **kwargs)

    def Waves(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Waves" decpreciated.  Use "waves" instead'))
        return self.waves(*args, **kwargs)

    def Ldele(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ldele" decpreciated.  Use "ldele" instead'))
        return self.ldele(*args, **kwargs)

    def Dmove(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Dmove" decpreciated.  Use "dmove" instead'))
        return self.dmove(*args, **kwargs)

    def Mshpattern(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mshpattern" decpreciated.  Use "mshpattern" instead'))
        return self.mshpattern(*args, **kwargs)

    def Pdexe(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pdexe" decpreciated.  Use "pdexe" instead'))
        return self.pdexe(*args, **kwargs)

    def Trlcy(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Trlcy" decpreciated.  Use "trlcy" instead'))
        return self.trlcy(*args, **kwargs)

    def Asol(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Asol" decpreciated.  Use "asol" instead'))
        return self.asol(*args, **kwargs)

    def Pdinqr(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pdinqr" decpreciated.  Use "pdinqr" instead'))
        return self.pdinqr(*args, **kwargs)

    def Slist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Slist" decpreciated.  Use "slist" instead'))
        return self.slist(*args, **kwargs)

    def Edcnstr(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edcnstr" decpreciated.  Use "edcnstr" instead'))
        return self.edcnstr(*args, **kwargs)

    def Esol(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Esol" decpreciated.  Use "esol" instead'))
        return self.esol(*args, **kwargs)

    def Quit(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Quit" decpreciated.  Use "quit" instead'))
        return self.quit(*args, **kwargs)

    def Addam(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Addam" decpreciated.  Use "addam" instead'))
        return self.addam(*args, **kwargs)

    def Nsla(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Nsla" decpreciated.  Use "nsla" instead'))
        return self.nsla(*args, **kwargs)

    def Nprint(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Nprint" decpreciated.  Use "nprint" instead'))
        return self.nprint(*args, **kwargs)

    def Gline(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Gline" decpreciated.  Use "gline" instead'))
        return self.gline(*args, **kwargs)

    def Pspec(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pspec" decpreciated.  Use "pspec" instead'))
        return self.pspec(*args, **kwargs)

    def Rmmlist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rmmlist" decpreciated.  Use "rmmlist" instead'))
        return self.rmmlist(*args, **kwargs)

    def Kscon(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Kscon" decpreciated.  Use "kscon" instead'))
        return self.kscon(*args, **kwargs)

    def Int1(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Int1" decpreciated.  Use "int1" instead'))
        return self.int1(*args, **kwargs)

    def Vput(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vput" decpreciated.  Use "vput" instead'))
        return self.vput(*args, **kwargs)

    def Edasmp(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edasmp" decpreciated.  Use "edasmp" instead'))
        return self.edasmp(*args, **kwargs)

    def Chkmsh(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Chkmsh" decpreciated.  Use "chkmsh" instead'))
        return self.chkmsh(*args, **kwargs)

    def Pldisp(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pldisp" decpreciated.  Use "pldisp" instead'))
        return self.pldisp(*args, **kwargs)

    def Cfopen(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cfopen" decpreciated.  Use "cfopen" instead'))
        return self.cfopen(*args, **kwargs)

    def Mater(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mater" decpreciated.  Use "mater" instead'))
        return self.mater(*args, **kwargs)

    def Igesin(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Igesin" decpreciated.  Use "igesin" instead'))
        return self.igesin(*args, **kwargs)

    def Emf(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Emf" decpreciated.  Use "emf" instead'))
        return self.emf(*args, **kwargs)

    def Smax(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Smax" decpreciated.  Use "smax" instead'))
        return self.smax(*args, **kwargs)

    def Ndist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ndist" decpreciated.  Use "ndist" instead'))
        return self.ndist(*args, **kwargs)

    def Knode(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Knode" decpreciated.  Use "knode" instead'))
        return self.knode(*args, **kwargs)

    def Selist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Selist" decpreciated.  Use "selist" instead'))
        return self.selist(*args, **kwargs)

    def Emft(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Emft" decpreciated.  Use "emft" instead'))
        return self.emft(*args, **kwargs)

    def Solu(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Solu" decpreciated.  Use "solu" instead'))
        return self.solu(*args, **kwargs)

    def Slashfdele(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Slashfdele" decpreciated.  Use "slashfdele" instead'))
        return self.slashfdele(*args, **kwargs)

    def Prrfor(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Prrfor" decpreciated.  Use "prrfor" instead'))
        return self.prrfor(*args, **kwargs)

    def Xfdata(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Xfdata" decpreciated.  Use "xfdata" instead'))
        return self.xfdata(*args, **kwargs)

    def Rmsave(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rmsave" decpreciated.  Use "rmsave" instead'))
        return self.rmsave(*args, **kwargs)

    def Pnum(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pnum" decpreciated.  Use "pnum" instead'))
        return self.pnum(*args, **kwargs)

    def Rsopt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rsopt" decpreciated.  Use "rsopt" instead'))
        return self.rsopt(*args, **kwargs)

    def Fk(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Fk" decpreciated.  Use "fk" instead'))
        return self.fk(*args, **kwargs)

    def Pmacro(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pmacro" decpreciated.  Use "pmacro" instead'))
        return self.pmacro(*args, **kwargs)

    def Emore(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Emore" decpreciated.  Use "emore" instead'))
        return self.emore(*args, **kwargs)

    def Jsol(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Jsol" decpreciated.  Use "jsol" instead'))
        return self.jsol(*args, **kwargs)

    def Gcolumn(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Gcolumn" decpreciated.  Use "gcolumn" instead'))
        return self.gcolumn(*args, **kwargs)

    def Add(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Add" decpreciated.  Use "add" instead'))
        return self.add(*args, **kwargs)

    def Numcmp(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Numcmp" decpreciated.  Use "numcmp" instead'))
        return self.numcmp(*args, **kwargs)

    def Enddo(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Enddo" decpreciated.  Use "enddo" instead'))
        return self.enddo(*args, **kwargs)

    def Mmf(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mmf" decpreciated.  Use "mmf" instead'))
        return self.mmf(*args, **kwargs)

    def Sfact(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sfact" decpreciated.  Use "sfact" instead'))
        return self.sfact(*args, **kwargs)

    def Se(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Se" decpreciated.  Use "se" instead'))
        return self.se(*args, **kwargs)

    def Cgomga(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cgomga" decpreciated.  Use "cgomga" instead'))
        return self.cgomga(*args, **kwargs)

    def Nlgeom(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Nlgeom" decpreciated.  Use "nlgeom" instead'))
        return self.nlgeom(*args, **kwargs)

    def Slashclog(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Slashclog" decpreciated.  Use "slashclog" instead'))
        return self.slashclog(*args, **kwargs)

    def Quad(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Quad" decpreciated.  Use "quad" instead'))
        return self.quad(*args, **kwargs)

    def Center(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Center" decpreciated.  Use "center" instead'))
        return self.center(*args, **kwargs)

    def Sexp(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sexp" decpreciated.  Use "sexp" instead'))
        return self.sexp(*args, **kwargs)

    def Pmgtran(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pmgtran" decpreciated.  Use "pmgtran" instead'))
        return self.pmgtran(*args, **kwargs)

    def Clocal(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Clocal" decpreciated.  Use "clocal" instead'))
        return self.clocal(*args, **kwargs)

    def Create(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Create" decpreciated.  Use "create" instead'))
        return self.create(*args, **kwargs)

    def Plmc(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Plmc" decpreciated.  Use "plmc" instead'))
        return self.plmc(*args, **kwargs)

    def Smsurf(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Smsurf" decpreciated.  Use "smsurf" instead'))
        return self.smsurf(*args, **kwargs)

    def Kscale(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Kscale" decpreciated.  Use "kscale" instead'))
        return self.kscale(*args, **kwargs)

    def Cycfiles(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cycfiles" decpreciated.  Use "cycfiles" instead'))
        return self.cycfiles(*args, **kwargs)

    def Nstore(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Nstore" decpreciated.  Use "nstore" instead'))
        return self.nstore(*args, **kwargs)

    def Gtype(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Gtype" decpreciated.  Use "gtype" instead'))
        return self.gtype(*args, **kwargs)

    def Pscontrol(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pscontrol" decpreciated.  Use "pscontrol" instead'))
        return self.pscontrol(*args, **kwargs)

    def Edpc(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edpc" decpreciated.  Use "edpc" instead'))
        return self.edpc(*args, **kwargs)

    def Sallow(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sallow" decpreciated.  Use "sallow" instead'))
        return self.sallow(*args, **kwargs)

    def Usrelem(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Usrelem" decpreciated.  Use "usrelem" instead'))
        return self.usrelem(*args, **kwargs)

    def Oczone(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Oczone" decpreciated.  Use "oczone" instead'))
        return self.oczone(*args, **kwargs)

    def Susel(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Susel" decpreciated.  Use "susel" instead'))
        return self.susel(*args, **kwargs)

    def Emodif(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Emodif" decpreciated.  Use "emodif" instead'))
        return self.emodif(*args, **kwargs)

    def Cmdele(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cmdele" decpreciated.  Use "cmdele" instead'))
        return self.cmdele(*args, **kwargs)

    def Ksymm(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ksymm" decpreciated.  Use "ksymm" instead'))
        return self.ksymm(*args, **kwargs)

    def Plcrack(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Plcrack" decpreciated.  Use "plcrack" instead'))
        return self.plcrack(*args, **kwargs)

    def Torqsum(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Torqsum" decpreciated.  Use "torqsum" instead'))
        return self.torqsum(*args, **kwargs)

    def Bsm2(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Bsm2" decpreciated.  Use "bsm2" instead'))
        return self.bsm2(*args, **kwargs)

    def Cskp(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cskp" decpreciated.  Use "cskp" instead'))
        return self.cskp(*args, **kwargs)

    def Kuse(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Kuse" decpreciated.  Use "kuse" instead'))
        return self.kuse(*args, **kwargs)

    def Icscale(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Icscale" decpreciated.  Use "icscale" instead'))
        return self.icscale(*args, **kwargs)

    def Ssbt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ssbt" decpreciated.  Use "ssbt" instead'))
        return self.ssbt(*args, **kwargs)

    def Axlab(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Axlab" decpreciated.  Use "axlab" instead'))
        return self.axlab(*args, **kwargs)

    def N(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"N" decpreciated.  Use "n" instead'))
        return self.n(*args, **kwargs)

    def Svtyp(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Svtyp" decpreciated.  Use "svtyp" instead'))
        return self.svtyp(*args, **kwargs)

    def Rigid(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rigid" decpreciated.  Use "rigid" instead'))
        return self.rigid(*args, **kwargs)

    def Abs(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Abs" decpreciated.  Use "abs" instead'))
        return self.abs(*args, **kwargs)

    def Qrdopt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Qrdopt" decpreciated.  Use "qrdopt" instead'))
        return self.qrdopt(*args, **kwargs)

    def Dcvswp(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Dcvswp" decpreciated.  Use "dcvswp" instead'))
        return self.dcvswp(*args, **kwargs)

    def Mfrelax(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mfrelax" decpreciated.  Use "mfrelax" instead'))
        return self.mfrelax(*args, **kwargs)

    def Asel(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Asel" decpreciated.  Use "asel" instead'))
        return self.asel(*args, **kwargs)

    def Rmflvec(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rmflvec" decpreciated.  Use "rmflvec" instead'))
        return self.rmflvec(*args, **kwargs)

    def Hemiopt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Hemiopt" decpreciated.  Use "hemiopt" instead'))
        return self.hemiopt(*args, **kwargs)

    def Keyopt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Keyopt" decpreciated.  Use "keyopt" instead'))
        return self.keyopt(*args, **kwargs)

    def Ktran(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ktran" decpreciated.  Use "ktran" instead'))
        return self.ktran(*args, **kwargs)

    def Ui(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ui" decpreciated.  Use "ui" instead'))
        return self.ui(*args, **kwargs)

    def Fmagsum(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Fmagsum" decpreciated.  Use "fmagsum" instead'))
        return self.fmagsum(*args, **kwargs)

    def Cyl5(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cyl5" decpreciated.  Use "cyl5" instead'))
        return self.cyl5(*args, **kwargs)

    def Unpause(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Unpause" decpreciated.  Use "unpause" instead'))
        return self.unpause(*args, **kwargs)

    def Cmmod(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cmmod" decpreciated.  Use "cmmod" instead'))
        return self.cmmod(*args, **kwargs)

    def Edcontact(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edcontact" decpreciated.  Use "edcontact" instead'))
        return self.edcontact(*args, **kwargs)

    def Vtype(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vtype" decpreciated.  Use "vtype" instead'))
        return self.vtype(*args, **kwargs)

    def Dlist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Dlist" decpreciated.  Use "dlist" instead'))
        return self.dlist(*args, **kwargs)

    def Vdrag(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vdrag" decpreciated.  Use "vdrag" instead'))
        return self.vdrag(*args, **kwargs)

    def Spopt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Spopt" decpreciated.  Use "spopt" instead'))
        return self.spopt(*args, **kwargs)

    def Noerase(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Noerase" decpreciated.  Use "noerase" instead'))
        return self.noerase(*args, **kwargs)

    def Edclist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edclist" decpreciated.  Use "edclist" instead'))
        return self.edclist(*args, **kwargs)

    def Fsnode(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Fsnode" decpreciated.  Use "fsnode" instead'))
        return self.fsnode(*args, **kwargs)

    def Wsprings(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Wsprings" decpreciated.  Use "wsprings" instead'))
        return self.wsprings(*args, **kwargs)

    def Estif(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Estif" decpreciated.  Use "estif" instead'))
        return self.estif(*args, **kwargs)

    def Trpdel(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Trpdel" decpreciated.  Use "trpdel" instead'))
        return self.trpdel(*args, **kwargs)

    def Mmass(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mmass" decpreciated.  Use "mmass" instead'))
        return self.mmass(*args, **kwargs)

    def Mfrc(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mfrc" decpreciated.  Use "mfrc" instead'))
        return self.mfrc(*args, **kwargs)

    def Mpdata(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mpdata" decpreciated.  Use "mpdata" instead'))
        return self.mpdata(*args, **kwargs)

    def Write(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Write" decpreciated.  Use "write" instead'))
        return self.write(*args, **kwargs)

    def Adams(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Adams" decpreciated.  Use "adams" instead'))
        return self.adams(*args, **kwargs)

    def Cycspec(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cycspec" decpreciated.  Use "cycspec" instead'))
        return self.cycspec(*args, **kwargs)

    def Atran(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Atran" decpreciated.  Use "atran" instead'))
        return self.atran(*args, **kwargs)

    def Nladaptive(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Nladaptive" decpreciated.  Use "nladaptive" instead'))
        return self.nladaptive(*args, **kwargs)

    def Cs(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cs" decpreciated.  Use "cs" instead'))
        return self.cs(*args, **kwargs)

    def Nsll(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Nsll" decpreciated.  Use "nsll" instead'))
        return self.nsll(*args, **kwargs)

    def Cbdof(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cbdof" decpreciated.  Use "cbdof" instead'))
        return self.cbdof(*args, **kwargs)

    def Tref(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Tref" decpreciated.  Use "tref" instead'))
        return self.tref(*args, **kwargs)

    def Smcons(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Smcons" decpreciated.  Use "smcons" instead'))
        return self.smcons(*args, **kwargs)

    def Hptcreate(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Hptcreate" decpreciated.  Use "hptcreate" instead'))
        return self.hptcreate(*args, **kwargs)

    def A(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"A" decpreciated.  Use "a" instead'))
        return self.a(*args, **kwargs)

    def Mpdres(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mpdres" decpreciated.  Use "mpdres" instead'))
        return self.mpdres(*args, **kwargs)

    def Mptgen(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mptgen" decpreciated.  Use "mptgen" instead'))
        return self.mptgen(*args, **kwargs)

    def Anfile(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Anfile" decpreciated.  Use "anfile" instead'))
        return self.anfile(*args, **kwargs)

    def Bfv(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Bfv" decpreciated.  Use "bfv" instead'))
        return self.bfv(*args, **kwargs)

    def Arctrm(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Arctrm" decpreciated.  Use "arctrm" instead'))
        return self.arctrm(*args, **kwargs)

    def Edtp(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edtp" decpreciated.  Use "edtp" instead'))
        return self.edtp(*args, **kwargs)

    def Bfescal(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Bfescal" decpreciated.  Use "bfescal" instead'))
        return self.bfescal(*args, **kwargs)

    def Neqit(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Neqit" decpreciated.  Use "neqit" instead'))
        return self.neqit(*args, **kwargs)

    def Asbl(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Asbl" decpreciated.  Use "asbl" instead'))
        return self.asbl(*args, **kwargs)

    def Mplib(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mplib" decpreciated.  Use "mplib" instead'))
        return self.mplib(*args, **kwargs)

    def Smin(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Smin" decpreciated.  Use "smin" instead'))
        return self.smin(*args, **kwargs)

    def Vsum(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vsum" decpreciated.  Use "vsum" instead'))
        return self.vsum(*args, **kwargs)

    def Eusort(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Eusort" decpreciated.  Use "eusort" instead'))
        return self.eusort(*args, **kwargs)

    def Srss(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Srss" decpreciated.  Use "srss" instead'))
        return self.srss(*args, **kwargs)

    def Sfl(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sfl" decpreciated.  Use "sfl" instead'))
        return self.sfl(*args, **kwargs)

    def Vsbv(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Vsbv" decpreciated.  Use "vsbv" instead'))
        return self.vsbv(*args, **kwargs)

    def Impd(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Impd" decpreciated.  Use "impd" instead'))
        return self.impd(*args, **kwargs)

    def Tiff(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Tiff" decpreciated.  Use "tiff" instead'))
        return self.tiff(*args, **kwargs)

    def Radopt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Radopt" decpreciated.  Use "radopt" instead'))
        return self.radopt(*args, **kwargs)

    def Cformat(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cformat" decpreciated.  Use "cformat" instead'))
        return self.cformat(*args, **kwargs)

    def Filname(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Filname" decpreciated.  Use "filname" instead'))
        return self.filname(*args, **kwargs)

    def Fsplot(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Fsplot" decpreciated.  Use "fsplot" instead'))
        return self.fsplot(*args, **kwargs)

    def Edadapt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edadapt" decpreciated.  Use "edadapt" instead'))
        return self.edadapt(*args, **kwargs)

    def Klist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Klist" decpreciated.  Use "klist" instead'))
        return self.klist(*args, **kwargs)

    def D(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"D" decpreciated.  Use "d" instead'))
        return self.d(*args, **kwargs)

    def Fclist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Fclist" decpreciated.  Use "fclist" instead'))
        return self.fclist(*args, **kwargs)

    def Ppath(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ppath" decpreciated.  Use "ppath" instead'))
        return self.ppath(*args, **kwargs)

    def Clrmshln(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Clrmshln" decpreciated.  Use "clrmshln" instead'))
        return self.clrmshln(*args, **kwargs)

    def Pvect(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pvect" decpreciated.  Use "pvect" instead'))
        return self.pvect(*args, **kwargs)

    def Cmsel(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cmsel" decpreciated.  Use "cmsel" instead'))
        return self.cmsel(*args, **kwargs)

    def Tbpt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Tbpt" decpreciated.  Use "tbpt" instead'))
        return self.tbpt(*args, **kwargs)

    def Dsurf(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Dsurf" decpreciated.  Use "dsurf" instead'))
        return self.dsurf(*args, **kwargs)

    def Plvar(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Plvar" decpreciated.  Use "plvar" instead'))
        return self.plvar(*args, **kwargs)

    def Pdlhs(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pdlhs" decpreciated.  Use "pdlhs" instead'))
        return self.pdlhs(*args, **kwargs)

    def Rsfit(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rsfit" decpreciated.  Use "rsfit" instead'))
        return self.rsfit(*args, **kwargs)

    def Edint(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edint" decpreciated.  Use "edint" instead'))
        return self.edint(*args, **kwargs)

    def Mshkey(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mshkey" decpreciated.  Use "mshkey" instead'))
        return self.mshkey(*args, **kwargs)

    def Intsrf(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Intsrf" decpreciated.  Use "intsrf" instead'))
        return self.intsrf(*args, **kwargs)

    def Device(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Device" decpreciated.  Use "device" instead'))
        return self.device(*args, **kwargs)

    def Block(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Block" decpreciated.  Use "block" instead'))
        return self.block(*args, **kwargs)

    def Modseloption(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Modseloption" decpreciated.  Use "modseloption" instead'))
        return self.modseloption(*args, **kwargs)

    def Ksel(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ksel" decpreciated.  Use "ksel" instead'))
        return self.ksel(*args, **kwargs)

    def Mfem(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mfem" decpreciated.  Use "mfem" instead'))
        return self.mfem(*args, **kwargs)

    def Trplis(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Trplis" decpreciated.  Use "trplis" instead'))
        return self.trplis(*args, **kwargs)

    def Norl(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Norl" decpreciated.  Use "norl" instead'))
        return self.norl(*args, **kwargs)

    def Mult(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mult" decpreciated.  Use "mult" instead'))
        return self.mult(*args, **kwargs)

    def Etable(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Etable" decpreciated.  Use "etable" instead'))
        return self.etable(*args, **kwargs)

    def Bfalist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Bfalist" decpreciated.  Use "bfalist" instead'))
        return self.bfalist(*args, **kwargs)

    def Lcsum(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Lcsum" decpreciated.  Use "lcsum" instead'))
        return self.lcsum(*args, **kwargs)

    def Anim(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Anim" decpreciated.  Use "anim" instead'))
        return self.anim(*args, **kwargs)

    def Ocread(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ocread" decpreciated.  Use "ocread" instead'))
        return self.ocread(*args, **kwargs)

    def Mfdtime(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mfdtime" decpreciated.  Use "mfdtime" instead'))
        return self.mfdtime(*args, **kwargs)

    def Edri(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edri" decpreciated.  Use "edri" instead'))
        return self.edri(*args, **kwargs)

    def Fdele(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Fdele" decpreciated.  Use "fdele" instead'))
        return self.fdele(*args, **kwargs)

    def Latt(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Latt" decpreciated.  Use "latt" instead'))
        return self.latt(*args, **kwargs)

    def Rmclist(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Rmclist" decpreciated.  Use "rmclist" instead'))
        return self.rmclist(*args, **kwargs)

    def Edsp(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Edsp" decpreciated.  Use "edsp" instead'))
        return self.edsp(*args, **kwargs)

    def Czmesh(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Czmesh" decpreciated.  Use "czmesh" instead'))
        return self.czmesh(*args, **kwargs)

    def Keep(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Keep" decpreciated.  Use "keep" instead'))
        return self.keep(*args, **kwargs)

    def Voper(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Voper" decpreciated.  Use "voper" instead'))
        return self.voper(*args, **kwargs)

    def Bfadele(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Bfadele" decpreciated.  Use "bfadele" instead'))
        return self.bfadele(*args, **kwargs)

    def F(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"F" decpreciated.  Use "f" instead'))
        return self.f(*args, **kwargs)

    def Ewrite(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Ewrite" decpreciated.  Use "ewrite" instead'))
        return self.ewrite(*args, **kwargs)

    def Writemap(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Writemap" decpreciated.  Use "writemap" instead'))
        return self.writemap(*args, **kwargs)

    def Sfcalc(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Sfcalc" decpreciated.  Use "sfcalc" instead'))
        return self.sfcalc(*args, **kwargs)

    def Hptdelete(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Hptdelete" decpreciated.  Use "hptdelete" instead'))
        return self.hptdelete(*args, **kwargs)

    def Tbplot(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Tbplot" decpreciated.  Use "tbplot" instead'))
        return self.tbplot(*args, **kwargs)

    def Pras(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pras" decpreciated.  Use "pras" instead'))
        return self.pras(*args, **kwargs)

    def Cscir(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Cscir" decpreciated.  Use "cscir" instead'))
        return self.cscir(*args, **kwargs)

    def Pdshis(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Pdshis" decpreciated.  Use "pdshis" instead'))
        return self.pdshis(*args, **kwargs)

    def Mforder(self, *args, **kwargs):
        warnings.warn(DeprecationWarning('"Mforder" decpreciated.  Use "mforder" instead'))
        return self.mforder(*args, **kwargs)

    
