from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivy.properties import ObjectProperty


Window.size = (400, 800)


class FirstScreen(Screen):

    drop_item = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self._post_init)

    def _post_init(self, dt):
        menu_items = [{"icon": "git", "text": f"Item {i}"} for i in range(5)]
        self.menu = MDDropdownMenu(
            caller=self.ids.drop_item,
            items=menu_items,
            #callback=self.set_item,
            width_mult=4,
        )

    def set_item(self, instance_menu_item):
        self.ids.drop_item.text = instance_menu_item.text
        self.menu.dismiss()

class SecondScreen(Screen):
    pass

class WindowManager(ScreenManager):
    pass

#GUI = Builder.load_file("main.kv")

class App(MDApp):

    def build(self):
        GUI = Builder.load_file("main.kv")
        return GUI


if __name__ == "__main__":
    App().run()