import logging
import os
import subprocess
import sys
import time

import gphoto2 as gp


class Camera(object):
    _singletonInstance = None
    
    @staticmethod
    def getInstance():
        if Camera._singletonInstance == None:
            Camera()
        
        return Camera._singletonInstance

    def __init__(self):   
        if Camera._singletonInstance != None:
            raise Exception("Critical Error: Camera is a Singleton!")
        else:
            Camera._singletonInstance = self
            self.log = logging.getLogger("mainApp")
            self.log.info("Initializing Camera...")
            self.camera = gp.Camera()
            self.camera.init()
            self._captureMode = None
            self._initializeConfig()

    def _initializeConfig(self):
        self._config = self.camera.get_config()
        self.mainConfigs = {
        'capturetarget': None,
        'iso': None,
        'f-number':None,
        'shutterspeed': None,
        'imagequality': None,
        'imagesize': None
        }
        self._updateMainConfigs()
        

    def _updateMainConfigs(self):
        self.log.info("Parsing 'mainConfigs'")
        for sections in self._config.get_children():
            if "settings" not in sections.get_name(): #TODO: update this 
                continue
            for child in sections.get_children():
                if child.get_name() not in self.mainConfigs:
                    continue
                choicelist = []
                if child.get_type() == 5:
                    for choice in child.get_choices():
                        choicelist.append(choice)
                self.mainConfigs[child.get_name()] = [child.get_value(), choicelist]
        self._updateCaptureMode()
        self.log.debug(str(self.mainConfigs))

    def adjustSettings(self, settingName, settingValue):
        setting = gp.gp_widget_get_child_by_name(self._config,settingName)
        settingValue = gp.gp_widget_get_choice(setting, settingValue)
        gp.gp_widget_set_value(setting, settingValue)
        gp.gp_camera_set_config(self.camera,self._config)
        self._config = self.camera.get_config() #update local config value to match the camera
        self._updateMainConfigs()


    def _updateCaptureMode(self):
        if str(self.mainConfigs['imagequality']).lower()[0] == 'j':
            self._captureMode = gp.GP_FILE_TYPE_NORMAL
        elif str(self.mainConfigs['imagequality']).lower()[0] == 'n':
            self._captureMode = gp.GP_FILE_TYPE_RAW

    def takePhoto(self, folderName, prefix=None):
        self.log.info("Capturing Photo...")
        #TODO: ensure capture target is properly setup?
        #self.adjustSettings('capturetarget', 1)
        file_path = gp.check_result(gp.gp_camera_capture(self.camera, gp.GP_CAPTURE_IMAGE))
        if prefix is not None:
            target = os.path.join(folderName, str(prefix) + file_path.name )
        else:
            target = os.path.join(folderName, file_path.name)
        camera_file = gp.check_result(gp.gp_camera_file_get(self.camera, file_path.folder, file_path.name, self._captureMode))
        gp.check_result(gp.gp_file_save(camera_file, target))
        return target


    def getCameraSummary(self):
        self.log.info("Return Camera Summary:")
        return self.camera.get_summary()


    def close(self):
        self.log.info("Camera is exiting")
        self.camera.exit()

if __name__ == "__main__":
    print('Potato')
