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

__inline int fast_atoi2(char * raw, int intsz, int *i){
    int val;
    int c;

    val = 0;
    for (c=0; c<intsz; ++c){
        // Seek throug white space
        if (raw[*(i)] == ' '){
            ++*(i);
            continue;
        }

        val = val*10 + (raw[*(i)] - '0');
        ++*(i);
    }

    // Pass counter position back to file position counter
//    *(i) = c;

    return val;
}


__inline int verbose_fast_atoi(char * raw, int intsz, int *i){
    int val;
    int c;

    val = 0;
    for (c=0; c<intsz; ++c){
        ++*(i);
        printf("%c", raw[*(i)]);

        // Seek throug white space
        if (raw[*(i)] == ' ') continue;

        val = val*10 + (raw[*(i)] - '0');
    }

    // Pass counter position back to file position counter
//    *(i) = c;

    return val;
}




__inline int verbose_fast_atoi2(char * raw, int intsz, int *i){
    int val;
    int c;

    val = 0;
    for (c=0; c<intsz; ++c){
        printf("%c", raw[*(i)]);
        // Seek throug white space
        if (raw[*(i)] == ' '){
            ++*(i);
            continue;
        }

        val = val*10 + (raw[*(i)] - '0');
        ++*(i);
    }

    // Pass counter position back to file position counter
//    *(i) = c;

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

__inline int verbose_checkneg(char * raw, int intsz, int *i){
    int c;
    int found = 0;
    for (c=0; c<intsz; ++c){
        printf("%c", raw[*(i)]);
        // Seek throug white space
        if (raw[*(i)] == '-'){
            found = 1;
        }
        ++*(i);
    }

    return found;
}




void main(){
    //
}


//=============================================================================
// Fast string to flot converter for ANSYS formatted floats
//=============================================================================
__inline double fast_atof(char *raw, int fltsz, int*i){

    int ivalue, j, nread;
    double dvalue, sign, scale, pow;
    char tempstr[100];

    int c = *(i);
    *(i) += fltsz;

    //init value
    dvalue = 1.0;

    // check sign
    if (raw[c] == '-') {
        sign = -1.0;
    }
    else{
        sign = 1.0;
    }

    // read first interger
    ++c;            
    dvalue *= raw[c] - '0';

    // next is always a '.', skip it
    ++c;

    nread = fltsz - 7; // sign, first int, point, xxx, scinot (4)
    pow = 0.1;
    for (j=0; j<nread; ++j){
        ++c;
        dvalue += (raw[c] - '0')*pow;
        pow *= 0.1;

    }

    // apply sign
    dvalue *= sign;

    // Read exponent
    // Skip the E
    ++c; 

    // store sign of exponent
    ++c;
    tempstr[0] = raw[c];
    
    // read exponent
    ++c;
    ivalue = 10*(raw[c] - '0');
    ++c;
    ivalue += raw[c] - '0';

    ++c;
    if (ivalue == 0) {
        // Store value
        return dvalue;
    }

    scale = 1.0;
    while (ivalue > 0) { scale *= 10.0; ivalue -=  1; }

    if (tempstr[0] == '+'){
        return dvalue *= scale;
    }
    else{
        return dvalue /= scale;
    }
   
}


//=============================================================================
// Reads NBLOCK from ANSYS.  Raw string is from Python reader and file is
// positioned at the start of the data of NBLOCK
//=============================================================================
int read_nblock(char *raw, int *nnum, double *nodes, int nnodes, int intsz,
                 int fltsz, int *n, int EOL){


    char tempstr[100];
    int i, j, k, dof, nread, t;
    double dvalue, sign, pow, scale;

    int ivalue;

    // set file position
    i = *(n);

//     Read node data
    for (k=0; k<nnodes; ++k){
        // Starts assuming file is positioned on node number

        // Read node number
//        nnum[k] = fast_atoi2(raw, intsz, &i);
        nnum[k] = fast_atoi2(raw, intsz, &i);

        // skip fields 2 and 3
        i += intsz*2;

        // Read next 6 fields
        for (t=0; t<7; ++t){
            
            // Check if end of line character
            if (raw[i + EOL - 1] == '\n'){
                i += EOL;
                break;
            }


            //init value
            dvalue = 1.0;

            // check sign
            if (raw[i] == '-') {
                sign = -1.0;
            }
            else{
                sign = 1.0;
            }

            // read first interger
            ++i;
            dvalue *= raw[i] - '0';

            // next is always a '.', skip it
            ++i;

            nread = fltsz - 7; // sign, first int, point, xxx, scinot (4)
            pow = 0.1;
            for (j=0; j<nread; ++j){
                ++i;
                dvalue += (raw[i] - '0')*pow;
                pow *= 0.1;

            }

            // apply sign
            dvalue *= sign;

            // Read exponent
            // Skip the E
            ++i; 


            // store sign of exponent
            ++i;
            tempstr[0] = raw[i];

            
            // read exponent
            ++i;
            ivalue = 10*(raw[i] - '0');
            ++i;
            ivalue += raw[i] - '0';

            ++i;
//            printf("%c", raw[i]);
            if (ivalue == 0) {
                // Store value
                nodes[k*6 + t] = dvalue;
                continue;
            }

            scale = 1.0;
            while (ivalue > 0) { scale *= 10.0; ivalue -=  1; }

            if (tempstr[0] == '+'){
                dvalue *= scale;
            }
            else{
                dvalue /= scale;
            }

            // Store value
            nodes[k*6 + t] = dvalue;

        }

        // make empty fields 0.0
        for (j=t; j<6; ++j){
            nodes[k*6 + j] = 0.0;
        }

    }


//=============================================================================
// DEBUG
//=============================================================================
//    for (k=0; k<3; ++k){
//        // Starts assuming file is positioned on node number
//
//        // Read node number
////        nnum[k] = fast_atoi2(raw, intsz, &i);
//        printf("%d\t|", k);
//        nnum[k] = verbose_fast_atoi2(raw, intsz, &i);
//        printf("|%d", nnum[k]);
//
//        // skip fields 2 and 3
//        i += intsz*2;
//
//        // Read next 6 fields
////        dof = 0;
//        printf("||\n");
//        for (t=0; t<7; ++t){
//            printf("%4d||", t);
//            
//            // Check if end of line character
//            if (raw[i + EOL - 1] == '\n'){
//                i += EOL;
//                printf("\tNewLine\n");
//                break;
//            }
//
//
//            //init value
//            dvalue = 1.0;
//
//            // check sign
//            printf("%c", raw[i]);
//            if (raw[i] == '-') {
//                sign = -1.0;
//            }
//            else{
//                sign = 1.0;
//            }
//
//            // read first interger
//            ++i;
//            printf("%c", raw[i]);
//            dvalue *= raw[i] - '0';
//
//            // next is always a '.', skip it
//            ++i;
//            printf("%c", raw[i]);
//
//            nread = fltsz - 7; // sign, first int, point, xxx, scinot (4)
//            pow = 0.1;
//            for (j=0; j<nread; ++j){
//                ++i;
//                printf("%c", raw[i]);
//                dvalue += (raw[i] - '0')*pow;
//                pow *= 0.1;
//
//            }
//
//            // apply sign
//            dvalue *= sign;
//
//            // Read exponent
//            // Skip the E
//            ++i; 
//            printf("%c", raw[i]);
//
//
//            // store sign of exponent
//            ++i;
//            tempstr[0] = raw[i];
//            printf("%c", raw[i]);
//
//            
//            // read exponent
//            ++i;
//            printf("%c", raw[i]);
//            ivalue = 10*(raw[i] - '0');
//            ++i;
//            printf("%c", raw[i]);
//            ivalue += raw[i] - '0';
//
//            ++i;
////            printf("%c", raw[i]);
//            if (ivalue == 0) {
//                // Store value
//                nodes[k*6 + t] = dvalue;
//                printf("|%20.13f\n", dvalue);
//                t += 1;
//                continue;
//            }
//
//            scale = 1.0;
//            while (ivalue > 0) { scale *= 10.0; ivalue -=  1; }
//
//            if (tempstr[0] == '+'){
//                dvalue *= scale;
//            }
//            else{
//                dvalue /= scale;
//            }
//
//            // Store value
//            nodes[k*6 + t] = dvalue;
//            printf("|%20.13f\n", dvalue);
////            dof += 1;
//
//        }
//
//        // make empty fields 0.0
//        for (j=t; j<6; ++j){
//            nodes[k*6 + j] = 0.0;
//        }
//
//    }

    // return file position
    return i;
    
}


//=============================================================================
// Reads EBLOCK from ANSYS.  Raw string is from Python reader and file is
// positioned at the start of the data of EBLOCK
//=============================================================================
//int dummy(char )

int read_eblock(char *raw, int *etype, int *e_rcon, int *elemnum, 
                 int *elem, int nelem, int intsz, int *j, int EOL){

    int i, n, c, k, nnode, tempint, val, g;
    n = *(j) - 1;
    

    // Loop through elements
    for (i=0; i<nelem; ++i){

        // Check if end of line
        if (raw[n + EOL] == '\n'){
            n += EOL;
        }

        if (checkneg(raw, intsz, &n)){
            break;
        }
        
        // Field 2: Read element type
        etype[i] = fast_atoi(raw, intsz, &n);
    
        // Field 3: Read real constant
        e_rcon[i] = fast_atoi(raw, intsz, &n);

        // Skip Fields 4 - 8 and store 9, the number of nodes    
        n += 5*intsz;
        nnode = fast_atoi(raw, intsz, &n);


        // Skip Field 10 and read Field 11: Element number
        n += intsz;
        elemnum[i] = fast_atoi(raw, intsz, &n);

            
        // Read nodes in element
        c = 0;
        while (c < nnode){

            // Check if end of line
            if (raw[n + EOL] == '\n'){
                n += EOL;
            }

            // Read node

            // Called so much it's worth inlining it
            // (same as function fast_atoi)
            val = 0;
            for (g=0; g<intsz; ++g){
                ++n;
        
                // Seek throug white space
                if (raw[n] == ' ') continue;
        
                val = val*10 + (raw[n] - '0');
            }

            elem[20*i + c] = val;

            ++c;

        }
            
        // Set remaining element numbers to -1
        for (c; c<20; ++c){
                elem[20*i + c] = -1;
        }

    }


//=============================================================================
// DEBUG
//=============================================================================
//    for (i=0; i<100; ++i){
//        printf("||\t%9d\t||\n", i);
//        // Check if end of line
//        if (raw[n + EOL] == '\n'){
//            n += EOL;
//        }
//
//        // Check Field 1 is not -1
//        if (fast_atoi(raw, intsz, &n) == -1){
//            return i;
//            };
//        
//        // Field 2: Read element type
//        etype[i] = fast_atoi(raw, intsz, &n);
//        printf("|%8d\n", etype[i]);
//    
//        // Field 3: Read real constant
//        e_rcon[i] = fast_atoi(raw, intsz, &n);
//        printf("|%8d\n", e_rcon[i]);
//
////        // Skip Fields 4 - 8 and store 9, the number of nodes    
//        n += 5*intsz;
//        nnode = fast_atoi(raw, intsz, &n);
//        printf("|%8d\n", nnode);
//
//
//        // Skip Field 10 and read Field 11: Element number
//        n += intsz;
//        elemnum[i] = fast_atoi(raw, intsz, &n);
//        printf("|%8d\n", elemnum[i]);
//
//            
//        // Read nodes in element
//        c = 0;
//        while (c < nnode){
//
//            // Check if end of line
//            if (raw[n + EOL] == '\n'){
//                n += EOL;
//                printf("EOL in while\n");
//            }
//            printf("%2d|", c);
//            // Read node
//            elem[20*i + c] = verbose_fast_atoi(raw, intsz, &n);
//            printf("|%8d\n", elem[20*i + c]);
//            ++c;
//
//        }
//            
//        // Set remaining element numbers to -1
//        for (c; c<20; ++c){
//                elem[20*i + c] = -1;
//            printf("%2d|%8d\n", c, -1);
////            ++c;
//        }
//
//    }

    // update file position
    *(j) = n;

    // return file position
    return i;


}
