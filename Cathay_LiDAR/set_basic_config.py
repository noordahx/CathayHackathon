import logging
import numpy as np

from numba_variable_initialization import *
from grid.axis_aligned_grid import AxisAlignedGrid

@njit
def map_points_to_each_grid(points_indices):
    grid_point_dict = NDict.empty(
        # key_type=UniTuple(numba.float64, 3),
        key_type = T_Tuple_type_3,
        value_type = T_ListType_64
    )
    for i in range(len(points_indices)):
        t_tuple = (points_indices[i][0], points_indices[i][1], points_indices[i][2])
        if t_tuple not in grid_point_dict:
            grid_point_dict[t_tuple] = NList.empty_list(int64)
        grid_point_dict[t_tuple].append(i)
    return grid_point_dict

def rearrange_grids(all_point_cloud_points, unit_size = [0.1, 0.1, 0.1]):
    _min_roi = [np.min(all_point_cloud_points[:, 0]), np.min(all_point_cloud_points[:, 1]), np.min(all_point_cloud_points[:, 2])]
    _max_roi = [np.max(all_point_cloud_points[:, 0]), np.max(all_point_cloud_points[:, 1]), np.max(all_point_cloud_points[:, 2])]
    print(" Setting grid config...")
    grid = AxisAlignedGrid(unit_per_grids=unit_size, min_roi=_min_roi, max_roi=_max_roi)
    print(f" grid_unit_size: {grid.unit_per_grids} \n grid_shape: {grid.grid_shape} \n min_roi: {_min_roi} \n max_roi: {_max_roi}")
    points_to_grid = grid.map_points(all_point_cloud_points)
    grid_to_points = map_points_to_each_grid(points_to_grid)
    print(f"{len(grid_to_points)} grids contain points")
    return grid, points_to_grid, grid_to_points

@njit
def get_lowest_indices_by_xy(grid_to_points_dict, min_points_per_cube = 20):
    valid_tiles_by_xy = NDict.empty(
        key_type = T_Tuple_type_2,
        value_type = T_ListType_64
    )
    for k in grid_to_points_dict:

        if len(grid_to_points_dict[k]) > min_points_per_cube:
            if (k[0], k[1]) not in valid_tiles_by_xy:
                valid_tiles_by_xy[(k[0], k[1])] = NList.empty_list(int64)
                valid_tiles_by_xy[(k[0], k[1])].append(k[2])
            
            if valid_tiles_by_xy[(k[0], k[1])][0] > k[2]:
                valid_tiles_by_xy[(k[0], k[1])][0] = k[2]

            # if valid_tiles_by_xy[(k[0], k[1])][0] > valid_tiles_by_xy[(k[0], k[1])][1]:
            #     valid_tiles_by_xy[(k[0], k[1])][0] = k[2]
            # else:
            #     valid_tiles_by_xy[(k[0], k[1])][1] = k[2]
    
    for k in valid_tiles_by_xy:
        upper_tile = valid_tiles_by_xy[k][0] + 1
        if (k[0], k[1], upper_tile) not in grid_to_points_dict:
            continue
        if len(grid_to_points_dict[(k[0], k[1], upper_tile)]) > min_points_per_cube:
            valid_tiles_by_xy[(k[0], k[1])].append(upper_tile)

    print(f"{len(valid_tiles_by_xy)} bottom tiles have more than {min_points_per_cube} points")

    stacked_bottom_tiles = NDict.empty(
        key_type = T_Tuple_type_2,
        value_type = T_ListType_64
    ) 
    double_cnt = 0
    for k in valid_tiles_by_xy:
        if len(valid_tiles_by_xy[k]) > 1:
            true_key_1 = (k[0], k[1], valid_tiles_by_xy[k][0])
            true_key_2 = (k[0], k[1], valid_tiles_by_xy[k][1])

            stacked_bottom_tiles[k] = grid_to_points_dict[true_key_1]

            for point in grid_to_points_dict[true_key_2]:
                stacked_bottom_tiles[k].append(point)
                
            double_cnt += 1
        else:
            true_key_1 = (k[0], k[1], valid_tiles_by_xy[k][0])
            stacked_bottom_tiles[k] = grid_to_points_dict[true_key_1]
    print(f"{double_cnt} tiles have 2 bottom tiles in the xy direction and have been stacked")
    return valid_tiles_by_xy, stacked_bottom_tiles



def Initialize_Grid(point_data, unit_size = [0.1, 0.1, 0.1]):
    '''
    OUTPUT:

    gird(class): AxisAlignedGrid((class))

    points_to_grid_dict(dict): { 
    
        Point Index(Int) -> Grid Index(Tuple)

        point_idx_1: (x1, y1, z1),
        ...
    }

    grid_to_points_dict(dict):{ 
    
        Grid Index(Tuple) -> Point Index(List)

        (x1, y1, z1): [point_idx_1, point_idx_2...],
        ...
    }

    valid_bottom_tiles_by_xy(dict):{ 
    
        Grid XY Index(Tuple) -> the top 2/1 lowest Z Index(List)

        (x1, y1): [z1, z2],
        (x2, y2): [z1],
        ...
    }

    stacked_bottom_tiles_to_points_by_xy(dict):{
    
        Grid XY Index(Tuple) -> Point Index(List)

        (x1, y1): [point_idx_1, point_idx_2...],
        ...
    }
    '''

    grid, points_to_grid_dict, grid_to_points_dict = rearrange_grids(point_data, unit_size = unit_size)

    valid_bottom_tiles_by_xy, stacked_bottom_tiles_to_points_by_xy = get_lowest_indices_by_xy(grid_to_points_dict)

    return grid, points_to_grid_dict, grid_to_points_dict, valid_bottom_tiles_by_xy, stacked_bottom_tiles_to_points_by_xy


if __name__ == '__main__':

    point_data = np.random.rand(10000, 3)

    grid_data = Initialize_Grid(point_data = point_data, unit_size = [0.2, 0.2, 0.1])

    grid, points_to_grid_dict, grid_to_points_dict, valid_bottom_tiles_by_xy, stacked_bottom_tiles_to_points_by_xy = grid_data