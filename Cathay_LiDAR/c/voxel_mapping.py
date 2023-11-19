import numpy as np
import time
from ctypes import *
import os
from numpy.ctypeslib import ndpointer


class VoxelMapping:
    def __init__(self, dll_path:str = None) -> None:
        if dll_path is None:
            dll_path = os.path.join( os.path.realpath(os.path.dirname(__file__)), 'compiled/voxel_mapping.so' )
        self.dll = CDLL(dll_path)
        self.dll_path = dll_path
    
        
    def reload_dll(self, ):
        del self.dll
        self.dll = CDLL(self.dll_path)
            
        

    def plane_detection(
            self,

            points : np.ndarray,
            point_shape : np.ndarray,
            
            grid_indices : np.ndarray,
            grid_shape : np.ndarray,

            grid_min_roi : np.ndarray,
            grid_max_roi : np.ndarray,
            grid_multi_dim_indices : np.ndarray,

            p_z_tolerance : float,
            p_min_area : float,
        ):
        
        self.dll.plane_detection.argtypes = [
            ndpointer(c_double, flags="C_CONTIGUOUS"),
            ndpointer(c_uint64, flags="C_CONTIGUOUS"),
            
            ndpointer(c_uint64, flags="C_CONTIGUOUS"),
            ndpointer(c_uint64, flags="C_CONTIGUOUS"),

            ndpointer(c_double, flags="C_CONTIGUOUS"),
            ndpointer(c_double, flags="C_CONTIGUOUS"),
            ndpointer(c_uint64, flags="C_CONTIGUOUS"),
            
            c_double,
            c_double,

            ndpointer(c_int32, flags="C_CONTIGUOUS"),
            ndpointer(c_double, flags="C_CONTIGUOUS"),
            ndpointer(c_int32, flags="C_CONTIGUOUS"),
        ]


        ret_determined = np.zeros(grid_shape, dtype=np.int32, order='C')
        ret_planes = np.zeros( (grid_shape[0], grid_shape[1], grid_shape[2], 4), dtype=np.float64, order='C')
        debug_points = np.zeros((points.shape[0],), dtype=np.int32, order='C')

        
        ret = self.dll.plane_detection(
            points,
            point_shape,
            
            grid_indices,
            grid_shape,

            grid_min_roi,
            grid_max_roi,
            grid_multi_dim_indices,
            
            p_z_tolerance,
            p_min_area,

            ret_determined,
            ret_planes,
            debug_points
        )
        
        return ret_determined, debug_points, ret_planes
