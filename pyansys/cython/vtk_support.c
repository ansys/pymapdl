#include <stdint.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>

/* VTK numbering for vtk cells */
uint8_t VTK_EMPTY_CELL = 0;
uint8_t VTK_VERTEX = 1;
uint8_t VTK_LINE = 3;
uint8_t VTK_TRIANGLE = 5;
uint8_t VTK_QUAD = 9;
uint8_t VTK_QUADRATIC_TRIANGLE = 22;
uint8_t VTK_QUADRATIC_QUAD = 23;
uint8_t VTK_HEXAHEDRON = 12;
uint8_t VTK_PYRAMID = 14;
uint8_t VTK_TETRA = 10;
uint8_t VTK_WEDGE = 13;
uint8_t VTK_QUADRATIC_EDGE = 21;
uint8_t VTK_QUADRATIC_TETRA = 24;
uint8_t VTK_QUADRATIC_PYRAMID = 27;
uint8_t VTK_QUADRATIC_WEDGE = 26;
uint8_t VTK_QUADRATIC_HEXAHEDRON = 25;


// Contains data for VTK UnstructuredGrid
struct VtkData {
  int64_t *offset;
  int64_t *cells;
  uint8_t *celltypes;
  int loc;  // current position within cells
  int *nref;  // conversion between ansys and vtk numbering
};
struct VtkData vtk_data;


// Populate offset, cell type, and prepare the cell array for a cell
static inline void add_cell(bool build_offset, int n_points, uint8_t celltype){
  if (build_offset){
    vtk_data.offset[0] = vtk_data.loc;
    vtk_data.offset++;
  }
  vtk_data.celltypes[0] = celltype;
  vtk_data.celltypes++;
  vtk_data.cells[vtk_data.loc++] = n_points;
  return;
}



/* ============================================================================
 * Store hexahedral element in vtk arrays.  ANSYS elements are
 * ordered in the same manner as VTK.
 * 
 * VTK DOCUMENTATION
 * Linear Hexahedral
 * The hexahedron is defined by the eight points (0-7) where
 * (0,1,2,3) is the base of the hexahedron which, using the right
 * hand rule, forms a quadrilaterial whose normal points in the
 * direction of the opposite face (4,5,6,7).
 * 
 * Quadradic Hexahedral
 * The ordering of the twenty points defining the cell is point ids
 * (0-7, 8-19) where point ids 0-7 are the eight corner vertices of
 * the cube; followed by twelve midedge nodes (8-19)
 * Note that these midedge nodes correspond lie on the edges defined by:
 * Midside   Edge nodes
 * 8         (0, 1)
 * 9         (1, 2)
 * 10        (2, 3)
 * 11        (3, 0)
 * 12        (4, 5)
 * 13        (5, 6)
 * 14        (6, 7)
 * 15        (7, 4)
 * 16        (0, 4)
 * 17        (1, 5)
 * 18        (2, 6)
 * 19        (3, 7)
 */
static inline void add_hex(bool build_offset, int *elem, int nnode){
  int i;
  bool quad = nnode > 8;
  if (quad){
    add_cell(build_offset, 20, VTK_QUADRATIC_HEXAHEDRON);
  } else {
    add_cell(build_offset, 8, VTK_HEXAHEDRON);
  }

  // Always add linear
  for (i=0; i<8; i++){
    vtk_data.cells[vtk_data.loc++] = vtk_data.nref[elem[i]];
  }

  // translate connectivity
  if (quad){
    for (i=8; i<nnode; i++){
      vtk_data.cells[vtk_data.loc++] = vtk_data.nref[elem[i]];
      /* printf("added %d at %d using node %d\n", vtk_data.nref[elem[i]], vtk_data.loc - 1, elem[i]); */
    }
    // ANSYS sometimes doesn't write 0 at the end of the element block
    // and quadratic cells always contain 10 nodes
    for (i=nnode; i<20; i++){
      vtk_data.cells[vtk_data.loc++] = -1;
    }
  }

  return;
}



/* ============================================================================
Store wedge element in vtk arrays.  ANSYS elements are ordered
differently than vtk elements.  ANSYS orders counter-clockwise and
VTK orders clockwise
    
VTK DOCUMENTATION
Linear Wedge
The wedge is defined by the six points (0-5) where (0,1,2) is the
base of the wedge which, using the right hand rule, forms a
triangle whose normal points outward (away from the triangular
face (3,4,5)).

Quadradic Wedge 
The ordering of the fifteen points defining the
cell is point ids (0-5,6-14) where point ids 0-5 are the six
corner vertices of the wedge, defined analogously to the six
points in vtkWedge (points (0,1,2) form the base of the wedge
which, using the right hand rule, forms a triangle whose normal
points away from the triangular face (3,4,5)); followed by nine
midedge nodes (6-14). Note that these midedge nodes correspond lie
on the edges defined by : 
(0,1), (1,2), (2,0), (3,4), (4,5), (5,3), (0,3), (1,4), (2,5)
*/
static inline void add_wedge(bool build_offset, int *elem, int nnode){
  bool quad = nnode > 8;
  if (quad){
    add_cell(build_offset, 15, VTK_QUADRATIC_WEDGE);
  } else {
    add_cell(build_offset, 6, VTK_WEDGE);
  }

  // [0, 1, 2, 2, 3, 4, 5, 5]
  vtk_data.cells[vtk_data.loc++] = vtk_data.nref[elem[2]];
  vtk_data.cells[vtk_data.loc++] = vtk_data.nref[elem[1]];
  vtk_data.cells[vtk_data.loc++] = vtk_data.nref[elem[0]];
  vtk_data.cells[vtk_data.loc++] = vtk_data.nref[elem[6]];
  vtk_data.cells[vtk_data.loc++] = vtk_data.nref[elem[5]];
  vtk_data.cells[vtk_data.loc++] = vtk_data.nref[elem[4]];

  if (quad){  // todo: check if index > nnode - 1
    vtk_data.cells[vtk_data.loc++] = vtk_data.nref[elem[9]];
    vtk_data.cells[vtk_data.loc++] = vtk_data.nref[elem[8]];
    vtk_data.cells[vtk_data.loc++] = vtk_data.nref[elem[11]];
    vtk_data.cells[vtk_data.loc++] = vtk_data.nref[elem[13]];
    vtk_data.cells[vtk_data.loc++] = vtk_data.nref[elem[12]];
    vtk_data.cells[vtk_data.loc++] = vtk_data.nref[elem[15]];
    vtk_data.cells[vtk_data.loc++] = vtk_data.nref[elem[18]];
    vtk_data.cells[vtk_data.loc++] = vtk_data.nref[elem[17]];
    vtk_data.cells[vtk_data.loc++] = vtk_data.nref[elem[16]];
  }

  return;
}


static inline void add_pyr(bool build_offset, int *elem, int nnode){
  int i;  // counter
  bool quad = nnode > 8;
  if (quad){
    add_cell(build_offset, 13, VTK_QUADRATIC_PYRAMID);
  } else {
    add_cell(build_offset, 5, VTK_PYRAMID);
  }

  // [0, 1, 2, 3, 4, X, X, X]
  for (i=0; i<5; i++){
     vtk_data.cells[vtk_data.loc++] = vtk_data.nref[elem[i]];
  }

  if (quad){  // todo: check if index > nnode - 1
    for (i=8; i<12; i++){
      vtk_data.cells[vtk_data.loc++] = vtk_data.nref[elem[i]];
    }

    for (i=16; i<20; i++){
      vtk_data.cells[vtk_data.loc++] = vtk_data.nref[elem[i]];
    }
  }
  return;
}



/* ============================================================================
 * Stores tetrahedral element in vtk arrays.  ANSYS elements are
 * ordered the same as vtk elements.
 * 
 * VTK DOCUMENTATION:
 * Linear
 * The tetrahedron is defined by the four points (0-3); where (0,1,2)
 * is the base of the tetrahedron which, using the right hand rule,
 * forms a triangle whose normal points in the direction of the
 * fourth point.
 * 
 * Quadradic   
 * The cell includes a mid-edge node on each of the size edges of the
 * tetrahedron. The ordering of the ten points defining the cell is
 * point ids (0-3,4-9) where ids 0-3 are the four tetra vertices; and
 * point ids 4-9 are the midedge nodes between:
 * (0,1), (1,2), (2,0), (0,3), (1,3), and (2,3)
============================================================================ */
static inline void add_tet(bool build_offset, int *elem, int nnode){
  bool quad = nnode > 8;
  if (quad){
    add_cell(build_offset, 10, VTK_QUADRATIC_TETRA);
  } else {
    add_cell(build_offset, 4, VTK_TETRA);
  }

  // edge nodes
  // [0, 1, 2, 2, 3, 3, 3, 3]
  vtk_data.cells[vtk_data.loc++] = vtk_data.nref[elem[0]];
  vtk_data.cells[vtk_data.loc++] = vtk_data.nref[elem[1]];
  vtk_data.cells[vtk_data.loc++] = vtk_data.nref[elem[2]];
  vtk_data.cells[vtk_data.loc++] = vtk_data.nref[elem[4]];

  if (quad){  // todo: check if index > nnode - 1
    vtk_data.cells[vtk_data.loc++] = vtk_data.nref[elem[8]];
    vtk_data.cells[vtk_data.loc++] = vtk_data.nref[elem[9]];
    vtk_data.cells[vtk_data.loc++] = vtk_data.nref[elem[11]];
    vtk_data.cells[vtk_data.loc++] = vtk_data.nref[elem[16]];
    vtk_data.cells[vtk_data.loc++] = vtk_data.nref[elem[17]];
    vtk_data.cells[vtk_data.loc++] = vtk_data.nref[elem[18]];
  }

  return;
}


// ANSYS Tetrahedral style [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
static inline void add_tet10(bool build_offset, int *elem, int nnode){
  int i;  // counter
  bool quad = nnode > 4;
  if (quad){
    add_cell(build_offset, 10, VTK_QUADRATIC_TETRA);
  } else {
    add_cell(build_offset, 4, VTK_TETRA);
  }

  // edge nodes
  vtk_data.cells[vtk_data.loc++] = vtk_data.nref[elem[0]];
  vtk_data.cells[vtk_data.loc++] = vtk_data.nref[elem[1]];
  vtk_data.cells[vtk_data.loc++] = vtk_data.nref[elem[2]];
  vtk_data.cells[vtk_data.loc++] = vtk_data.nref[elem[3]];

  if (quad){
    for (i=4; i<nnode; i++){
      vtk_data.cells[vtk_data.loc++] = vtk_data.nref[elem[i]];
    }
    // ANSYS sometimes doesn't write 0 at the end of the element block
    // and quadratic cells always contain 10 nodes
    for (i=nnode; i<10; i++){
      vtk_data.cells[vtk_data.loc++] = -1;
    }
  }

  return;
}


static inline void add_quad(bool build_offset, int *elem, bool is_quad){
  int i;
  int n_points;
  if (is_quad){
    n_points = 8;
    add_cell(build_offset, n_points, VTK_QUADRATIC_QUAD);
  } else {
    n_points = 4;
    add_cell(build_offset, n_points, VTK_QUAD);
  }

  // translate connectivity
  for (i=0; i<n_points; i++){
    vtk_data.cells[vtk_data.loc++] = vtk_data.nref[elem[i]];
  }

  return;
}

void add_tri(bool build_offset, int *elem, bool quad){
  if (quad){
    add_cell(build_offset, 6, VTK_QUADRATIC_TRIANGLE);
  } else {
    add_cell(build_offset, 3, VTK_TRIANGLE);
  }

  // edge nodes
  vtk_data.cells[vtk_data.loc++] = vtk_data.nref[elem[0]];
  vtk_data.cells[vtk_data.loc++] = vtk_data.nref[elem[1]];
  vtk_data.cells[vtk_data.loc++] = vtk_data.nref[elem[2]];

  if (quad){
    vtk_data.cells[vtk_data.loc++] = vtk_data.nref[elem[4]];
    vtk_data.cells[vtk_data.loc++] = vtk_data.nref[elem[5]];
    vtk_data.cells[vtk_data.loc++] = vtk_data.nref[elem[7]];
  }

  return;
}


static inline void add_line(bool build_offset, int *elem, bool quad){
  if (quad){
    add_cell(build_offset, 3, VTK_QUADRATIC_EDGE);
  } else {
    add_cell(build_offset, 2, VTK_LINE);
  }

  // edge nodes
  vtk_data.cells[vtk_data.loc++] = vtk_data.nref[elem[0]];
  vtk_data.cells[vtk_data.loc++] = vtk_data.nref[elem[1]];
  if (quad){
    vtk_data.cells[vtk_data.loc++] = vtk_data.nref[elem[2]];
  }

  return;
}


static inline void add_point(bool build_offset, int *elem){
  add_cell(build_offset, 1, VTK_VERTEX);
  vtk_data.cells[vtk_data.loc++] = vtk_data.nref[elem[0]];
  return;
}



/*
Stores wedge element in vtk arrays.  ANSYS elements are ordered
differently than vtk elements.  ANSYS orders counter-clockwise and
VTK orders clockwise
    
VTK DOCUMENTATION
Linear Wedge
The wedge is defined by the six points (0-5) where (0,1,2) is the
base of the wedge which, using the right hand rule, forms a
triangle whose normal points outward (away from the triangular
face (3,4,5)).

Quadradic Wedge 
The ordering of the fifteen points defining the
cell is point ids (0-5,6-14) where point ids 0-5 are the six
corner vertices of the wedge, defined analogously to the six
points in vtkWedge (points (0,1,2) form the base of the wedge
which, using the right hand rule, forms a triangle whose normal
points away from the triangular face (3,4,5)); followed by nine
midedge nodes (6-14). Note that these midedge nodes correspond lie
on the edges defined by : 
(0,1), (1,2), (2,0), (3,4), (4,5), (5,3), (0,3), (1,4), (2,5)
*/



/* ============================================================================
 * function: ans_to_vtk
 * Convert raw ANSYS elements to a VTK UnstructuredGrid format.
 * 
 * Parameters
 * ----------
 * nelem : Number of elements.
 * 
 * elem: Array of elements
 *   Each element contains 10 items plus the nodes belonging to the
 *   element.  The first 10 items are:
 *     mat    - material reference number
 *     type   - element type number
 *     real   - real constant reference number
 *     secnum - section number
 *     esys   - element coordinate system
 *     death  - death flag (0 - alive, 1 - dead)
 *     solidm - solid model reference
 *     shape  - coded shape key
 *     elnum  - element number
 *     baseeid- base element number (applicable to reinforcing elements only
 *     nodes  - The nodes belonging to the element in ANSYS numbering.
 *
 * elem_off : Indices of the start of each element in ``elem``.
 *
 * tyep_ref : Maps an element type number of an element type to a
 *            correspoinding basic VTK element type:
 #       - TYPE 0 : Skip
 #       - TYPE 1 : Point
 #       - TYPE 2 : Line
 #       - TYPE 3 : Shell
 #       - TYPE 4 : 3D Solid (Hexahedral, wedge, pyramid, tetrahedral)
 #       - TYPE 5 : Tetrahedral
 *
 * nnode : Number of nodes.
 *
 * nnum : ANSYS Node numbering
 * 
 * build_offset: Enable, disable populating offset array
 * 
 * Returns (Given as as parameters)
 * -------
 * offset : VTK offset array to populate
 * 
 * cells : VTK cell connectivity
 * 
 * celltypes: VTK cell types
 * 

 * ==========================================================================*/
int ans_to_vtk(const int nelem, const int *elem, const int *elem_off,
	       const int *type_ref, const int nnode, const int* nnum,
	       int64_t *offset, int64_t *cells, uint8_t *celltypes,
	       const int build_offset){
  bool is_quad;
  int i;  // counter
  int nnode_elem;  // number of nodes belonging to the element
  int off;  // location of the element nodes
  int etype;  // ANSYS element type number

  // index ansys node number to VTK C based compatible indexing
  // max node number should be last node
  // Consider using a hash table here instead
  int *nref = (int*) malloc((nnum[nnode - 1] + 1) * sizeof(int));
  nref[0] = -1;  // for missing midside nodes ANSYS uses a node number of 0
  for (i=0; i<nnode; i++){
    nref[nnum[i]] = i;
  }

  // populate global vtk data
  vtk_data.offset = offset;
  vtk_data.cells = cells;
  vtk_data.celltypes = celltypes;
  vtk_data.nref = nref;
  vtk_data.loc = 0;

  // Convert each element from ANSYS connectivity to VTK connectivity
  for (i=0; i<nelem; i++){
    // etype
    etype = elem[elem_off[i] + 1];
    off = elem_off[i] + 10; // to the start of the nodes
    nnode_elem = elem_off[i + 1] - off;  // number of nodes in element

    switch (type_ref[etype]){
    case 0:  // not supported or not set
      add_cell(build_offset, 0, VTK_EMPTY_CELL);
      break;
    case 1: // point
      add_point(build_offset, &elem[off]);
      break;
    case 2: // line
      add_line(build_offset, &elem[off], nnode_elem > 2);
      break;
    case 3:  // shell
      is_quad = nnode_elem > 4;
      if (elem[off + 2] == elem[off + 3]){
  	add_tri(build_offset, &elem[off], is_quad);
      } else {  // is quadrilateral
  	add_quad(build_offset, &elem[off], is_quad);
      }
      break;
    case 4: // solid
      if (elem[off + 6] != elem[off + 7]){ // hexahedral
  	add_hex(build_offset, &elem[off], nnode_elem);
      } else if (elem[off + 5] != elem[off + 6]){ // wedge
  	add_wedge(build_offset, &elem[off], nnode_elem);
      } else if (elem[off + 2] != elem[off + 3]) { // pyramid
  	add_pyr(build_offset, &elem[off], nnode_elem);
      } else { // tetrahedral
  	add_tet(build_offset, &elem[off], nnode_elem);
      }
      break;
    case 5: // tetrahedral
      add_tet10(build_offset, &elem[off], nnode_elem);
      break;
    case 6:  // linear line
      add_line(build_offset, &elem[off], false);
    // should never reach here
    } // end of switch
  }  // end of loop

  free(nref);
  return vtk_data.loc;
}
