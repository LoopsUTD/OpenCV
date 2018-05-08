from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.factory import Factory
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
from kivy.config import ConfigParser

import os
import pathlib
from time import sleep
from multiprocessing import Process, Manager, Event
import logging
from settingsWidget import Settings, SettingsWithSidebar
from MoreSettingOptions import SettingScrollOptions, LensHolderOptions, FileBrowserIconView

from linearActuator import LinearActuator
from cameraHandling import Camera

log = logging.getLogger('uiApp')

"""
Main Thread for Our Device is Launched from here. User Interface on the touchscreen is controlled
by one thread, launched by the ProcessManager in the def __main__() function below

"""

def main_process(shared_data_dict, is_master, exit_event):

	if is_master:
		os.environ["KIVY_BCM_DISPMANX_ID"] = "4"
	else:
		os.environ["KIVY_BCM_DISPMANX_ID"] = "5"

	"""
	Initialization Screen - Displays the initialization screen?

	"""

	class InitializeScreen(Screen):
		myInfoLabel = ObjectProperty()
		myVals = {}

		def __init__(self, **kwargs):
			super(InitializeScreen, self).__init__(**kwargs)
			Clock.schedule_once(self._finish_init)
			print("InitializeScreen is instantiated")
			print 
			self.myRoot = RootWidget.rootIds
			

		def _finish_init(self, dt):
			print("finished init InitializeScreen")
			print(self)
			print(self.ids)

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

		def updateInfoBox(self, text):
			self.myRoot.updateInfoLabel(text)

		def onCameraUpdate(self):
			print("testing Camera Update")
			return "Adding Stuff to camera Update\n"

		def setCameraFocus(self, instance):
			self.camera = Camera.getInstance()
			self.outputDirectory = App.get_running_app().config.get('Output','defaultpath')
			content = BoxLayout(orientation='vertical')
			cameraPop = popup = Popup(content=content, title="Set Camera Focus", size_hint=(0.7, 0.9),  auto_dismiss=True)        
			popup.open()

			#Display Test Image Pattern
			shared_data_dict['displayedImage'] = "/home/pi/LoopsUTD/OpenCV/ReferenceImages/indianHeadTestPattern.png"
			sleep(.5)
			self.curImg = Image()#Path to test pattern)
			content.add_widget(self.curImg)
			# 2 buttons are created for accept or cancel the current value
			btnlayout = BoxLayout(size_hint_y=None, height='50dp', spacing='5dp')
			btn = Button(text='Take Photo')
			btn.bind(on_release=lambda x:self._bindNewImage())
			btnlayout.add_widget(btn)
			btn = Button(text='Cancel')
			btn.bind(on_release=popup.dismiss)
			btnlayout.add_widget(btn)
			content.add_widget(btnlayout)

			instance.text = "Initialized Camera"


			return

		def _bindNewImage(self):
			self.curImg.source = self._takePhotoNowReturnsName(filePrefix='focusing', sampleFolder='testing')
			self.curImg.reload()

		def _takePhotoNowReturnsName(self, filePrefix = None, sampleFolder = None):
			if sampleFolder is not None:
				currentOutFolder = self.outputDirectory + "/" + sampleFolder
				self._makeFolder(currentOutFolder)
			else:
				currentOutFolder = self.outputDirectory

			target = self.camera.takePhoto(folderName = currentOutFolder, prefix = filePrefix)
			return target

		def _makeFolder(self, dir_path):
			pathlib.Path(dir_path).mkdir(parents=True,exist_ok=True)

		def initializeDisplay(self):
			print(App.get_running_app().config.get('Output','defaulttestimage'))
			return True

		def initializeCamera(self):
			camera = Camera.getInstance()
			ct = App.get_running_app().config.get('Camera','capturetarget')
			fnum = App.get_running_app().config.get('Camera','f-number')
			iso = App.get_running_app().config.get('Camera','iso')
			shutter = App.get_running_app().config.get('Camera','shutterspeed')
			imgqual = App.get_running_app().config.get('Camera','imagequality')

			camera.adjustSettings('capturetarget', ct)
			camera.adjustSettings('f-number', fnum)
			camera.adjustSettings('iso',iso)
			camera.adjustSettings('shutterspeed', shutter)
			camera.adjustSettings('imagequality', imgqual)

			if "JPEG" in imgqual:
				imsize = App.get_running_app().config.get('Camera','imagesize')
				print("Image Size = %s " % imsize)
				#camera.adjustSettings('imagesize', imsize)

			return True

		def initializeLensHolder(self):
			#How to access: https://stackoverflow.com/questions/45663871/kivy-access-configuration-values-from-any-widget
			pos = App.get_running_app().config.get('LensHolder','position')
			print("Current Lin Actuator Config Pos: %d " % int(pos))
			actuator = LinearActuator.getInstance()
			actuator.moveTo(int(pos))
			return True
	"""
	Screen for Running Tests


	"""
	class RunTestScreen(Screen):
		"""docstring for RunTestScreen"""
		def __init__(self, **kwargs):
			super(RunTestScreen, self).__init__(**kwargs)
			print("RunTestScreen: IDS: ")
			self._updateConsoleTrigger = Clock.create_trigger(self.updateRootConsole)
			
			Clock.schedule_once(self._do_this_thing)
			

		def _do_this_thing(self, dt):
			self.myRoot = RootWidget.rootIds

		def validateText(self, instance):
			print("user entered: %s", instance.text)
			self.cleanSampleFolderName = self._cleanInputs(instance.text)
			print(self)

		def _cleanInputs(self, usr_input):
			strippedName = usr_input.strip()
			nameWithSlashes = strippedName.replace(' ', '')
			goodName = nameWithSlashes.replace('\\', '')
			betterName = goodName.replace("\'", '')
			bestName = betterName.replace('\"', '')
			return bestName
		"""
		Run the Actual Test 
		Check the Config 


		"""

		def runTest(self):
			self.outputDirectory = App.get_running_app().config.get('Output','defaultpath')
			#Ensure that the user "Validated their text"
			#outputFolder = self.cleanSampleFolderName

			self.myRoot.updateRunConsole("Test Running - values stored at: %s/%s" % (self.outputDirectory, self.cleanSampleFolderName))
			linearActuator = LinearActuator.getInstance()
			self.camera = Camera.getInstance()
			

			linearActuator.moveOutOfPath()
			
			shared_data_dict['displayedImage'] = App.get_running_app().config.get('Output','defaulttestimage')
			sleep(2)
			self.takePhoto("noLens_")

			shared_data_dict['displayedImage'] = App.get_running_app().config.get('Output','magnificationtest')
			sleep(2)
			self.takePhoto("power_noLens_")
			
	
			linearActuator.moveIntoPath()
		
			shared_data_dict['displayedImage'] = App.get_running_app().config.get('Output','defaulttestimage')
			sleep(2)
			self.takePhoto("withLens_")

			shared_data_dict['displayedImage'] = App.get_running_app().config.get('Output','lensfindingtest')
			sleep(2)
			self.takePhoto("lensFinding_")
			
			shared_data_dict['displayedImage'] = App.get_running_app().config.get('Output','magnificationtest')
			sleep(2)
			self.takePhoto("power_withLens_")
			

		def takePhoto(self, filepre):
			#self.myRoot.updateRunConsole("Image Taken: %s \n" % self._takePhotoNowReturnsName(filePrefix = filepre, sampleFolder = self.cleanSampleFolderName))

			imgFilePath = self._takePhotoNowReturnsName(filePrefix = filepre, sampleFolder = self.cleanSampleFolderName)
			self.myRoot.updateRunConsole("Image Taken: %s \n" % imgFilePath)
			self._updateConsoleTrigger("Image Taken: %s \n" % imgFilePath)

		def updateRootConsole(self, *largs):
			print(largs)
			self.myRoot.updateRunConsole("Testing Finished\n")


		def _takePhotoNowReturnsName(self, filePrefix = None, sampleFolder = None):
			if sampleFolder is not None:
				currentOutFolder = self.outputDirectory + "/" + sampleFolder
				self._makeFolder(currentOutFolder)
			else:
				currentOutFolder = self.outputDirectory

			target = self.camera.takePhoto(folderName = currentOutFolder, prefix = filePrefix)
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

			# if self.ids.initializeScreen.initializeDisplay():
			# 	self.ids.initializeScreen.updateLabelColor(self.ids.btnDisplay)
			# else:
			# 	self.ids.initializeScreen.updateInfoBox("\nFATAL ERROR: Display Not Working!")

			# if self.ids.initializeScreen.initializeCamera():
			# 	self.ids.initializeScreen.updateLabelColor(self.ids.camInitialize)
			# else:
			# 	self.ids.initializeScreen.updateInfoBox("\nFATAL ERROR: Camera Not Connected!")

			# #if self.ids.initializeScreen.initializeLensHolder():
			# #	self.ids.initializeScreen.updateLabelColor(self.ids.lensInitialize)
			# #else:
			# self.ids.initializeScreen.updateInfoBox("\nFATAL ERROR: Linear Actuator Not Connected!")


		def updateInfoLabel(self, text):
			self.ids.infoTextLabel.text += text

		def updateRunConsole(self, text):
			self.ids.runConsole.text += text


	class DisplayWindow(Image):
	    src = ObjectProperty()
	    def __init__(self, **kwargs):
	        super(DisplayWindow, self).__init__(**kwargs)
	        #print("Source: %s" % self.src.value)
	        self.src = shared_data_dict
	        self.source = self.src['displayedImage']
	        Clock.schedule_interval(self.update, 1/30.)

	    def on_src(self, instance, value):
	        newVal = dict(value)['displayedImage']
	        print(newVal == self.source)
	        if newVal != self.source:
	            print("Detected a Value Change! %s" % newVal)
                    #self.s2ource = newVal
	            #self.reload()

	    def update(self, *args):
	        self.source = shared_data_dict['displayedImage']
	        self.reload()
	        #newVal =
	        #if newVal != self.source:
		#        print("Updating with... %s" % shared_data_dict['displayedImage'])
		#        self.source = shared_data_dict['displayedImage']
		#        self.reload()

	class LoopsApp(App):
		def __init__(self):
			App.__init__(self)
			#super(LoopsApp, self).__init__()

			if is_master:
				self.title = "Master Display"
			else:
				self.title = "Slave Display"
		
		def build(self):
			#Builder.load_file("loopsutd.kv")
			print("I'm building!")
			if is_master:
				self.use_kivy_settings = False
				return Builder.load_file('touchscreenUI.kv')
			else:
				return self._otherbuild()

		def _otherbuild(self):
			self.root = None    
			layout1 = BoxLayout(orientation='horizontal')
			dispWin = DisplayWindow()
			#testing
			layout1.add_widget(dispWin)
			#testing
			return layout1


		def build_config(self, config):
			if is_master:
				self.settings_cls=SettingsWithSidebar
				config.read('loopsutd.ini')
			else:
				self.config = None
			#app.open_settings()

		def build_settings(self, settings):
			settings.register_type('scrolloptions', SettingScrollOptions)
			settings.register_type('lensHolderAdjust', LensHolderOptions)
			settings.register_type('filebrowse', FileBrowserIconView)
			settings.add_json_panel('Testing', self.config, 'config/outputSettings.json')
			settings.add_json_panel('Camera', self.config, 'config/cameraSettings.json')
			settings.add_json_panel('Lens Holder', self.config, 'config/lensSettings.json')
		
		def on_config_change(self, config, section, key, value):
			print("Config Change Detected!")
			print("Config Changed! Section: %s Key: %s Value: %s" % (section, key, value))
			if key in ['position']:
				print('moving linear actuator to: %d'  % int(value))
				#TODO: update linear actuator position
				actuator = LinearActuator.getInstance()
				actuator.moveTo(int(value))

			if key in ['defaulttestimage']:
				print('updating Displayed Image to: %s ' % value)
				shared_data_dict['displayedImage'] = value
				

			if section in ['Camera']:
				print('updating Camera Config: %s:%s' %(key, value))
				#TODO: Update Camera Obj
				camera = Camera.getInstance()
				camera.adjustSettings(key, value)
		
	app = LoopsApp()
	app.run()

if __name__ == '__main__':
	# LoopsUTDApp().run()
	m = Manager()
	shared_data = m.dict() #This creates a managed proxy object that will update between the two processes
	shared_data['displayedImage'] = "ReferenceImages/circle.png"#"ReferenceImages/indianHeadTestPattern.png"
	#Link for the Proxy Object Documentation:
	#https://docs.python.org/3/library/multiprocessing.html#module-multiprocessing
	ev = Event()
	proc_master = Process(target=main_process, args=(shared_data,True, ev))
	proc_slave = Process(target=main_process, args=(shared_data, False, ev))
	proc_master.start()
	proc_slave.start()
	proc_master.join()