#include <stdio.h>
#include <stdlib.h>
#include <string.h>
//#include <unistd.h>
//#include <stdbool.h>

// To Optimize
// - read in blocks rather than intergers
// - convert memcpy to double conversion for read_double

// To fix
// - add big endianness compatability

// reads int from current position in file

//int e;

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

//=============================================================================
//// Read an array from fotran file (without loading to memory)
//=============================================================================
//int read_array(int **rows, int **cols, double **data, int *rref, int *cref,
//               bool *isfree, int nterm, int neqn, FILE* ptr, int fileloc,
//               bool *skipped){
//    // Max array size
//    int arrsz = 2*nterm - neqn;
//    *rows = (int*)malloc(arrsz * sizeof(int));
//    *cols = (int*)malloc(arrsz * sizeof(int));
//    *data = (double*)malloc(arrsz * sizeof(double));
//
//    int i, j;
//
//
//    int nitems, row, col;
//    double vald;
//    int c = 0;
//    int d = 0;
//    int inval = 0;
//    fseek(ptr, (fileloc)*4, SEEK_SET);
//    for (i = 0; i<neqn; ++i){
//        nitems = read_int(ptr);
//
//        if (isfree[i]){
//            fseek(ptr, 4, SEEK_CUR);
//            col = cref[i];
//            
//            // Read rows and assemble symmetric matrix (skip last item)
//                for (j = 0; j < nitems - 1; j += 1){
//                    row = rref[read_int(ptr)];
//        
//                    // check if this value refers to a invalid node
////                    skipped[j] = 0;
//                    if (row == -1){
//                        skipped[j] = 1;
//                        ++inval;
//                        continue;
//                    }
//                    else{
//                        skipped[j] = 0;
//                    }
//
//                    // Write only the lower half of the matrix
////                    if (row > col){
////                        (*rows)[c] = row;
////                        (*cols)[c] = col;
////                    }
////                    else{                   
////                        (*rows)[c] = col;
////                        (*cols)[c] = row;
////                    }
////                    ++c;
//
//                    // Write entire matrix
//                    (*rows)[c] = row;
//                    (*cols)[c] = col;
//                    ++c;
//                    
//                    (*rows)[c] = col;
//                    (*cols)[c] = row;
//                    ++c;
//                }
//        
//                // Last item is always the diagional, don't bother reading
//                (*rows)[c] = col;
//                (*cols)[c] = col;
//                ++c;
//        
//                // Read data
//                fseek(ptr, 16, SEEK_CUR);
//                for (j = 0; j < nitems - 1; ++j){
//                    // Skip if this value has not been stored
//                    if (skipped[j]){
//                        fseek(ptr, 8, SEEK_CUR);
//                        continue;
//                    }
//                    vald = read_double(ptr);
//                    (*data)[d] = vald;
//                    ++d;
//                    // writing symmetric part
//                    (*data)[d] = vald;
//                    ++d;
//                }
//        
//                // Last item belongs to diagional
//                vald = read_double(ptr);
//                (*data)[d] = vald;
//                d += 1;
//                fseek(ptr, 4, SEEK_CUR);
//        }
//        // Otherwise, skip this section
//        else{
//            fseek(ptr, (3*nitems + 5)*4, SEEK_CUR);
//        }
//
//    }
//
//    // Return number of entries in array
//    printf("%d\n", fileloc*4);
//    printf("%lu\n", ftell(ptr));
//    return c;
//}


//=============================================================================
// for standalone application
//=============================================================================
int main( int argc, char **argv ){

    FILE *ptr, *kfile, *mfile;

    // Counters and temporary variables
    int i, j, c, val, nfree;

    // header items
    int fheader[101];
    int neqn, wfmax, ntermK, ptrSTF, ptrMAS, lenbac, nNodes, ntermM, ptrDOF;

    // arrays
    int *skipped, *isfree;
    int *nref, *dref, *cref, *rref, *neqv_dof, *index;

    // for stiffness data
    int kentry, mentry, arrsz;
    int *mrows, *mcols, *krows, *kcols;
    double *mdata, *kdata;

    // Parse user inputs and open file
    if (argc == 1){
        printf("No file selected by user.  Defaulting to file.full\n");

        ptr = fopen("file.full", "rb");
		 if (ptr == NULL){
            printf("File file.full does not exist.  Terminating\n");
            return 1;
        }


    }
	// Otherwise, try to open custom user file
	else{

        ptr = fopen(argv[1], "rb");
		if (ptr == NULL){
			printf("File %s does not exist.  Terminating\n", argv[1]);
            return 1;
        }
    }

    //=========================================================================
    // Parse header     
    //=========================================================================
    // Read header.  Reading extra interger in the beginning to line up with
    // ansys interface manual
    fseek(ptr, 104*4, SEEK_SET);
    
    for (i=0; i<101; ++i){
        fheader[i] = read_int(ptr);
    }

    // Check if symbolic assembled
    if (fheader[1] != -4){
        printf("Can only read symbolically assembled file.  Terminating");
        return 1;
    }


    // Check if lumped (item 11)
    if (fheader[11]){
        printf("Unable to read a lumped mass matrix.  Terminating.\n");
        return 1;
    }

    // Check if unsymmetric (item 14)
    if (fheader[14]){
        printf("Unable to read an unsymmetric mass/stiffness matrix.  Terminating.\n");
        return 1;
    }

    neqn = fheader[2]; //  Number of equations (Item 2)
    wfmax = fheader[6]; // Maximum number of rows in an entry (item 6)
//    lenbac = fheader[7]; // Number of nodes // (item 7)
    ntermK = fheader[9]; // number of terms in stiffness matrix (item 9)
    ptrSTF = fheader[19]; // Location of stiffness matrix (item 19)
    ptrMAS = fheader[27]; // Location in file to mass matrix (item 27)
    nNodes = fheader[33]; // Number of nodes considered by assembly (item 33)
    ntermM = fheader[34]; // number of terms in mass matrix (item 34)
    ptrDOF = fheader[36]; // pointer to DOF info (item 36)

    // Generate skipped array
    skipped = (int*)malloc(wfmax*sizeof(int)); 

    //=========================================================================
    // Read nodal constraints
    //=========================================================================
    fseek(ptr, (ptrDOF + 5 + nNodes)*4, SEEK_SET); // skip DOF at each node
    isfree = (int*)malloc(nNodes*3*sizeof(int)); // change 3 to numdof
    nfree = pop_isfree(ptr, ptrDOF, nNodes, &isfree);

    // Populate dof nodal equivalance array and create indices to active DOF
    // and original node numbering
    nref = (int*)malloc(nNodes*3*sizeof(int));
    dref = (int*)malloc(nNodes*3*sizeof(int));

    // column and row reference arrays
    cref = (int*)malloc(neqn * sizeof(int));
    rref = (int*)malloc((neqn + 1)* sizeof(int));
    
    // populate reference arrays
    neqv_dof = (int*)malloc(nNodes*3*sizeof(int)); // change 3 to numdof
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

    // not sorting right now
//    array = neqv_dof;
//    qsort(index, nfree, sizeof(*index), cmp);
    free(neqv_dof);

    c = 0;
    for (i = 0; i<neqn; ++i){
        if (isfree[i]){
            val = index[index[c]] + 1; // adding +1 here for one based indexing
            cref[i] = val;
            rref[i + 1] = val;
            ++c;
        }
        else{
            cref[i] = -1;
            rref[i + 1] = -1;
        }
    }
    free(index);


    ////////////////////////
    // Read stiffness matrix
    ////////////////////////
    arrsz = 2*ntermK - neqn;
    krows = (int*)malloc(arrsz * sizeof(int));
    kcols = (int*)malloc(arrsz * sizeof(int));
    kdata = (double*)malloc(arrsz * sizeof(double));
    kentry = read_array(&krows, &kcols, &kdata, rref, cref, isfree, ntermK, 
                            neqn, ptr, ptrSTF, skipped);

    //=========================================================================
    // Write stiffness data
    //=========================================================================
    kfile = fopen("k.bin", "wb");
    fwrite(&kentry, sizeof(int), 1, kfile);       // number of entries
    fwrite(&nfree, sizeof(int), 1, kfile);        // sparse matrix dim (n x n)
    fwrite(krows, sizeof(int), kentry, kfile);
    fwrite(kcols, sizeof(int), kentry, kfile);
    fwrite(kdata, sizeof(double), kentry, kfile);

    // Write indices of original nodes and DOF in ANSYS
    fwrite(nref, sizeof(int), nfree, kfile);
    fwrite(dref, sizeof(int), nfree, kfile);

    fclose(kfile);

    // Free items associated with stiffness file only
    free(krows);
    free(kcols);
    free(kdata);
    free(nref);
    free(dref);

    ////////////////////////
    // Read mass matrix
    ////////////////////////
    arrsz = 2*ntermM - neqn;
    mrows = (int*)malloc(arrsz * sizeof(int));
    mcols = (int*)malloc(arrsz * sizeof(int));
    mdata = (double*)malloc(arrsz * sizeof(double));
    mentry = read_array(&mrows, &mcols, &mdata, rref, cref, isfree, ntermM, 
                        neqn, ptr, ptrMAS, skipped);

    //=========================================================================
    // Write mass data
    //=========================================================================
    mfile = fopen("m.bin", "wb");
    fwrite(&mentry, sizeof(int), 1, mfile);
    fwrite(&nfree, sizeof(int), 1, mfile);
    fwrite(mrows, sizeof(int), mentry, mfile);
    fwrite(mcols, sizeof(int), mentry, mfile);
    fwrite(mdata, sizeof(double), mentry, mfile);
    fclose(mfile);

    // Free memory
    free(mrows);
    free(mcols);
    free(mdata);

    free(skipped);
    free(isfree);
    free(cref);
    free(rref);

    // close full file
    fclose(ptr);
    return 0;
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


// Populate arrays from matlab
void read_full(int *numdat, int *nref, int *dref, int *krows, int *kcols, 
               double *kdata, int *mrows, int *mcols, double *mdata,
               int *fheader, char *filename){

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
    neqv_dof = (int*)malloc(nNodes*3*sizeof(int)); // change 3 to numdof
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

    // Not sorting right now
    // array = neqv_dof;
    // qsort(index, nfree, sizeof(*index), cmp);
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




