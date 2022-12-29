"""Using ``gmsh``, read the STEP file, mesh it, and save it as a MSH file."""
import gmsh

gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 1)

gmsh.model.add("t20")

# Load a STEP file (using `importShapes' instead of `merge' allows to directly
# retrieve the tags of the highest dimensional imported entities):
filename = "pf_coil_case_1.stp"
v = gmsh.model.occ.importShapes(filename)


# Get the bounding box of the volume:
gmsh.model.occ.synchronize()

# Specify a global mesh size and mesh the partitioned model:
gmsh.option.setNumber("Mesh.CharacteristicLengthMin", 10)
gmsh.option.setNumber("Mesh.CharacteristicLengthMax", 10)
gmsh.model.mesh.generate(3)
gmsh.write("from_gmsh.msh")

gmsh.finalize()
