#include <stdio.h>
#include <stdlib.h>
#include <string.h>


//=============================================================================
// Fast string to interger convert to ANSYS formatted intergers 
//=============================================================================
__inline int fast_atoi(char * raw, int intsz, int *i){
    int val;
    int c;

    val = 0;
    for (c=0; c<intsz; ++c){
        ++*(i);

        // Seek throug white space
        if (raw[*(i)] == ' ') continue;

        val = val*10 + (raw[*(i)] - '0');
    }

    // Pass counter position back to file position counter
//    *(i) = c;

    return val;
}

__inline int fast_atoi2(char * raw, int intsz){

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
// Checks for negative
//=============================================================================
__inline int checkneg(char * raw, int intsz, int *i){
    int c;
    int found = 0;
    for (c=0; c<intsz; ++c){
        // Seek throug white space
        if (raw[*(i)] == '-'){
            found = 1;
        }
        ++*(i);
    }

    return found;
}

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
    nnum[i] = fast_atoi2(raw, intsz[0]);
    raw += intsz[0];
    raw += intsz[1];
    raw += intsz[2];
    
    for (j=0; j<6; j++){
      if (raw[0] == '\r' || raw[0] == '\n'){
	break;
      }
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


//=============================================================================
// Reads EBLOCK from ANSYS.  Raw string is from Python reader and file is
// positioned at the start of the data of EBLOCK
//=============================================================================
int read_eblock(char *raw, int *mtype, int *etype, int *e_rcon, int *sec_id,
                int *elemnum, int *elem, int nelem, int intsz, int *j,
                int EOL){

    int i, n, c, nnode, val, g;
    n = *(j) - 1;

    // Loop through elements
    for (i=0; i<nelem; ++i){

        // Check if end of line
        while (raw[n + 1] == '\r' || raw[n + 1] == '\n' ){
	  ++n;
	}

        // Check if at end of the block
        if (checkneg(raw, intsz, &n)){
            break;
        }
        
        // Field 1: Read material type
        n -= intsz; // since checkneg advances by intsz
        mtype[i] = fast_atoi(raw, intsz, &n);
        
        // Field 2: Read element type
        etype[i] = fast_atoi(raw, intsz, &n);
    
        // Field 3: Read real constant
        e_rcon[i] = fast_atoi(raw, intsz, &n);
        
        // Field 4: The section ID attribute (beam section) number.
        sec_id[i] = fast_atoi(raw, intsz, &n);
        
        // Skip Fields 5 - 8 and store 9, the number of nodes    
        n += 4*intsz;
        nnode = fast_atoi(raw, intsz, &n);

        // Skip Field 10 and read Field 11: Element number
        n += intsz;
        elemnum[i] = fast_atoi(raw, intsz, &n);

	/* printf("%d\n", elemnum[i]); */
            
        // Read nodes in element
        c = 0;
        while (c < nnode){
            // Check if end of line
            while (raw[n + 1] == '\r' || raw[n + 1] == '\n' ) ++n;

            // Parse node (same as function fast_atoi)
            val = 0;
            for (g=0; g<intsz; ++g){
                ++n;
                if (raw[n] == ' ') continue;  // Seek through white space
                val = val*10 + (raw[n] - '0');
            }

	    /* if (val < 0){ */
	    /*     printf("File position: %d\n", n); */
	    /*     printf("Invalid node number on element number %d\n", elemnum[i]); */
	    /*     perror(""); */
	    /* 	return 0; */
	    /* } */

	    /* printf("\t%d", val); */
            elem[20*i + c] = val;
            ++c;

        }
            
        // Set remaining element numbers to -1
        for (c; c<20; ++c){
                elem[20*i + c] = -1;
        }

    }

    // update file position
    *(j) = n;

    // return file position
    return i;


}
