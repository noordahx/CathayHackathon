#include <string.h>
#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include "indexing.h"
#include "calculate.h"


#define MIN(i, j) (((i) < (j)) ? (i) : (j))
#define MAX(i, j) (((i) > (j)) ? (i) : (j))

void plane_detection
(
    double *points,
    ulong* point_shape,

    ulong* grid_indices,
    ulong* grid_shape,
    
    double* grid_min_roi,
    double* grid_max_roi,
    ulong* grid_multi_dim_indices,

    double p_z_tolerance,
    double p_min_area,

    int* ret_determined,
    double* ret_planes,
    int* debug_point
)
{   

    double std_area = (grid_max_roi[0] - grid_min_roi[0]) * (grid_max_roi[1] - grid_min_roi[1]);
    double min_area = std_area * p_min_area;

    ulong grid_size = grid_shape[0] * grid_shape[1] * grid_shape[2];
    for (ulong grid_idx = 0; grid_idx < grid_size; grid_idx ++)
    {
        // top left, top right, bottom left, bottom right
        double corners[4][3] = { {}, {}, {}, {} };
        double ideal_corners_xy[4][2] = 
        {
            { grid_min_roi[3 * grid_idx + 0], grid_min_roi[3 * grid_idx + 1] },
            { grid_max_roi[3 * grid_idx + 0], grid_min_roi[3 * grid_idx + 1] },
            { grid_min_roi[3 * grid_idx + 0], grid_max_roi[3 * grid_idx + 1] },
            { grid_max_roi[3 * grid_idx + 0], grid_max_roi[3 * grid_idx + 1] },
        };

        // fprintf(fp, "grid = %ld, grid_min_roi = %f, %f, %f, grid_max_roi = %f, %f, %f\n", 
        //     grid_idx,
        //     grid_min_roi[3 * grid_idx + 0], grid_min_roi[3 * grid_idx + 1], grid_min_roi[3 * grid_idx + 2],
        //     grid_max_roi[3 * grid_idx + 0], grid_max_roi[3 * grid_idx + 1], grid_max_roi[3 * grid_idx + 2]
        // );

        int corner_set[4] = { -1, -1, -1, -1 };
        double corner_dist[4] = { };
        
        // obtain corners
        for (ulong point_idx = 0; point_idx < point_shape[0]; point_idx ++)
        {          
            double x = points[ 3 * point_idx + 0 ];
            double y = points[ 3 * point_idx + 1 ];
            double z = points[ 3 * point_idx + 2 ];

            // printf("x, y, z = %f %f %f\n", x, y, z);
            
            if (x < grid_min_roi[3 * grid_idx + 0] || y < grid_min_roi[3 * grid_idx + 1] || z < grid_min_roi[3 * grid_idx + 2])
                continue;
            if (x >= grid_max_roi[3 * grid_idx + 0] || y >= grid_max_roi[3 * grid_idx + 1] || z >= grid_max_roi[3 * grid_idx + 2])
                continue;

            for (int corner_idx = 0; corner_idx < 4; corner_idx ++)
            {
                double p[2] = { x, y };
                double dist_to_ideal = square_dist_between_points( p, ideal_corners_xy[corner_idx], 2 );
                // printf( "grid = %ld, corner_idx = %d, (%f, %f), (%f, %f), dist = %f\n", grid_idx, corner_idx, p[0], p[1], ideal_corners_xy[corner_idx][0], ideal_corners_xy[corner_idx][1], dist_to_ideal );
                if (corner_set[corner_idx] == -1 || dist_to_ideal < corner_dist[corner_idx])
                {
                    corners[corner_idx][0] = x;
                    corners[corner_idx][1] = y;
                    corners[corner_idx][2] = z;
                    corner_set[corner_idx] = point_idx;
                    corner_dist[corner_idx] = dist_to_ideal;
                }
            }
        }


        // verify
        bool has_corners = true;
        for (int i = 0; i < 4; i ++) if (corner_set[i] == -1) { has_corners = false; break; }
        if (!has_corners) {
            // printf("[%ld] No corner\n", grid_idx);
            continue;
        }

         // order: top left, top right,bottom right, bottom left
        double cornerXs[] = { corners[0][0], corners[1][0], corners[3][0], corners[2][0] };
        double cornerYs[] = { corners[0][1], corners[1][1], corners[3][1], corners[2][1] };
        double corner_area = polygon_area(cornerXs, cornerYs, 4);
        if (corner_area < min_area)
        {
            // printf("[%ld] Corner area too small: %f\n", grid_idx, corner_area);
            continue;
        }


        for (int i = 0; i < 4; i ++)
            debug_point[corner_set[i]] =  1;
        // printf("[%ld] Corner idx: %d %d %d %d \n", grid_idx, debug_point[0], debug_point[1], debug_point[2], debug_point[3] );
        
        // debug_point[temp[0]] = 1;
        // debug_point[temp[1]] = 1;
        // debug_point[temp[2]] = 1;
        // debug_point[temp[0]] = 1;



        
        //
        int plane_idx_tuples[1][3] = {
            {0, 1, 2},
            // {1, 3, 2}
        };

        bool distance_exceed = false;
        for (int tuple_idx = 0; tuple_idx < 1; tuple_idx ++)
        {
            int* pidx = plane_idx_tuples[tuple_idx];

            double plane_coefs[4] = {-1};
            double* point1 = corners[pidx[0]];
            double* point2 = corners[pidx[1]];
            double* point3 = corners[pidx[2]];
            
            plane_from_points(point1, point2, point3, plane_coefs);

            ret_planes[4 * grid_idx + 0] = plane_coefs[0];
            ret_planes[4 * grid_idx + 1] = plane_coefs[1];
            ret_planes[4 * grid_idx + 2] = plane_coefs[2];
            ret_planes[4 * grid_idx + 3] = plane_coefs[3];

            
            // Check point to plane dist
            for (ulong point_idx = 0; point_idx < point_shape[0]; point_idx ++)
            {
                double x = points[ 3 * point_idx + 0 ];
                double y = points[ 3 * point_idx + 1 ];
                double z = points[ 3 * point_idx + 2 ];

                // printf("x, y, z = %f %f %f\n", x, y, z);
                
                if (x < grid_min_roi[3 * grid_idx + 0] || y < grid_min_roi[3 * grid_idx + 1] || z < grid_min_roi[3 * grid_idx + 2])
                    continue;
                if (x >= grid_max_roi[3 * grid_idx + 0] || y >= grid_max_roi[3 * grid_idx + 1] || z >= grid_max_roi[3 * grid_idx + 2])
                    continue;

                
                double *p = &points[3 * point_idx];
                double dist = dist_from_point_to_plane(plane_coefs, p);

                if (dist > p_z_tolerance)
                {
                    // printf("[%ld] Exceed %f plane=%f %f %f %f point(%ld)=%f %f %f\n", grid_idx, dist, plane_coefs[0], plane_coefs[1], plane_coefs[2], plane_coefs[3], point_idx, p[0], p[1], p[2]);
                    distance_exceed = true;
                    break;
                }
            }

            // fprintf(fp, "[%ld] %f %f %f %f (%f %f %f) (%f %f %f) (%f %f %f)\n", 
            //     grid_idx, plane_coefs[0], plane_coefs[1], plane_coefs[2], plane_coefs[3],
            //     point1[0], point1[1], point1[2],
            //     point2[0], point2[1], point2[2],
            //     point3[0], point3[1], point3[2]
            // );

            if (distance_exceed)
                break;
                

        }

        if (distance_exceed)
            continue;

        // // check for height tolerance
        // double z_max = MAX( corner_z[0], MAX(corner_z[1], MAX(corner_z[2], corner_z[3])) );
        // double z_min = MIN( corner_z[0], MIN(corner_z[1], MIN(corner_z[2], corner_z[3])) );
        // // printf("%ld %f\n", grid_idx, z_max - z_min);

        // if (z_max - z_min > p_z_tolerance)
        //     continue;

        
        // Update flag
        ret_determined[grid_idx] = 1;
        
        // fclose(fp);
    }
}