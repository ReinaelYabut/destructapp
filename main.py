from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.uix.relativelayout import RelativeLayout

class ListWidget(RecycleView):

    def update(self):
        self.data = [{'text': str(item)} for item in self.items]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.items = []

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            self.update()

class SettingsScreen(Screen):
    pass

class RootWidget(BoxLayout):
    text_input = ObjectProperty(None)
    inputcontent = ObjectProperty(None)  
    outputcontent = ObjectProperty(None)

    def add_item(self):
        if self.inputcontent.text != "":
            formatted = f'\n {self.inputcontent.text}'  
            self.outputcontent.items.append(formatted)
            self.outputcontent.update()
            self.inputcontent.text = ""
            delay_time = App.get_running_app().config.get('settings', 'delay_time')
            Clock.schedule_once(lambda dt: self.outputcontent.remove_item(formatted), float(delay_time))
    def delete_all_items(self):
        self.outputcontent.items = []
        self.outputcontent.update()


class MyApp(App):
    def build(self):
        # Initialize settings
        self.config.read('settings.ini')
        return RootWidget()

    def build_config(self, config):
        config.setdefaults('settings', {'delay_time': '2'})

    def build_settings(self, settings):
        settings.add_json_panel('App Settings', self.config, data='''
        [
            {"type": "title", "title": "App Settings"},
            {"type": "options",
             "title": "Edit Self Destruct Timer",
             "desc": "Adjust the delay time for removing notes",
             "section": "settings",
             "key": "delay_time",
             "options": ["5", "10", "30", "60", "86400", "2592000","31536000"]
            }
        ]
        ''')

    def on_config_change(self, config, section, key, value):
        super(MyApp, self).on_config_change(config, section, key, value)
        if key == 'delay_time':
            # Handle changes to the delay_time setting
            pass

if __name__ == "__main__":
    MyApp().run()
