#include <math.h>
#include <stdio.h>
#include <stdlib.h>


double dot(double vect_A[], double vect_B[], int n)
{
    double product = 0;
     for (int i = 0; i < n; i++)
        product = product + vect_A[i] * vect_B[i];
    return product;
}
 

void cross(double vect_A[], double vect_B[], double out[])
{
    out[0] = vect_A[1] * vect_B[2] - vect_A[2] * vect_B[1];
    out[1] = vect_A[2] * vect_B[0] - vect_A[0] * vect_B[2];
    out[2] = vect_A[0] * vect_B[1] - vect_A[1] * vect_B[0];
}



double dist_from_point_to_plane(double coefs[], double point[])
{
    // https://www.cuemath.com/geometry/distance-between-point-and-plane/
    double n = fabs( coefs[0] * point[0] + coefs[1] * point[1] + coefs[2] * point[2] + coefs[3] );
    double dn = sqrt(coefs[0] * coefs[0] + coefs[1] * coefs[1] + coefs[2] * coefs[2]);
    return n / dn;
}



double dist_between_points(double pa[], double pb[], int dim)
{
    if (dim == 2)
        return sqrt( (pa[0] - pb[0]) *  (pa[0] - pb[0]) +  (pa[1] - pb[1]) *  (pa[1] - pb[1]) );
    return sqrt( (pa[0] - pb[0]) *  (pa[0] - pb[0]) + (pa[1] - pb[1]) *  (pa[1] - pb[1]) + (pa[2] - pb[2]) *  (pa[2] - pb[2]) );
}


double square_dist_between_points(double pa[], double pb[], int dim)
{
    if (dim == 2)
        return  (pa[0] - pb[0]) *  (pa[0] - pb[0]) +  (pa[1] - pb[1]) *  (pa[1] - pb[1]);
    return  (pa[0] - pb[0]) *  (pa[0] - pb[0]) + (pa[1] - pb[1]) *  (pa[1] - pb[1]) + (pa[2] - pb[2]) *  (pa[2] - pb[2]);
}


void plane_from_points(double pa[], double pb[], double pc[], double out[])
{
    // https://www.maplesoft.com/support/help/maple/view.aspx?path=MathApps%2FEquationofaPlane3Points

    double ab[3] = { pb[0] - pa[0], pb[1] - pa[1], pb[2] - pa[2] };
    double ac[3] = { pc[0] - pa[0], pc[1] - pa[1], pc[2] - pa[2] };
    double norm[3] = { 0 };
    
    // printf("pa: %f %f %f\n", pa[0], pa[1], pa[2]);
    // printf("pb: %f %f %f\n", pb[0], pb[1], pb[2]);
    // printf("pc: %f %f %f\n", pc[0], pc[1], pc[2]);

    // printf("ab: %f %f %f\n", ab[0], ab[1], ab[2]);
    // printf("ac: %f %f %f\n", ac[0], ac[1], ac[2]);
    
    // printf("Pre norm: %f %f %f\n", norm[0], norm[1], norm[2]);
    cross(ab, ac, norm);
    // printf("Post norm: %f %f %f\n", norm[0], norm[1], norm[2]);
    

    out[0] = norm[0];
    out[1] = norm[1];
    out[2] = norm[2];

    // d = -(ax + by + cz)
    out[3] = -( out[0] * pa[0] + out[1] * pa[1] + out[2] * pa[2]);
}



double polygon_area(double X[], double Y[], int n)
{
    // Initialize area
    double area = 0.0;
 
    // Calculate value of shoelace formula
    int j = n - 1;
    for (int i = 0; i < n; i++)
    {
        area += (X[j] + X[i]) * (Y[j] - Y[i]);
        j = i;  // j is previous vertex to i
    }
 
    // Return absolute value
    return fabs(area / 2.0);
}