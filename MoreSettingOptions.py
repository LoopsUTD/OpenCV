from MySettings import SettingOptions, SettingString
from kivy.uix.gridlayout import GridLayout 
from kivy.uix.scrollview import ScrollView 
from kivy.uix.widget import Widget 
from kivy.uix.togglebutton import ToggleButton
from MySettings import SettingSpacer
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.uix.popup import Popup

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

