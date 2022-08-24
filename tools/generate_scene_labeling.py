"""
Uses MetadataGenerator and SemanticLabelingGenerator to generate scene labeling:
Specifically generates 00000_label.png and 00000_meta.json.
"""

import argparse
import numpy as np
import yaml

import os, sys 
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, ".."))

from data_processing import CameraPoseSynchronizer
from pose_refinement import ScenePoseRefiner
from scene_labeling_generation import MetadataGenerator, SemanticLabelingGenerator
from utils.constants import SCENES_DIR
from utils.object_utils import load_object_meshes
from utils.pose_dataframe_utils import convert_pose_df_to_dict

def main():
    parser = argparse.ArgumentParser(description='Generate semantic labeling and meta labeling')
    parser.add_argument('scene_name', type=str, help='scene directory (contains scene_meta.yaml and data (frames) and camera_poses)')
    parser.add_argument('--refine', action='store_true')
    parser.add_argument('--no-refine', dest='refine', action='store_false')
    parser.add_argument('--icp_refine', action='store_true')
    parser.add_argument('--no-icp-refine', dest='icp_refine', action='store_false')
    parser.add_argument('--fast', default=False, action='store_true')
    parser.add_argument('--use-prev-refinement', default=False, action='store_true')
    parser.add_argument('--use-prev-obj-poses', default=False, action='store_true', help='use the object poses created during a previous call to this tool to generate semantic segmentations only.')
    parser.set_defaults(refine=True, icp_refine=True)

    args = parser.parse_args()

    scene_dir = os.path.join(SCENES_DIR, args.scene_name)

    scene_metadata_file = os.path.join(scene_dir, "scene_meta.yaml")
    with open(scene_metadata_file, 'r') as file:
        scene_metadata = yaml.safe_load(file)
    
    objects = load_object_meshes(scene_metadata["objects"])

    if args.refine and len(objects) == 1:
        print("WARNING!, ICP refinement with only 1 object is dangerous. May result in bad ICP result.")

    if args.fast:
        num_points = 10000
    else:
        num_points = 1000000

    if not args.use_prev_obj_poses:
        annotated_poses_csv = os.path.join(scene_dir, "annotated_object_poses", "annotated_object_poses.yaml")
        with open(annotated_poses_csv, "r") as file:
            annotated_poses_data = yaml.safe_load(file)

        annotated_poses_frameid = annotated_poses_data["frame"]
        annotated_poses = annotated_poses_data["object_poses"]
        annotated_poses = {k: np.array(v) for k, v in annotated_poses.items()}

        cam_pose_sync = CameraPoseSynchronizer()

        if args.use_prev_refinement:
            synchronized_poses_csv = os.path.join(scene_dir, "camera_poses", "camera_poses_synchronized_refined.csv")
        else:
            synchronized_poses_csv = os.path.join(scene_dir, "camera_poses", "camera_poses_synchronized.csv")

        synchronized_poses = cam_pose_sync.load_from_file(synchronized_poses_csv)
        synchronized_poses = convert_pose_df_to_dict(synchronized_poses)

        if args.refine:
            scene_pose_refiner = ScenePoseRefiner(objects)
            synchronized_poses = scene_pose_refiner.refine_poses(scene_dir, annotated_poses_frameid, annotated_poses, synchronized_poses, icp_refine=args.icp_refine, write_to_file=True)

        #generate labels
        semantic_labeling_generator = SemanticLabelingGenerator(objects, number_of_points=num_points)
        semantic_labeling_generator.generate_semantic_labels(scene_dir, annotated_poses_frameid, annotated_poses, synchronized_poses, debug=True)

        #metadata labeling requires semantic labeling
        metadata_labeling_generator = MetadataGenerator()
        metadata_labeling_generator.generate_metadata_labels(scene_dir, annotated_poses_frameid, annotated_poses, synchronized_poses)

    else:
        semantic_labeling_generator = SemanticLabelingGenerator(objects, number_of_points=num_points)
        semantic_labeling_generator.generate_semantic_labels_from_obj_poses(scene_dir, debug=True)


if __name__ == "__main__":
    main()
    