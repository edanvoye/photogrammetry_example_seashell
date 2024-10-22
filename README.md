# Photogrammetry Example: Seashell

This is an example imageset with associated scripts to illustrate the usage of Control Point Registration in OpenMVG.

* Camera: Canon EOS 5D Mark IV
* Lens: Canon 85mm f1.2 at f16
* Image Resolution: 6720 x 4480
* Sensor Pixel size: 0.00536 mm
* f = 85 mm / 0.00536 mm/pixels = 15858 pixels

Executing the script requires the new exe in this PR : https://github.com/openMVG/openMVG/pull/1239

![alt text](https://github.com/edanvoye/photogrammetry_example_seashell/raw/master/jpg/M97A2474.JPG)


<a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/">Creative Commons Attribution-NonCommercial 4.0 International License</a>.

## Aruco Board

The aruco board used to scale and align the object can be created as a 300 dpi image file with the following code : 

    import cv2
    import cv2.aruco as aruco

    # Generate Aruco Board
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    board = cv2.aruco.GridBoard_create(5, 3, 1.0, 0.5, aruco_dict) # unit is cm

    # Save aruco board as 300 dpi image
    cm_to_inch = 0.3937007874
    img = board.draw((int(300*7*cm_to_inch), int(300*4*cm_to_inch))) # 300 dpi
    cv2.imwrite(r'aruco_DICT_4X4_300dpi_7cm_4cm.png', img)
