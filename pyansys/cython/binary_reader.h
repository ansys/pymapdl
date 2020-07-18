/* #include <fstream> */

void read_nodes(const char*, int64_t, int, int *, double *);
void* read_record(const char*, int64_t, int*, int*, int*, int*);
void read_record_stream(std::ifstream*, int64_t, void*, int*, int*, int*);
