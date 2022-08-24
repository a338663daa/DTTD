import numpy as np
import cv2
import open3d as o3d

def pointcloud_from_rgb_depth(rgb, depth, depth_scale, intrinsic, distortion, prune_zero=True):

    points = np.array([[(k, i) for k in range(depth.shape[1])] for i in range(depth.shape[0])]).reshape((-1, 2)).astype(np.float32)
    Z = depth.flatten() * depth_scale

    f_x = intrinsic[0, 0]
    f_y = intrinsic[1, 1]
    c_x = intrinsic[0, 2]
    c_y = intrinsic[1, 2]

    rgb = rgb.reshape((-1, 3))

    if prune_zero:
        points = points[Z > 0]
        rgb = rgb[Z > 0]
        Z = Z[Z > 0]

    # Step 1. Undistort.
    points_undistorted = cv2.undistortPoints(np.expand_dims(points, 1), intrinsic, distortion, P=intrinsic)
    points_undistorted = np.squeeze(points_undistorted, axis=1)

    # Step 2. Reproject.
    pts_xyz = np.zeros((points_undistorted.shape[0], 3))

    pts_xyz[:,0] = (points_undistorted[:, 0] - c_x) / f_x * Z
    pts_xyz[:,1] = (points_undistorted[:, 1] - c_y) / f_y * Z
    pts_xyz[:,2] = Z

    pcld = o3d.geometry.PointCloud()
    pcld.points = o3d.utility.Vector3dVector(pts_xyz)
    pcld.colors = o3d.utility.Vector3dVector(rgb.astype(np.float32) / 255.)

    return pcld

def unproject_pixels(pixels, depths, depth_scale, intrinsic, distortion):
    f_x = intrinsic[0, 0]
    f_y = intrinsic[1, 1]
    c_x = intrinsic[0, 2]
    c_y = intrinsic[1, 2]

    depths = depths.astype(np.float32) * depth_scale

    # Step 1. Undistort.
    pixels_undistorted = cv2.undistortPoints(np.expand_dims(pixels, 1), intrinsic, distortion, P=intrinsic)
    pixels_undistorted = np.squeeze(pixels_undistorted, axis=1)

    # Step 2. Reproject.
    pts_xyz = np.zeros((pixels_undistorted.shape[0], 3))

    pts_xyz[:,0] = (pixels_undistorted[:, 0] - c_x) / f_x * depths
    pts_xyz[:,1] = (pixels_undistorted[:, 1] - c_y) / f_y * depths
    pts_xyz[:,2] = depths

    return pts_xyz

def apply_affine_to_points(points, aff):
    ones = np.ones((points.shape[0], 1))
    points_homo = np.hstack((points, ones))
    points_homo_aff = points_homo @ aff.T
    return np.ascontiguousarray(points_homo_aff[:,:3])
    