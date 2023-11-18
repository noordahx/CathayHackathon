import numpy as np
import time
from ctypes import *
import os
os.environ['LD_LIBRARY_PATH'] = '/usr/local/lib'
from numpy.ctypeslib import ndpointer


class PointClustering:

    def __init__(self, dll:str = None) -> None:
        if dll is None:
            dll = os.path.join( os.path.realpath(os.path.dirname(__file__)), 'compiled/point_clustering.so' )
        
        self.dll = CDLL(dll)
    
    def height_clustering(self, 
        points,
        point_shape,
        p_max_z_dist,
        p_max_xy_dist
    ) -> np.ndarray:
        
        ret_groups = np.full((points.shape[0], 1), 0, dtype=np.int64, order='C')
        

        ret = self.dll.height_clustering(
            points,
            point_shape,
            p_max_z_dist,
            p_max_xy_dist,
            ret_groups
        )

        return ret_groups
        


if __name__ == "__main__":
    

    point_clustering = PointClustering()

    points = np.array([
        [1, 1, 0],
        [0, 1, 1],
        [1, 2, 3],
        [4, 5, 6]
    ], dtype=np.float32, order='C')


    point_clustering.height_clustering(
        points=points,
        point_shape=np.ascontiguousarray(points.shape, dtype=np.uint64),
        p_max_z_dist=1,
        p_max_xy_dist=1
    )