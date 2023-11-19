from set_basic_config import *
from numba_variable_initialization import *

@njit
def find_neighbours(idx0, idx1, idx2, _range = 1):
    neighbours = NList.empty_list(T_Tuple_type_3)
    for x in range(idx0 - _range, idx0 + _range + 1):
        for y in range(idx1 - _range, idx1 + _range + 1):
            for z in range(idx2 - _range, idx2 + _range + 1):
                if (x, y, z) != (idx0, idx1, idx2):
                    neighbours.append((x, y, z))
    return neighbours

@njit
def cluster(dfs_grids, grid_hash_table, neighbours_range = 1):

    cluster_table = np.full(len(dfs_grids), -1)
    cluster_cnt = -1
    for i in range(len(dfs_grids)):
        if cluster_table[i] == -1:
            cluster_cnt += 1
            
            stack = NList.empty_list(int32)
            stack.append(i)

            while len(stack):
                cur = stack.pop()
                cluster_table[cur] = cluster_cnt
                neighbours = find_neighbours(dfs_grids[cur][0], dfs_grids[cur][1], dfs_grids[cur][2], neighbours_range)
                for neighbour in neighbours:
                    if neighbour in grid_hash_table and cluster_table[grid_hash_table[neighbour]] == -1:
                        stack.append(grid_hash_table[neighbour])
    return cluster_table, cluster_cnt + 1

@njit
def pre_work_for_objects_dfs(valid_tiles_by_xy, grid_to_points):
    dfs_grids = NList.empty_list(T_Tuple_type_3)
    hash_table = NDict.empty(
        key_type = T_Tuple_type_3,
        value_type = int32
    ) 
    grids_table = NDict.empty(
        key_type = T_Tuple_type_2,
        value_type = T_ListType
    ) 
    for k in grid_to_points:
        if (k[0], k[1]) not in valid_tiles_by_xy:
            continue
        if (k[0], k[1]) not in grids_table and k[2] not in valid_tiles_by_xy[(k[0], k[1])]:
            grids_table[(k[0], k[1])] = NList.empty_list(int32)
        if k[2] not in valid_tiles_by_xy[(k[0], k[1])]:
            grids_table[(k[0], k[1])].append(k[2])
    
    cnt = 0
    for k in grids_table:
        for z in grids_table[k]:
            hash_table[(k[0], k[1], z)] = cnt
            dfs_grids.append((k[0], k[1], z))
            cnt += 1
    return dfs_grids, hash_table


@njit
def get_objects_cluster_points(objects_dfs_grids, objects_cluster_table, objects_cluster_num, grid_to_points):
    objects_cluster_points = NList.empty_list(T_ListType)
    for i in range(objects_cluster_num + 1):
        grids_indices = objects_dfs_grids[objects_cluster_table == i]
        # if len(grids_indices) < 150:
        #     continue
        _objects_cluster_points = NList.empty_list(int32)
        for grid_idx in grids_indices:
            for point in grid_to_points[(grid_idx[0], grid_idx[1], grid_idx[2])]:
                _objects_cluster_points.append(point)
        if len(_objects_cluster_points) < 150:
            continue
        objects_cluster_points.append(_objects_cluster_points)
    # print(_objects_cluster_points)
    return objects_cluster_points


def object_cluster(point_data, unit_size = [0.1, 0.1, 0.1]):

    grid_data = Initialize_Grid(point_data = point_data, unit_size = unit_size)

    grid, points_to_grid_dict, grid_to_points_dict, valid_bottom_tiles_by_xy, stacked_bottom_tiles_to_points_by_xy = grid_data

    objects_dfs_grids, objects_hash_table = pre_work_for_objects_dfs(valid_bottom_tiles_by_xy, grid_to_points_dict)

    objects_cluster_table, objects_cluster_num = cluster(objects_dfs_grids, objects_hash_table, 1)

    objects_dfs_grids = np.asarray(objects_dfs_grids)

    objects_cluster_points = get_objects_cluster_points(objects_dfs_grids, objects_cluster_table, objects_cluster_num, grid_to_points_dict)
    
    return objects_cluster_points

if __name__ == '__main__':

    point_data = np.random.rand(10000000, 3)

    cluster = object_cluster(point_data, unit_size = [0.2, 0.2, 0.1])

    print(f"{len(cluster)} cluster")