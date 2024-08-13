from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from kivy.lang import Builder

class MainApp (MDApp):
    theme_cls = ThemeManager()
    
MainApp().run()

class App(MDApp):
    
    theme_cls = ThemeManager()

    def build(self):
        GUI = Builder.load_file("main.kv")
        return GUI


if __name__ == "__main__":
    App().run()