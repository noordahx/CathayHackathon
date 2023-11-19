import numpy as np

from c.map_to_grid import MapToGrid
from numba import njit

class AxisAlignedGrid:
    def __init__(self,
        unit_per_grids : np.ndarray,
        min_roi : np.ndarray,
        max_roi: np.ndarray,
        **kwargs
    ) -> None:
        

        self.unit_per_grids = np.ascontiguousarray(unit_per_grids,  dtype=np.float64)
        self.max_roi = np.ascontiguousarray(max_roi, dtype=np.float64)
        self.min_roi = np.ascontiguousarray(min_roi, dtype=np.float64)
        self.grid_shape = ((self.max_roi - self.min_roi) // self.unit_per_grids).astype(np.uint64)
        


        # grid vars for fast accessing
        # self.grid_min_roi = None
        # self.grid_max_roi = None
        # self.grid_multi_dim_indices = None
        # self._compute_grid_fast_vars()


        # external wrapper
        self.map_to_grid_dll = MapToGrid()
        



    
        
    # def _compute_grid_fast_vars(self, ):
    #     '''
    #     compute grid vars for fast accessing
    #     '''
    #     x = np.arange(0, self.grid_shape[0], 1)
    #     y = np.arange(0, self.grid_shape[1], 1)
    #     z = np.arange(0, self.grid_shape[2], 1)

    #     indices = np.transpose( np.array(np.meshgrid(x, y, z, indexing='ij')), (1, 2, 3, 0)).reshape(self.grid_shape[0], self.grid_shape[1], self.grid_shape[2], 3)
    #     self.grid_min_roi = np.ascontiguousarray( (indices) * self.unit_per_grids + self.min_roi, dtype=np.float64 )
    #     self.grid_max_roi = np.ascontiguousarray( (indices + 1) * self.unit_per_grids + self.min_roi, dtype=np.float64 )
    #     # self.grid_multi_dim_indices = np.ascontiguousarray(indices, dtype=np.uint64)

        

        
    def map_points(self, points : np.ndarray):
        '''
        Return a Nx3 array indicating the multi dim index on the grid
        '''
        indices = self.map_to_grid_dll.map_to_grid2(
            points = points,
            points_shape = np.ascontiguousarray(points.shape, dtype=np.uint64),
            unit_per_grid = self.unit_per_grids,
            min_roi = self.min_roi,
            max_roi = self.max_roi,
        )

        return indices


    def map_points_rmi(self, points : np.ndarray):
        '''
        Return a Nx1 array indicating the index in row major order on the grid
        '''
        indices = self.map_to_grid_dll.map_to_grid_rmi(
            points = points,
            points_shape = np.ascontiguousarray(points.shape, dtype=np.uint64),
            unit_per_grid = self.unit_per_grids,
            min_roi = self.min_roi,
            max_roi = self.max_roi,
            grid_shape = self.grid_shape
        )

        return indices
    

    

    def grid_index_to_ijk(self, index):
        return _grid_index_to_ijk_njit(index, self.grid_shape[1], self.grid_shape[2])
        z = index % self.grid_shape[2]
        index = index // self.grid_shape[2]
        
        y = index % self.grid_shape[1]
        index = index // self.grid_shape[1]

        return index, y, z

    
    def ijk_to_grid_index(self, i, j, k):
        return _ijk_to_grid_index_njit(i, j, k, self.grid_shape[1], self.grid_shape[2])
        return k + self.grid_shape[2] * (j + self.grid_shape[1] * i);


@njit
def _grid_index_to_ijk_njit(index, grid_shape_1, grid_shape_2):
    z = index % grid_shape_2
    index = index // grid_shape_2
    
    y = index % grid_shape_1
    index = index // grid_shape_1

    return index, y, z

@njit('u8(u8, u8, u8, u8, u8)')
def _ijk_to_grid_index_njit(i, j, k, grid_shape_1, grid_shape_2):
    return k + grid_shape_2 * (j + grid_shape_1 * i)


if __name__ == "__main__":
    grid = AxisAlignedGrid(
        unit_per_grids=[1, 1, 1],
        min_roi=[-10, -10, 0],
        max_roi=[10, 10, 1]

    )

    print(grid.grid_shape)

    print(grid)
        
    # print(grid.grid_min_roi[0, 0, 0])
    # print(grid.grid_max_roi[0, 0, 0])

    # print(grid.grid_min_roi[19, 19, 0])
    # print(grid.grid_max_roi[19, 19, 0])

    
    points = np.array([
        [1, 7, 0],
        [2, 6, 2],
        [100, 100, 0]
    ], dtype=np.float64)
    indices = grid.map_points(points)
    
    for p, i in zip(points, indices):
        print(p, i, grid.grid_min_roi[i[0], i[1], i[2]], grid.grid_max_roi[i[0], i[1], i[2]] )

