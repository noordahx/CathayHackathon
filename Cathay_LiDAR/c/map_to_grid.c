#include <string.h>
#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include "indexing.h"
#include "types.h"

void map_to_grid(
    double* points, 
    ulong* points_shape,
    double* unit_per_grid,
    double* min_roi,
    double* max_roi,
    long* ret
)
{
    for (size_t pt_idx = 0; pt_idx < points_shape[0]; pt_idx ++)
    {
        ulong xi = 3*pt_idx;
        ulong yi = 3*pt_idx+1;
        ulong zi = 3*pt_idx+2;

        double x = points[xi];
        double y = points[yi];
        double z = points[zi];

        if (x < min_roi[0] || y < min_roi[1] || z < min_roi[2])
            continue;
        
        if (x >= max_roi[0] || y >= max_roi[1] || z >= max_roi[2])
            continue;

        // Compute index
        ulong x_grid_index = floor((x - min_roi[0]) / unit_per_grid[0]);
        ulong y_grid_index = floor((y - min_roi[1]) / unit_per_grid[1]);
        ulong z_grid_index = floor((z - min_roi[2]) / unit_per_grid[2]);

        // Assign
        ret[xi] = x_grid_index;
        ret[yi] = y_grid_index;
        ret[zi] = z_grid_index;
    }
}




void map_to_grid_rmi(
    double* points, 
    ulong* points_shape,
    double* unit_per_grid,
    double* min_roi,
    double* max_roi,
    ulong* grid_shape,
    long* ret
)
{
    for (size_t pt_idx = 0; pt_idx < points_shape[0]; pt_idx ++)
    {
        ulong xi = 3*pt_idx;
        ulong yi = 3*pt_idx+1;
        ulong zi = 3*pt_idx+2;

        double x = points[xi];
        double y = points[yi];
        double z = points[zi];

        if (x < min_roi[0] || y < min_roi[1] || z < min_roi[2])
            continue;
        
        if (x >= max_roi[0] || y >= max_roi[1] || z >= max_roi[2])
            continue;

        // Compute index
        ulong x_grid_index = floor((x - min_roi[0]) / unit_per_grid[0]);
        ulong y_grid_index = floor((y - min_roi[1]) / unit_per_grid[1]);
        ulong z_grid_index = floor((z - min_roi[2]) / unit_per_grid[2]);

        // Assign
        ret[pt_idx] = rmi3(grid_shape, x_grid_index, y_grid_index, z_grid_index);
    }
}






void reduce_by_key(
    ulong* grid_indices,
    double* keys,
    size_t* keys_shape,
    long* ret,
    size_t* ret_shape
)
{  
    ulong ret_len = (ret_shape[0] * ret_shape[1] * ret_shape[2]);

    double* ret_best_vals = malloc( ret_len * sizeof(double) );
    bool* ret_best_vals_used = malloc( ret_len * sizeof(bool) );
     for (ulong i = 0; i < ret_len; i ++)
        ret_best_vals_used[i] = false;

    for (ulong i = 0; i < keys_shape[0]; i ++)
    {
        ulong grid_index_x = grid_indices[3 * i + 0];
        ulong grid_index_y = grid_indices[3 * i + 1];
        ulong grid_index_z = grid_indices[3 * i + 2];
    
        ulong grid_index = rmi3(ret_shape, grid_index_x, grid_index_y, grid_index_z);
        if (!ret_best_vals_used[grid_index])
        {
            ret_best_vals_used[grid_index] = true;
            ret_best_vals[grid_index] = keys[i];
            ret[grid_index] = (long)i;
        }
        else if (keys[i] < ret_best_vals[grid_index])
        {
            ret_best_vals[grid_index] = keys[i];
            ret[grid_index] = (long)i;
        }
    }

    free(ret_best_vals);
    free(ret_best_vals_used);

}



void compute_grid_occupied(
    double *points,
    ulong* point_shape,

    ulong* grid_indices,
    ulong* grid_shape,

    bool* ret_occupied
)
{
    for (ulong i = 0; i < grid_shape[0] * grid_shape[1] * grid_shape[2]; i ++)
        ret_occupied[i] = false;
    
    for (ulong point_idx = 0; point_idx < point_shape[0]; point_idx ++)
    {
        ulong grid_i = grid_indices[3 * point_idx];
        ulong grid_j = grid_indices[3 * point_idx + 1];
        ulong grid_k = grid_indices[3 * point_idx + 2];
        ulong i = rmi3(grid_shape, grid_i, grid_j, grid_k);
        ret_occupied[rmi3(grid_shape, grid_i, grid_j, grid_k)] = true;
    }
}