import open3d as o3d
import laspy
# from coord_tools import *
import numpy as np
import matplotlib.pyplot as plt
from numba.typed import List as NList
from numba import njit

paths = ['C:/Users/Hp/Desktop/CathayHackathon/Cathay_pcd/luggage1.ply', 'C:/Users/Hp/Desktop/CathayHackathon/Cathay_pcd/luggage2.ply']


def show_pcd(pcd):
    o3d.visualization.draw_geometries([pcd])

def visualize_pcd(pcd_array, xyz1, xyz2):
    plt.scatter(pcd_array[:,xyz1], pcd_array[:,xyz2])


def rotate(pcd_array, angle):
    mid_point_y = np.mean(pcd_array[:,1])
    mid_point_z = np.mean(pcd_array[:,2])
    mid_point_x = np.mean(pcd_array[:,0])
    pcd_array[:,1] = pcd_array[:,1] - mid_point_y
    pcd_array[:,2] = pcd_array[:,2] - mid_point_z
    pcd_array[:,0] = pcd_array[:,0] - mid_point_x
    pcd_array = np.hstack((pcd_array,np.ones((pcd_array.shape[0],1))))
    pcd_array = pcd_array.T

    rotator_x = np.array([[1,0,0, 0],[0,-np.cos(angle),np.sin(angle),0], [0, -np.sin(angle), -np.cos(angle),0], [0,0,0,1]])
    rotator_y = np.array([[-np.cos(angle),0,-np.sin(angle), 0],[0,1,0,0], [np.sin(angle), 0, -np.cos(angle),0], [0,0,0,1]])
    rotator_z = np.array([[np.cos(angle), 0, np.sin(angle), 0],[0,1,0,0], [-np.sin(angle), 0, np.cos(angle),0], [0,0,0,1]])
    res = rotator_x @ pcd_array

    res = res.T
    res = res[:,[0,1,2]]

    return res


# @njit
# def get_array_from_pcd(pcd):
#     return np.asarray

# point_data, color_data = HK80_LAS_FILE(path)
# point_cloud = o3d.geometry.PointCloud()

# point_cloud.points = point_data
# point_cloud.colors = color_data
print(f'INFO : Loading point cloud ...')



# vis2 = o3d.visualization.Visualizer()
# vis2.create_window(height=500, width=500)
# vis2.add_geometry(original_pcd)

print(f'INFO : Removing ground surface ...')
point_cloud = o3d.io.read_point_cloud(paths[0])
point_cloud2 = o3d.io.read_point_cloud(paths[1])

pcd_array = np.asarray(point_cloud.points, dtype=object)
pcd_array2 = np.asarray(point_cloud2.points, dtype=object)
# pcd1_points = pcd_array[pcd_array[:,0]> 0]
# pcd2_points = pcd_array[pcd_array[:,0]< 0]
# pcd1_points = pcd1_points[pcd1_points[:,2] > -0.52]
# pcd2_points = pcd2_points[pcd2_points[:,2] > -0.52]
# luggage1 = o3d.geometry.PointCloud()
# luggage2 = o3d.geometry.PointCloud()
# luggage1.points = o3d.utility.Vector3dVector(pcd1_points)
# luggage2.points = o3d.utility.Vector3dVector(pcd2_points)

# @njit
def get_dimension(pcd_array):

    _length = np.max(pcd_array[:,0])-np.min(pcd_array[:,0])
    _width = np.max(pcd_array[:,1])-np.min(pcd_array[:,1])
    height = np.max(pcd_array[:,2])-np.min(pcd_array[:,2])


    length = max(_length, _width)
    width = min(_length, _width)

    return length, width, height





# length = obb1.extent[0]
# width = obb1.extent[1]r
# height = obb1.extent[2]




length, width, height = get_dimension(pcd_array)


print(f'INFO : Getting dimension ...')
pcd_array = rotate(pcd_array, 90)

print(f'Cargo 1 dimension : ')
print(f'Height : {round(height,2)} meters\nLength: {round(length,2)} meters\nWidth : {round(width, 2)} meters')
print(f'-----------------------------------------------------------')

length, width, height = get_dimension(pcd_array2) 

print(f'INFO : Getting dimension ...')
pcd_array2 = rotate(pcd_array2, 90)

print(f'Cargo 2 dimension : ')
print(f'Height : {round(height,2)} meters\nLength: {round(length,2)} meters\nWidth : {round(width, 2)} meters')


point_cloud = o3d.geometry.PointCloud()

point_cloud.points = o3d.utility.Vector3dVector(pcd_array) 

obb1 = point_cloud.get_oriented_bounding_box()
obb1.color = [0, 1, 0]

vis = o3d.visualization.Visualizer()
vis.create_window(height=500, width=500)
vis.add_geometry(point_cloud)
vis.add_geometry(obb1)


### pcd2 

point_cloud2 = o3d.geometry.PointCloud()

point_cloud2.points = o3d.utility.Vector3dVector(pcd_array2) 

obb2 = point_cloud2.get_oriented_bounding_box()
obb2.color = [0, 1, 0]




vis2 = o3d.visualization.Visualizer()
vis2.create_window(height=500, width=500, top=560)
vis2.add_geometry(point_cloud2)
vis2.add_geometry(obb2)


print(f'DONE.')
# vis2.run()
vis.run()

# vis2.destroy_window()
vis.destroy_window()
vis2.run()
vis2.destroy_window()

# o3d.visualization.draw_geometries([point_cloud, obb1])

