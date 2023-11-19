#include <string.h>
#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <glib.h>


void height_clustering
(
    double *points,
    ulong* point_shape,

    double p_max_z_dist,
    double p_max_xy_dist,

    ulong *ret_groups
)
{
    // Prepare DFS
    GSList *stack = NULL;
    ulong *point_indices = malloc(sizeof(ulong) * point_shape[0]);
    bool *visited = malloc(sizeof(bool) * point_shape[0]);
    for (ulong point_idx = 0; point_idx < point_shape[0]; point_idx ++)
    {
        visited[point_idx] = false;
        point_indices[point_idx] = point_idx;
    }

    // DFS
    stack = g_slist_prepend(stack, &point_indices[0]);

    
    while (stack)
    {
        ulong curr_pidx = *((ulong*)&stack->data);
        stack = g_slist_delete_link(stack, stack);
        printf("%ld\n", curr_pidx);
    }


    // Free
    free(visited);
    free(point_indices);
}