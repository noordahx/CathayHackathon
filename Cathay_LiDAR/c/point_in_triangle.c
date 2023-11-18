#include <string.h>
#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>

#define min(a,b) (((a)<(b))?(a):(b))
#define max(a,b) (((a)>(b))?(a):(b))

bool judge(double x, double y, double x1, double y1, double x2, double y2, double x3, double y3){
    if(x > max(x1, max(x2, x3)) || y > max(y1, max(y2, y3)) || x < min(x1, min(x2, x3)) || y < min(y1, min(y2, y3)))  {
        return false;
    }
    double as_x = x - x1;
    double as_y = y - y1;
    bool s_ab = (x2 - x1) * as_y - (y2 - y1) * as_x > 0;
    if ((x3 - x1) * as_y - (y3 - y1) * as_x > 0 == s_ab) 
        return false;
    if ((x3 - x2) * (y - y2) - (y3 - y2) * (x - x2) > 0 != s_ab) 
        return false;
    return true;
}

// void height_diff(double* points, ulong* points_shape, double* height, double* diff_x, double* diff_y){
//     for(size_t i = 0; i < points_shape[0]; i++){
//         // ulong x1 = 2*i;
//         // ulong y1 = 2*i + 1;
//         for(size_t j = 0; j < points_shape[1] - 1; j++){
//             diff_x[i * points_shape[1] + j] = height[i * points_shape[1] + j + 1] - height[i * points_shape[1] + j];
//         }
//     }
//     for(size_t i = 0; i < points_shape[1]; i++){
//         for(size_t j = 0; j < points_shape[0] - 1; j++){
//             diff_y[i * points_shape[0] + j] = height[i * points_shape[0] + j + 1] - height[i * points_shape[0] + j];
//     }
// }


void point_in_triangle(
    double* points, 
    ulong* points_shape, 
    ulong* triangles, 
    ulong* triangles_shape,
    double* vertices, 
    double* ret,
    bool* ret_mask
){


    double* triangle_heights = malloc(sizeof(double) * triangles_shape[0]);

    #pragma omp parallel for
    for(size_t triangle_index = 0; triangle_index < triangles_shape[0]; triangle_index++){
        ulong vertex1 = triangles[3 * triangle_index];
        ulong vertex2 = triangles[3 * triangle_index + 1];
        ulong vertex3 = triangles[3 * triangle_index + 2];

        double x1 = vertices[vertex1 * 3];
        double y1 = vertices[vertex1 * 3 + 1];
        double z1 = vertices[vertex1 * 3 + 2];
        double x2 = vertices[vertex2 * 3];
        double y2 = vertices[vertex2 * 3 + 1];
        double z2 = vertices[vertex2 * 3 + 2];
        double x3 = vertices[vertex3 * 3];
        double y3 = vertices[vertex3 * 3 + 1];
        double z3 = vertices[vertex3 * 3 + 2];
        triangle_heights[triangle_index] = (z1 + z2 + z3) / 3;
    }


    for(size_t pt_idx = 0; pt_idx < points_shape[0] * points_shape[1]; pt_idx++){
        ulong xi = 2*pt_idx;
        ulong yi = 2*pt_idx+1;

        double x = points[xi];
        double y = points[yi];

        double highest_z = 0;
        bool has_found = false;

        #pragma omp parallel for
        for(size_t triangle_index = 0; triangle_index < triangles_shape[0]; triangle_index++){
            ulong vertex1 = triangles[3 * triangle_index];
            ulong vertex2 = triangles[3 * triangle_index + 1];
            ulong vertex3 = triangles[3 * triangle_index + 2];

            double x1 = vertices[vertex1 * 3];
            double y1 = vertices[vertex1 * 3 + 1];
            double z1 = vertices[vertex1 * 3 + 2];
            double x2 = vertices[vertex2 * 3];
            double y2 = vertices[vertex2 * 3 + 1];
            double z2 = vertices[vertex2 * 3 + 2];
            double x3 = vertices[vertex3 * 3];
            double y3 = vertices[vertex3 * 3 + 1];
            double z3 = vertices[vertex3 * 3 + 2];
            if(judge(x, y, x1, y1, x2, y2, x3, y3)){

                if (highest_z) {
                    if (triangle_heights[triangle_index] > highest_z)
                        highest_z = triangle_heights[triangle_index];
                }
                else {
                    has_found = true;
                    highest_z = triangle_heights[triangle_index];
                    // ret[pt_idx] = (z1 + z2 + z3) / 3;
                    // ret_mask[pt_idx] = true;
                }
            }
            // ret[pt_idx] = -28;
        }

        if (has_found)
        {
            ret_mask[pt_idx] = true;
            ret[pt_idx] = highest_z;
        }
        // printf("%f, %f, %f\n", x, y, ret[pt_idx]);
    }


    free(triangle_heights);
}

