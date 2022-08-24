
# DTTD: Using OptiTrack output to generate labeled 3D object tracking data

![Demo](doc/images/label_demo.PNG)

## Objects and Scenes data:

Final dataset output:
 * `objects` folder
 * `cameras` folder
 * `scenes` folder certain data:
 	 * `scenes/<scene number>/data/` folder
 	 * `scenes/<scene number>/scene_meta.yaml` metadata
 * `toolbox` folder

# How to run
 1. Setup
	 1. Place ARUCO marker near origin (doesn't actually matter where it is anymore, but makes sense to be near OptiTrack origin)
	 2. Calibrate Opti (if you want, don't need to do this everytime, or else extrinsic changes)
	 3. Place markers on the corners of the aruco marker, use this to compute the aruco -> opti transform
	 	 * Place marker positions into `calculate_extrinsic/aruco_corners.yaml`
 2. Record Data (`tools/capture_data.py`)
     1. ARUCO Calibration
	 2. Data collection
	 	 * If extrinsic scene, data collection phase should be spent observing ARUCO marker
	 3. Example: <code>python tools/capture_data.py --scene_name official_test az_camera</code>
		 
 3. Check if the Extrinsic file exists
	 1. If Extrinsic file doesn't exist, then you need to calculate Extrinsic through Step 4
	 2. Otherwise, process data through Step 5 to generate groundtruth labels
 4. Process iPhone Data (if iPhone Data)
	1. Convert iPhone data formats to Kinect data formats (`tools/process_iphone_data.py`)
		* This tool converts everything to common image names, formats, and does distortion parameter fitting
	2. Continue with step 5 or 6 depending on whether computing an extrinsic or capturing scene data
 5. Process Extrinsic Data to Calculate Extrinsic (If extrinsic scene)
	 1. Clean raw opti poses (`tools/process_data.py`) 
	 2. Sync opti poses with frames (`tools/process_data.py`)
	 3. Calculate camera extrinsic (`tools/calculate_camera_extrinsic.py`)
 6. Process Data (If data scene)
	 1. Clean raw opti poses (`tools/process_data.py`) <br>
	 Example: <code>python tools/process_data.py --scene_name [SCENE_NAME]</code>
	 2. Sync opti poses with frames (`tools/process_data.py`) <br>
	 Example: <code>python tools/process_data.py --scene_name [SCENE_NAME]</code>
	 3. Manually annotate first frame object poses (`tools/manual_annotate_poses.py`)
	 	 1. Modify (`[SCENE_NAME]/scene_meta.yml`) by adding (`objects`) field to the file according to objects and their corresponding ids.<br>
			Example: <code>python tools/manual_annotate_poses.py official_test</code>
	 4. Recover all frame object poses and verify correctness (`tools/generate_scene_labeling.py`) <br>
	 Example: <code>python tools/generate_scene_labeling.py --fast [SCENE_NAME]</code>
	 5. Generate semantic labeling (`tools/generate_scene_labeling.py`)<br>
	 Example: <code>python /tools/generate_scene_labeling.py [SCENE_NAME]</code>
	 6. Generate per frame object poses (`tools/generate_scene_labeling.py`)<br>
	 Example: <code>python tools/generate_scene_labeling.py [SCENE_NAME]</code>


# Minutia
 * Extrinsic scenes have their color images inside of `data` stored as `png`. This is to maximize performance. Data scenes have their color images inside of `data` stored as `jpg`. This is necessary so the dataset remains usable.
 * iPhone spits out `jpg` raw color images, while Azure Kinect skips out `png` raw color images.

# Best Scene Collection Practices
 * Good synchronization phase by observing ARUCO marker, for Azure Kinect keep in mind interference from OptiTrack system.
 * Don't have objects that are in our datasets in the background. Make sure they are out of view!
 * Minimize number of extraneous ARUCO markers/APRIL tags that appear in the scene.
 * Stay in the yellow area for best OptiTrack tracking.
 * Move other cameras out of area when collecting data to avoid OptiTrack confusion.
 * Run `manual_annotate_poses.py` on all scenes after collection in order to archive extrinsic.
 * We want to keep the data anonymized. Avoid school logos and members of the lab appearing in frame.
 * Perform 90-180 revolution around objects, one way. Try to minimize stand-still time.