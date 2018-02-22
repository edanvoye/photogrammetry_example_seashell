# Sample code: Detect Aruco Markers and add them to the OpenMVG json SfM scene file
# Author: Etienne Danvoye

import cv2
import json
import sys
import os

def add_aruco_markers(sfm_filename):

    # Generate Aruco Board
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

    # These are our desired positions for the markers
    marker_info = {       
    
        # Markers from new Aruco calibration panel
        # These are the desired world position of the markers
        'aruco_0':  (0.0, 4.0, 0.0),
        'aruco_1':  (1.5, 4.0, 0.0),
        'aruco_2':  (3.0, 4.0, 0.0),
        'aruco_3':  (4.5, 4.0, 0.0),
        'aruco_4':  (6.0, 4.0, 0.0),

        'aruco_5':  (0.0, 2.5, 0.0),
        'aruco_6':  (1.5, 2.5, 0.0),
        'aruco_7':  (3.0, 2.5, 0.0),
        'aruco_8':  (4.5, 2.5, 0.0),
        'aruco_9':  (6.0, 2.5, 0.0),

        'aruco_10': (0.0, 1.0, 0.0),
        'aruco_11': (1.5, 1.0, 0.0),
        'aruco_12': (3.0, 1.0, 0.0),
        'aruco_13': (4.5 ,1.0, 0.0),
        'aruco_14': (6.0, 1.0, 0.0),
    }

    # sfm_filename needs to be a SfM file in json format
    if not '.json' in sfm_filename:
        raise Exception("First convert SfM file to json")

    # Load json SFM Data
    with open(sfm_filename, 'r') as f:
        sfm_data = json.load(f)

    # Clear existing control points
    sfm_data['control_points'] = []

    marker_index = 0
    marker_dict = {}

    # Detect markers
    root_path = sfm_data['root_path']
    for view in sfm_data['views']:
        filename = view['value']['ptr_wrapper']['data']['filename']
        full_path = os.path.join(root_path, filename)

        print 'Detecting markers in %s' % filename

        # Read image file
        img = cv2.imread(full_path, cv2.IMREAD_UNCHANGED)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # detect aruco markers in image
        corners,ids,rejected = cv2.aruco.detectMarkers(gray, aruco_dict)

        print '--- %d markers found' % len(corners)

        if len(corners)>0:
            for corner,marker_id in zip(corners, ids):

                marker_name = 'aruco_%d' % marker_id
                marker_upper_left = corner[0][0]

                if marker_name not in marker_info:
                    continue

                # Create new marker
                if marker_name not in marker_dict:
                    item = {}
                    item['key'] = marker_index
                    marker_index = marker_index + 1
                    item['value'] = {}
                    item['value']['X'] = list(marker_info[marker_name])
                    item['value']['observations'] = []

                    marker_dict[marker_name] = item
                    sfm_data['control_points'].append(item)
                else:
                    item = marker_dict[marker_name]

                #  Add observation to marker
                obs = {}
                obs['key'] = view['value']['ptr_wrapper']['data']['id_view']
                obs['value'] = {}
                obs['value']['id_feat'] = 0 # not used for control_points                        
                obs['value']['x'] = [float(marker_upper_left[0]),float(marker_upper_left[1])]
                item['value']['observations'].append( obs )

    # Write new json
    json_file_with_markers = os.path.splitext(sfm_filename)[0] + '_markers.json'
    with open(json_file_with_markers, 'w') as f:
        print 'Writing json file %s' % json_file_with_markers
        json_str = json.dumps(sfm_data)
        f.write(json_str)
    
if __name__ == "__main__":

    add_aruco_markers(sys.argv[1])
    