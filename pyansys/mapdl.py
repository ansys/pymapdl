"""Module to control interaction with MAPDL through Python"""
import glob
import re
import os
import logging
from functools import wraps
import tempfile
from shutil import rmtree, copyfile

import appdirs
import pyvista as pv
import numpy as np

import pyansys
from pyansys.mapdl_functions import _MapdlCommands
from pyansys.misc import random_string, supress_logging
from pyansys.geometry_commands import geometry_commands
from pyansys.element_commands import element_commands
from pyansys.errors import MapdlRuntimeError


MATPLOTLIB_LOADED = True
try:
    import matplotlib
    matplotlib.use('tkagg')  # for windows
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg
except:
    MATPLOTLIB_LOADED = False

# test for png file
PNG_TEST = re.compile('WRITTEN TO FILE(.*).png')

INVAL_COMMANDS = {'*vwr':  'Use "with ansys.non_interactive:\n\t*ansys.Run("VWRITE(..."',
                  '*cfo': '',
                  '*CRE': 'Create a function within python or run as non_interactive',
                  '*END': 'Create a function within python or run as non_interactive',
                  '*IF': 'Use a python if or run as non_interactive'}

PLOT_COMMANDS = ['NPLO', 'EPLO', 'KPLO', 'LPLO', 'APLO', 'VPLO', 'PLNS', 'PLES']
MAX_COMMAND_LENGTH = 600  # actual is 640, but seems to fail above 620


def parse_to_short_cmd(command):
    """Takes any MAPDL command and returns the first 4 characters of
    the command

    Examples
    --------
    >>> parse_to_short_cmd('K,,1,0,0,')
    'K'

    >>> parse_to_short_cmd('VPLOT, ALL')
    'VPLO'
    """
    try:
        short_cmd = command.split(',')[0]
        return short_cmd[:4].upper()
    except:
        return


def setup_logger(loglevel='INFO'):
    """Setup logger"""

    # return existing log if this function has already been called
    if hasattr(setup_logger, 'log'):
        setup_logger.log.setLevel(loglevel)
        ch = setup_logger.log.handlers[0]
        ch.setLevel(loglevel)
        return setup_logger.log

    # create logger
    log = logging.getLogger(__name__)
    log.setLevel(loglevel)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(loglevel)

    # create formatter
    formatstr = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    formatter = logging.Formatter(formatstr)

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    log.addHandler(ch)

    # make persistent
    setup_logger.log = log

    return log


class _MapdlCore(_MapdlCommands):
    """Contains methods in common between all Mapdl subclasses"""

    def __init__(self, loglevel='DEBUG', use_vtk=True, log_apdl=False):
        """ Initialize connection with ANSYS program """
        self._show_matplotlib_figures = True  # for testing
        self._exited = False
        self._allow_ignore = False
        self._apdl_log = None
        self._store_commands = False
        self._stored_commands = []
        self._response = None
        self._use_vtk = use_vtk
        self._log_filehandler = None
        self._version = None  # cached version
        self._local = None
        self._path = None
        self._jobname = None
        self._cleanup = True

        self._log = setup_logger(loglevel.upper())
        self._log.debug('Logging set to %s', loglevel)
        self.non_interactive = self._non_interactive(self)

        from pyansys.parameters import Parameters
        self._parameters = Parameters(self)

        if log_apdl:
            filename = os.path.join(self.path, 'log.inp')
            self.open_apdl_log(filename, mode=log_apdl)

    @property
    def chain_commands(self):
        """Chain several mapdl commands."""
        return self._chain_commands(self)

    def _chain_stored(self):
        """Send a series of commands to MAPDL"""
        # appears to be an (arbitrary?) limit to 640 characters per command

        # Create chained commamnds less than 640 characters each
        c = 0
        chained_commands = []
        chunk = []
        for command in self._stored_commands:
            len_command = len(command) + 1  # include sep var
            if len_command + c > MAX_COMMAND_LENGTH:
                chained_commands.append('$'.join(chunk))
                chunk = [command]
                c = 0
            else:
                chunk.append(command)
                c += len_command

        # join the last
        chained_commands.append('$'.join(chunk))
        self._stored_commands = []

        responses = [self._run(command) for command in chained_commands]
        self._response = '\n'.join(responses)

    @property
    def parameters(self):
        """Collection of MAPDL parameters obtainable from the *GET command

        Examples
        --------
        >>> mapdl.parameters.routine
        'PREP7'

        >>> mapdl.parameters.units
        'SI'

        >>> mapdl.parameters.csys
        0
        """
        return self._parameters

    class _non_interactive:
        """Allows user to enter commands that need to run
        non-interactively.

        Examples
        --------
        To use an non-interactive command like *VWRITE, use:

        >>> with ansys.non_interactive:
                ansys.run("*VWRITE,LABEL(1),VALUE(1,1),VALUE(1,2),VALUE(1,3)")
                ansys.run("(1X,A8,'   ',F10.1,'  ',F10.1,'   ',1F5.3)")

        """
        def __init__(self, parent):
            self._parent = parent

        def __enter__(self):
            self._parent._log.debug('entering non-interactive mode')
            self._parent._store_commands = True

        def __exit__(self, *args):
            self._parent._log.debug('entering non-interactive mode')
            self._parent._flush_stored()

    class _chain_commands:
        """Store MAPDL commands and send one chained command."""

        def __init__(self, parent):
            self._parent = parent

        def __enter__(self):
            self._parent._log.debug('entering chained command mode')
            self._parent._store_commands = True

        def __exit__(self, *args):
            self._parent._log.debug('entering chained command mode')
            self._parent._chain_stored()
            self._parent._store_commands = False

    @property
    def last_response(self):
        """Returns the last response from MAPDL.

        Examples
        --------
        >>> mapdl.last_response()
        'KEYPOINT      1   X,Y,Z=   1.00000       1.00000       1.00000'
        """
        return self._response

    @wraps(_MapdlCommands.clear)
    def clear(self, *args, **kwargs):
        kwargs['read'] = 'NOSTART'
        super().clear(**kwargs)

    def __str__(self):
        try:
            if self._exited:
                return 'MAPDL exited'
            stats = self.slashstatus('PROD')
        except:
            return 'MAPDL exited'

        st = stats.find('*** Products ***')
        en = stats.find('*** PrePro')
        product = '\n'.join(stats[st:en].splitlines()[1:]).strip()

        # get product version
        stats = self.slashstatus('TITLE')
        st = stats.find('RELEASE')
        en = stats.find('INITIAL', st)
        mapdl_version = stats[st:en].split('CUSTOMER')[0].strip()

        info = 'Product:          %s\n' % product
        info += 'MAPDL Version:   %s\n' % mapdl_version
        info += 'PyANSYS Version: %s\n' % pyansys.__version__

        return info

    @property
    def geometry(self):
        """Geometry (CAD) information."""
        return self._geometry

    @property
    def _geometry(self):
        """Implemented by child class"""
        from pyansys.mapdl_geometry import Geometry
        return Geometry(self)

    @property
    def mesh(self):
        """Mesh information.

        Examples
        --------
        Return an array of the active nodes

        >>> mapdl.mesh.nodes
        array([[ 1.,  0.,  0.],
               [ 2.,  0.,  0.],
               [ 3.,  0.,  0.],
               [ 4.,  0.,  0.],
               [ 5.,  0.,  0.],
               [ 6.,  0.,  0.],
               [ 7.,  0.,  0.],
               [ 8.,  0.,  0.],
               [ 9.,  0.,  0.],
               [10.,  0.,  0.]])

        Return an array of the node numbers of the active nodes

        >>> mapdl.mesh.nnum
        array([ 1,  2,  3,  4,  5,  6,  7,  8,  9, 10], dtype=int32)

        Simply query and print the geometry

        >>> print(mapdl.mesh)
          ANSYS Mapdl Mesh
          Number of Nodes:              321
          Number of Elements:           40
          Number of Element Types:      1
          Number of Node Components:    2
          Number of Element Components: 2

        Access the geometry as a VTK object

        >>> mapdl.mesh.grid

        """
        return self._mesh

    @property
    def _mesh(self):
        """Implemented by child class"""
        raise NotImplementedError('Implemented by child class')

    def _reset_cache(self):
        """Reset cached items and other items"""
        raise NotImplementedError('Implemented by child class')

    @property
    def allow_ignore(self):
        """Invalid commands will be ignored rather than exceptions

        A command executed in the wrong processor will raise an
        exception when ``allow_ignore=False``.  This is the default
        behavior.

        Examples
        --------
        >>> mapdl.post1()
        >>> mapdl.k(1, 0, 0, 0)
        Exception:  K is not a recognized POST1 command, abbreviation, or macro.

        Ignore these messages by setting allow_ignore=True

        >>> mapdl.allow_ignore = True
        2020-06-08 21:39:58,094 [INFO] pyansys.mapdl: K is not a
        recognized POST1 command, abbreviation, or macro.  This
        command will be ignored.

        *** WARNING *** CP = 0.372 TIME= 21:39:58
        K is not a recognized POST1 command, abbreviation, or macro.
        This command will be ignored.

        """
        return self._allow_ignore

    @allow_ignore.setter
    def allow_ignore(self, value):
        """Set allow ignore"""
        self._allow_ignore = bool(value)

    def open_apdl_log(self, filename, mode='w'):
        """Start writing all APDL commands to an ANSYS input file.

        Parameters
        ----------
        filename : str
            Filename of the log.
        """
        if self._apdl_log is not None:
            raise RuntimeError('APDL command logging already enabled')

        self._log.debug('Opening ANSYS log file at %s', filename)
        self._apdl_log = open(filename, mode=mode, buffering=1)  # line buffered
        if mode != 'w':
            self._apdl_log.write('! APDL script generated using pyansys %s\n' %
                                 pyansys.__version__)

    @supress_logging
    def _generate_iges(self):
        """Save IGES geometry representation to disk"""
        tmp_name = '_tmp.iges'
        filename = os.path.join(self.path, tmp_name)
        prior_processor = self.parameters.routine
        self.prep7()
        self.igesout(filename, att=1)
        self.run('/%s' % prior_processor)
        return filename

    def open_gui(self, include_result=True):
        """Saves existing database and opens up APDL GUI

        Parameters
        ----------
        include_result : bool, optional
            Allow the result file to be post processed in the GUI.
        """

        if not self._local:
            raise RuntimeError('``open_gui`` can only be called from a local '
                               'MAPDL instance')

        # specify a path for the temporary database
        temp_dir = tempfile.gettempdir()
        save_path = os.path.join(temp_dir, 'ansys_tmp')
        if os.path.isdir(save_path):
            rmtree(save_path)
        os.mkdir(save_path)

        name = 'tmp'
        tmp_database = os.path.join(save_path, '%s.db' % name)
        if os.path.isfile(tmp_database):
            os.remove(tmp_database)

        # get the state, close, and finish
        prior_processor = self.processor
        self.finish()
        self.save(tmp_database)
        self.exit(close_log=False)

        # copy result file to temp directory
        if include_result:
            resultfile = os.path.join(self.path, '%s.rst' % self.jobname)
            if os.path.isfile(resultfile):
                tmp_resultfile = os.path.join(save_path, '%s.rst' % name)
                copyfile(resultfile, tmp_resultfile)

        # write temporary input file
        start_file = os.path.join(save_path, 'start%s.ans' % self.version)
        with open(start_file, 'w') as f:
            f.write('RESUME\n')

        # some versions of ANSYS just look for "start.ans" when starting
        other_start_file = os.path.join(save_path, 'start.ans')
        with open(other_start_file, 'w') as f:
            f.write('RESUME\n')

        # issue system command to run ansys in GUI mode
        cwd = os.getcwd()
        os.chdir(save_path)
        os.system('cd "%s" && "%s" -g -j %s' % (save_path, self._exec_file, name))
        os.chdir(cwd)

        # must remove the start file when finished
        os.remove(start_file)
        os.remove(other_start_file)

        # reload database when finished
        self._launch()
        self.resume(tmp_database)
        if prior_processor is not None:
            if 'BEGIN' not in prior_processor:
                self.run('/%s' % prior_processor)

    def _close_apdl_log(self):
        """ Closes APDL log """
        if self._apdl_log is not None:
            self._apdl_log.close()
        self._apdl_log = None

    def nplot(self, knum="", vtk=None, **kwargs):
        """APDL Command: NPLOT

        Displays nodes.

        Parameters
        ----------
        knum : bool, int, optional
            Node number key:

            - 0 : No node numbers on display (default).
            - 1 : Include node numbers on display.  See also /PNUM command.

        vtk : bool, optional
           Display nodes using VTK.

        Examples
        --------
        Plot using VTK while showing labels and changing the background

        >>> mapdl.prep7()
        >>> mapdl.n(1, 0, 0, 0)
        >>> mapdl.n(11, 10, 0, 0)
        >>> mapdl.fill(1, 11, 9)
        >>> mapdl.nplot(knum=True, background='w', color='k',
                        show_bounds=True)

        Plot without using VTK

        >>> mapdl.prep7()
        >>> mapdl.n(1, 0, 0, 0)
        >>> mapdl.n(11, 10, 0, 0)
        >>> mapdl.fill(1, 11, 9)
        >>> mapdl.nplot(vtk=False)

        Notes
        -----
        Only selected nodes [NSEL] are displayed.  Elements need not
        be defined.  See the DSYS command for display coordinate
        system.

        This command is valid in any processor.
        """
        if vtk is None:
            vtk = self._use_vtk
        elif not vtk:
            self._enable_interactive_plotting()

        if vtk:
            if not self.mesh.nodes.size:
                raise RuntimeError('There are no nodes to plot.')

            kwargs.setdefault('color', 'w')
            cpos = kwargs.pop('cpos', None)
            show_bounds = kwargs.pop('show_bounds', False)
            show_axes = kwargs.pop('show_axes', False)
            background = kwargs.pop('background', None)
            pl = pv.Plotter(off_screen=kwargs.pop('off_screen', None))

            if background:
                pl.set_background(background)

            pl.add_points(self.mesh.nodes, **kwargs)
            pl.show_axes()

            if isinstance(knum, str):
                knum = knum == '1'

            if knum:
                pl.add_point_labels(self.mesh.nodes, self.mesh.nnum)
            if cpos:
                pl.camera_position = cpos
            if show_bounds:
                pl.show_bounds()
            if show_axes:
                pl.show_axes()

            return pl.show()

        # otherwise, use the built-in nplot
        return super().nplot(knum, **kwargs)

    def vplot(self, nv1="", nv2="", ninc="", degen="", scale="",
              vtk=False, quality=7, show_numbering=False,
              random_colors=False, show_edges=True, edge_width=1,
              **kwargs):
        """APDL Command: VPLOT

        Displays the selected volumes.

        Parameters
        ----------
        nv1, nv2, ninc
            Display volumes from NV1 to NV2 (defaults to NV1) in steps
            of NINC (defaults to 1).  If NV1 = ALL (default), NV2 and
            NINC are ignored and all selected volumes [VSEL] are
            displayed.

        degen
            Degeneracy marker:

            (blank) - No degeneracy marker is used (default).

            DEGE - A red star is placed on keypoints at degeneracies (see the Modeling and Meshing
                   Guide).  Not available if /FACET,WIRE is set.

        scale
            Scale factor for the size of the degeneracy-marker star.  The scale
            is the size in window space (-1 to 1 in both directions) (defaults
            to .075).

        vtk : bool, optional
            Plot the currently selected volumes using ``pyvista``.  As
            this creates a temporary surface mesh, this may have a
            long execution time for large meshes.

        quality : int, optional
            quality of the mesh to display.  Varies between 1 (worst)
            to 10 (best).

        show_numbering : bool, optional
            Display line and keypoint numbers when ``vtk=True``.

        Notes
        -----
        Displays selected volumes.  (Only volumes having areas within the
        selected area set [ASEL] will be plotted.)  With PowerGraphics on
        [/GRAPHICS,POWER], VPLOT will display only the currently selected
        areas. This command is also a utility command, valid anywhere.  The
        degree of tessellation used to plot the volumes is set through the
        /FACET command.
        """
        if vtk:
            cm_name = '__tmp_area2__'
            self.cm(cm_name, 'AREA')
            self.aslv('S')  # select areas attached to active volumes
            self.aplot(vtk=True, random_colors=False, show_edges=True,
                       edge_width=edge_width, **kwargs)
            self.cmsel('S', cm_name, 'AREA')
        else:
            return super().vplot(nv1=nv1, nv2=nv2, ninc=ninc)

    def aplot(self, na1="", na2="", ninc="", degen="", scale="",
              vtk=False, quality=7, show_numbering=False, show_line_numbering=False,
              random_colors=False, show_edges=True, edge_width=1, **kwargs):
        """APDL Command: APLOT

        Displays the selected areas.

        Parameters
        ----------
        na1, na2, ninc
            Displays areas from NA1 to NA2 (defaults to NA1) in steps of NINC
            (defaults to 1).  If NA1 = ALL (default), NA2 and NINC are ignored
            and all selected areas [ASEL] are displayed.

        degen
            Degeneracy marker.

            (blank) - No degeneracy marker is used (default).

            DEGE - A red star is placed on keypoints at degeneracies
            (see the Modeling and Meshing Guide ).  Not available if
            /FACET,WIRE is set.

            This option is ignored when ``vtk=True``.

        scale
            Scale factor for the size of the degeneracy-marker star.
            The scale is the size in window space (-1 to 1 in both
            directions) (defaults to .075).

            This option is ignored when ``vtk=True``.

        vtk : bool, optional
            Plot the currently selected areas using ``pyvista``.  As
            this creates a temporary surface mesh, this may have a
            long execution time for large meshes.

        quality : int, optional
            quality of the mesh to display.  Varies between 1 (worst)
            to 10 (best).

        show_numbering : bool, optional
            Display line and keypoint numbers when ``vtk=True``.

        Notes
        -----
        This command is valid in any processor.  The degree of tessellation
        used to plot the selected areas is set through the /FACET command.
        """
        if vtk:
            if quality > 10:
                quality = 10
            if quality < 1:
                quality = 1
            surf = self.generate_surface(11 - quality, na1, na2, ninc)

            pl = pv.Plotter(off_screen=kwargs.pop('off_screen', None))
            pl.set_background(kwargs.pop('background', None))

            if kwargs.pop('show_axes', False):
                pl.add_axes()

            cpos = kwargs.pop('cpos', None)
            kwargs.setdefault('color', 'w')
            font_size = kwargs.pop('font_size', None)

            areas = []
            anums = np.unique(surf['area_num'])
            for anum in anums:
                areas.append(surf.extract_cells(surf['area_num'] == anum))

            centers = []
            for area in areas:
                if random_colors:
                    kwargs['color'] = np.random.random(3)
                pl.add_mesh(area, **kwargs)
                centers.append(area.center)

                if show_edges:
                    pl.add_mesh(area.extract_feature_edges(),
                                color=kwargs.get('edge_color', 'k'),
                                line_width=edge_width)

            if show_numbering:
                pl.add_point_labels(centers, anums, font_size=font_size)

            # allow only unique line numbers
            if show_line_numbering:
                self.cm('__tmp_line__', 'LINE')
                self.lsla('S')
                lnum = self._lnum
                lines = self.lines
                self.cmsel('S', '__tmp_line__', 'LINE')

                font_size = kwargs.pop('font_size', None)
                pl.add_point_labels(lines.points[50::101], lnum,
                                    font_size=font_size)

            pl.camera_position = cpos
            return pl.show()
        else:
            return super().aplot(na1=na1, na2=na2, ninc=ninc)

    @supress_logging
    def _enable_interactive_plotting(self, pixel_res=1600):
        """Enables interactive plotting.  Requires matplotlib

        Parameters
        ----------
        pixel_res : int
            Pixel resolution.  Valid values are from 256 to 2400.
            Lowering the pixel resolution produces a "fuzzier" image.
            Increasing the resolution produces a "sharper" image but
            takes longer to render.
        """
        if MATPLOTLIB_LOADED:
            if not self._png_mode:
                self.show('PNG')
                self.gfile(pixel_res)
        else:
            raise ImportError('Install matplotlib to use enable interactive plotting,'
                              ' or turn interactive plotting off with:\n'
                              '``interactive_plotting=False``')

    @property
    def _png_mode(self):
        """Returns True when MAPDL is writing plots as png to file."""
        return 'PNG' in self.show()

    def set_log_level(self, loglevel):
        """Sets log level

        Parameters
        ----------
        loglevel : str, int
            Log level.  Must be one of: ``'DEBUG', 'INFO', 'WARNING', 'ERROR'``.

        Examples
        --------
        Set the log level to debug

        >>> mapdl.set_log_level('DEBUG')

        Set the log level to info

        >>> mapdl.set_log_level('INFO')

        Set the log level to warning

        >>> mapdl.set_log_level('WARNING')

        Set the log level to error

        >>> mapdl.set_log_level('ERROR')
        """
        if isinstance(loglevel, str):
            loglevel = loglevel.upper()
        setup_logger(loglevel=loglevel)

    def _list(self, command):
        """ Replaces *LIST command """
        items = command.split(',')
        filename = os.path.join(self.path, '.'.join(items[1:]))
        if os.path.isfile(filename):
            self._response = open(filename).read()
            self._log.info(self._response)
        else:
            raise Exception('Cannot run:\n%s\n' % command + 'File does not exist')

    def eplot(self, vtk=False, **kwargs):
        """APDL Command: EPLOT

        Produces an element display.

        Parameters
        ----------
        vtk : bool, optional
            Plot the currently selected elements using ``pyvista``.

        **kwargs
            See ``help(pyvista.plot)`` for more keyword arguments
            related to visualizing using ``vtk``.

        Notes
        -----
        Produces an element display of the selected elements. In full
        graphics, only those elements faces with all of their
        corresponding nodes selected are plotted. In PowerGraphics,
        all element faces of the selected element set are plotted
        irrespective of the nodes selected.  However, for both full
        graphics and PowerGraphics, adjacent or otherwise duplicated
        faces of 3-D solid elements will not be displayed in an
        attempt to eliminate plotting of interior facets. See the DSYS
        command for display coordinate system issues.

        This command will display curvature in midside node elements
        when PowerGraphics is activated [/GRAPHICS,POWER] and
        /EFACET,2 or /EFACET,4 are enabled.  (To display curvature,
        two facets per edge is recommended [/EFACET,2]).  When you
        specify /EFACET,1, PowerGraphics does not display midside
        nodes. /EFACET has no effect on EPLOT for non-midside node
        elements.

        This command is valid in any processor.
        """
        if vtk:
            # default kwargs
            kwargs.setdefault('color', 'w')
            kwargs.setdefault('show_axes', True)
            kwargs.setdefault('show_edges', True)
            if self._vtk_grid:
                self._vtk_grid.plot(**kwargs)
            else:
                raise RuntimeError('No elements selected to plot')
        else:
            return super().eplot(**kwargs)

    def lplot(self, nl1="", nl2="", ninc="", vtk=False,
              show_keypoints=False, show_numbering=True,
              show_keypoint_numbering=False, random_color=False,
              **kwargs):
        """APDL Command: LPLOT

        Displays the selected lines.

        Parameters
        ----------
        nl1, nl2, ninc
            Display lines from NL1 to NL2 (defaults to NL1) in steps
            of NINC (defaults to 1).  If NL1 = ALL (default), NL2 and
            NINC are ignored and display all selected lines [LSEL].

        vtk : bool, optional
            Plot the currently selected lines using ``pyvista``.

        show_numbering : bool, optional
            Display line and keypoint numbers when ``vtk=True``.

        show_keypoints : bool, optional
            Display keypoints associated with current lines.  Only
            valid with ``vtk=True``.

        show_keypoint_numbering : bool, optional
            Number keypoints.  Only valid when show_keypoints is True

        **kwargs
            See ``help(pyvista.plot)`` for more keyword arguments
            related to visualizing using ``vtk``.

        Examples
        --------
        >>> mapdl.lplot(vtk=True, cpos='xy', line_width=10)

        Notes
        -----
        Mesh divisions on plotted lines are controlled by the LDIV option of
        the /PSYMB command.

        This command is valid in any processor.
        """
        if vtk:
            if not self.geometry.n_line:
                raise MapdlRuntimeError('Either no lines have been selected or there '
                                        'is nothing to plot')

            pl = pv.Plotter(off_screen=kwargs.pop('off_screen', None))
            pl.set_background(kwargs.pop('background', None))

            if kwargs.pop('show_axes', False):
                pl.add_axes()

            cpos = kwargs.pop('cpos', None)
            kwargs.setdefault('color', 'w')

            # allow only unique line numbers
            lines = self.geometry.lines
            lnum = lines.cell_arrays['entity_num'].astype(np.int32)

            # TODO: partially select lines
            font_size = kwargs.pop('font_size', None)
            if show_numbering:
                pl.add_point_labels(lines.points[50::101], lnum, font_size=font_size)

            if show_keypoints:
                pl.add_points(self.geometry.keypoints)
                if show_numbering:
                    pl.add_point_labels(self.geometry.keypoints, self.geometry.knum,
                                        font_size=font_size)

            if random_color:
                kwargs['scalars'] = np.random.random(lines.n_cells)

            pl.add_mesh(lines, **kwargs)

            pl.camera_position = cpos
            return pl.show()
        else:
            return super().lplot(nl1=nl1, nl2=nl2, ninc=ninc)

    def kplot(self, np1="", np2="", ninc="", lab="", vtk=False,
              show_numbering=True, **kwargs):
        """Displays the selected keypoints.

        APDL Command: KPLOT

        Parameters
        ----------
        np1, np2, ninc
            Display keypoints from NP1 to NP2 (defaults to NP1) in
            steps of NINC (defaults to 1).  If NP1 = ALL (default),
            NP2 and NINC are ignored and all selected keypoints [KSEL]
            are displayed.

        lab
            Determines what keypoints are plotted (one of the following):

            (blank) - Plots all keypoints.

            HPT - Plots only those keypoints that are hard points.

        vtk : bool, optional
            Plot the currently selected lines using ``pyvista``.

        show_numbering : bool, optional
            Display line and keypoint numbers when ``vtk=True``.

        Notes
        -----
        This command is valid in any processor.
        """
        if vtk:
            if not self.geometry.n_keypoint:
                raise MapdlRuntimeError('Either no keypoints have been'
                                        'selected or there is '
                                        'nothing to plot')
            pl = pv.Plotter(off_screen=kwargs.pop('off_screen', None))

            if kwargs.pop('show_axes', False):
                pl.add_axes()

            cpos = kwargs.pop('cpos', None)

            kwargs.setdefault('color', 'w')
            keypoints = self.geometry.keypoints
            pl.add_points(keypoints, **kwargs)

            if show_numbering:
                pl.add_point_labels(keypoints, self.geometry.knum)

            pl.camera_position = cpos
            return pl.show()
        else:
            return super().kplot(np1=np1, np2=np2, ninc=ninc, lab=lab)

    @property
    def result(self):
        """Binary interface to the result file using ``pyansys.ResultFile``

        Examples
        --------
        >>> mapdl.solve()
        >>> mapdl.finish()
        >>> result = mapdl.result
        >>> print(result)

        """
        if not self._local:
            raise RuntimeError('Binary interface only available when result is local.')

        try:
            result_path = self.inquire('RSTFILE')
        except RuntimeError:
            result_path = ''

        if not result_path:
            result_path = os.path.join(self.path, '%s.rst' % self._jobname)
        elif not os.path.dirname(result_path):
            result_path = os.path.join(self.path, '%s.rst' % result_path)

        # there may be multiple result files at this location (if not
        # combining results)
        if not os.path.isfile(result_path):
            raise FileNotFoundError('No results found at %s' % result_path)
        return pyansys.read_binary(result_path)

    def _get(self, *args, **kwargs):
        raise NotImplementedError('Implemented by child class')

    def add_file_handler(self, filepath, append=False, level='DEBUG'):
        """Add a file handler to the mapdl log.  This allows you to
        redirect the APDL logging to a file.

        Parameters
        ----------
        filepath : str
            Filename of the log.

        append : bool
            When ``True``, appends to an existing log file.  When
            ``False``, overwrites the log file if it already exists.

        level : str
            Log level.  Must be one of: ``'DEBUG', 'INFO', 'WARNING', 'ERROR'``.

        Examples
        --------
        Start writing the log to a new file named "mapdl.log"

        >>> mapdl.add_file_handler('mapdl.log')

        """
        if append:
            mode = 'a'
        else:
            mode = 'w'

        self._log_filehandler = logging.FileHandler(filepath)
        formatstr = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'

        self._log_filehandler = logging.FileHandler(filepath, mode=mode)
        self._log_filehandler.setFormatter(logging.Formatter(formatstr))
        if isinstance(level, str):
            level = level.uppder()
        self._log_filehandler.setLevel(level)
        self._log.addHandler(self._log_filehandler)
        self._log.info('Added file handler at %s', filepath)

    def remove_file_handler(self):
        """Removes the filehander from the log"""
        self._log.removeHandler(self._log_filehandler)
        self._log.info('Removed file handler')

    def _flush_stored(self):
        """Writes stored commands to an input file and runs the input
        file.  Used with non_interactive.
        """
        self._log.debug('Flushing stored commands')
        tmp_out = os.path.join(appdirs.user_data_dir('pyansys'),
                               'tmp_%s.out' % random_string())
        self._stored_commands.insert(0, "/OUTPUT, '%s'" % tmp_out)
        self._stored_commands.append('/OUTPUT')
        commands = '\n'.join(self._stored_commands)
        self._apdl_log.write(commands + '\n')

        # write to a temporary input file
        filename = os.path.join(appdirs.user_data_dir('pyansys'),
                                'tmp_%s.inp' % random_string())
        self._log.debug('Writing the following commands to a temporary '
                        'apdl input file:\n%s', commands)

        with open(filename, 'w') as f:
            f.writelines(commands)

        self._store_commands = False
        self._stored_commands = []
        self.run("/INPUT, '%s'" % filename, write_to_log=False)
        if os.path.isfile(tmp_out):
            self._response = '\n' + open(tmp_out).read()

        if self._response is None:
            self._log.warning('Unable to read response from flushed commands')
        else:
            self._log.info(self._response)

    def get_float(self, *args, **kwargs):
        raise NotImplementedError('Please use ``get_value`` instead')

    def get_value(self, entity="", entnum="", item1="", it1num="",
                  item2="", it2num="", **kwargs):
        """Runs the *GET command and returns a Python value.

        See `help(get)` for more details.

        Parameters
        ----------
        entity
            Entity keyword. Valid keywords are NODE, ELEM, KP, LINE, AREA,
            VOLU, PDS, etc., as shown for Entity = in the tables below.

        entnum
            The number or label for the entity (as shown for ENTNUM = in the
            tables below). In some cases, a zero (or blank) ENTNUM represents
            all entities of the set.

        item1
            The name of a particular item for the given entity. Valid items are
            as shown in the Item1 columns of the tables below.

        it1num
            The number (or label) for the specified Item1 (if any). Valid
            IT1NUM values are as shown in the IT1NUM columns of the tables
            below. Some Item1 labels do not require an IT1NUM value.

        item2, it2num
            A second set of item labels and numbers to further qualify the item
            for which data are to be retrieved. Most items do not require this
            level of information.

        Returns
        -------
        par : float
            Floating point value of the parameter.

        Examples
        --------
        Retreive the number of nodes.

        >>> value = ansys.get('node', '', 'count')
        >>> value
        3003

        Retreive the number of nodes using keywords.

        >>> value = ansys.get(entity='node', item1='count')
        >>> value
        3003
        """
        return self._get(entity=entity, entnum=entnum, item1=item1, it1num=it1num,
                         item2=item2, it2num=it2num, **kwargs)

    def get(self, par="__floatparameter__", entity="", entnum="",
            item1="", it1num="", item2="", it2num="", **kwargs):
        """APDL Command: *GET

        Retrieves a value and stores it as a scalar parameter or part
        of an array parameter.

        Parameters
        ----------
        par
            The name of the resulting parameter. See *SET for name
            restrictions.

        entity
            Entity keyword. Valid keywords are NODE, ELEM, KP, LINE, AREA,
            VOLU, PDS, etc., as shown for Entity = in the tables below.

        entnum
            The number or label for the entity (as shown for ENTNUM = in the
            tables below). In some cases, a zero (or blank) ENTNUM represents
            all entities of the set.

        item1
            The name of a particular item for the given entity. Valid items are
            as shown in the Item1 columns of the tables below.

        it1num
            The number (or label) for the specified Item1 (if any). Valid
            IT1NUM values are as shown in the IT1NUM columns of the tables
            below. Some Item1 labels do not require an IT1NUM value.

        item2, it2num
            A second set of item labels and numbers to further qualify the item
            for which data are to be retrieved. Most items do not require this
            level of information.

        Returns
        -------
        par : float
            Floating point value of the parameter.

        Examples
        --------
        Retreive the number of nodes

        >>> value = ansys.get('val', 'node', '', 'count')
        >>> value
        3003

        Retreive the number of nodes using keywords.  Note that the
        parameter name is optional.

        >>> value = ansys.get(entity='node', item1='count')
        >>> value
        3003

        Notes
        -----
        *GET retrieves a value for a specified item and stores the value as a
        scalar parameter, or as a value in a user-named array parameter. An
        item is identified by various keyword, label, and number combinations.
        Usage is similar to the *SET command except that the parameter values
        are retrieved from previously input or calculated results. For example,
        *GET,A,ELEM,5,CENT,X returns the centroid x-location of element 5 and
        stores the result as parameter A. *GET command operations, along with
        the associated Get functions return values in the active coordinate
        system unless stated otherwise. A Get function is an alternative in-
        line function that can be used to retrieve a value instead of the *GET
        command (see Using In-line Get Functions for more information).

        Both *GET and *VGET retrieve information from the active data stored in
        memory. The database is often the source, and sometimes the information
        is retrieved from common memory blocks that the program uses to
        manipulate information. Although POST1 and POST26 operations use a
        *.rst file, *GET data is accessed from the database or from the common
        blocks. Get operations do not access the *.rst file directly. For
        repeated gets of sequential items, such as from a series of elements,
        see the *VGET command.

        Most items are stored in the database after they are calculated and are
        available anytime thereafter. Items are grouped according to where they
        are usually first defined or calculated. Preprocessing data will often
        not reflect the calculated values generated from section data. Do not
        use *GET to obtain data from elements that use calculated section data,
        such as beams or shells. Most of the general items listed below are
        available from all modules. Each of the sections for accessing *GET
        parameters are shown in the following order:

        *GET General Entity Items

        *GET Preprocessing Entity Items

        *GET Solution Entity Items

        *GET Postprocessing Entity Items

        *GET Probabilistic Design Entity Items

        The *GET command is valid in any processor.
        """
        command = "*GET,%s,%s,%s,%s,%s,%s,%s" % (str(par),
                                                 str(entity),
                                                 str(entnum),
                                                 str(item1),
                                                 str(it1num),
                                                 str(item2),
                                                 str(it2num))
        response = self.run(command, **kwargs)
        value = response.split('=')[-1].strip()
        try:  # always either a float or string
            return float(value)
        except:
            return value

    def read_float_parameter(self, parameter_name):
        """Read out the value of a ANSYS parameter to use in python.

        Parameters
        ----------
        parameter_name : str
            Name of the parameter inside ANSYS.

        Returns
        -------
        float
            Value of ANSYS parameter.

        Examples
        --------
        >>> ansys.get('myparm', 'node', '', 'count')
        >>> value = ansys.read_float_parameter('myparm')
        >>> value
        3003

        Retreive the value in an array.  This example creates a block
        of elements and stores the element numbers in an array.  Then
        it retreives the first value of that array

        >>> ansys.prep7()
        >>> ansys.block(0,1,0,1,0,1)
        >>> ansys.et(1, 186)
        >>> ansys.vmesh('all')
        >>> ansys.run('*VGET, ELEM_ARR, ELEM, , elist')
        >>> ansys.read_float_parameter('ELEM_ARR(1)')
        1.0

        You could also retrieve ELEM_ARR with

        >>> values, arrays = ansys.load_parameters()
        >>> arrays
        {'ELEM_ARR': array([1., 2., 3., 4., 5., 6., 7., 8.])}

        """
        try:
            response = self.run(parameter_name + " = " + parameter_name)
        except TypeError:
            raise TypeError('Input variable `parameter_name` should be string')
        return float(response.split('=')[-1])

    def read_float_from_inline_function(self, function_str):
        """Use a APDL inline function to get a float value from ANSYS.
        Take note, that internally an APDL parameter __floatparameter__ is
        created/overwritten.

        Parameters
        ----------
        function_str : str
            String containing an inline function as used in APDL..

        Returns
        -------
        float
            Value returned by inline function..

        Examples
        --------
        >>> inline_function = "node({},{},{})".format(x, y, z)
        >>> node = apdl.read_float_from_inline_function(inline_function)
        """
        self.run("__floatparameter__="+function_str)
        return self.read_float_parameter("__floatparameter__")

    @property
    def jobname(self):
        """MAPDL job name.

        This is requested from the active mapdl instance.
        """
        try:
            self._jobname = self.inquire('JOBNAME')
        except:
            pass
        return self._jobname

    def inquire(self, func):
        """Returns system information.

        Parameters
        ----------
        func : str
           Specifies the type of system information returned.  See the
           notes section for more information.

        Returns
        -------
        value : str
            Value of the inquired item.

        Notes
        -----
        Allowable func entries
        LOGIN - Returns the pathname of the login directory on Linux
        systems or the pathname of the default directory (including
        drive letter) on Windows systems.

        - ``DOCU`` - Pathname of the ANSYS docu directory.
        - ``APDL`` - Pathname of the ANSYS APDL directory.
        - ``PROG`` - Pathname of the ANSYS executable directory.
        - ``AUTH`` - Pathname of the directory in which the license file resides.
        - ``USER`` - Name of the user currently logged-in.
        - ``DIRECTORY`` - Pathname of the current directory.
        - ``JOBNAME`` - Current Jobname.
        - ``RSTDIR`` - Result file directory
        - ``RSTFILE`` - Result file name
        - ``RSTEXT`` - Result file extension
        - ``OUTPUT`` - Current output file name

        Examples
        --------
        Return the job name

        >>> mapdl.inquire('JOBNAME')
        file

        Return the result file name

        >>> mapdl.inquire('RSTFILE')
        'file.rst'
        """
        response = ''
        try:
            response = self.run('/INQUIRE, , %s' % func)
            return response.split('=')[1].strip()
        except IndexError:
            raise RuntimeError('Cannot parse %s' % response)

    def modal_analysis(self, method='lanb', nmode='', freqb='', freqe='', cpxmod='',
                       nrmkey='', modtype='', memory_option='', elcalc=False):
        """Run a modal with basic settings analysis

        Parameters
        ----------
        method : str
            Mode-extraction method to be used for the modal analysis.
            Defaults to lanb (block lanczos).  Must be one of the following:

            - LANB : Block Lanczos
            - LANPCG : PCG Lanczos
            - SNODE : Supernode modal solver
            - SUBSP : Subspace algorithm
            - UNSYM : Unsymmetric matrix
            - DAMP : Damped system
            - QRDAMP : Damped system using QR algorithm
            - VT : Variational Technology

        nmode : int, optional
            The number of modes to extract. The value can depend on
            the value supplied for Method. NMODE has no default and
            must be specified. If Method = LANB, LANPCG, or SNODE, the
            number of modes that can be extracted can equal the DOFs
            in the model after the application of all boundary
            conditions.

        freqb : float, optional
            The beginning, or lower end, of the frequency range of
            interest.

        freqe : float, optional
            The ending, or upper end, of the frequency range of
            interest (in Hz). The default for Method = SNODE is
            described below. The default for all other methods is to
            calculate all modes, regardless of their maximum
            frequency.

        cpxmod : str, optional
            Complex eigenmode key. Valid only when ``method='QRDAMP'``
            or ``method='unsym'``

            - AUTO : Determine automatically if the eigensolutions are
              real or complex and output them accordingly. This is
              the default for ``method='UNSYM'``.  Not supported for
              Method = QRDAMP.
            - ON or CPLX : Calculate and output complex eigenmode
              shapes.
            - OFF or REAL : Do not calculate complex eigenmode
              shapes. This is required if a mode-
              superposition analysis is intended after the
              modal analysis for Method = QRDAMP. This is the
              default for this method.

        nrmkey : bool, optional
            Mode shape normalization key.  When ``True`` (default),
            normalize the mode shapes to the mass matrix.  When False,
            Normalize the mode shapes to unity instead of to the mass
            matrix.  If a subsequent spectrum or mode-superposition
            analysis is planned, the mode shapes should be normalized
            to the mass matrix.

        modtype : str, optional
            Type of modes calculated by the eigensolver. Only
            applicable to the unsymmetric eigensolver.

            - Blank : Right eigenmodes. This value is the default.
            - BOTH : Right and left eigenmodes. The left eigenmodes are
              written to Jobname.LMODE.  This option must be
              activated if a mode-superposition analysis is intended.

        memory_option : str, optional
            Memory allocation option:

            * ``DEFAULT`` - Default Memory mode
                      Use the default memory allocation strategy for
                      the sparse solver. The default strategy attempts
                      to run in the INCORE memory mode. If there is
                      not enough available physical memory when the
                      solver starts to run in the ``INCORE`` memory
                      mode, the solver will then attempt to run in the
                      ``OUTOFCORE`` memory mode.

            * ``INCORE`` - In-core memory mode
                     Use a memory allocation strategy in the sparse
                     solver that will attempt to obtain enough memory
                     to run with the entire factorized matrix in
                     memory. This option uses the most amount of
                     memory and should avoid doing any I/O. By
                     avoiding I/O, this option achieves optimal solver
                     performance. However, a significant amount of
                     memory is required to run in this mode, and it is
                     only recommended on machines with a large amount
                     of memory. If the allocation for in-core memory
                     fails, the solver will automatically revert to
                     out-of-core memory mode.

            * ``OUTOFCORE`` - Out of core memory mode.
                        Use a memory allocation strategy in the sparse
                        solver that will attempt to allocate only
                        enough work space to factor each individual
                        frontal matrix in memory, but will store the
                        entire factorized matrix on disk. Typically,
                        this memory mode results in poor performance
                        due to the potential bottleneck caused by the
                        I/O to the various files written by the
                        solver.

        elcalc : bool, optional
            Calculate element results, reaction forces, energies, and
            the nodal degree of freedom solution.  Default ``False``.

        Examples
        --------
        Modal analysis using default parameters for the first 6 modes

        >>> mapdl.modal_analysis(nmode=6)

        Notes
        -----
        For models that involve a non-symmetric element stiffness
        matrix, as in the case of a contact element with frictional
        contact, the QRDAMP eigensolver (MODOPT, QRDAMP) extracts
        modes in the modal subspace formed by the eigenmodes from the
        symmetrized eigenproblem. The QRDAMP eigensolver symmetrizes
        the element stiffness matrix on the first pass of the
        eigensolution, and in the second pass, eigenmodes are
        extracted in the modal subspace of the first eigensolution
        pass. For such non- symmetric eigenproblems, you should verify
        the eigenvalue and eigenmode results using the non-symmetric
        matrix eigensolver (MODOPT,UNSYM).

        The DAMP and QRDAMP options cannot be followed by a subsequent
        spectrum analysis. The UNSYM method supports spectrum analysis
        when eigensolutions are real.

        """
        if nrmkey:
            if nrmkey.upper() != 'OFF':
                nrmkey = 'ON'
        nrmkey = 'OFF'

        self.slashsolu()
        self.antype(2, 'new')
        self.modopt(method, nmode, freqb, freqe, cpxmod, nrmkey, modtype)
        self.bcsoption(memory_option)

        if elcalc:
            self.mxpand(elcalc='YES')

        self.solve()
        self.finish()

    def run(self, command, write_to_log=True):
        """Runs APDL command

        Parameters
        ----------
        command : str
            ANSYS APDL command.

        write_to_log : bool, optional
            Overrides APDL log writing.  Default True.  When set to
            False, will not write command to log, even if APDL
            command logging is enabled.

        Returns
        -------
        command_output : str
            Command output from ANSYS.

        Examples
        --------
        >>> mapdl.run('/PREP7')

        Equivalent Pythonic method:

        >>> mapdl.prep7()

        Notes
        -----
        When two or more commands need to be run non-interactively
        (i.e. ``*VWRITE``) use

        >>> with ansys.non_interactive:
        >>>     ansys.run("*VWRITE,LABEL(1),VALUE(1,1),VALUE(1,2),VALUE(1,3)")
        >>>     ansys.run("(1X,A8,'   ',F10.1,'  ',F10.1,'   ',1F5.3)")
        """
        if self._store_commands:
            self._stored_commands.append(command)
            return
        elif command[:3].upper() in INVAL_COMMANDS:
            exception = RuntimeError('Invalid pyansys command "%s"\n\n%s' %
                                     (command, INVAL_COMMANDS[command[:3]]))
            raise exception
        elif command[:4].upper() in INVAL_COMMANDS:
            exception = RuntimeError('Invalid pyansys command "%s"\n\n%s' %
                                     (command, INVAL_COMMANDS[command[:4]]))
            raise exception
        elif write_to_log and self._apdl_log is not None:
            if not self._apdl_log.closed:
                self._apdl_log.write('%s\n' % command)

        if command[:4] in self._redirected_commands:
            function = self._redirected_commands[command[:4]]
            return function(command)

        text = self._run(command)
        if text:
            self._response = text.strip()
        else:
            self._response = ''

        if self._response:
            self._log.info(self._response)

        if 'is not a recognized' in text:
            if not self.allow_ignore:
                text = text.replace('This command will be ignored.', '')
                text += '\n\nIgnore these messages by setting allow_ignore=True'
                raise Exception(text)

        if '*** ERROR ***' in self._response:  # flag error
            self._log.error(self._response)
            # if not continue_on_error:
            raise Exception(self._response)

        # special returns for certain geometry commands
        short_cmd = parse_to_short_cmd(command)

        # command parsing
        if short_cmd in geometry_commands:
            return geometry_commands[short_cmd](self._response)
        if short_cmd in element_commands:
            return element_commands[short_cmd](self._response)
        if short_cmd in PLOT_COMMANDS:
            return self._display_plot(self._response)

        self._response = self._response.replace('\\r\\n', '\n').replace('\\n', '\n')
        return self._response

    def _display_plot(self, *args, **kwargs):
        raise NotImplementedError('Implemented by child class')

    def _run(self, *args, **kwargs):
        raise NotImplementedError('Implemented by child class')

    @property
    @supress_logging
    def version(self):
        """Return MAPDL build version

        Examples
        --------
        >>> mapdl.version
        20.2
        """
        try:
            status = self.slashstatus()
            return float(re.findall(r'Build=\s*(\d*.\d*)', status)[0])
        except:
            return self._version

    @property
    @supress_logging
    def path(self):
        """Current MAPDL directory"""
        try:
            return self.inquire('DIRECTORY')
        except:
            return self._path

    @property
    def _lockfile(self):
        """lockfile path"""
        path = self.path
        if path is not None:
            return os.path.join(path, self.jobname + '.lock').replace('\\', '/')

    def _remove_lockfile(self):
        """Removes lockfile"""
        if os.path.isfile(self._lockfile):
            try:
                os.remove(self._lockfile)
            except:
                pass

    @property
    def _result_file(self):
        """Full path to the result file"""
        return os.path.join(self.path, self.jobname).replace('\\', '/')

    def exit(self):
        """Exit from MAPDL"""
        raise NotImplementedError('Implemented by child class')

    def __del__(self):
        """Clean up when complete"""
        if self._cleanup:
            try:
                self.exit()
            except Exception as e:
                self._log.error('exit: %s', str(e))

    @supress_logging
    def get_array(self, entity='', entnum='', item1='', it1num='', item2='',
                  it2num='', kloop='', **kwargs):
        """Uses the VGET command to get an array from ANSYS

        Parameters
        ----------
        entity
            Entity keyword.  Valid keywords are NODE, ELEM, KP, LINE,
            AREA, VOLU, etc

        entnum
            The number of the entity (as shown for ENTNUM = in the tables
            below).

        item1
            The name of a particular item for the given entity.  Valid
            items are as shown in the Item1 columns of the tables
            below.

        it1num
            The number (or label) for the specified Item1 (if any).
            Valid IT1NUM values are as shown in the IT1NUM columns of
            the tables below.  Some Item1 labels do not require an
            IT1NUM value.

        item2, it2num
            A second set of item labels and numbers to further qualify
            the item for which data is to be retrieved.  Most items do
            not require this level of information.

        kloop
            Field to be looped on:

            - 0 or 2 : Loop on the ENTNUM field (default).
            - 3 : Loop on the Item1 field.
            - 4 : Loop on the IT1NUM field. Successive items are as shown with IT1NUM.
            - 5 : Loop on the Item2 field.
            - 6 : Loop on the IT2NUM field. Successive items are as shown with IT2NUM.

        Examples
        --------
        List the current selected node numbers

        >>> mapdl.get_array('NODE', item1='NLIST')
        array([  1.,   2.,   3.,   4.,   5.,   6.,   7.,   8.,
              ...
              314., 315., 316., 317., 318., 319., 320., 321.])

        Notes
        -----
        Please reference your ANSYS help manual *VGET command tables
        for all the available *VGET values

        """
        return self._get_array(entity, entnum, item1, it1num, item2,
                               it2num, kloop)

    def _get_array(self, *args, **kwargs):
        """Implemented by child class"""
        raise NotImplementedError('Implemented by child class')

    def _display_plot(self, text):
        """Display the last generated plot (*.png) from MAPDL"""
        png_found = PNG_TEST.findall(text)
        if png_found:
            # flush graphics writer
            self.show('CLOSE')
            self.show('PNG')

            import matplotlib.pyplot as plt
            import matplotlib.image as mpimg
            filename = self._screenshot_path()

            if os.path.isfile(filename):
                img = mpimg.imread(filename)
                plt.imshow(img)
                plt.axis('off')
                if self._show_matplotlib_figures:
                    plt.show()  # consider in-line plotting
            else:
                self._log.error('Unable to find screenshot at %s' % filename)

    def _screenshot_path(self):
        """Return last filename based on the current jobname"""
        filenames = glob.glob(os.path.join(self.path, '%s*.png' % self.jobname))
        filenames.sort()
        return filenames[-1]
