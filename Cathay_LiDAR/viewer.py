import open3d as o3d
import laspy
# from coord_tools import *
import numpy as np


path = 'C:/Users/Hp/Desktop/CathayHackathon/Cathay_LiDAR/point_cloud.ply'


# point_data, color_data = HK80_LAS_FILE(path)
# point_cloud = o3d.geometry.PointCloud()

# point_cloud.points = point_data
# point_cloud.colors = color_data

point_cloud = o3d.io.read_point_cloud(path)
# Create an Open3D point cloud

vis = o3d.visualization.Visualizer()
vis.create_window(height=500, width=500, left=1450)
vis.add_geometry(point_cloud)
# o3d.visualization.draw_geometries([point_cloud])
vis.run()


vis.destroy_window()