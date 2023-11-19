#include <string.h>
#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include "types.h"


// Address of A[I][J] = B + W * ((I – LR) * N + (J – LC))   

// I = Row Subset of an element whose address to be found, 
// J = Column Subset of an element whose address to be found, 
// B = Base address, 
// W = Storage size of one element store in an array(in byte), 
// LR = Lower Limit of row/start row index of the matrix(If not given assume it as zero), 
// LC = Lower Limit of column/start column index of the matrix(If not given assume it as zero), 
// N = Number of column given in the matrix.
ulong row_major_index2(size_t* shape, ulong i, ulong j)
{
    return i * shape[1] + j;
}
ulong rmi2(size_t* shape, ulong i, ulong j)
{
    return row_major_index2(shape, i, j);
}




ulong row_major_index3(size_t* shape, ulong i, ulong j, ulong k)
{
    return k + shape[2] * (j + shape[1] * i);
}
ulong rmi3(size_t* shape, ulong i, ulong j, ulong k)
{
    return row_major_index3(shape, i, j, k);
}


void rmi3_inverse(size_t* shape, ulong index, ulong* ijk)
{
    // offset = x + WIDTH*(y + HEIGHT*(z + DEPTH*time));

    // x = offset % WIDTH
    // offset = offset / WIDTH

    // y = offset % HEIGHT
    // offset = offset / HEIGHT

    // z = offset % DEPTH
    // offset = offset / DEPTH

    // time = offset

    ulong z = index % shape[2];
    index = index / shape[2];
    
    ulong y = index % shape[1];
    index = index / shape[1];

    ijk[0] = index;
    ijk[1] = y;
    ijk[2] = z;
}