#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// To Optimize
// - read in blocks rather than intergers

// To add
// - add big endianness compatability


__inline int read_int(FILE* ptr){
    int n;
    unsigned char c[4];

    // Read and convert assuming small endian
    fread(c, sizeof(int), 1, ptr);
    n = (int)c[0] + ((int)c[1] << 8) + ((int)c[2]<<16) + ((int)c[3]<<24);

    return n;
}

__inline double read_double(FILE* ptr){
    double val;
    char str[8];

    fread(str, sizeof(double), 1, ptr);
    memcpy(&val, str, sizeof(double));
    return val;
}

// returns an interger from a position along a char array
__inline int read_int_raw(char **c, int e){
    // Assuming small endian
    int n;
    memcpy(&n, (*c) + e, sizeof(int));
    return n;
}

// returns a double from a position along a char array
__inline double read_double_raw(char **c, int e){
    double val;
    memcpy(&val, (*c) + e, sizeof(double));
    return val;
}


// index sorting
int *array;
int cmp(const void *a, const void *b){
    int ia = *(int *)a;
    int ib = *(int *)b;
    return array[ia] < array[ib] ? -1 : array[ia] > array[ib];
}

// Make index array
void make_index(int **idx, int size){
    int i;
    *idx = (int*)malloc(size * sizeof(int));

    for(i=0; i<size; i++){
        (*idx)[i] = i;
    }
}

// populate isfree array
int pop_isfree(FILE* ptr, int ptrDOF, int nNodes, int **isfree){
    int val, i;
    int nfree = 0;

    for (i = 0; i<nNodes*3; i += 1){
        val = read_int(ptr);

        if (val > 0){
            (*isfree)[i] = 1;
            ++nfree;
        }
        else{
            (*isfree)[i] = 0;
        }
    }

    return nfree;
}


//=============================================================================
// Read an array from fortran file
//=============================================================================
int read_array(int **rows, int **cols, double **data, int *rref, int *cref,
               int *isfree, int nterm, int neqn, FILE* ptr, int fileloc,
               int *skipped){
    // Max array size
    int i, j, val;
    int e = 0;
    int nitems, row, col;
    double vald;
    int c = 0;
    int d = 0;
    int inval = 0;
    int val2, vald2;

    // Read entire matrix to memory
    int nread = neqn*24 + nterm*12;
    char *raw = (char*)malloc(nread*sizeof(char));
    fseek(ptr, (fileloc)*4, SEEK_SET);
    fread(raw, sizeof(char), nread, ptr);

    for (i = 0; i<neqn; ++i){
        nitems = read_int_raw(&raw, e); e += 4;

        if (isfree[i]){
            e += 4;
            col = cref[i];
            
            // Read rows and assemble symmetric matrix (skip last item)
                for (j = 0; j < nitems - 1; j += 1){
                    val = read_int_raw(&raw, e); e += 4;
                    row = rref[val];
        
                    // check if this value refers to a invalid node
                    if (row == -1){
                        skipped[j] = 1;
                        ++inval;
                        continue;
                    }
                    else{
                        skipped[j] = 0;
                    }

                    // Write entire matrix
                    (*rows)[c] = row;
                    (*cols)[c] = col;
                    ++c;
                    
                    (*rows)[c] = col;
                    (*cols)[c] = row;
                    ++c;
                }
        
                // Last item is always the diagional, don't bother reading
                (*rows)[c] = col;
                (*cols)[c] = col;
                ++c;
        
                // Read data
                e += 16;
                for (j = 0; j < nitems - 1; ++j){
                    // Skip if this value has not been stored
                    if (skipped[j]){
                        e += 8;
                        continue;
                    }
//                    vald2 = read_double(ptr);
                    vald = read_double_raw(&raw, e); e += 8;
                    (*data)[d] = vald;
                    ++d;
                    // writing symmetric part
                    (*data)[d] = vald;
                    ++d;
                }
        
                // Last item belongs to diagional
                vald = read_double_raw(&raw, e); e += 8;

                (*data)[d] = vald;
                d += 1;
                fseek(ptr, 4, SEEK_CUR);
                e += 4;
        }
        // Otherwise, skip this section
        else{
            fseek(ptr, (3*nitems + 5)*4, SEEK_CUR);
            e += (3*nitems + 5)*4;
        }

    }
    
    // remove loaded file from memory
    free(raw);

    // Return number of entries in array
    return c;
}


// Interface for Cython
int return_fheader(char *filename, int *fheader){
    int i;
    FILE *ptr;
    // open file
    ptr = fopen(filename, "rb");
	if (ptr == NULL){
		printf("File %s does not exist.  Terminating\n", filename);
            return 1;
    }

    // Read header and populate fheader array
    fseek(ptr, 104*4, SEEK_SET);
    for (i=0; i<101; ++i){
        fheader[i] = read_int(ptr);
        }

    // Success
    fclose(ptr);
    return 0;
}


// Populate external arrays
void read_full(int *numdat, int *nref, int *dref, int *krows, int *kcols, 
               double *kdata, int *mrows, int *mcols, double *mdata,
               int *fheader, char *filename, int *sidx, int sort){

    FILE *ptr;

    // counters and temp variables
    int i, j, c, val, nfree;

    // header items
    int neqn, wfmax, ntermK, ptrSTF, ptrMAS, nNodes, ntermM, ptrDOF;

    // Arrays and mass/stiffness array items
    int *skipped, *isfree, *neqv_dof, *index, *cref, *rref;
    int kentry, mentry;

    // Open result file
    ptr = fopen(filename, "rb");

    // Get values from header files
    // Read Table Matches values from ansys interface guide
    neqn = fheader[2];    //  Number of equations
    wfmax = fheader[6];   // Maximum number of rows in an entry
    ntermK = fheader[9];  // number of terms in stiffness matrix
    ptrSTF = fheader[19]; // Location of stiffness matrix (item 19)
    ptrMAS = fheader[27]; // Location in file to mass matrix
    nNodes = fheader[33]; // Number of nodes considered by assembly
    ntermM = fheader[34]; // number of terms in mass matrix
    ptrDOF = fheader[36]; // pointer to DOF info

    // Tracks if an entry has been stored
    skipped = (int*)malloc(wfmax*sizeof(int)); 

    //=========================================================================
    // Read nodal constraints
    //=========================================================================
    fseek(ptr, (ptrDOF + 5 + nNodes)*4, SEEK_SET); // skip DOF at each node
    isfree = (int*)malloc(nNodes*3*sizeof(int)); // change 3 to numdof
    nfree = pop_isfree(ptr, ptrDOF, nNodes, &isfree);

    //=============================================================================
    // Populate reference arrays
    //=============================================================================
    //TODO: change 3 to numdof
    neqv_dof = (int*)malloc(nNodes*3*sizeof(int));
    fseek(ptr, (212 + 2)*4, SEEK_SET);
    c = 0;
    for (i = 0; i<nNodes; i += 1){
        val = read_int(ptr);
        for (j = 0; j < 3; j += 1){
            if (isfree[i*3 + j]){
                neqv_dof[c] = val*3 + j;
                nref[c] = val;
                dref[c] = j;
                ++c;
            }
        }
    }

    // Sort nodes and generate indices
    make_index(&index, nfree);

    // Resort index array based on the degree of freedom 
    if (sort){
        array = neqv_dof;
        qsort(index, nfree, sizeof(*index), cmp);
    }
    free(neqv_dof);

    // column and row reference arrays
    cref = (int*)malloc(neqn * sizeof(int));
    rref = (int*)malloc((neqn + 1)* sizeof(int));
    c = 0;
    for (i = 0; i<neqn; ++i){
        if (isfree[i]){
            val = index[index[c]]; // zero based indexing
            cref[i] = val;
            rref[i + 1] = val;
            ++c;
        }
        else{
            cref[i] = -1;
            rref[i + 1] = -1;
        }
    }

    //populate sorting array
    if (sort){
        for (i=0; i<nfree; ++i){
            sidx[i] = index[i];
        }
    }

    free(index);

    // Read stiffness matrix into memory
    kentry = read_array(&krows, &kcols, &kdata, rref, cref, isfree, ntermK, 
                            neqn, ptr, ptrSTF, skipped);

    // Read mass matrix
    mentry = read_array(&mrows, &mcols, &mdata, rref, cref, isfree, ntermM, 
                            neqn, ptr, ptrMAS, skipped);

    // Populate the array sizes array
    numdat[0] = nfree;
    numdat[1] = kentry;
    numdat[2] = mentry;

    // close full file
    fclose(ptr);

}

