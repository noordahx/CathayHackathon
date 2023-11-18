import numpy as np
import time
from ctypes import *
import os
from numpy.ctypeslib import ndpointer


class MapToGrid:

    def __init__(self, dll:str = None) -> None:
        if dll is None:
            dll = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'compiled/map_to_grid.so')
        
        self.dll = CDLL(dll)
    
    def map_to_grid(self, points : np.ndarray, x_grid_per_unit : float, y_grid_per_unit : float, z_grid_per_unit : float, point_min : np.ndarray = None, point_max : np.ndarray = None) -> np.ndarray:
        '''
        Map points(Nx3) to a fixed grid.

        Return an ( array(Nx3) indicating the grid index, shape_of_grid )
        '''
        # if self.dll.map_to_grid is None:
        self.dll.map_to_grid.argtypes = [
            ndpointer(c_double, flags="C_CONTIGUOUS"),
            ndpointer(c_size_t),
            ndpointer(c_double),
            ndpointer(c_double),
            ndpointer(c_uint64, flags="C_CONTIGUOUS"),
        ]
        
        if point_min is None:
            point_min = np.min(points, axis=0)

        if point_max is None:
            point_max = np.max(points, axis=0)

                
        # point_max = np.max(points, axis=0)
        ret_arr = np.full((points.shape[0], 3), 0, dtype=np.uint64, order='C')
        # print(ret_arr.flags)

        ret = self.dll.map_to_grid(
            points,
            np.array(points.shape, dtype=np.uint64),
            np.array([x_grid_per_unit, y_grid_per_unit, z_grid_per_unit], dtype=np.float64),
            point_min,
            ret_arr
        )

        # print(ret_arr[0])

        grid_shape = ((point_max - point_min) // np.array([x_grid_per_unit, y_grid_per_unit, z_grid_per_unit]) + 1).astype(np.uint64)

        return ret_arr, grid_shape
        


    def map_to_grid2(self, points : np.ndarray, points_shape : np.ndarray, unit_per_grid : np.ndarray, min_roi : np.ndarray, max_roi : np.ndarray) -> np.ndarray:
        '''
        Map points(Nx3) to a fixed grid.

        Return an array(Nx3) indicating the grid index
        '''

        self.dll.map_to_grid.argtypes = [
            ndpointer(c_double, flags="C_CONTIGUOUS"),
            ndpointer(c_uint64, flags="C_CONTIGUOUS"),
            ndpointer(c_double, flags="C_CONTIGUOUS"),
            ndpointer(c_double, flags="C_CONTIGUOUS"),
            ndpointer(c_double, flags="C_CONTIGUOUS"),
            ndpointer(c_int64, flags="C_CONTIGUOUS"),
        ]
        
        ret_arr = np.full((points_shape[0], 3), -1, dtype=np.int64, order='C')

        ret = self.dll.map_to_grid(
            points,
            points_shape,
            unit_per_grid,
            min_roi,
            max_roi,
            ret_arr
        )
        return ret_arr


    
    def map_to_grid_rmi(self, 
        points : np.ndarray, 
        points_shape : np.ndarray, 
        unit_per_grid : np.ndarray, 
        min_roi : np.ndarray, 
        max_roi : np.ndarray,
        grid_shape : np.ndarray,

    ) -> np.ndarray:
        '''
        Map points(Nx3) to a fixed grid.

        Return an array(Nx1) indicating the grid index in row major order
        '''

        
        ret_arr = np.full((points_shape[0], 1), -1, dtype=np.int64, order='C')


        self.dll.map_to_grid_rmi.argtypes = [
            ndpointer(c_double, flags="C_CONTIGUOUS"),
            ndpointer(c_uint64, flags="C_CONTIGUOUS"),
            ndpointer(c_double, flags="C_CONTIGUOUS"),
            ndpointer(c_double, flags="C_CONTIGUOUS"),
            ndpointer(c_double, flags="C_CONTIGUOUS"),
            ndpointer(c_uint64, flags="C_CONTIGUOUS"),
            ndpointer(c_int64, flags="C_CONTIGUOUS"),
        ]

        ret = self.dll.map_to_grid_rmi(
            points,
            points_shape,
            unit_per_grid,
            min_roi,
            max_roi,
            grid_shape,
            ret_arr
        )
        return ret_arr



    def reduce_by_key(self, grid_indices : np.ndarray, keys: np.ndarray, grid_shape: tuple ):
        self.dll.reduce_by_key.argtypes = [
            ndpointer(c_uint64, flags="C_CONTIGUOUS"),
            ndpointer(c_double, flags="C_CONTIGUOUS"),
            ndpointer(c_size_t),
            ndpointer(c_int64, flags="C_CONTIGUOUS"),
            ndpointer(c_size_t),
        ]
        

        # print( np.max(grid_indices, axis=0) + 1)
        point_indices_in_grid = np.full( grid_shape, -1, dtype=np.int64, order='C' ) 
        # print(point_indices_in_grid.shape)
        # print(keys.shape)
        ret = self.dll.reduce_by_key(
            grid_indices,
            keys,
            np.array(keys.shape, dtype=np.uint64),
            point_indices_in_grid,
            np.array(point_indices_in_grid.shape, dtype=np.uint64),
        )

        return point_indices_in_grid
            


    def compute_grid_occupied(self,
        points : np.ndarray,
        points_shape : np.ndarray,
        
        grid_indices : np.ndarray,
        grid_shape : np.ndarray,
    ):
        self.dll.compute_grid_occupied.argtypes = [
           
            ndpointer(c_double, flags="C_CONTIGUOUS"), # double *points,
            ndpointer(c_uint64, flags="C_CONTIGUOUS"), # ulong* point_shape,

            ndpointer(c_uint64, flags="C_CONTIGUOUS"), # ulong* grid_indices,
            ndpointer(c_uint64, flags="C_CONTIGUOUS"), # ulong* grid_shape,

            ndpointer(c_bool, flags="C_CONTIGUOUS"), # bool* ret_occupied
        ]
        
        ret_occupied = np.zeros((grid_shape[0], grid_shape[1], grid_shape[2]), dtype=np.bool8, order='C')
        self.dll.compute_grid_occupied(
            points,
            points_shape,


            grid_indices,
            grid_shape,

            ret_occupied
        )

        return ret_occupied


if __name__ == "__main__":
    map_to_grid = MapToGrid()