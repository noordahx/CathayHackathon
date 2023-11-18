import numpy as np
from ctypes import *
import os
from numpy.ctypeslib import ndpointer
from c.map_to_grid import MapToGrid
from grid.axis_aligned_grid import AxisAlignedGrid
from numba import njit

class PointInTriangle:
    def __init__(self, dll:str = None) -> None:
        if dll is None:
            dll = os.path.join( os.path.realpath(os.path.dirname(__file__)), 'compiled/point_in_triangle.so' )
        self.dll = CDLL(dll)
        '''
        Implemented 2 functions
        1. get_cross_points:
            1. input a grid.
            2. use cutting lines with fixed interval to get all the cross points.
            3. ouput N x 2 vector, representing x, y of all cross points.
        2. get_diff_and_select_vaild_points:
            1. compute diff
            2. make invaild points'z value become -28
        3. point_in_triangle:
            1. input cross points, triangles, vertices
            2. output N x 3 vector, representing 3d indices of cross points and its original shape.
        '''
    def get_cross_points(self, grids: AxisAlignedGrid, grid_1d_index: int, interval: float) -> np.ndarray:

        grid_3d_index = grids.grid_index_to_ijk(grid_1d_index)
        tx, ty, tz = grid_3d_index

        # compute min_roi and max_roi of the grid
        grid_pos = np.array([tx * grids.unit_per_grids[0] + grids.min_roi[0],
                    ty * grids.unit_per_grids[1] + grids.min_roi[1],
                    tz * grids.unit_per_grids[2] + grids.min_roi[2]], dtype = np.float64)

        # create cross points
        points_x = np.arange(grid_pos[0], grid_pos[0] + grids.unit_per_grids[0], interval[0], dtype=np.float64)
        points_y = np.arange(grid_pos[1], grid_pos[1] + grids.unit_per_grids[1], interval[1], dtype=np.float64)
        # cross_points_x, cross_points_y = np.meshgrid(points_x, points_y)
        
        # cross_points = np.ascontiguousarray(np.stack((cross_points_x, cross_points_y)).transpose(1, 2, 0).reshape((points_x.shape[0] * points_y.shape[0], 2)))
        # cross_points_shape = np.array([points_x.shape[0], points_y.shape[0]], dtype=np.uint16)
        
        cross_points = np.array(np.meshgrid(points_x, points_y)).T.reshape(-1, 2)
        cross_points_shape = np.array([points_x.shape[0], points_y.shape[0]], dtype=np.uint16)


        # print(cross_points, cross_points_shape)
        return cross_points, cross_points_shape

    def get_diff_and_select_vaild_points(self, cross_points, cross_points_shape, scale, interval = 2): # n x m x 3,  n x m, [height_diff_scale]
        cross_points = cross_points.reshape((cross_points_shape[0], cross_points_shape[1], 3))
        print("cross_points", cross_points, cross_points.shape)

        # compute diff from cross points with interval 2 vertices
        diff_x = np.array([cross_points[:, i, 2] - cross_points[:, i - interval, 2] for i in range(0, cross_points_shape[1] - interval)]).transpose(1, 0)
        diff_y = np.array([cross_points[i, :, 2] - cross_points[i - interval, :, 2] for i in range(0, cross_points_shape[0] - interval)])
        diff_x_transpose = np.array([cross_points[:, i, 2] - cross_points[:, i - interval, 2] for i in range(2, cross_points_shape[1])]).transpose(1, 0)
        diff_y_transpose = np.array([cross_points[i, :, 2] - cross_points[i - interval, :, 2] for i in range(2, cross_points_shape[0])])
        # print(diff_x.shape, diff_y.shape)
        mask_x = (scale[0] <= abs(diff_x)) & (abs(diff_x) <= scale[1])
        mask_y = (scale[0] <= abs(diff_y)) & (abs(diff_y) <= scale[1])
        mask_x_transpose = (scale[0] <= abs(diff_x_transpose)) & (abs(diff_x_transpose) <= scale[1])
        mask_y_transpose = (scale[0] <= abs(diff_y_transpose)) & (abs(diff_y_transpose) <= scale[1])

        # make z-value of invaild points equal -28. -28 is for better view. 
        cross_points[:, :-interval, 2][mask_x == False] = -28
        cross_points[:-interval, :, 2][mask_y == False] = -28
        cross_points[:, :-interval, 2][mask_x_transpose == False] = -28
        cross_points[:-interval, :, 2][mask_y_transpose == False] = -28

        # zoom in 3 times of all the cross points' range.

        # x_range = cross_points_shape[0] - (cross_points_shape[0] // 6) * 2
        # y_range = cross_points_shape[1] - (cross_points_shape[1] // 6) * 2
        # print("x_range", x_range, "y_range", y_range)
        # cross_points = cross_points[cross_points_shape[0] // 6: cross_points_shape[0] - cross_points_shape[0] // 6, cross_points_shape[1] // 6: cross_points_shape[1] - cross_points_shape[1] // 6, :]
        # cross_points = cross_points.reshape((x_range * y_range, 3))
        # cross_points_shape[0], cross_points_shape[1] = x_range, y_range

        cross_points = cross_points.reshape((cross_points_shape[0] * cross_points_shape[1], 3))
        return cross_points, cross_points_shape


    def point_in_triangle(self, points : np.ndarray, points_shape : np.ndarray, triangles : np.ndarray, 
                            triangles_shape : np.ndarray, vertices : np.ndarray):
        
        self.dll.point_in_triangle.argtypes = [
            ndpointer(c_double, flags="C_CONTIGUOUS"),
            ndpointer(c_uint64, flags="C_CONTIGUOUS"),
            ndpointer(c_uint64, flags="C_CONTIGUOUS"),
            ndpointer(c_uint64, flags="C_CONTIGUOUS"),
            ndpointer(c_double, flags="C_CONTIGUOUS"),
            ndpointer(c_double, flags="C_CONTIGUOUS"),
            ndpointer(c_bool, flags="C_CONTIGUOUS")
        ]
        ret_arr = np.full((points_shape[0] * points_shape[1], 1), 0, dtype=np.float64, order='C')
        ret_mask = np.full((points_shape[0] * points_shape[1], ), 0, dtype=np.bool8, order='C')

        ret = self.dll.point_in_triangle(
            points,
            points_shape,
            triangles,
            triangles_shape,
            vertices,
            ret_arr,
            ret_mask
        )
        

        ret_arr = np.hstack((points, ret_arr))
        return ret_arr, ret_mask



@njit
def get_edge_from_cross_points(cross_points_3d, cross_points_3d_is_valid, cross_points_shape, accept_min_height, accept_max_height, interval = 1):
    cross_points_3d = cross_points_3d.reshape(cross_points_shape[0], cross_points_shape[1], 3)
    cross_points_3d_is_valid = cross_points_3d_is_valid.reshape(cross_points_shape[0], cross_points_shape[1], 1)
    height_diff = np.zeros((cross_points_shape[0], cross_points_shape[1]))
    height_diff_is_valid = np.zeros((cross_points_shape[0], cross_points_shape[1]), dtype=np.bool8)

    for x in range(0, cross_points_3d.shape[0]):
        for y in range(0, cross_points_3d.shape[1]):
            # print(x, y, cross_points_3d[x, y])
            # break
            if cross_points_3d_is_valid[x, y] == False:
                continue

            for ix in range( max(0, x - interval), min(x + interval + 1, cross_points_shape[0]) ):
                if ix == x:
                    continue
                if cross_points_3d_is_valid[ix, y] == True:
                    if not height_diff_is_valid[x, y]:
                        height_diff_is_valid[x, y] = 1
                        height_diff[x, y] = abs(cross_points_3d[x, y, 2] - cross_points_3d[ix, y, 2])
                    else:
                        height_diff[x, y] = max( height_diff[x, y], abs(cross_points_3d[x, y, 2] - cross_points_3d[ix, y, 2]) )
            
            for iy in range( max(0, y - interval), min(y + interval + 1, cross_points_shape[1]) ):
                if iy == y:
                    continue
                if cross_points_3d_is_valid[x, iy] == True:
                    if not height_diff_is_valid[x, y]:
                        height_diff_is_valid[x, y] = 1
                        height_diff[x, y] = abs(cross_points_3d[x, y, 2] - cross_points_3d[x, iy, 2])
                    else:
                        height_diff[x, y] = max( height_diff[x, y], abs(cross_points_3d[x, y, 2] - cross_points_3d[x, iy, 2]))

            # print(x, y, height_diff[x, y])

    valid_mask = height_diff_is_valid > 0
    valid_mask &= height_diff >= accept_min_height
    valid_mask &= height_diff <= accept_max_height
    valid_mask = valid_mask.reshape(-1)
    # print(np.min(height_diff), np.max(height_diff))
    return cross_points_3d.reshape(-1, 3)[valid_mask]#, valid_mask

if __name__ == '__main__':
    point_in_triangle = PointInTriangle()