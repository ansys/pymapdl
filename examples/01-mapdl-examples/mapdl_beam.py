"""
This is an example from FINITE ELEMENT ANALYSIS USING ANSYS 11.0

"""

import pyansys

# mapdl = pyansys.launch_mapdl(override=True, loglevel='WARNING',
#                              interactive_plotting=True)
mapdl.clear(), mapdl.clear()

# reduce pixel count for larger font documentation plots
mapdl.gfile(800)

mapdl.prep7()
mapdl.et(1, 'BEAM188')
mapdl.keyopt(1, 4, 1)  # transverse shear stress output

# define beam properties in CM
sec_num = 1
mapdl.sectype(sec_num, 'BEAM', 'I', 'ISection', 3)
mapdl.secoffset('CENT')
beam_info = mapdl.secdata(15, 15, 29, 2, 2, 1)  # dimensions are in centimeters
mapdl.secplot(sec_num)

mapdl.mp('EX', 1, 2E7)  # N/cm2
mapdl.mp('PRXY', 1, 0.27)  #  Poisson's ratio

# create nodes
mapdl.n(1, 0, 0, 0)
mapdl.n(12, 110, 0, 0)
mapdl.n(23, 220, 0, 0)
mapdl.fill(1, 12, 10)
mapdl.fill(12, 23, 10)

# list the node coordinates
print(mapdl.nodes)

# list the node numbers
print(mapdl.nnum)

# plot the nodes without using vtk
mapdl.nplot(knum=True)

# plot the nodes using VTK
mapdl.nplot(vtk=True, knum=True, cpos='xy', show_bounds=True)

# create elements between the nodes
# we can just manually create elements since we know that the elements
# are sequential
for node in mapdl.nnum[:-1]:
    mapdl.e(node, node + 1)

# print the elements from MAPDL
print(mapdl.elist())

# also, access them as a list of arrays
mapdl.elements


# Allow movement only in the X and Z direction
for const in ['UX', 'UY', 'ROTX', 'ROTZ']:
    mapdl.d('all', const)


# constrain just nodes 1 and 23 in the Z direction
mapdl.d(1, 'UZ')
mapdl.d(23, 'UZ')

# apply a -Z force at node 12
mapdl.f(12, 'FZ', -22840)


mapdl.run('/solu')
mapdl.antype('static')
mapdl.solve()

rst0 = pyansys.read_binary('/tmp/ansys/file0.rst')
rst0.geometry

rst1 = pyansys.read_binary('/tmp/ansys/file1.rst')
rst1.geometry
