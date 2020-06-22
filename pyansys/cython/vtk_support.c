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


// element type to VTK conversion function call map
//  0: skip
//  1: Point
//  2: Line
//  3: Shell
// 4: 3d Solid (Hexahedral, wedge, pyramid, tetrahedral)
// 5: Tetrahedral

/*
int ETYPE_MAP[] = {0, // Empty for FORTRAN based indexing
		   2,  // LINK1
		   3,  // PLANE2
		   3,  // BEAM3
		   3,  // BEAM4
		   4,  // SOLID5
		   0,  // UNUSED6
		   1,  // COMBIN7
		   2,  // LINK8
		   0,  // INFIN9
		   2,  // LINK10
		   2,  // LINK11
		   2,  // CONTAC12
		   3,  // PLANE13
		   2,  // COMBIN14
		   0,  // FLUID15
		   2,  // PIPE16
		   2,  // PIPE17
		   2,  // PIPE18
		   0,  // SURF19
		   2,  // PIPE20
		   1,  // MASS21
		   3,  // SURF22
		   2,  // BEAM23
		   2,  // BEAM24
		   3,  // PLANE25
		   0,  // UNUSED26
		   0,  // MATRIX27
		   3,  // SHELL28
		   3,  // FLUID29
		   4,  // FLUID30
		   2,  // LINK31
		   2,  // LINK32
		   2,  // LINK33
		   2,  // LINK34
		   3,  // PLANE35
		   0,  // SOURC36
		   2,  // COMBIN37
		   2,  // FLUID38
		   2,  // COMBIN39
		   2,  // COMBIN40
		   3,  // SHELL41
		   3,  // PLANE42
		   3,  // SHELL43
		   2,  // BEAM44
		   4,  // SOLID45
		   4,  // SOLID46
		   0,  // INFIN47
		   0,  // UNUSED48
		   0,  // UNUSED49
		   0,  // MATRIX50
		   3,  // SHELL51
		   0,  // CONTAC52
		   3,  // PLANE53
		   3,  // BEAM54
		   3,  // PLANE55
		   0,  // UNUSED56
		   3,  // SHELL57
		   0,  // UNUSED58
		   0,  // PIPE59
		   0,  // PIPE60
		   2,  // SHELL61
		   4,  // SOLID62
		   3,  // SHELL63
		   4,  // SOLID64
		   4,  // SOLID65
		   2,  // FLUID66
		   3,  // PLANE67
		   2,  // LINK68
		   4,  // SOLID69
		   4,  // SOLID70
		   1,  // MASS71
		   0,  // UNUSED72
		   0,  // UNUSED73
		   0,  // UNUSED74
		   3,  // PLANE75
		   0,  // UNUSED76
		   3,  // PLANE77
		   3,  // PLANE78
		   3,  // FLUID79
		   4,  // FLUID80
		   3,  // FLUID81
		   3,  // PLANE82
		   3,  // PLANE83
		   0,  // UNUSED84
		   0,  // UNUSED85
		   0,  // UNUSED86
		   5,  // SOLID87
		   3,  // VISCO88
		   4,  // VISCO89
		   4,  // SOLID90
		   3,  // SHELL91
		   5,  // SOLID92
		   3,  // SHELL93
		   0,  // CIRCU94
		   4,  // SOLID95
		   4,  // SOLID96
		   4,  // SOLID97
		   5,  // SOLID98
		   3,  // SHELL99
		   4,  // USER100
		   4,  // USER101
		   4,  // USER102
		   4,  // USER103
		   4,  // USER104
		   4,  // USER105
		   3,  // VISCO106
		   4,  // VISCO107
		   4,  // VISCO108
		   0,  // TRANS109
		   0,  // INFIN110
		   0,  // INFIN111
		   0,  // ROT112
		   0,  // UNUSED113
		   0,  // UNUSED114
		   3,  // INTER115
		   3,  // FLUID116
		   4,  // EDGE117
		   3,  // HF118
		   5,  // HF119
		   4,  // HF120
		   3,  // PLANE121
		   4,  // SOLID122
		   5,  // SOLID123
		   0,  // CIRCU124
		   0,  // CIRCU125
		   2,  // TRANS126
		   0,  // UNUSED127
		   0,  // UNUSED128
		   2,  // FLUID129
		   3,  // FLUID130
		   3,  // SHELL131
		   3,  // SHELL132
		   0,  // UNUSED133
		   0,  // UNUSED134
		   0,  // TRANS135
		   3,  // FLUID136
		   0,  // FLUID137
		   0,  // FLUID138
		   0,  // FLUID139
		   5,  // ROM140
		   0,  // UNUSED141
		   0,  // UNUSED142
		   3,  // SHELL143
		   0,  // ROM144
		   0,  // UNUSED145
		   0,  // UNUSED146
		   0,  // UNUSED147
		   0,  // UNUSED148
		   0,  // UNUSED149
		   0,  // UNUSED150
		   2,  // SURF151
		   3,  // SURF152
		   2,  // SURF153
		   3,  // SURF154
		   3,  // SURF155
		   2,  // SURF156
		   3,  // SHELL157
		   0,  // UNUSED158
		   0,  // SURF159
		   0,  // UNUSED160
		   2,  // BEAM161
		   0,  // UNUSED162
		   3,  // SHELL163
		   4,  // SOLID164
		   0,  // UNUSED165
		   0,  // UNUSED166
		   0,  // UNUSED167
		   5,  // SOLID168
		   0,  // TARGE169
		   0,  // TARGE170
		   2,  // CONTA171
		   2,  // CONTA172
		   3,  // CONTA173
		   3,  // CONTA174
		   1,  // CONTA175
		   2,  // CONTA176
		   2,  // CONTA177
		   2,  // CONTA178
		   0,  // PRETS179
		   2,  // LINK180
		   3,  // SHELL181
		   3,  // PLANE182
		   3,  // PLANE183
		   0,  // RBAR184
		   4,  // SOLID185
		   4,  // SOLID186
		   5,  // SOLID187
		   2,  // BEAM188
		   2,  // BEAM189
		   4,  // SOLSH190
		   4,  // INTER192
		   0,  // INTER193
		   0,  // INTER194
		   0,  // INTER195
		   0,  // LAYER196
		   0,  // LAYER197
		   0,  // UNUSED198
		   0,  // UNUSED199
		   0,  // UNUSED200
		   0,  // FOLLW201
		   0,  // INTER202
		   0,  // INTER203
		   0,  // INTER204
		   0,  // INTER205
		   0,  // INTER206
		   0,  // UNUSED207
		   2,  // SHELL208
		   2,  // SHELL209
		   0,  // UNUSED210
		   0,  // UNUSED211
		   0,  // CPT212
		   0,  // CPT213
		   0,  // COMBI214
		   0,  // CPT215
		   5,  // CPT217
		   3,  // FLUID218
		   3,  // FLUID219
		   4,  // FLUID220
		   5,  // FLUID221
		   3,  // PLANE222
		   3,  // PLANE223
		   0,  // UNUSED224
		   0,  // SOLID225
		   4,  // SOLID226
		   5,  // SOLID227
		   0,  // UNUSED228
		   0,  // UNUSED229
		   3,  // PLANE230
		   4,  // SOLID231
		   5,  // SOLID232
		   3,  // PLANE233
		   0,  // UNUSED234
		   0,  // UNUSED235
		   4,  // SOLID236
		   5,  // SOLID237
		   3,  // PLANE238
		   4,  // SOLID239
		   5,  // SOLID240
		   0,  // HSFLD241
		   0,  // HSFLD242
		   0,  // UNUSED243
		   0,  // UNUSED244
		   0,  // UNUSED245
		   0,  // UNUSED246
		   0,  // UNUSED247
		   0,  // UNUSED248
		   0,  // UNUSED249
		   2,  // COMBI250
		   2,  // SURF251
		   3,  // SURF252
		   0,  // UNUSED253
		   0,  // UNUSED254
		   0,  // UNUSED255
		   0,  // UNUSED256
		   0,  // INFIN257
		   0,  // INFIN258
		   0,  // INFIN259
		   4,  // UNUSED261
		   0,  // GLINK262
		   0,  // REINF263
		   0,  // REINF264
		   0,  // REINF265
		   0,  // UNUSED266
		   0,  // UNUSED267
		   0,  // UNUSED268
		   0,  // UNUSED269
		   0,  // UNUSED270
		   0,  // UNUSED271
		   0,  // SOLID272
		   0,  // SOLID273
		   0,  // UNUSED274
		   0,  // UNUSED275
		   0,  // UNUSED276
		   0,  // UNUSED277
		   4,  // SOLID278
		   4,  // SOLID279
		   2,  // CABLE280
		   3,  // SHELL281
		   3,  // SHELL282
		   3,  // SHELL283
		   0,  // UNUSED284
		   5,  // SOLID285
		   0,  // UNUSED286
		   0,  // UNUSED287
		   2,  // PIPE288
		   2,  // PIPE289
		   2,  // ELBOW290
		   5,  // SOLID291
		   3,  // PLANE292
		   3,  // PLANE293
		   0,  // UNUSED294
		   0,  // UNUSED295
		   0,  // UNUSED296
		   0,  // UNUSED297
		   0,  // UNUSED298
		   0,  // UNUSED299
		   0, // USER300 
};
*/

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
__inline void add_cell(bool build_offset, int n_points, uint8_t celltype){
  if (build_offset){
    vtk_data.offset[0] = vtk_data.loc;
    vtk_data.offset++;
  }
  vtk_data.celltypes[0] = celltype;
  vtk_data.celltypes++;
  vtk_data.cells[vtk_data.loc++] = n_points;
  /* printf("Added cell at %d\n", vtk_data.loc); */
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
__inline void add_hex(bool build_offset, int *elem, int nnode){
  int i;
  bool quad = nnode > 8;
  if (quad){
    add_cell(build_offset, 20, VTK_QUADRATIC_HEXAHEDRON);
  } else {
    add_cell(build_offset, 8, VTK_HEXAHEDRON);
  }

  // Always add linear
  for (int i=0; i<8; i++){
    vtk_data.cells[vtk_data.loc++] = vtk_data.nref[elem[i]];
    /* printf("added %d at %d using node %d\n", vtk_data.nref[elem[i]], vtk_data.loc - 1, elem[i]); */
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
__inline void add_wedge(bool build_offset, int *elem, int nnode){
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


__inline void add_pyr(bool build_offset, int *elem, int nnode){
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
__inline void add_tet(bool build_offset, int *elem, int nnode){
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
__inline void add_tet10(bool build_offset, int *elem, int nnode){
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


__inline void add_quad(bool build_offset, int *elem, bool is_quad){
  int n_points;
  if (is_quad){
    n_points = 8;
    add_cell(build_offset, n_points, VTK_QUADRATIC_QUAD);
  } else {
    n_points = 4;
    add_cell(build_offset, n_points, VTK_QUAD);
  }

  // translate connectivity
  for (int i=0; i<n_points; i++){
    vtk_data.cells[vtk_data.loc++] = vtk_data.nref[elem[i]];
  }

  return;
}

__inline void add_tri(bool build_offset, int *elem, bool quad){
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


__inline void add_line(bool build_offset, int *elem, bool quad){
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


__inline void add_point(bool build_offset, int *elem){
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
 * 
 * Returns (Given as as parameters)
 * -------
 * offset : VTK offset array to populate
 * 
 * cells : VTK cell connectivity
 * 
 * celltypes: VTK cell types
 * 
 * build_offset: Enable, disable populating offset array
 * ==========================================================================*/
int ans_to_vtk(int nelem, int *elem, int *elem_off, int *type_ref, int nnode,
	       int *nnum, int64_t *offset, int64_t *cells, uint8_t *celltypes,
	       int build_offset){
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
    /* printf("Element %d \n", i); */
    // etype
    etype = elem[elem_off[i] + 1];
    off = elem_off[i] + 10; // to the start of the nodes
    /* printf("off = %d \n", off); */
    nnode_elem = elem_off[i + 1] - off;  // number of nodes in element
    /* printf("nnode_elem = %d \n", nnode_elem); */
    /* printf("type_ref[%d]\n", type_ref[etype]); */

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
      if (elem[off + 2] == elem[off + 13]){
  	add_tri(build_offset, &elem[off], is_quad);
      } else {  // is quadrilateral
  	add_quad(build_offset, &elem[off], is_quad);
      }
      break;
    case 4: // solid
      /* printf("Adding SOLID\n"); */
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
      /* is_quad = nnode_elem > 4; */
      add_tet10(build_offset, &elem[off], nnode_elem);
      break;
    // should never reach here
    } // end of switch
    /* printf("Done\n\n"); */
  }  // end of loop

  /* printf("vtk_data.loc %d\n", vtk_data.loc); */
  /* printf("FINISHING\n\n"); */

  /* for (i=0; i<vtk_data.loc; i++){ */
  /*   printf("CELL %d: %d\n", i, cells[i]); */
  /* } */

  free(nref);
  return vtk_data.loc;
}
