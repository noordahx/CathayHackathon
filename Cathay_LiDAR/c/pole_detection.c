#include <string.h>
#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include "indexing.h"
#include "calculate.h"


#define MIN(i, j) (((i) < (j)) ? (i) : (j))
#define MAX(i, j) (((i) > (j)) ? (i) : (j))


// bool _is_grid_occupied(ulong x, ulong y, ulong z, ulong* point_shape, ulong* grid_indices, ulong* grid_shape)
// {
//     ulong grid_index = rmi3(grid_shape, x, y, z);
//     for (ulong i = 0; i < point_shape[0]; i ++)
//     {
//         if (grid_indices[i] == grid_index)
//             return true;
//     }
//     return false;
// }

void _longest_consective(bool *occupied, ulong len, ulong *ret)
{
    ulong from_idx[len];
    for (ulong i = 0; i < len; i ++)
        from_idx[i] = len;
    
    ret[0] = len;
    ret[1] = len;

    ulong current_from = 0;
    ulong best_len = 0;
    ulong l = 0;
    for (ulong i = 0; i < len; i ++)
    {
        if (occupied[i])
        {
            from_idx[i] = current_from;
            
            l = i - current_from;
            if (l >= best_len)
            {
                best_len = l;
                ret[0] = current_from;
                ret[1] = i;
            }
        }
        else
        {
            from_idx[i] = len;
            current_from = i + 1;
        }
    }
}

void pole_detection(
    double *points,
    ulong* point_shape,

    ulong* grid_indices,
    ulong* grid_shape,
    
    double* grid_min_roi,
    double* grid_max_roi,
    ulong* grid_multi_dim_indices,

    ulong p_min_block,
    ulong p_max_block,

    int* ret_determined
)
{
    bool* grid_occupied = malloc(sizeof(bool) * grid_shape[0] * grid_shape[1] * grid_shape[2]);
    for (ulong i = 0; i < grid_shape[0] * grid_shape[1] * grid_shape[2]; i ++)
        grid_occupied[i] = false;
    
    for (ulong point_idx = 0; point_idx < point_shape[0]; point_idx ++)
    {
        ulong grid_i = grid_indices[3 * point_idx];
        ulong grid_j = grid_indices[3 * point_idx + 1];
        ulong grid_k = grid_indices[3 * point_idx + 2];
        ulong i = rmi3(grid_shape, grid_i, grid_j, grid_k);
        grid_occupied[rmi3(grid_shape, grid_i, grid_j, grid_k)] = true;
    }


    ulong total_grid = 0;
    ulong occ_grid = 0;
    for (ulong x = 0; x < grid_shape[0]; x ++)
    {
        for (ulong y = 0; y < grid_shape[1]; y ++)
        {            
            for (ulong z = 0; z < grid_shape[2]; z ++)
            {
                if (grid_occupied[rmi3(grid_shape, x, y, z)])
                {
                    occ_grid ++;
                }
                total_grid ++;
            }
        }
    }

    printf("total_grid=%ld, occ_grid=%ld\n", total_grid, occ_grid);


    bool occupied[grid_shape[2]];
    ulong longest_consective_ret[2];
    for (ulong x = 0; x < grid_shape[0]; x ++)
    {
        for (ulong y = 0; y < grid_shape[1]; y ++)
        {            
            ulong lowest_occupied_z = grid_shape[2];
            for (ulong z = 0; z < grid_shape[2]; z ++)
            {
                occupied[z] = grid_occupied[rmi3(grid_shape, x, y, z)];
                if (occupied[z] && z < lowest_occupied_z)
                    lowest_occupied_z = z;       
            }
            

            _longest_consective(occupied, grid_shape[2], longest_consective_ret);
            // printf("(%ld, %ld): %ld, %ld \n", x, y, longest_consective_ret[0], longest_consective_ret[1]);

            // if has consective and long enough
            if (
                longest_consective_ret[0] < grid_shape[2] && 
                longest_consective_ret[0] == lowest_occupied_z &&
                longest_consective_ret[1] - longest_consective_ret[0] >= p_min_block &&
                longest_consective_ret[1] - longest_consective_ret[0] <= p_max_block
            )
            {
                // mark point as determined
                for (ulong z = longest_consective_ret[0]; z <= longest_consective_ret[1]; z ++)
                {
                    ulong idx = rmi3(grid_shape, x, y, z);
                    for (ulong point_idx = 0; point_idx < point_shape[0]; point_idx ++)
                    {
                        ulong grid_i = grid_indices[3 * point_idx];
                        ulong grid_j = grid_indices[3 * point_idx + 1];
                        ulong grid_k = grid_indices[3 * point_idx + 2];
                        if (rmi3(grid_shape, grid_i, grid_j, grid_k) == idx)
                        {
                            ret_determined[point_idx] = 1; 
                        }
                    }
                }
            }
        }
    }
}