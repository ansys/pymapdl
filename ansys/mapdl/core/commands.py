from ._commands import (element, element_type, real_constants,
                        database, materials, material_data_tables,
)


class Commands():
    """Wrapped MAPDL commands"""

    # database
    aflist = database.aflist
    cdread = database.cdread
    cdwrite = database.cdwrite
    cdopt = database.cdopt
    cecheck = database.cecheck
    check = database.check
    cncheck = database.cncheck
    fc = database.fc
    fccheck = database.fccheck
    fcdele = database.fcdele
    fclist = database.fclist
    igesout = database.igesout
    mfimport = database.mfimport
    nooffset = database.nooffset
    numcmp = database.numcmp
    nummrg = database.nummrg
    numoff = database.numoff
    numstr = database.numstr
    prep7 = database.prep7

    # element type
    dof = element_type.dof
    elbow = element_type.elbow
    et = element_type.et
    etchg = element_type.etchg
    etcontrol = element_type.etcontrol
    etdele = element_type.etdele
    etlist = element_type.etlist
    keyopt = element_type.keyopt
    nsrv = element_type.nsvr

    # real constants
    r = real_constants.r
    rdele = real_constants.rdele
    rlist = real_constants.rlist
    rmodif = real_constants.rmodif
    rmore = real_constants.rmore
    setfgap = real_constants.setfgap

    # materials
    emunit = materials.emunit
    mp = materials.mp
    mpamod = materials.mpamod
    mpchg = materials.mpchg
    mpcopy = materials.mpcopy
    mpdata = materials.mpdata
    mpdele = materials.mpdele
    mpdres = materials.mpdres
    mplib = materials.mplib
    mplist = materials.mplist
    mpplot = materials.mpplot
    mpread = materials.mpread
    mptemp = materials.mptemp
    mptgen = materials.mptgen
    mptres = materials.mptres
    mpwrite = materials.mpwrite
    tbft = materials.tbft
    uimp = materials.uimp

    # material_data_tables
    tb = material_data_tables.tb
    tbcopy = material_data_tables.tbcopy
    tbdata = material_data_tables.tbdata
    tbdele = material_data_tables.tbdele
    tbeo = material_data_tables.tbeo
    tbfield = material_data_tables.tbfield
    tbin = material_data_tables.tbin
    tblist = material_data_tables.tblist
    tbmodif = material_data_tables.tbmodif
    tbplot = material_data_tables.tbplot
    tbpt = material_data_tables.tbpt
    tbtemp = material_data_tables.tbtemp

    # Element commands
    e = element.e
    ealive = element.ealive
    edele = element.edele
    edtp = element.edtp
    egen = element.egen
    einfin = element.einfin
    eintf = element.eintf
    ekill = element.ekill
    elem = element.elem
    elist = element.elist
    ematwrite = element.ematwrite
    emodif = element.emodif
    emore = element.emore
    en = element.en
    engen = element.engen
    enorm = element.enorm
    ensym = element.ensym
    eorient = element.eorient
    eplot = element.eplot
    eread = element.eread
    erefine = element.erefine
    ereinf = element.ereinf
    errang = element.errang
    escheck = element.escheck
    esel = element.esel
    eshape = element.eshape
    esla = element.esla
    esll = element.esll
    esln = element.esln
    eslv = element.eslv
    esol = element.esol
    esort = element.esort
    estif = element.estif
    esurf = element.esurf
    esym = element.esym
    esys = element.esys
    etable = element.etable
    etype = element.etype
    eusort = element.eusort
    ewrite = element.ewrite
    extopt = element.extopt

