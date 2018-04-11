'''
Author: Aleksandr Spiridonov
This is a quick example of an app that will be modified for
mirroring to an HDMI driven screen with interactive UI on
a Raspberry Pi touchscreen.
'''

from multiprocessing import Process, Manager, Event

def display_process(dict_global, is_master, exit_event):

    import os

    if is_master:
        os.environ["KIVY_BCM_DISPMANX_ID"] = "4"
    else:
        os.environ["KIVY_BCM_DISPMANX_ID"] = "5"

    from kivy.app import App
    from kivy.uix.button import Button
    from kivy.clock import Clock
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.label import Label
    from kivy.uix.image import Image
    from kivy.properties import DictProperty

    import operator


    class ButtonDIPO(Button):
        def __init__(self,key_string,in_place_operator,IPO_value,**kwargs):
            super(ButtonDIPO, self).__init__(**kwargs)
            #dictionary is now global
            #self.dictionary = dictionary
            self.key_string = key_string
            self.IPO = in_place_operator
            self.IPO_value = IPO_value

        if is_master:
            def on_press(self):
                dict_global[self.key_string] = self.IPO(dict_global[self.key_string],self.IPO_value)

    class LabelD(Label):
        def __init__(self,key_string,**kwargs):
            super(LabelD, self).__init__(**kwargs)
            # dictionary is now global
            # self.dictionary = dictionary
            self.key_string = key_string
            Clock.schedule_interval(self.update, 1 / 30.)

        def update(self, *args):
            self.text = str(dict_global[self.key_string])

    class DisplayWidget(Image):
        localsrc = DictProperty(dict_global, rebind=True)
        def __init__(self,img_source, **kwargs):
            super(MyImage, self).__init__(source=img_source)
            #if self.localsrc > "":

            #dict_global[imSource] = self.localsrc

        def on_localsrc(self, instance, value):
            print("value")
            self.source = dict_global['imSource']
            print("Value Changed!")
            #self.

    class ChangeImageButton(Button):
        def __init__(self, **kwargs):
            super(ChangeImageButton, self).__init__(**kwargs)
            self.bind(on_press=self.callback1)


        def callback1(self, instance):
            print('Btn <%s> is being pressed.' % instance.text)
            dict_global['imSource'] = 'rock.png'
            print('New DIct Value: ')

    class MyApp(App):
        #src = StringProperty('test.jpg')

        def __init__(self):
            App.__init__(self)
            # dictionary is now global
            # self.dict_local = dictionary
            if is_master:
                self.title = 'Master display'
            else:
                self.title = 'Slave display'
            Clock.schedule_interval(self.update, 1 / 30.)


        def build(self):
            if is_master:
                return self._mainbuild()
            else:
                return self._otherbuild()

        def update(self, *args):
            if exit_event.is_set():
                exit()

        def _otherbuild(self):
            layout1 = BoxLayout(orientation='horizontal',spacing=10)
            #layout1.add_widget(LabelD('counter',font_size=200))
            layout1.add_widget(DisplayWidget(img_source='test.jpg'))
            return layout1

        def _mainbuild(self):
            layout1 = BoxLayout(orientation='horizontal',spacing=10)
            layout1.add_widget(LabelD('counter',font_size=200))
            layout2 = BoxLayout(orientation='vertical', spacing=10)
            layout2.add_widget(ButtonDIPO('counter',operator.add,1,text="+1",font_size=200))
            layout2.add_widget(ButtonDIPO('counter', operator.mul, 0, text="Reset",font_size=200))
            
            btn = ChangeImageButton(text="Change Image")
            #btn.bind(on_press=self.callback1)
            layout2.add_widget(btn)
            layout1.add_widget(layout2)

            return layout1


        def on_stop(self):
            exit_event.set()

    app = MyApp()
    app.run()



if __name__ == '__main__':
    m = Manager()
    dict_main = m.dict()
    dict_main['imSource'] = 'test.jpg'
    ev = Event()
    dict_main['counter'] = 0
    proc_master = Process(target=display_process, args=(dict_main,True, ev))
    proc_slave = Process(target=display_process, args=(dict_main, False, ev))
    proc_master.start()
    proc_slave.start()
    proc_master.join()
    proc_slave.join()
