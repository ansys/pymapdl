#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

//=============================================================================
// Fast string to interger convert to ANSYS formatted intergers 
//=============================================================================
__inline int fast_atoi(char* raw, int intsz){

  int val;
  int c;

  val = 0;
  for (c=0; c<intsz; ++c){
    // Seek through white space
    if (raw[0] == ' '){
      ++raw;
      continue;
    }

    val = val*10 + (raw[0] - '0');
    ++raw;
  }
  return val;
}


//=============================================================================
// Checks for negative character 
//=============================================================================
__inline int checkneg(char * raw, int intsz){
  int c;
  for (c=0; c<intsz; ++c){
    if (raw[0] == '-'){
      return 1;
    }
    ++raw;
  }
  return 0;
}

// Reads various ansys float formats in the form of 
// 3.7826539829200E+00
// 
// 
/* double ans_strtod( */

//=============================================================================
// reads nblock from ANSYS.  Raw string is from Python reader and file is
// positioned at the start of the data of NBLOCK
//=============================================================================
int read_nblock(char *raw, int *nnum, double *nodes, int nnodes, int* intsz,
		int fltsz, int *n, int EOL, int nexp){

  // set to start of the NBLOCK
  raw += n[0];
  int len_orig = strlen(raw);
  int j;

  for (int i=0; i<nnodes; i++){
    nnum[i] = fast_atoi(raw, intsz[0]);
    raw += intsz[0];
    raw += intsz[1];
    raw += intsz[2];
    
    for (j=0; j<6; j++){
      if (raw[0] == '\r' || raw[0] == '\n'){
	break;
      }
      // performance is slow here.  Need a specialized strtod for ANSYS floats
      nodes[6*i + j] = strtod(raw, &raw);
    }

    // remaining are zeros
    for (; j<6; j++){
      nodes[6*i + j] = 0;
    }

    while (raw[0] == '\r' || raw[0] == '\n'){
      ++raw;
    }
  }

  // return file position
  int fpos = len_orig - strlen(raw) + n[0];
  return fpos;

}


/* ============================================================================
 * Function:  read_eblock
 *
 * Reads EBLOCK from ANSYS archive file.
 * raw : Raw string is from Python reader
 * 
 * elem_off : Indices of the start of each element in ``elem``
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
 * nelem : Number of elements.
 * 
 * pos : Position of the start of the EBLOCK.
 * ==========================================================================*/
int read_eblock(char *raw, int *elem_off, int *elem, int nelem, int intsz,
		int *pos){
  int i, j, nnode;

  // set to start of the EBLOCK
  raw += pos[0];
  int len_orig = strlen(raw);
  int c = 0;  // position in elem array

  // Loop through elements
  for (i=0; i<nelem; ++i){
    // store start of each element
    elem_off[i] = c;

    // Check if end of line
    while (raw[0] == '\r' || raw[0] == '\n' ){
      ++raw;
    }

    // Check if at end of the block
    if (checkneg(raw, intsz)){
      raw += intsz;
      break;
    }

    // ANSYS archive format:
    // Field 1: material reference number
    elem[c++] = fast_atoi(raw, intsz); raw += intsz;

    // Field 2: element type number
    elem[c++] = fast_atoi(raw, intsz); raw += intsz;

    // Field 3: real constant reference number
    elem[c++] = fast_atoi(raw, intsz); raw += intsz;

    // Field 4: section number
    elem[c++] = fast_atoi(raw, intsz); raw += intsz;

    // Field 5: element coordinate system
    elem[c++] = fast_atoi(raw, intsz); raw += intsz;

    // Field 6: Birth/death flag
    elem[c++] = fast_atoi(raw, intsz); raw += intsz;

    // Field 7: Solid model reference
    elem[c++] = fast_atoi(raw, intsz); raw += intsz;

    // Field 8: Coded shape key
    elem[c++] = fast_atoi(raw, intsz); raw += intsz;

    // Field 9: Number of nodes
    nnode = fast_atoi(raw, intsz); raw += intsz;

    /* // sanity check */
    /* if (nnode > 20){ */
    /*   printf("Element %d\n", i); */
    /*   perror("Greater than 20 nodes\n"); */
    /*   exit(1); */
    /* } */

    // Field 10: Not Used
    raw += intsz;
    
    // Field 11: Element number
    elem[c++] = fast_atoi(raw, intsz); raw += intsz;

    // Need an additional value for consitency with other formats
    elem[c++] = 0;

    // Read nodes in element
    for (j=0; j<nnode; j++){
      /* printf("reading node %d\n", j); */
      // skip through EOL
      while (raw[0] == '\r' || raw[0] == '\n' ) ++raw;
      elem[c++] = fast_atoi(raw, intsz); raw += intsz;
    }
  }

  // update file position
  *(pos) = len_orig - strlen(raw) + pos[0];

  // Return total data read
  elem_off[nelem] = c;
  return c;
}
