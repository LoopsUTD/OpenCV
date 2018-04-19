from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.properties import DictProperty
from kivy.properties import StringProperty
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.settings import SettingsWithTabbedPanel
from kivy.config import ConfigParser

import os
from multiprocessing import Process, Manager, Event
import logging
from MoreSettingOptions import SettingScrollOptions, LensHolderOptions

#from linearActuator import LinearActuator
#from cameraHandling import Camera

log = logging.getLogger('uiApp')

class InitializeScreen(Screen):
	myInfoLabel = ObjectProperty()
	myVals = {}

	def __init__(self, **kwargs):
		super(InitializeScreen, self).__init__(**kwargs)
		Clock.schedule_once(self._finish_init)
		print("InitializeScreen is instantiated")
		print 
		self.myRoot = RootWidget.rootIds
		
		
		# btn1 = self.ids['btnDisplay']
		# bt1.bind()
	def _finish_init(self, dt):
		print("finished init InitializeScreen")
		print(self.ids)
		#self.ids.update(self.myVals)
		print(self.ids)

		#myRoot = RootWidget.rootIds

		if self.initializeDisplay():
			self.updateLabelColor(self.ids.btnDisplay)
		else:
			self.updateInfoBox("\nFATAL ERROR: Display Not Working!")

		if self.initializeCamera():
			self.updateLabelColor(self.ids.camInitialize)
		else:
			self.updateInfoBox("\nFATAL ERROR: Camear Not Connected!")

		if self.initializeLensHolder():
			self.updateLabelColor(self.ids.lensInitialize)
		else:
			self.updateInfoBox("\nFATAL ERROR: Camear Not Connected!")

	def updateLabelColor(self,instance):
		print('updating Label...') #TODO: implement logger
		button = instance
		button.disabled = False
		button.background_normal = ""
		button.background_color = [.2,1,.2,.5]

	def onDisplay(self, instance):
		button = instance
		print("testing")
		print(button.color)
		button.disabled = False
		button.background_normal = ""
		button.background_color = [.2,1,.2,.5]
		# button.canvas.before.color.rgba = [.2,1,.2,1]
		#button.canvas.size.pos

	def updateInfoBox(self, text):
		self.myRoot.updateInfoLabel(text)

	def onCameraUpdate(self):
		print("testing Camera Update")
		return "Adding Stuff to camera Update\n"

	def initializeDisplay(self):
		print(App.get_running_app().config.get('Output','defaulttestimage'))
		return False

	def initializeCamera(self):
		#camera = Camera.getInstance()
		ct = App.get_running_app().config.get('Camera','capturetarget')
		fnum = App.get_running_app().config.get('Camera','f-number')
		iso = App.get_running_app().config.get('Camera','iso')
		shutter = App.get_running_app().config.get('Camera','shutterspeed')
		imgqual = App.get_running_app().config.get('Camera','imagequality')

		#camera.adjustSettings('capturetarget', ct)
		#camera.adjustSettings('f-number', fnum)
		# camera.adjustSettings('iso',iso)
		# camera.adjustSettings('shutterspeed', shutter)
		# camera.adjustSettings('imagequality', imgqual)

		# if "JPEG" in imgqual:
		# 	imsize = App.get_running_app().config.get('Camera','imagesize')
		# 	camera.adjustSettings('imagesize', imsize)

		return True

	def initializeLensHolder(self):
		#How to access: https://stackoverflow.com/questions/45663871/kivy-access-configuration-values-from-any-widget
		print(App.get_running_app().config.get('LensHolder','position'))
		#actuator = LinearActuator.getInstance()
		#actuator.move_to(self.myRoot.config)
		return True


class ConfigureScreen(Screen):
	"""docstring for ConfigureScreen"""
	def __init__(self, **kwargs):
		super(ConfigureScreen, self).__init__(**kwargs)
		# self.name = 'configure'
		#self.arg = arg

class LensHomeScreen(Screen):
	"""docstring for LensHomeScreen"""
	def __init__(self, **kwargs):
		super(LensHomeScreen, self).__init__(**kwargs)
		# self.name = 'lensHome'

class CameraSettingsScreen(Screen):
	"""docstring for CameraSettingsScreen"""
	def __init__(self, **kwargs):
		super(CameraSettingsScreen, self).__init__(**kwargs)
		# self.name = 'cameraSettings'

class PrepareScreen(Screen):
	"""docstring for PrepareScreen"""
	def __init__(self, **kwargs):
		super(PrepareScreen, self).__init__(**kwargs)
		#app.open_settings()

class NamingConvScreen(Screen):
	"""docstring for NamingConvScreen"""
	def __init__(self, **kwargs):
		super(NamingConvScreen, self).__init__(**kwargs)

class RunTestScreen(Screen):
	"""docstring for RunTestScreen"""
	def __init__(self, **kwargs):
		super(RunTestScreen, self).__init__(**kwargs)
		print("RunTestScreen: IDS: ")
		self.myRoot = RootWidget.rootIds

	def validateText(self, instance):
		print("user entered: %s", instance.text)
		self.cleanSampleFolderName = self._cleanInputs(instance.text)

		self.myRoot.ids.runTest.disabled = False

	def _cleanInputs(self, usr_input):
		strippedName = usr_input.strip()
		nameWithSlashes = strippedName.replace(' ', '')
		goodName = nameWithSlashes.replace('\\', '')
		betterName = goodName.replace("\'", '')
		bestName = betterName.replace('\"', '')
		return bestName

	def runTest(self):
		self.outputDirectory = App.get_running_app().config.get('Output','defaultpath')
		#Ensure that the user "Validated their text"
		outputFolder = self.cleanSampleFolderName

		print("Test Running - values stored at: %s/%s" % (self.outputDirectory, outputFolder))
		#linearActuator = LinearActuator.getInstance()
		#camera = Camera.getInstance()

		# #TODO: Run Global Magnification
		# #TODO: Alignment Calibration?

		#Move lens out of path:
		# linearActuator.moveOutOfPath()
		# self.ids.runConsole.text += "Captured Image: " + self._takePhotoNowReturnsName(filePrefix="noLens_", sampleFolder=outputFolder) + "\n"
		# linearActuator.moveIntoPath()
		# self.ids.runConsole.text += "Captured Image: " + self._takePhotoNowReturnsName(filePrefix="withLens_", sampleFolder=outputFolder) + "\n"

	def _takePhotoNowReturnsName(self, filePrefix = None, sampleFolder = None):
		if sampleFolder is not None:
			currentOutFolder = self.outputDirectory + "/" + sampleFolder
			self._makeFolder(currentOutFolder)
		else:
			currentOutFolder = self.outputDirectory
		self.log.info("user is storing image in: %s with test photo: %s" % (currentOutFolder, self.testImages))
		self.display.updateImage(self.testImages[0])
		target = self.camera.takePhoto(folderName = currentOutFolder, prefix = filePrefix)
		self.log.info("photo saved at: %s" % target)
		return target

	def _makeFolder(self, dir_path):
		pathlib.Path(dir_path).mkdir(parents=True,exist_ok=True)


class RootWidget(FloatLayout):
	rootIds = None

	def __init__(self, **kwargs):
		super(RootWidget, self).__init__(**kwargs)
		print("Root Widget Instantiated")
		RootWidget.rootIds = self
		#print(self.ids)
		Clock.schedule_once(self._finish_init)
	
	def _finish_init(self, dt):
		print("RootWidget finish Init!")
		#print(self.ids)
		#print(self.ids.sm.get_screen('initialize').ids)


	def updateInfoLabel(self, text):
		self.ids.infoTextLabel.text += text

class LoopsUTDApp(App):
	def __init__(self):
		super(LoopsUTDApp, self).__init__()
	
	def build(self):
		#Builder.load_file("loopsutd.kv")
		self.use_kivy_settings = False
		return self.root

	def build_config(self, config):
		self.settings_cls=SettingsWithTabbedPanel
		config.read('loopsutd.ini')
		#app.open_settings()

	def build_settings(self, settings):
		settings.register_type('scrolloptions', SettingScrollOptions)
		settings.register_type('lensHolderAdjust', LensHolderOptions)
		settings.add_json_panel('Testing', self.config, 'config/outputSettings.json')
		settings.add_json_panel('Camera', self.config, 'config/cameraSettings.json')
		settings.add_json_panel('Lens Holder', self.config, 'config/lensSettings.json')
	
	def on_config_change(self, config, section, key, value):
		print("Config Change Detected!")
		print("Config Changed! Section: %s Key: %s Value: %s" % (section, key, value))
		if key in ['position']:
			print('moving linear actuator to: %d'  % int(value))
			#TODO: update linear actuator position
			#actuator = LinearActuator.getInstance()
			#actuator.move_to(value)

		if key in ['defaulttestimage']:
			print('updating Displayed Image to: %s ' % value)
			#TODO: Update Display

		if section in ['Camera']:
			print('updating Camera Config: %s:%s' %(key, value))
			#TODO: Update Camera Obj

if __name__ == '__main__':
	LoopsUTDApp().run()

		


		

		
		
		