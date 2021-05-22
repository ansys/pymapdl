from ._commands import element  # TODO: move out of this module

from ._commands import hidden
from ._commands import session, database, preproc


class Commands:
    """Wrapped MAPDL commands"""

    ##################
    # Session commands
    ##################

    config = session.run_controls.config
    cwd = session.run_controls.cwd
    filname = session.run_controls.filname
    keyw = session.run_controls.keyw
    memm = session.run_controls.memm
    nerr = session.run_controls.nerr
    pause = session.run_controls.pause
    starstatus = session.run_controls.starstatus
    syp = session.run_controls.syp
    sys = session.run_controls.sys
    unpause = session.run_controls.unpause

    anstoaqwa = session.files.anstoaqwa
    anstoasas = session.files.anstoasas
    assign = session.files.assign
    slashclog = session.files.slashclog
    copy = session.files.copy
    delete = session.files.delete
    fcomp = session.files.fcomp
    lgwrite = session.files.lgwrite
    list = session.files.list
    rename = session.files.rename

    com = session.list_controls.com
    golist = session.list_controls.golist
    gopr = session.list_controls.gopr
    nolist = session.list_controls.nolist
    nopr = session.list_controls.nopr

    aux2 = session.processor_entry.aux2
    aux3 = session.processor_entry.aux3
    aux12 = session.processor_entry.aux12
    aux15 = session.processor_entry.aux15
    finish = session.processor_entry.finish
    map = session.processor_entry.map
    post1 = session.processor_entry.post1
    post26 = session.processor_entry.post26
    prep7 = session.processor_entry.prep7
    quit = session.processor_entry.quit
    slashsolu = session.processor_entry.slashsolu

    ###################
    # Database commands
    ###################
    cm = database.components.cm
    cmdele = database.components.cmdele
    cmedit = database.components.cmedit
    cmgrp = database.components.cmgrp
    cmlist = database.components.cmlist
    cmmod = database.components.cmmod
    cmplot = database.components.cmplot
    cmsel = database.components.cmsel
    cmwrite = database.components.cmwrite

    clocal = database.coord_sys.clocal
    cs = database.coord_sys.cs
    cscir = database.coord_sys.cscir
    csdele = database.coord_sys.csdele
    cskp = database.coord_sys.cskp
    cslist = database.coord_sys.cslist
    cswpla = database.coord_sys.cswpla
    csys = database.coord_sys.csys
    local = database.coord_sys.local

    fitem = database.picking.fitem
    flst = database.picking.flst

    allsel = database.selecting.allsel
    asll = database.selecting.asll
    asel = database.selecting.asel
    aslv = database.selecting.aslv
    dofsel = database.selecting.dofsel
    esel = database.selecting.esel
    esla = database.selecting.esla
    esll = database.selecting.esll
    esln = database.selecting.esln
    eslv = database.selecting.eslv
    ksel = database.selecting.ksel
    ksll = database.selecting.ksll
    ksln = database.selecting.ksln
    lsel = database.selecting.lsel
    lsla = database.selecting.lsla
    lslk = database.selecting.lslk
    nsel = database.selecting.nsel
    nsla = database.selecting.nsla
    nsle = database.selecting.nsle
    nslk = database.selecting.nslk
    nsll = database.selecting.nsll
    nslv = database.selecting.nslv
    partsel = database.selecting.partsel
    vsel = database.selecting.vsel
    vsla = database.selecting.vsla

    resume = database.setup.resume
    save = database.setup.save
    smbc = database.setup.smbc
    stat = database.setup.stat
    stitle = database.setup.stitle
    title = database.setup.title
    units = database.setup.units

    


    ################
    # PREP7 commands
    ################
    aflist = preproc.database.aflist
    cdread = preproc.database.cdread
    cdwrite = preproc.database.cdwrite
    cdopt = preproc.database.cdopt
    cecheck = preproc.database.cecheck
    check = preproc.database.check
    cncheck = preproc.database.cncheck
    fc = preproc.database.fc
    fccheck = preproc.database.fccheck
    fcdele = preproc.database.fcdele
    fclist = preproc.database.fclist
    igesout = preproc.database.igesout
    mfimport = preproc.database.mfimport
    nooffset = preproc.database.nooffset
    numcmp = preproc.database.numcmp
    nummrg = preproc.database.nummrg
    numoff = preproc.database.numoff
    numstr = preproc.database.numstr

    # element type
    dof = preproc.element_type.dof
    elbow = preproc.element_type.elbow
    et = preproc.element_type.et
    etchg = preproc.element_type.etchg
    etcontrol = preproc.element_type.etcontrol
    etdele = preproc.element_type.etdele
    etlist = preproc.element_type.etlist
    keyopt = preproc.element_type.keyopt
    nsrv = preproc.element_type.nsvr

    # real constants
    r = preproc.real_constants.r
    rdele = preproc.real_constants.rdele
    rlist = preproc.real_constants.rlist
    rmodif = preproc.real_constants.rmodif
    rmore = preproc.real_constants.rmore
    setfgap = preproc.real_constants.setfgap

    # materials
    emunit = preproc.materials.emunit
    mp = preproc.materials.mp
    mpamod = preproc.materials.mpamod
    mpchg = preproc.materials.mpchg
    mpcopy = preproc.materials.mpcopy
    mpdata = preproc.materials.mpdata
    mpdele = preproc.materials.mpdele
    mpdres = preproc.materials.mpdres
    mplib = preproc.materials.mplib
    mplist = preproc.materials.mplist
    mpplot = preproc.materials.mpplot
    mpread = preproc.materials.mpread
    mptemp = preproc.materials.mptemp
    mptgen = preproc.materials.mptgen
    mptres = preproc.materials.mptres
    mpwrite = preproc.materials.mpwrite
    tbft = preproc.materials.tbft
    uimp = preproc.materials.uimp

    # material_data_tables
    tb = preproc.material_data_tables.tb
    tbcopy = preproc.material_data_tables.tbcopy
    tbdata = preproc.material_data_tables.tbdata
    tbdele = preproc.material_data_tables.tbdele
    tbeo = preproc.material_data_tables.tbeo
    tbfield = preproc.material_data_tables.tbfield
    tbin = preproc.material_data_tables.tbin
    tblist = preproc.material_data_tables.tblist
    tbmodif = preproc.material_data_tables.tbmodif
    tbplot = preproc.material_data_tables.tbplot
    tbpt = preproc.material_data_tables.tbpt
    tbtemp = preproc.material_data_tables.tbtemp

    # hidden
    _batch = hidden.batch
