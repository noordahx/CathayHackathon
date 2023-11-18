import numpy as np
import time
from ctypes import *
import os
from numpy.ctypeslib import ndpointer


class PoleDetection:
    def __init__(self, dll_path:str = None) -> None:
        if dll_path is None:
            dll_path = os.path.join( os.path.realpath(os.path.dirname(__file__)), 'compiled/pole_detection.so' )
        self.dll = CDLL(dll_path)
        self.dll_path = dll_path
    
        
    def reload_dll(self, ):
        del self.dll
        self.dll = CDLL(self.dll_path)
            
        

    def pole_detection(
            self,

            points : np.ndarray,
            point_shape : np.ndarray,
            
            grid_indices : np.ndarray,
            grid_shape : np.ndarray,

            grid_min_roi : np.ndarray,
            grid_max_roi : np.ndarray,
            grid_multi_dim_indices : np.ndarray,

            p_min_block : int,
            p_max_block : int,
        ):
        
        self.dll.pole_detection.argtypes = [


            ndpointer(c_double, flags="C_CONTIGUOUS"), # double *points,
            ndpointer(c_uint64, flags="C_CONTIGUOUS"), # ulong* point_shape,

            ndpointer(c_uint64, flags="C_CONTIGUOUS"), # ulong* grid_indices,
            ndpointer(c_uint64, flags="C_CONTIGUOUS"), # ulong* grid_shape,
            
            ndpointer(c_double, flags="C_CONTIGUOUS"), # double* grid_min_roi,
            ndpointer(c_double, flags="C_CONTIGUOUS"), # double* grid_max_roi,
            ndpointer(c_uint64, flags="C_CONTIGUOUS"), # ulong* grid_multi_dim_indices,

            c_uint64, # ulong p_min_block,
            c_uint64, # ulong p_max_block,
            ndpointer(c_int32, flags="C_CONTIGUOUS"), # int* ret_determined
        ]


        ret_determined = np.zeros((points.shape[0], 1), dtype=np.int32, order='C')

        
        ret = self.dll.pole_detection(
            points,
            point_shape,
            
            grid_indices,
            grid_shape,

            grid_min_roi,
            grid_max_roi,
            grid_multi_dim_indices,
            
            c_ulong(p_min_block),
            c_ulong(p_max_block),

            ret_determined,
        )
        
        return ret_determined
