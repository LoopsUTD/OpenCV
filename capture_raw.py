import logging
import os
import subprocess
import sys
import time

import gphoto2 as gp

def main():
    logging.basicConfig(
        format='%(levelname)s: %(name)s: %(message)s', level=logging.WARNING)
    gp.check_result(gp.use_python_logging())
    camera = gp.check_result(gp.gp_camera_new())
    gp.check_result(gp.gp_camera_init(camera))
    
    configStartTime = time.time()*1000
     # get configuration tree
    config = gp.check_result(gp.gp_camera_get_config(camera))
    # find the capture target config item
    capture_target = gp.check_result(
        gp.gp_widget_get_child_by_name(config, 'capturetarget'))
    
    value = gp.check_result(gp.gp_widget_get_choice(capture_target, 1))
    gp.check_result(gp.gp_widget_set_value(capture_target, value))
    # set config
    gp.check_result(gp.gp_camera_set_config(camera, config))    
    endConfig = time.time()*1000
    
    #print('Capturing image')
    imgTimeStart = time.time()*1000
    file_path = gp.check_result(gp.gp_camera_capture(camera, gp.GP_CAPTURE_IMAGE))
    #print('Camera file path: {0}/{1}'.format(file_path.folder, file_path.name))
    target = os.path.join('RAW/', file_path.name)
    endImgCap = time.time()*1000
    #print('Copying image to', target)
    saveImgStart = time.time()*1000
    camera_file = gp.check_result(gp.gp_camera_file_get(camera, file_path.folder, file_path.name, gp.GP_FILE_TYPE_RAW))
    gp.check_result(gp.gp_file_save(camera_file, target))
    saveImgEnd= time.time()*1000
    subprocess.call(['xdg-open', target])
    gp.check_result(gp.gp_camera_exit(camera))
    #print("Config Time: %f" % (endConfig - configStartTime))
    #print("Img Capture Time: %f" % (endImgCap - imgTimeStart))
    #print("Img Save Time: %f" % (saveImgEnd - saveImgStart))
    return 0

if __name__ == "__main__":
    sys.exit(main())