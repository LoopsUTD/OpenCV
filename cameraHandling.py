import logging
import os
import subprocess
import sys
import time

import gphoto2 as gp


class Camera(object):
    _singletonInstance = None
    
    # This is a singleton class!!

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
        # self._updateCaptureMode()
        self.log.debug(str(self.mainConfigs))
        # with open('configs.txt', 'w') as configs:
        #     configs.write(str(self.mainConfigs))
        #self.log.debug("imagequality = %s " % str(self.mainConfigs['imagequality'][0]))


    def adjustSettings(self, settingName, settingValue):
        #ObjectOriented?!
        #http://gphoto-software.10949.n7.nabble.com/Beginner-Using-libgphoto2-how-to-find-set-config-values-td16449.html       
        node = self._config.get_child_by_name(settingName)
        node.set_value(settingValue)
        self.camera.set_config(self._config) #'UNSPECIFIED ERROR -> tried to change a "disabled" setting (i.e. RAW image with a "low" resolution makes no sense)
        self._updateMainConfigs()

    def takePhoto(self, folderName, prefix=None):
        self.log.info("Capturing Photo...")
        #TODO: ensure capture target is properly setup?
        #self.adjustSettings('capturetarget', 1)
        file_path = gp.check_result(gp.gp_camera_capture(self.camera, gp.GP_CAPTURE_IMAGE))
        self.log.debug("Capture Path: %s %s" % (file_path.folder, file_path.name))
        if prefix is not None:
            target = os.path.join(folderName, str(prefix) + file_path.name)
        else:
            target = os.path.join(folderName, file_path.name)

        self.log.debug(target)
        
        if str(self.mainConfigs['imagequality'][0]).lower()[0] == 'j':
            self.log.info("Capturing JPEG...")
            camera_file = gp.check_result(gp.gp_camera_file_get(self.camera, file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL))
            self.log.info(camera_file)
            gp.check_result(gp.gp_file_save(camera_file, target))       
        elif str(self.mainConfigs['imagequality'][0]).lower()[0] == 'n':
            self.log.info("Capturing NEF...")
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
