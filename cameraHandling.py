import logging
import os
import subprocess
import sys
import time

import gphoto2 as gp


class Camera:
    def __init__(self):
        #self.singletonInstance = None
        self.log = logging.getLogger(__name__)
        loggingLevel = 10
        handler = logging.StreamHandler()
        handler.setLevel(loggingLevel)
        #format = logging.Formatter('%(name)s -- %(levelname)s -- %(message)s')
        format = logging.Formatter('%(levelname)s -- %(message)s')
        handler.setFormatter(format)
        self.log.addHandler(handler)
        self.log.info("Initializing...")
        self.camera = gp.Camera()
        self.camera.init()
        self._initializeConfig()

    def __new__(cls):
        if not cls._singletonInstance:
            cls._singletonInstance = cls.__init__(cls)
        return cls._singletonInstance

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

    def adjustSettings(self, settingName, settingValue):
        setting = gp.gp_widget_get_child_by_name(self._config,settingName)
        settingValue = gp.gp_widget_get_choice(setting, settingValue)
        gp.gp_widget_set_value(setting, settingValue)
        gp.gp_camera_set_config(self.camera,self._config)
        self._config = self.camera.get_config() #update local config value to match the camera
        #TODO: Make this Object Oriented? 

    def takePhoto(self, folderName):
        self.log.info("Capturing Photo...")
        #TODO: ensure capture target is properly setup?
        #self.adjustSettings('capturetarget', 1)
        file_path = gp.check_result(gp.gp_camera_capture(self.camera, gp.GP_CAPTURE_IMAGE))
        target = os.path.join(folderName, file_path.name)
        camera_file = gp.check_result(gp.gp_camera_file_get(self.camera, file_path.folder, file_path.name, gp.GP_FILE_TYPE_RAW))
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
