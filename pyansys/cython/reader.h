int read_nblock(char*, int*, double*, int, int, int, int*, int);


//int read_eblock(char *raw, int *mtype, int *etype, int *e_rcon, int *sec_id,
//                int *elemnum, int *elem, int nelem, int intsz, int *j,
//                int EOL){
int read_eblock(char*, int*, int*, int*, int*, int*, int*, int, int, int*,
                int);
