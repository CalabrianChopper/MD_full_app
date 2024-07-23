from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
Window.size = (310, 580)

class Slope(MDApp):
    
    def build(self):
        screen_manager = ScreenManager()
        screen_manager.add_widget(Builder.load_file("main.kv"))
        screen_manager.add_widget(Builder.load_file("login.kv"))
        screen_manager.add_widget(Builder.load_file("signup.kv"))
        return screen_manager
    
    
if __name__ == "__main__":
    
    LabelBase.register(name = "Roboto", fn_regular = "C:\\Users\\Francesco\\Desktop\\MD_Full_App\\MDEnv\\RobotoMono-VariableFont_wght.ttf")
    
    Slope().run()
    
