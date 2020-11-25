#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <math.h>

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
__inline int checkneg(char *raw, int intsz){
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
// "3.7826539829200E+00"
// "1.0000000000000E-001"
// "        -6.01203 "
//
// fltsz : Number of characters to read in a floating point number
__inline int ans_strtod(char *raw, int fltsz, double *arr){
  int i;
  double sign = 1;

  for (i=0; i<fltsz; i++){
    if (*raw == '\r' || *raw == '\n'){
      // value is zero then
      arr[0] = 0;
      /* printf("EOL"); */
      return 1;
    }
    else if (*raw != ' '){  // always skip whitespace
      break;
    }
    raw++;
  }

  // either a number of a sign
  if (*raw == '-'){
    sign = -1;
    ++raw;
    ++i;
  }

  // next value is always a number
  double val = *raw++ - '0'; i++;

  // next value is always a "."
  raw++; i++;

  // Read through the rest of the number
  double k = 0.1;
  for (; i<fltsz; i++){
    if (*raw == 'e' || *raw == 'E'){  // incredibly, can be lowercase
      break;
    }
    else if (*raw >= '0' && *raw <= '9') {
      val += (*raw++ - '0') * k;
      k *= 0.1;
    }
  }

  // Might have scientific notation left, for example:
  // 1.0000000000000E-001
  int evalue = 0;
  int esign = 1;
  if (*raw == 'e' || *raw == 'E'){
    raw++; // skip "E"
    // always a sign of some sort
    if (*raw == '-'){
      esign = -1;
    }
    raw++; i++; i++;  // skip E and sign
    /* printf(" %d<%d ", i, fltsz); */
    for (; i<fltsz; i++){
      // read to whitespace or end of the line
      if (*raw == ' ' || *raw == '\r' || *raw == '\n'){
	break;
      }
      evalue = evalue*10 + (*raw++ - '0');
    }
    val *= pow(10, esign*evalue);
      
  }

  // seek through end of float value
  if (sign == -1){
    *arr = -val;
  }
  else {
    *arr = val;
  }
  /* printf(", %f", val); */

  return 0;  // Return 0 when a number has a been read
}

static inline double ans_strtod2(char *raw, int fltsz){
  int i;
  double sign = 1;

  for (i=0; i<fltsz; i++){
    if (*raw == '\r' || *raw == '\n'){
      // value is zero then
      return 0;
    }
    else if (*raw != ' '){  // always skip whitespace
      break;
    }
    raw++;
  }

  // either a number of a sign
  if (*raw == '-'){
    sign = -1;
    ++raw;
    ++i;
  }

  // next value is always a number
  double val = *raw++ - '0'; i++;
  double k = 10;
  for (; i<fltsz; i++){
    if (*raw == '.'){
      raw++;
      break;
    }
    else {
      val *= k;
      val += (*raw++ - '0');
      k *= 10; 
    }
  }

  // Read through the rest of the number
  k = 0.1;
  for (; i<fltsz; i++){
    if (*raw == 'e' || *raw == 'E'){
      break;
    }
    else if (*raw >= '0' && *raw <= '9') {
      val += (*raw++ - '0') * k;
      k *= 0.1;
    }
  }

  // Might have scientific notation left, for example:
  // 1.0000000000000E-001
  int evalue = 0;
  int esign = 1;
  if (*raw == 'e' || *raw == 'E'){
    raw++; // skip "E"
    // always a sign of some sort
    if (*raw == '-'){
      esign = -1;
    }
    raw++; i++; i++;  // skip E and sign
    for (; i<fltsz; i++){
      // read to whitespace or end of the line
      if (*raw == ' ' || *raw == '\r' || *raw == '\n'){
	break;
      }
      evalue = evalue*10 + (*raw++ - '0');
    }
    val *= pow(10, esign*evalue);
      
  }

  // seek through end of float value
  if (sign == -1){
    return -val;
  }
  return val;

}


//=============================================================================
// reads nblock from ANSYS.  Raw string is from Python reader and file is
// positioned at the start of the data of NBLOCK
//
// Returns
// -------
// nnodes_read : int
//     Number of nodes read.
//=============================================================================
int read_nblock(char *raw, int *nnum, double *nodes, int nnodes, int* intsz,
		int fltsz, int *n){

  // set to start of the NBLOCK
  raw += n[0];
  int len_orig = strlen(raw);
  int i, j, i_val, eol;

  for (i=0; i<nnodes; i++){

    // It's possible that less nodes are written to the record than
    // indicated.  In this case the line starts with a -1
    if (raw[0] == '-'){
      break;
    }

    i_val = fast_atoi(raw, intsz[0]);
    /* printf("%d", i_val); */
    nnum[i] = i_val;
    raw += intsz[0];
    raw += intsz[1];
    raw += intsz[2];
    
    for (j=0; j<6; j++){
      eol = ans_strtod(raw, fltsz, &nodes[6*i + j]);
      if (eol) {
	break;
      }
      else {
	raw += fltsz;
      }
    }

    // remaining are zeros
    for (; j<6; j++){
      nodes[6*i + j] = 0;
    }

    // possible whitespace (occurs in hypermesh generated files)
    while (*raw == ' '){
      ++raw;
    }

    while (*raw == '\r' || *raw == '\n'){
      ++raw;
    }
    /* printf("\n"); */
  }

  // return file position
  /* int fpos = len_orig - strlen(raw) + n[0]; */
  /* return fpos; */
  n[0] += len_orig - strlen(raw);
  return i;

}


/* Read just the node coordinates from the output from the MAPDL
 *  NWRITE command
 * (I8, 6G20.13) to write out NODE,X,Y,Z,THXY,THYZ,THZX
 */
int read_nblock_from_nwrite(const char* filename, int *nnum, double *nodes,
			    int nnodes){
  FILE * stream = fopen(filename, "r");

  if(stream == NULL)
    {
      printf("Error opening file");
      exit(1);
    }

  // set to start of the NBLOCK
  const int bufsize = 74;  // One int, 3 floats, two end char max (/r/n)
  char buffer[74];
  int i;

  for (i=0; i<nnodes; i++){
    fgets(buffer, bufsize, stream);
    nnum[i] = fast_atoi(&buffer[0], 9);

    // X
    if (buffer[9] == '\r' || buffer[9] == '\n'){
      nodes[i*3 + 0] = 0;
      nodes[i*3 + 1] = 0;
      nodes[i*3 + 2] = 0;
      continue;
    }
    nodes[i*3 + 0] = ans_strtod2(&buffer[9], 21);

    // Y
    if (buffer[30] == '\r' || buffer[30] == '\n'){
      nodes[i*3 + 1] = 0;
      nodes[i*3 + 2] = 0;
      continue;
    }
    nodes[i*3 + 1] = ans_strtod2(&buffer[30], 21);

    // Z
    if (buffer[51] == '\r' || buffer[51] == '\n'){
      nodes[i*3 + 2] = 0;
      continue;
    }
    nodes[i*3 + 2] = ans_strtod2(&buffer[51], 21);

  }

  fclose(stream);
  return 0;
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
    /* printf("reading element %d\n", elem[c - 1]); */

    // Need an additional value for consitency with other formats
    elem[c++] = 0;

    // Read nodes in element
    for (j=0; j<nnode; j++){
      /* printf("reading node %d\n", j); */
      // skip through EOL
      while (raw[0] == '\r' || raw[0] == '\n' ) ++raw;
      elem[c++] = fast_atoi(raw, intsz); raw += intsz;
    }

    // Edge case where missing midside nodes are not written (because
    // MAPDL refuse to write zeros at the end of a line)
    if (nnode < 20 && nnode > 10){
      for (j=nnode; j<20; j++){
        elem[c++] = 0;
      }
    }
    /* else if (nnode < 8 && nnode > 4){ */
    /*   for (j=nnode; j<8; j++){ */
    /*     elem[c++] = 0; */
    /*   } */
    /* } */

  }

  // update file position
  *(pos) = len_orig - strlen(raw) + pos[0];

  // Return total data read
  elem_off[nelem] = c;
  return c;
}


// Simply write an array to disk as ASCII
int write_array_ascii(const char* filename, const double *arr,
		      const int nvalues){
  FILE * stream = fopen(filename, "w");
  int i;

  for (i=0; i<nvalues; i++) {
    fprintf(stream, "%20.12E\n", arr[i]);
  }

  fclose(stream);

  return 0;
}


/* int main(){ */
/*   const char* filename = "/tmp/ */
/*   read_nblock_from_nwrite( filename, int *nnum, double *nodes, */
/* 			  int nnodes){ */
