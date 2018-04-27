from MySettings import SettingOptions, SettingString, SettingPath
from kivy.uix.gridlayout import GridLayout 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView 
from kivy.uix.widget import Widget 
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from MySettings import SettingSpacer
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView

#FROM: https://github.com/kivy/kivy/wiki/Scollable-Options-in-Settings-panel

class SettingScrollOptions(SettingOptions):

    def _create_popup(self, instance):
        
        #global oORCA
        # create the popup
       
        content         = GridLayout(cols=1, spacing='5dp')
        scrollview      = ScrollView( do_scroll_x=False)
        scrollcontent   = GridLayout(cols=1,  spacing='5dp', size_hint=(None, None))
        scrollcontent.bind(minimum_height=scrollcontent.setter('height'))
        self.popup   = popup = Popup(content=content, title=self.title, size_hint=(0.5, 0.9),  auto_dismiss=False)

        #we need to open the popup first to get the metrics 
        popup.open()
        #Add some space on top
        content.add_widget(Widget(size_hint_y=None, height=dp(2)))
        # add all the options
        uid = str(self.uid)
        for option in self.options:
            state = 'down' if option == self.value else 'normal'
            btn = ToggleButton(text=option, state=state, group=uid, size=(popup.width, dp(55)), size_hint=(None, None))
            btn.bind(on_release=self._set_option)
            scrollcontent.add_widget(btn)

        # finally, add a cancel button to return on the previous panel
        scrollview.add_widget(scrollcontent)
        content.add_widget(scrollview)
        content.add_widget(SettingSpacer())
        #btn = Button(text='Cancel', size=((oORCA.iAppWidth/2)-sp(25), dp(50)),size_hint=(None, None))
        btn = Button(text='Cancel', size=(popup.width, dp(50)),size_hint=(0.9, None))
        btn.bind(on_release=popup.dismiss)
        content.add_widget(btn)

class FileBrowserIconView(SettingPath):
    def _create_popup(self, instance):

        #Main Container
        content = BoxLayout(orientation='vertical')
        
        self.popup   = popup = Popup(content=content, title=self.title, size_hint=(0.7, 0.9),  auto_dismiss=True)        
        popup.open()

        #Header with Current Path - enter a new value and press return
        header = BoxLayout(size_hint_y=None, height='35dp', spacing='5dp')
        btn1 = Button(text="Path: ", size_hint=(.1,1))
        btn1.bind(on_release=self._updatePath)
        header.add_widget(btn1)
        #TODO: Uncomment for production
        #header.add_widget(Label(text="Current Path: ", size_hint=(.1,1)))

        #Current Path Input
        self.pathInput = TextInput(text=self.value, size_hint=(.9,1), multiline=False)
        self.pathInput.bind(on_text_validate=self._updatePath)
        header.add_widget(self.pathInput)
        content.add_widget(header)
        

        content.add_widget(SettingSpacer())
        self.textinput = FileChooserIconView(path=self.value, size_hint=(1,1), dirselect=True, show_hidden=False)
        self.textinput.bind(on_path=self.val)
        content.add_widget(self.textinput)

         # 2 buttons are created for accept or cancel the current value
        btnlayout = BoxLayout(size_hint_y=None, height='50dp', spacing='5dp')
        btn = Button(text='Ok')
        btn.bind(on_release=self._validate)
        btnlayout.add_widget(btn)
        btn = Button(text='Cancel')
        btn.bind(on_release=self._dismiss)
        btnlayout.add_widget(btn)
        content.add_widget(btnlayout)

    def val(self):
        self.value = self.textinput
        self._validate()

    def _updatePath(self, instance):
        print(self.pathInput.text)
        self.textinput.path = self.pathInput.text

class LensHolderOptions(SettingString):

    def _create_popup(self, instance):
        content = GridLayout(cols=3, rows = 2, spacing = '10dp')

        self.popup = popup = Popup(content=content, title=self.title, size_hint=(.5,.5), auto_dismiss=False)

        popup.open()

        btn100p = Button(text='+100')
        btn100m = Button(text='-100')
        btn1p = Button(text="+1")
        btn1m = Button(text="-1")
        self.label = label = Label(text=self.value)
        btnCancel = Button(text="cancel")

        btn100p.bind(on_release=lambda x:self._incrementVal(100))
        btn100m.bind(on_release=lambda x:self._incrementVal(-100))
        btn1p.bind(on_release=lambda x:self._incrementVal(1))
        btn1m.bind(on_release=lambda x:self._incrementVal(-1))
        btnCancel.bind(on_release=popup.dismiss)


        content.add_widget(btn100p)
        content.add_widget(btn1p)
        content.add_widget(label)
        content.add_widget(btn100m)
        content.add_widget(btn1m)
        content.add_widget(btnCancel)


    def _incrementVal(self, increment):
        self.value = str(int(self.value) + increment)
        self.label.text = self.value

