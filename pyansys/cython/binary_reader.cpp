#include <iostream>
#include <string.h>
#include <stdio.h>
#include <fstream>
#include <exception>

using namespace std;

// #define	MEM_ZERO(where, size)	memset((where),'\0',(size))
// #define IS_ON(e, p)   ((e) & (1u << (p)))

#define	MEM_ZERO(where,size)	memset((where),'\0',(size))
#define	MEM_COPY(from,to,size)	memcpy((to),(from),(size))
#define	MEMCOPY(from,to,n_items,type) MEM_COPY((char *)(from),(char *)(to),(unsigned)(n_items)*sizeof(type))
#define IS_ON(e,p)   ((e) & (1u << (p)))


static int NbBitsOn( int iVal)
{
  static int nbbitsperchar[] =
    {0,1,1,2,1,2,2,3,1,2,2,3,2,3,3,4,1,2,2,3,2,3,3,4,2,3,3,4,
     3,4,4,5,1,2,2,3,2,3,3,4,2,3,3,4,3,4,4,5,2,3,3,4,3,4,4,5,
     3,4,4,5,4,5,5,6,1,2,2,3,2,3,3,4,2,3,3,4,3,4,4,5,2,3,3,4,
     3,4,4,5,3,4,4,5,4,5,5,6,2,3,3,4,3,4,4,5,3,4,4,5,4,5,5,6,
     3,4,4,5,4,5,5,6,4,5,5,6,5,6,6,7,1,2,2,3,2,3,3,4,2,3,3,4,
     3,4,4,5,2,3,3,4,3,4,4,5,3,4,4,5,4,5,5,6,2,3,3,4,3,4,4,5,
     3,4,4,5,4,5,5,6,3,4,4,5,4,5,5,6,4,5,5,6,5,6,6,7,2,3,3,4,
     3,4,4,5,3,4,4,5,4,5,5,6,3,4,4,5,4,5,5,6,4,5,5,6,5,6,6,7,
     3,4,4,5,4,5,5,6,4,5,5,6,5,6,6,7,4,5,5,6,5,6,6,7,5,6,6,7,6,7,7,8};
 
  unsigned char	*cval = (unsigned char *)(&iVal);
  
  return( nbbitsperchar[cval[0]] + nbbitsperchar[cval[1]] +
	  nbbitsperchar[cval[2]] + nbbitsperchar[cval[3]]);
}


// populate a node given a record using the bsparse algorithm
void populate_node_bsparse(int *buffer, int n, int *nnum, double *nodes){

  int size = *buffer++;
  int bitcod = *buffer++;
  double *tbuf = (double*)buffer;

  int iloc = -1;
  while (++iloc < size){
    if (IS_ON(bitcod, iloc)){

      // store node number
      if (iloc == 0){
        nnum[n] = *tbuf++;
      } else{  // otherwise, store node values
        nodes[n*6 + iloc - 1] = *tbuf++;
      }

    } else{  // set value to zero
      nodes[n*6 + iloc - 1] = 0;
    }
  }

  // printf("%d, %f, %f, %f, %f, %f, %f\n", nnum[n],
  // 	 nodes[n*6 + 0],
  // 	 nodes[n*6 + 1],
  // 	 nodes[n*6 + 2],
  // 	 nodes[n*6 + 3],
  // 	 nodes[n*6 + 4],
  // 	 nodes[n*6 + 5]);

}

void populate_node(double *buffer, int n, int *nnum, double *nodes){
  nnum[n] = buffer[0];

  // is it safe to unwrap?
  nodes[n*6 + 0] = buffer[1];
  nodes[n*6 + 1] = buffer[2];
  nodes[n*6 + 2] = buffer[3];
  nodes[n*6 + 3] = buffer[4];
  nodes[n*6 + 4] = buffer[5];
  nodes[n*6 + 5] = buffer[6];
}


// Read in record and determine size
// bsparse_flag true when record uses binary compression
// type_flag true when using integers
// prec_flag true when using single precision (short for int)
int read_header(ifstream* binFile, int* bsparse_flag, int* wsparse_flag,
		int* zlib_flag, int* prec_flag, int* type_flag){

  char *raw = new char[8];

  // read the first 8 bytes, includes total buffer size and flags
  // printf("preparing to read\n");
  binFile->read(raw, 8);
  int bufsize = *(int*)&raw[0];

  // bsparse flag
  *bsparse_flag = (raw[7] >> 3) & 1;
  *wsparse_flag = (raw[7] >> 4) & 1;
  *zlib_flag = (raw[7] >> 5) & 1;
  *prec_flag = (raw[7] >> 6) & 1;
  *type_flag = (raw[7] >> 7) & 1;

  return bufsize;
}


void read_nodes(const char* filename, int ptrLOC, int nrec, int *nnum, double *nodes){

  // max buf size
  char *raw = new char[68*4];
  ifstream binFile (filename, ios::in | ios::binary);
  binFile.seekg(ptrLOC*4);

  // read remainder of buffer excluding initial bytes and last bytes
  int bufsize, n;
  int bsparse_flag, wsparse_flag, zlib_flag, prec_flag, type_flag;

  for (n=0; n<nrec; n++){
    bufsize = read_header(&binFile, &bsparse_flag, &wsparse_flag,
			  &zlib_flag, &prec_flag, &type_flag);
    binFile.read(raw, 4*bufsize);
    // printf("%d, %d\n", n, bufsize);

    if (bsparse_flag){
      populate_node_bsparse((int*)raw, n, nnum, nodes);
    } else { // standard read in
      populate_node((double*)raw, n, nnum, nodes);
    }

    // skip footer
    binFile.seekg(4, ios_base::cur);
  }

  // flags
  // int i, flag;
  // for (i=0; i<8; i++){
  //   flag = (buffer[7] >> i) & 1;
  //   printf("%d, %d\n", i, flag);
  // }

}


// T GetMax (T a, T b) {
//   T result;
//   result = (a>b)? a : b;
//   return (result);
// }

template <class T>
char* ReadBsparseRecord(T *buffer, int *size){
  int *raw = (int*)buffer;
  *size = *raw++;
  int bitcod = *raw++;

  T *tbuf = (T*)raw;
  T *vec = new T[*size];

  int iloc = -1;
  while (++iloc < *size){
    if (IS_ON(bitcod, iloc)){ // store value
        vec[iloc] = *tbuf++;
    } else{  // set value to zero
      vec[iloc] = 0;
    }
  }

  // int i;
  // for (i=0; i<*size; i++){
  //   printf("%f\n", vec[i]);
  // }

  return (char*)vec;

}

char* ReadShortBsparseRecord(int *raw, int *size)
{
  *size = *raw++;
  int bitcod = *raw++;

  short *vec = new short[*size]();
  short	*tbuf = (short *)raw;
  int	iloc = -1;
  int nb = NbBitsOn(bitcod);

  if (nb%2) nb++;
  while ( ++iloc < *size)
    {
      if ( IS_ON( bitcod, iloc)){
	vec[iloc] = *tbuf++;
      }
    }

  return (char*)vec;
}


template <class T>
char* WindowedSparseBufferToVec(T *buffer, int *size){

  int iShift = sizeof(T)/sizeof(int);

  int *raw = (int*)buffer;
  *size = *raw++;
  int NWin = *raw++;

  T *vec = new T[*size];
  T *adr = vec;
  MEM_ZERO( adr, *size*sizeof(T));

  int iLoc, iLen;
  if ( NWin > 0)
  do {

    /* ===== We read the location of the new Window */
    iLoc = *raw++;	/* ===== iLoc = Where start the next window */
    // cout << "iLoc: " << iLoc << endl;

    if ( iLoc > 0)	/* ===== One isolated NonZero Value - no need to store a Window Len */
      {
	vec[iLoc] = ((T *)raw)[0];
	raw += iShift;
      }
    else		/* ===== New Window of size iLen */
      {
	T *adr = vec + (-iLoc);	/* Start of the Windows in the output vector */
	iLen = *raw++;		/* Length of the Window */
	// cout << "Length of the Window: " << iLen << endl;

	if (iLen > 0)			/* ===== Non Constant Values */
	  {
	    // cout << "Non Constant Values: " << iLen << endl;
	    MEMCOPY( (T *)raw, adr, iLen, T);
	    
	    raw += iShift*iLen;
	  }
	else /* ===== Constant Value : only one value is stored */
	  {
	    // cout << "Constant Value : only one value is stored: " << iLoc << endl;
	    iLen = - iLen;
	    T ValCst = *((T *)(raw)); raw += iShift;
	    do (*(adr++) = ValCst); while (--iLen > 0);
	  }
      }
  } while ( --NWin > 0);

  return (char*)vec;
}


// read a record and return the pointer to the array
void* read_record(const char* filename, int ptr, int* prec_flag, int* type_flag,
		  int* size, int* out_bufsize){

  int bsparse_flag, wsparse_flag, zlib_flag;

  ifstream binFile (filename, ios::in | ios::binary);
  binFile.seekg(ptr*4);
  int bufsize = read_header(&binFile, &bsparse_flag, &wsparse_flag,
			    &zlib_flag, prec_flag, type_flag);

  *size = bufsize;

  // always read record
  char *raw = new char[4*bufsize];
  binFile.read(raw, 4*bufsize);
  *out_bufsize = bufsize + 3;  // include header and footer

  if (bsparse_flag){
    // cout << "bsparse_record" << endl;
    if (*type_flag){
      if (*prec_flag){
	raw = ReadShortBsparseRecord((int*)raw, size);
	// *size /= 2;
      } else{
	raw = ReadBsparseRecord((int*)raw, size);
	// *size *= 2;
      }
    } else{  // a float/double
      if (*prec_flag){
	raw = ReadBsparseRecord((float*)raw, size);
      } else{
	raw = ReadBsparseRecord((double*)raw, size);
	// *size *= 2;
      }
    }
  } else if (wsparse_flag) {
    // cout << "windowed_record" << endl;
    if (*type_flag){
      if (*prec_flag){
	raw = WindowedSparseBufferToVec((short*)raw, size);
      } else{
	raw = WindowedSparseBufferToVec((int*)raw, size);
	// *size *= 2;
      }
    } else{  // a float/double
      if (*prec_flag){
	raw = WindowedSparseBufferToVec((float*)raw, size);
      } else{
	raw = WindowedSparseBufferToVec((double*)raw, size);
	// *size *= 2;
      }
    }
    
  }
  

  return raw;
}

/** 
 *! This function decrypts and expands a sparse vector
 * 
 * \param kbfint		[IN]  1 if the [31] flag is true, 0 otherwize
 * \param precision		[IN]  1 if the [30] flag is true, 0 otherwize
 * \param bsparse		[IN]  1 if the [27] flag is true, 0 otherwize
 * \param Buffer4		[IN]  The sparse buffer to be expanded
 * \param kL			[OUT] The size of the expanded record
 * \param ivect4		[OUT] The expanded record
 */


