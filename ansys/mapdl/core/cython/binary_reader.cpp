#include <iostream>
#include <string.h>
#include <stdio.h>
#include <fstream>
#include <exception>

// necessary for ubuntu build on azure
#ifdef __linux__
  #include <stdint.h>
#endif

using namespace std;

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


// Read in record and determine size
// bsparse_flag true when record uses binary compression
// type_flag true when using integers
// prec_flag true when using single precision (short for int)
int read_header(ifstream* binFile, int* bsparse_flag, int* wsparse_flag,
		int* zlib_flag, int* prec_flag, int* type_flag){

  char *raw = new char[8];

  // read the first 8 bytes, includes total buffer size and flags
  binFile->read(raw, 8);
  int bufsize = *(int*)&raw[0];

  // bsparse flag
  *bsparse_flag = (raw[7] >> 3) & 1;
  *wsparse_flag = (raw[7] >> 4) & 1;
  *zlib_flag = (raw[7] >> 5) & 1;
  *prec_flag = (raw[7] >> 6) & 1;
  *type_flag = (raw[7] >> 7) & 1;

  delete[] raw;
  return bufsize;
}


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
  return (char*)vec;
}


// read binary sparse record and store in a vector
template <class T>
void ReadBsparseRecordToVec(int *raw, int *size, T*vec){
  *size = *raw++;
  int bitcod = *raw++;

  T *tbuf = (T*)raw;

  int iloc = -1;
  while (++iloc < *size){
    if (IS_ON(bitcod, iloc)){ // store value
        vec[iloc] = *tbuf++;
    } else{  // set value to zero
      vec[iloc] = 0;
    }
  }
}



char* ReadShortBsparseRecord(int *raw, int *size){
  *size = *raw++;
  int bitcod = *raw++;

  short *vec = new short[*size]();
  short	*tbuf = (short *)raw;
  int iloc = -1;
  int nb = NbBitsOn(bitcod);

  if (nb%2) nb++;
  while ( ++iloc < *size)
    {
      if ( IS_ON( bitcod, iloc)){
	vec[iloc] = *tbuf++;
      } else{
	vec[iloc] = 0;
      }
    }

  return (char*)vec;
}


void ReadShortBsparseRecordToVec(int *raw, int *size, short *vec)
{
  *size = *raw++;
  int bitcod = *raw++;

  short	*tbuf = (short *)raw;
  int	iloc = -1;
  int nb = NbBitsOn(bitcod);

  if (nb%2) nb++;
  while ( ++iloc < *size)
    {
      if ( IS_ON( bitcod, iloc)){
	vec[iloc] = *tbuf++;
      } else {
	vec[iloc] = 0;
      }
    }

}


template <class T>
char* ReadWindowedSparseBuffer(T *buffer, int *size){

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
    if ( iLoc > 0)	/* ===== One isolated NonZero Value - no need to store a Window Len */
      {
	vec[iLoc] = ((T *)raw)[0];
	raw += iShift;
      }
    else		/* ===== New Window of size iLen */
      {
	T *adr = vec + (-iLoc);	/* Start of the Windows in the output vector */
	iLen = *raw++;		/* Length of the Window */

	if (iLen > 0)			/* ===== Non Constant Values */
	  {
	    MEMCOPY( (T *)raw, adr, iLen, T);
	    
	    raw += iShift*iLen;
	  }
	else /* ===== Constant Value : only one value is stored */
	  {
	    iLen = - iLen;
	    T ValCst = *((T *)(raw)); raw += iShift;
	    do (*(adr++) = ValCst); while (--iLen > 0);
	  }
      }
  } while ( --NWin > 0);

  return (char*)vec;
}


char* ReadWindowedSparseBufferDouble(int *raw, int *size, double *vec){
  int iShift = sizeof(double)/sizeof(int);
  *size = *raw++;
  int NWin = *raw++;

  double *adr = vec;
  MEM_ZERO( adr, *size*sizeof(double));

  int iLoc, iLen;
  if ( NWin > 0)
  do {

    /* ===== We read the location of the new Window */
    iLoc = *raw++;	/* ===== iLoc = Where start the next window */

    if ( iLoc > 0)	/* ===== One isolated NonZero Value - no need to store a Window Len */
      {
	vec[iLoc] = ((double *)raw)[0];
	raw += iShift;
      }
    else		/* ===== New Window of size iLen */
      {
	double *adr = vec + (-iLoc);	/* Start of the Windows in the output vector */
	iLen = *raw++;		/* Length of the Window */

	if (iLen > 0)			/* ===== Non Constant Values */
	  {
	    MEMCOPY( (double *)raw, adr, iLen, double);
	    
	    raw += iShift*iLen;
	  }
	else /* ===== Constant Value : only one value is stored */
	  {
	    iLen = - iLen;
	    double ValCst = *((double *)(raw)); raw += iShift;
	    do (*(adr++) = ValCst); while (--iLen > 0);
	  }
      }
  } while ( --NWin > 0);

  return (char*)vec;
}


char* ReadWindowedSparseBufferFloat(int *raw, int *size, float *vec){
  int iShift = sizeof(float)/sizeof(int);
  *size = *raw++;
  int NWin = *raw++;

  float *adr = vec;
  MEM_ZERO( adr, *size*sizeof(float));

  int iLoc, iLen;
  if ( NWin > 0)
  do {

    /* ===== We read the location of the new Window */
    iLoc = *raw++;	/* ===== iLoc = Where start the next window */

    if ( iLoc > 0)	/* ===== One isolated NonZero Value - no need to store a Window Len */
      {
	vec[iLoc] = ((float *)raw)[0];
	raw += iShift;
      }
    else		/* ===== New Window of size iLen */
      {
	float *adr = vec + (-iLoc);	/* Start of the Windows in the output vector */
	iLen = *raw++;		/* Length of the Window */

	if (iLen > 0)			/* ===== Non Constant Values */
	  {
	    MEMCOPY( (float *)raw, adr, iLen, float);
	    
	    raw += iShift*iLen;
	  }
	else /* ===== Constant Value : only one value is stored */
	  {
	    iLen = - iLen;
	    float ValCst = *((float *)(raw)); raw += iShift;
	    do (*(adr++) = ValCst); while (--iLen > 0);
	  }
      }
  } while ( --NWin > 0);

  return (char*)vec;
}


char* ReadWindowedSparseBufferInt(int *raw, int *size, int *vec){

  int iShift = sizeof(int)/sizeof(int);
  *size = *raw++;
  int NWin = *raw++;

  int *adr = vec;
  MEM_ZERO( adr, *size*sizeof(int));

  int iLoc, iLen;
  if ( NWin > 0)
  do {

    /* ===== We read the location of the new Window */
    iLoc = *raw++;	/* ===== iLoc = Where start the next window */

    if ( iLoc > 0)	/* ===== One isolated NonZero Value - no need to store a Window Len */
      {
	vec[iLoc] = ((int *)raw)[0];
	raw += iShift;
      }
    else		/* ===== New Window of size iLen */
      {
	int *adr = vec + (-iLoc);	/* Start of the Windows in the output vector */
	iLen = *raw++;		/* Length of the Window */

	if (iLen > 0)			/* ===== Non Constant Values */
	  {
	    MEMCOPY( (int *)raw, adr, iLen, int);
	    
	    raw += iShift*iLen;
	  }
	else /* ===== Constant Value : only one value is stored */
	  {
	    iLen = - iLen;
	    int ValCst = *((int *)(raw)); raw += iShift;
	    do (*(adr++) = ValCst); while (--iLen > 0);
	  }
      }
  } while ( --NWin > 0);

  return (char*)vec;
}


char* ReadWindowedSparseBufferShort(int *raw, int *size, short *vec){

  int iShift = sizeof(short)/sizeof(int);

  *size = *raw++;
  int NWin = *raw++;

  short *adr = vec;
  MEM_ZERO( adr, *size*sizeof(short));

  int iLoc, iLen;
  if ( NWin > 0)
  do {

    /* ===== We read the location of the new Window */
    iLoc = *raw++;	/* ===== iLoc = Where start the next window */

    if ( iLoc > 0)	/* ===== One isolated NonZero Value - no need to store a Window Len */
      {
	vec[iLoc] = ((short *)raw)[0];
	raw += iShift;
      }
    else		/* ===== New Window of size iLen */
      {
	short *adr = vec + (-iLoc);	/* Start of the Windows in the output vector */
	iLen = *raw++;		/* Length of the Window */

	if (iLen > 0)			/* ===== Non Constant Values */
	  {
	    MEMCOPY( (short *)raw, adr, iLen, short);
	    
	    raw += iShift*iLen;
	  }
	else /* ===== Constant Value : only one value is stored */
	  {
	    iLen = - iLen;
	    short ValCst = *((short *)(raw)); raw += iShift;
	    do (*(adr++) = ValCst); while (--iLen > 0);
	  }
      }
  } while ( --NWin > 0);

  return (char*)vec;
}


// read a record and return the pointer to the array
void* read_record(const char* filename, int64_t ptr, int* prec_flag, int* type_flag,
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
    if (*type_flag){
      if (*prec_flag){
	raw = ReadShortBsparseRecord((int*)raw, size);
      } else{
	raw = ReadBsparseRecord((int*)raw, size);
      }
    } else{  // a float/double
      if (*prec_flag){
	raw = ReadBsparseRecord((float*)raw, size);
      } else{
	raw = ReadBsparseRecord((double*)raw, size);
      }
    }
  } else if (wsparse_flag) {
    if (*type_flag){
      if (*prec_flag){
	raw = ReadWindowedSparseBuffer((short*)raw, size);
      } else{
	raw = ReadWindowedSparseBuffer((int*)raw, size);
      }
    } else{  // a float/double
      if (*prec_flag){
	raw = ReadWindowedSparseBuffer((float*)raw, size);
      } else{
	raw = ReadWindowedSparseBuffer((double*)raw, size);
      }
    }
    
  }
  

  return raw;
}

// populate arr with a record
// This function differs from read_record as it must be supplied with ``arr``, which must be sized properly to support the data coming from the file.
void read_record_stream(ifstream* file, int64_t loc, void* arr, int* prec_flag,
			 int* type_flag, int* size){

  // seek to data location if supplied with a pointer
  if (loc >= 0){
    file->seekg(loc*4);
  }

  int bsparse_flag, wsparse_flag, zlib_flag;
  int bufsize = read_header(file, &bsparse_flag, &wsparse_flag,
			    &zlib_flag, prec_flag, type_flag);
  *size = bufsize;

  // always read record
  if (bufsize <= 0){
    return;
  }

  char *raw = new char[4*bufsize];

  if (bsparse_flag){
    // write to temporary record
    file->read(raw, 4*bufsize);
    
     if (*type_flag){
      if (*prec_flag){
  	ReadShortBsparseRecordToVec((int*)raw, size, (short*)arr);
      } else{
  	ReadBsparseRecordToVec((int*)raw, size, (int*)arr);
      }
    } else{  // a float or a double
      if (*prec_flag){
  	ReadBsparseRecordToVec((int*)raw, size, (float*)arr);
      } else{
  	ReadBsparseRecordToVec((int*)raw, size, (double*)arr);
      }
    }

  } else if (wsparse_flag) {
    file->read(raw, 4*bufsize);
    if (*type_flag){
      if (*prec_flag){
  	ReadWindowedSparseBufferShort((int*)raw, size, (short*)arr);
      } else{
  	ReadWindowedSparseBufferInt((int*)raw, size, (int*)arr);
      }
    } else{  // a float/double
      if (*prec_flag){
  	ReadWindowedSparseBufferFloat((int*)raw, size, (float*)arr);
      } else{
  	ReadWindowedSparseBufferDouble((int*)raw, size, (double*)arr);
      }
    }

  } else {// write directly to the array
    file->read((char*)arr, 4*bufsize);
  }    

  delete[] raw;
  
}


void read_nodes(const char* filename, int64_t ptrLOC, int nrec, int *nnum,
		double *nodes){

  // max buf size
  char *raw = new char[68*4];
  ifstream binFile (filename, ios::in | ios::binary);
  binFile.seekg(ptrLOC*4);

  // read remainder of buffer excluding initial bytes and last bytes
  int bufsize, n;
  int prec_flag, type_flag;

  for (n=0; n<nrec; n++){
    read_record_stream(&binFile, -1,
		       raw, &prec_flag, &type_flag, &bufsize);
    binFile.seekg(4, ios_base::cur);  // skip footer

    nnum[n] = *((double*) raw);
    nodes[n*6 + 0] = *((double*) &raw[8]);
    nodes[n*6 + 1] = *((double*) &raw[16]);
    nodes[n*6 + 2] = *((double*) &raw[24]);
    nodes[n*6 + 3] = *((double*) &raw[32]);
    nodes[n*6 + 4] = *((double*) &raw[40]);
    nodes[n*6 + 5] = *((double*) &raw[48]);    

  }

  delete[] raw;

}
