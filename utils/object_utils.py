import numpy as np
import open3d as o3d
import pandas as pd
import trimesh

import os, sys 
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, ".."))

from utils.mesh_utils import convert_mesh_uvs_to_colors

dir_path = os.path.dirname(os.path.realpath(__file__))
object_dir = os.path.join(dir_path, "..", "objects")

object_ids_csv = os.path.join(object_dir, "objectids.csv")
object_ids_df = pd.read_csv(object_ids_csv)

"""
loads all meshes into an object dict:
{object_id: {'name': name, 'mesh': object mesh (o3d.geometry.TriangleMesh)}}
"""
def load_object_meshes(object_ids):
    object_ids_and_names = []
    for object_id in object_ids:
        object_row = object_ids_df.loc[object_ids_df['id'] == object_id]
        if not object_row.empty:
            object_ids_and_names.append((object_id, object_row['name'].item()))
        else:
            raise KeyError("ERROR, Object {0} not valid".format(object_id))

    object_meshes = {}
    for object_id, object_name in object_ids_and_names:
        obj_path = os.path.join(object_dir, object_name, object_name + ".obj")
        obj_mesh = o3d.io.read_triangle_mesh(obj_path)
        obj_mesh = convert_mesh_uvs_to_colors(obj_mesh)

        object_meshes[object_id] = {'name': object_name, 'mesh': obj_mesh}

    return object_meshes

def load_all_object_meshes():
    object_meshes = {}
    for _, row in object_ids_df.iterrows():
        object_id, object_name = row
        obj_path = os.path.join(object_dir, object_name, object_name + ".obj")
        obj_mesh = o3d.io.read_triangle_mesh(obj_path)
        obj_mesh = convert_mesh_uvs_to_colors(obj_mesh)

        object_meshes[object_id] = {'name': object_name, 'mesh': obj_mesh}

    return object_meshes

#Uses trimesh library to load meshes instead of Open3D
def load_object_meshes_trimesh(object_ids):
    object_ids_and_names = []
    for object_id in object_ids:
        object_row = object_ids_df.loc[object_ids_df['id'] == object_id]
        if not object_row.empty:
            object_ids_and_names.append((object_id, object_row['name'].item()))
        else:
            raise KeyError("ERROR, Object {0} not valid".format(object_id))

    object_meshes = {}
    for object_id, object_name in object_ids_and_names:
        obj_path = os.path.join(object_dir, object_name, object_name + ".obj")
        obj_mesh = trimesh.load(obj_path)
        object_meshes[object_id] = {'name': object_name, 'mesh': obj_mesh}

    return object_meshes

def get_objectids():
    return np.array(object_ids_df['id'])
