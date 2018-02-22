set PROJECT_FOLDER=D:\code\github\edanvoye\photogrammetry_example_seashell
set OPENMVG_BIN=d:\bin\openmvg
set SENSOR_DATABASE=D:\code\github\openMVG\src\openMVG\exif\sensor_width_database\sensor_width_camera_database.txt

set IMAGE_FOLDER=%PROJECT_FOLDER%\jpg

%OPENMVG_BIN%\openMVG_main_SfMInit_ImageListing.exe -i "%IMAGE_FOLDER%" -o "%PROJECT_FOLDER%\matches" -d "%SENSOR_DATABASE%" -c 3
%OPENMVG_BIN%\openMVG_main_ComputeFeatures.exe -i "%PROJECT_FOLDER%\matches\sfm_data.json" -o "%PROJECT_FOLDER%\matches" -m SIFT -f 1
%OPENMVG_BIN%\openMVG_main_ComputeMatches.exe -i "%PROJECT_FOLDER%\matches\sfm_data.json" -o "%PROJECT_FOLDER%\matches" -f 1 -n ANNL2
%OPENMVG_BIN%\openMVG_main_IncrementalSfM.exe -i "%PROJECT_FOLDER%\matches\sfm_data.json" -m "%PROJECT_FOLDER%\matches" -o "%PROJECT_FOLDER%\recons"
%OPENMVG_BIN%\openMVG_main_ConvertSfM_DataFormat.exe -i "%PROJECT_FOLDER%\recons\sfm_data.bin" -o "%PROJECT_FOLDER%\recons\sfm_data.json"
python "%PROJECT_FOLDER%\add_markers.py" "%PROJECT_FOLDER%\recons\sfm_data.json"
%OPENMVG_BIN%\openMVG_main_ControlPointsRegistration.exe -i "%PROJECT_FOLDER%\recons\sfm_data_markers.json" -o "%PROJECT_FOLDER%\recons\sfm_data_aligned.bin"

REM sfm_data_aligned.bin is properly aligned and scaled

%OPENMVG_BIN%\openMVG_main_openMVG2openMVS.exe -i "%PROJECT_FOLDER%\recons\sfm_data_aligned.bin" -o "%PROJECT_FOLDER%\recons\test.mvs" -d "%PROJECT_FOLDER%\undistort"

set OPENMVS_BIN=d:\bin\openmvs
MKDIR "%PROJECT_FOLDER%\mvs"
COPY "%PROJECT_FOLDER%\recons\test.mvs" "%PROJECT_FOLDER%\mvs\test.mvs"
%OPENMVS_BIN%\DensifyPointCloud.exe test.mvs -w "%PROJECT_FOLDER%\mvs" -v 2 --resolution-level 2 --estimate-colors 1
%OPENMVS_BIN%\ReconstructMesh.exe test.mvs -w "%PROJECT_FOLDER%\mvs" -v 2 --decimate 1 --smooth 20 --quality-factor 1.0 --thickness-factor 0.1 --close-holes 20 --min-point-distance 2.5
%OPENMVS_BIN%\RefineMesh.exe test_mesh.mvs -w "%PROJECT_FOLDER%\mvs" -v 2 --close-holes 0 --decimate 1 --max-face-area 0 --scales 1 --regularity-weight 0.05 --rigidity-elasticity-ratio 1.0


