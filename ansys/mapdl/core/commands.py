from ._commands import (hidden, session, database, preproc, aux15_, map_cmd,
                        aux2_, aux3_, aux12_, reduced, apdl
)

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

    kwpave = database.working_plane.kwpave
    kwplan = database.working_plane.kwplan
    lwplan = database.working_plane.lwplan
    nwpave = database.working_plane.nwpave
    nwplan = database.working_plane.nwplan
    wpave = database.working_plane.wpave
    wpcsys = database.working_plane.wpcsys
    wplane = database.working_plane.wplane
    wpoffs = database.working_plane.wpoffs
    wprota = database.working_plane.wprota
    wpstyl = database.working_plane.wpstyl

    # mapping processor
    ftype = map_cmd.ftype
    map_ = map_cmd.map_
    plgeom = map_cmd.plgeom
    plmap = map_cmd.plmap
    read = map_cmd.read
    slashmap = map_cmd.slashmap
    target = map_cmd.target
    writemap = map_cmd.writemap

    # AUX15
    igesin = aux15_.igesin
    ioptn = aux15_.ioptn

    # AUX2
    combine = aux2_.bin_manip.combine
    hbmat = aux2_.bin_manip.hbmat
    psmat = aux2_.bin_manip.psmat
    dump = aux2_.bin_dump.dump
    fileaux2 = aux2_.bin_dump.fileaux2
    form = aux2_.bin_dump.form
    ptr = aux2_.bin_dump.ptr

    # AUX3
    compress = aux3_.compress
    fileaux3 = aux3_.fileaux3
    modify = aux3_.modify
    undelete = aux3_.undelete

    # AUX12
    emis = aux12_.radiation_mat.emis
    geom = aux12_.radiation_mat.geom
    mprint = aux12_.radiation_mat.mprint
    space = aux12_.radiation_mat.space
    vtype = aux12_.radiation_mat.vtype
    write = aux12_.radiation_mat.write
    stef = aux12_.general_radiation.stef
    toffst = aux12_.general_radiation.toffst
    hemiopt = aux12_.radiosity_solver.hemiopt
    radopt = aux12_.radiosity_solver.radopt
    spcnod = aux12_.radiosity_solver.spcnod
    spctemp = aux12_.radiosity_solver.spctemp
    v2dopt = aux12_.radiosity_solver.v2dopt
    vfopt = aux12_.radiosity_solver.vfopt
    vfquery = aux12_.radiosity_solver.vfquery

    # reduced processor
    rmndisp = reduced.preparation.rmndisp
    rmnevec = reduced.preparation.rmnevec
    rmresume = reduced.setup.rmresume
    rmsave = reduced.setup.rmsave
    dcvswp = reduced.use_pass.dcvswp
    rmlvscale = reduced.use_pass.rmlvscale
    rmuse = reduced.use_pass.rmuse
    rmalist = reduced.generation.rmalist
    rmanl = reduced.generation.rmanl
    rmaster = reduced.generation.rmaster
    rmcap = reduced.generation.rmcap
    rmclist = reduced.generation.rmclist
    rmmlist = reduced.generation.rmmlist
    rmmrange = reduced.generation.rmmrange
    rmmselect = reduced.generation.rmmselect
    rmporder = reduced.generation.rmporder
    rmrgenerate = reduced.generation.rmrgenerate
    rmroptions = reduced.generation.rmroptions
    rmrplot = reduced.generation.rmrplot
    rmrstatus = reduced.generation.rmrstatus
    rmsmple = reduced.generation.rmsmple
    rmxport = reduced.generation.rmxport

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

    # APDL commands
    cfclos = apdl.macro_files.cfclos
    cfopen = apdl.macro_files.cfopen
    cfwrite = apdl.macro_files.cfwrite
    create = apdl.macro_files.create
    dflab = apdl.macro_files.dflab
    end = apdl.macro_files.end
    mkdir = apdl.macro_files.mkdir
    msg = apdl.macro_files.msg
    pmacro = apdl.macro_files.pmacro
    psearch = apdl.macro_files.psearch
    rmdir = apdl.macro_files.rmdir
    tee = apdl.macro_files.tee
    ulib = apdl.macro_files.ulib
    use = apdl.macro_files.use
    mfouri = apdl.array_parm.mfouri
    mfun = apdl.array_parm.mfun
    moper = apdl.array_parm.moper
    mwrite = apdl.array_parm.mwrite
    sread = apdl.array_parm.sread
    toper = apdl.array_parm.toper
    vabs = apdl.array_parm.vabs
    vcol = apdl.array_parm.vcol
    vcum = apdl.array_parm.vcum
    vfact = apdl.array_parm.vfact
    vfun = apdl.array_parm.vfun
    vitrp = apdl.array_parm.vitrp
    vlen = apdl.array_parm.vlen
    vmask = apdl.array_parm.vmask
    voper = apdl.array_parm.voper
    vput = apdl.array_parm.vput
    vscfun = apdl.array_parm.vscfun
    vstat = apdl.array_parm.vstat
    vwrite = apdl.array_parm.vwrite
    afun = apdl.parameter_definition.afun
    dim = apdl.parameter_definition.dim
    get = apdl.parameter_definition.get
    inquire = apdl.parameter_definition.inquire
    parres = apdl.parameter_definition.parres
    parsav = apdl.parameter_definition.parsav
    set = apdl.parameter_definition.set
    taxis = apdl.parameter_definition.taxis
    tread = apdl.parameter_definition.tread
    vfill = apdl.parameter_definition.vfill
    vget = apdl.parameter_definition.vget
    vread = apdl.parameter_definition.vread
    abbr = apdl.abbreviations.abbr
    abbres = apdl.abbreviations.abbres
    abbsav = apdl.abbreviations.abbsav
    ucmd = apdl.abbreviations.ucmd
    axpy = apdl.matrix_op.axpy
    comp = apdl.matrix_op.comp
    dmat = apdl.matrix_op.dmat
    dot = apdl.matrix_op.dot
    eigen = apdl.matrix_op.eigen
    export = apdl.matrix_op.export
    fft = apdl.matrix_op.fft
    free = apdl.matrix_op.free
    init = apdl.matrix_op.init
    itengine = apdl.matrix_op.itengine
    lsbac = apdl.matrix_op.lsbac
    lsengine = apdl.matrix_op.lsengine
    lsfactor = apdl.matrix_op.lsfactor
    merge = apdl.matrix_op.merge
    mult = apdl.matrix_op.mult
    nrm = apdl.matrix_op.nrm
    remove = apdl.matrix_op.remove
    scal = apdl.matrix_op.scal
    smat = apdl.matrix_op.smat
    starprint = apdl.matrix_op.starprint
    sort = apdl.matrix_op.sort
    vec = apdl.matrix_op.vec

    # hidden
    _batch = hidden.batch
