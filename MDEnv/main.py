from bleak import BleakScanner
import subprocess
from kivy.properties import NumericProperty, ObjectProperty, StringProperty
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.button import MDButton, MDButtonText
from kivy.clock import Clock
from kivymd.uix.list import MDList
from kivymd.uix.boxlayout import BoxLayout

class MainWindow(MDScreen):
    pass

class ChangeColorWindow(MDScreen):
    pass

class ControlWindow(MDScreen):
    pass

class SecondWindow(MDScreen):
    pass

class ScreenManager(MDScreenManager):
    pass


def find_wifi_networks_containing_qmt():
    try:
        output = subprocess.check_output(['netsh', 'wlan', 'show', 'network'], text=True)
        qmt_networks = []
        
        lines = output.split('\n')
        for line in lines:
            if "SSID" in line and "QMT" in line:
                ssid = line.split(":")[1].strip()
                qmt_networks.append(ssid)
        
        return qmt_networks
    except Exception as e:
        print(f"Errore durante la scansione delle reti WiFi: {e}")
        return []
    
    
class mainApp(MDApp):
    
    temperature_label = ObjectProperty(None)
    humidity_label = ObjectProperty(None)
    temperature_bar = ObjectProperty(None)
    humidity_bar = ObjectProperty(None)
    pump_state_label = ObjectProperty(None)
    pump_icon = ObjectProperty(None)
    #Variabili regolazione manuale
    pump_duration_label = ObjectProperty(None)
    pause_duration_label = ObjectProperty(None)
    #Variabili dropdown 
    selected_value1 = StringProperty('Stadio')
    selected_value2 = StringProperty('Categoria')
    dropdown1 = ObjectProperty(None)
    dropdown2 = ObjectProperty(None)
    
    def build(self):
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style_switch_animation_duration = 0.8
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        return Builder.load_file("main.kv")
    
    
    def switch_theme_style(self):
        self.theme_cls.primary_palette =(
            "Orange" if self.theme_cls.primary_palette == "Red" else "Red"
        )
        self.theme_cls.theme_style =(
            "Dark" if self.theme_cls.theme_style == "Light" else "Light"
        )
    
        
mainApp().run()


networks = find_wifi_networks_containing_qmt()
for network in networks:
    print(network)