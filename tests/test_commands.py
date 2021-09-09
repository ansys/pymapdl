"""Test commands with unexpected or unintended behavior."""

import os 

import pytest  

from ansys.mapdl.core import launch_mapdl


@pytest.mark.skip_grpc
def test_cmatrix():
    """
    Unit test for `CMATRIX`.
    
    `CMATRIX` does not work in 'interactive' mode and also it switches the output to a 
    file called `cmatrix.out`. To fix all of this, it has been added to the list of 
    non-interactive commands (See PyMAPDL User-Guide documentation) and it has now a
    wrapper to recover the output from the `CMATRIX.out`.

    The 'Capname' parameter of `CMATRIX` (`CMATRIX,SYMFAC,Condname,NUMCOND,GRNDKEY,Capname`)
    changes the name of the array parameter and the file name where the array is written but
    it does not change the name of the output ('CMATRIX.OUT'). So we don't need to test that
    specific case.

    """

    mapdl = launch_mapdl(loglevel="WARNING")
    mapdl.run("/batch,list")
    mapdl.prep7()
    mapdl.title("Capacitance of two long cylinders above a ground plane")
    mapdl.run("a=100")  # Cylinder inside radius (μm)
    mapdl.run("d=400")  # Outer radius of air region
    mapdl.run("ro=800")  # Outer radius of infinite elements
    mapdl.et(1, 121)  # 8-node 2-D electrostatic element
    mapdl.et(2, 110, 1, 1)  # 8-node 2-D Infinite element
    mapdl.emunit("epzro", 8.854e-6)  # Set free-space permittivity for μMKSV units
    mapdl.mp("perx", 1, 1)
    mapdl.cyl4("d/2", "d/2", "a", 0)  # Create mode in first quadrant
    mapdl.cyl4(0, 0, "ro", 0, "", 90)
    mapdl.cyl4(0, 0, "2*ro", 0, "", 90)
    mapdl.aovlap("all")
    mapdl.numcmp("area")
    mapdl.run("smrtsiz,4")
    mapdl.mshape(1)  # Mesh air region
    mapdl.amesh(3)
    mapdl.lsel("s", "loc", "x", "1.5*ro")
    mapdl.lsel("a", "loc", "y", "1.5*ro")
    mapdl.lesize("all", "", "", 1)
    mapdl.type(2)
    mapdl.mshape(0)
    mapdl.mshkey(1)
    mapdl.amesh(2)  # Mesh infinite region
    mapdl.run("arsymm,x,all")  # Reflect model about y axis
    mapdl.nummrg("node")
    mapdl.nummrg("kpoi")
    mapdl.csys(1)
    mapdl.nsel("s", "loc", "x", "2*ro")
    mapdl.sf("all", 'inf')  # Set infinite flag in Infinite elements
    mapdl.local(11, 1, "d/2", "d/2")
    mapdl.nsel("s", "loc", "x", "a")
    mapdl.cm("cond1", "node")  # Assign node component to 1st conductor
    mapdl.local(12, 1, "-d/2", "d/2")
    mapdl.nsel("s", "loc", "x", "a")
    mapdl.cm("cond2", "node")  # Assign node component to 2nd conductor
    mapdl.csys(0)
    mapdl.nsel("s", "loc", "y", 0)
    mapdl.cm("cond3", "node")  # Assign node component to ground conductor
    mapdl.allsel("all")
    mapdl.finish()
    mapdl.run("/solu") 

    with mapdl.non_interactive:
        #CMATRIX,SYMFAC,Condname,NUMCOND,GRNDKEY,Capname
        mapdl.run("cmatrix,1, 'cond', 3, 0, 'aa'")

    # Next line is going to be included in the `CMATRIX` wrapper in `mapdl_grpc`.
    # See PR #571.
    # So please comment/delete when that PR is merged.
    # mapdl._response  = mapdl._download_as_raw('cmatrix.out').decode() #TODO: To delete/comment when PR #571 is merged.
    assert 'Capacitance matricies are stored in file' in mapdl.last_response
    
    mapdl.finish()
    mapdl.exit()