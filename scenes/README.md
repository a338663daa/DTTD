# Scenes

Each scene contains 2 folders:
1. data
2. camera_poses

`data` is the true output for our dataset in terms of per-frame data. The other stuff is what we use to generate `data`.

`data` contains frames of format `00001_color.jpg`, `00001_depth.png`, `00001_label.png`, `00001_meta.txt`. 
- `00001_color.jpg`: color image (3 channel 8 bit) (comes from camera)
- `00001_depth.png`: depth image (16 bit 1 channel) (comes from camera, aligned to color)
- `00001_label.png`: ground truth semantic segmentation (1 channel 8 bit). We generate this using a virtual camera.
- `00001_meta.json`: ground truth poses of objects in the scene. We calculate this using OptiTrack.

`camera_poses` contains data pertaining to the camera poses:
1. `camera_poses.csv` is raw optitrack pose data
2. `camera_poses_cleaned.csv` is cleaned optitrack pose data
3. `camera_poses_synchronized.csv`:    
    * this contains the virtual camera pose in optitrack coordinates for each frame
    * generated by CameraPoseSynchronizer
    * used by other parts of the codebase
    * not shipped as part of the dataset

Each scene also contains a file:
`scene_meta.yaml`:
* this contains scene level metadata
    * camera intrinsics
    * camera depth scale
    * which objects are in this scene
    * random stuff like time of day?