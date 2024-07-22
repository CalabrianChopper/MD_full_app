import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.properties import NumericProperty, ObjectProperty, StringProperty
from kivy.animation import Animation
from kivy.graphics import Color, Rectangle
import requests
import json
from functools import partial

#**********************************
# Riferimenti file .kv
#**********************************

Builder.load_file('mainApp.kv')

class CustomDropDown(DropDown):
    def __init__(self, **kwargs):
        super(CustomDropDown, self).__init__(**kwargs)
        self.auto_width = True
        self.max_height = 400  

    def open(self, widget):
        self.clear_widgets()
        for item in self.items:
            btn = Button(text=item, size_hint_y=None, height=80, size_hint_x=None, width=widget.width)
            btn.bind(on_release=lambda btn: self.select(btn.text))
            self.add_widget(btn)
        super(CustomDropDown, self).open(widget)

        # Animazione di apertura
        self.opacity = 0
        anim = Animation(opacity=1, duration=0.3, t='out_quad')
        anim.start(self)

#**********************************
# Variabile della grid principale
#**********************************

class MyGrid(BoxLayout):
    #Variabili lettura dati
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
    
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        self.dropdown1 = CustomDropDown()
        self.dropdown2 = CustomDropDown()
        self.initialize_dropdowns()

    def initialize_dropdowns(self):
        values1 = ['Seme', 'Talea', 'Germoglio', 'Pianta', 'Fioritura']
        values2 = ['Verdure a foglia verde', 'Ortaggi da frutto', 'Ortaggi a radice', 
                   'Ortaggi a bulbo', 'Ortaggi a tubero', 'Bacche', 
                   'Erbe aromatiche a foglia', 'Erbe perenni', 'Piante officinali']
        
        for value in values1:
            btn = Button(text=value, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.dropdown1.select(btn.text))
            self.dropdown1.add_widget(btn)
        
        for value in values2:
            btn = Button(text=value, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.dropdown2.select(btn.text))
            self.dropdown2.add_widget(btn)
            
        self.dropdown1.items = values1
        self.dropdown2.items = values2
            
        self.dropdown1.bind(on_select=self.on_dropdown_select1)
        self.dropdown2.bind(on_select=self.on_dropdown_select2)

    def show_dropdown1(self, button):
        self.dropdown1.open(button)

    def show_dropdown2(self, button):
        self.dropdown2.open(button)

    def on_dropdown_select1(self, instance, value):
        self.animate_button(self.ids.dropdown_button1, value, self.update_dropdown_text1)

    def on_dropdown_select2(self, instance, value):
        self.animate_button(self.ids.dropdown_button2, value, self.update_dropdown_text2)
        
    def animate_button(self, button, value, update_function):
        def single_animation(dt):
            anim = Animation(opacity=0, duration=0.1) + Animation(opacity=1, duration=0.1)
            anim.start(button)

        # Esegui l'animazione due volte
        Clock.schedule_once(single_animation, 0)
        #Clock.schedule_once(single_animation, 0.2)
        
        Clock.schedule_once(lambda dt: update_function(value), 0.4)

    def update_dropdown_text1(self, value):
        self.selected_value1 = value

    def update_dropdown_text2(self, value):
        self.selected_value2 = value

    def on_submit(self):
        combined_value = f"{self.selected_value1} - {self.selected_value2}"
        print(f"Valori selezionati: {combined_value}")
        
        if self.selected_value1 == 'Seme':
            self.set_pump_and_pause_duration(5, 20)
            print("Impostati: Durata Pompa = 5 min, Durata Pausa = 20 min")
        elif self.selected_value1 == 'Talea' or self.selected_value1 == 'Germoglio':
            if self.selected_value2 == 'Verdure a foglia verde' or self.selected_value2 == 'Ortaggi da frutto' or self.selected_value2 == 'Bacche' or self.selected_value2 == 'Piante officinali':
                self.set_pump_and_pause_duration(5, 30)
                print("Impostati: Durata Pompa = 5 min, Durata Pausa = 30 min")
            else:
                self.set_pump_and_pause_duration(3, 30)
                print("Impostati: Durata Pompa = 3 min, Durata Pausa = 30 min")
        elif self.selected_value1 == 'Pianta':
            if self.selected_value2 == 'Verdure a foglia verde' or self.selected_value2 == 'Ortaggi da frutto' or self.selected_value2 == 'Bacche' or self.selected_value2 == 'Piante officinali':
                self.set_pump_and_pause_duration(5, 60)
                print("Impostati: Durata Pompa = 5 min, Durata Pausa = 60 min")
            else:
                self.set_pump_and_pause_duration(3, 60)
                print("Impostati: Durata Pompa = 3 min, Durata Pausa = 60 min")
        else:
            if self.selected_value2 == 'Verdure a foglia verde' or self.selected_value2 == 'Ortaggi da frutto' or self.selected_value2 == 'Bacche' or self.selected_value2 == 'Piante officinali':
                self.set_pump_and_pause_duration(3, 60)
                print("Impostati: Durata Pompa = 3 min, Durata Pausa = 60 min")
            else:
                self.set_pump_and_pause_duration(2, 60)
                print("Impostati: Durata Pompa = 2 min, Durata Pausa = 60 min")
                
        with self.ids.submit_button.canvas.before:
            Color(0, 0, 1, 0.8)  # Blu semi-trasparente
            rect = Rectangle(pos=self.ids.submit_button.pos, size=(0, self.ids.submit_button.height))
            
        anim = Animation(size=(self.ids.submit_button.width, self.ids.submit_button.height), duration=1.5, t='out_elastic')
        anim.bind(on_complete=lambda *args: self.reset_submit_button())
        anim.start(rect)

        # Resetta i valori dei dropdown
        self.selected_value1 = 'Stadio'
        self.selected_value2 = 'Categoria'

    def reset_submit_button(self):
        self.ids.submit_button.canvas.before.clear()
        
    def set_pump_and_pause_duration(self, pump_duration, pause_duration):
        app = App.get_running_app()
        app.set_pump_duration(pump_duration)
        app.set_pause_duration(pause_duration)

    
# #**********************************
# # Variabile del dropdown
# #**********************************

# class CustomDropDown(DropDown):
#     pass
            
#**********************************
# App Principale
#**********************************

class MyApp(App):
    
    pump_duration = NumericProperty(1)
    pause_duration = NumericProperty(1)
    
#**********************************
# Riavvio forzato pompa
#**********************************
    
    def force_restart(self):
        try:
            response = requests.get("http://192.168.4.1/RESET/reset_device")
            if response.status_code == 200:
                print("Riavvio forzato eseguito con successo.")
                self.disable_force_buttons()
            else:
                print("Errore durante il riavvio forzato.")
        except requests.exceptions.RequestException as e:
            print("Errore durante il riavvio forzato:", e)
            
    def force_pump_start(self):
        try:
            response = requests.get("http://192.168.4.1/FORCE/start_pump")
            if response.status_code == 200:
                print("Avvio forzato della pompa eseguito con successo.")
                self.disable_force_buttons()
            else:
                print("Errore durante l'avvio forzato della pompa.")
        except requests.exceptions.RequestException as e:
            print("Errore durante l'avvio forzato della pompa:", e)

    def disable_force_buttons(self):
        restart_button = self.root.ids.restart_button
        force_start_button = self.root.ids.force_start_button
        
        for button in [restart_button, force_start_button]:
            button.disabled = True
            original_text = button.text
            button.text = 'Attendi...'
            
            with button.canvas.before:
                Color(0.7, 0, 0, 0.8)  # Blu semi-trasparente
                rect = Rectangle(pos=button.pos, size=(0, button.height))
            
            anim = Animation(size=(button.width, button.height), duration=1.5, t='out_elastic')
            anim.start(rect)
            
            Clock.schedule_once(partial(self.reset_force_button, button, original_text), 30)

    def reset_force_button(self, button, original_text, dt):
        button.disabled = False
        button.text = original_text
        button.canvas.before.clear()
        
    def set_substrate_mode(self):
        self.set_pump_duration(5)
        self.set_pause_duration(5)
        print("Modalità substrato attivata: Durata Pompa = 5 min, Durata Pausa = 5 min")

    # def enable_restart_button(self, button, dt):
    #     button.disabled = False
    #     button.text = 'Riavvio Forzato'

#**********************************
# Metodo di ricezione dati
#**********************************

    def update_data(self, dt=None):
        try:
            response = requests.get("http://192.168.4.1/GET/get_sensor_data")
            data = response.json()
            self.root.temperature_label.text = f"Temperatura: {data['temperature']} °C"
            self.root.humidity_label.text = f"Umidità: {data['humidity']} %"
            pump_state = int(data['pump_state'])
            self.root.pump_state_label.text = f"Pompa: {'Accesa' if pump_state == 1 else 'Spenta'}"
            self.root.pump_icon.source = 'green_circle.png' if pump_state == 1 else 'red_circle.png'
            self.pump_duration = data['pump_duration']
            self.pause_duration = data['pause_duration']
            self.root.pump_duration_label.text = f"Durata Pompa: {data['pump_duration']} min"
            self.root.pause_duration_label.text = f"Durata Pausa: {data['pause_duration']} min"
            self.root.temperature_bar.value = data['temperature'] + 20  
            self.root.humidity_bar.value = data['humidity']
        except requests.exceptions.RequestException as e:
            print("Errore durante l'aggiornamento dei dati:", e)
                
#**********************************
# Metodi di settaggio della pompa 
#**********************************
    
    def set_pump_duration(self, new_duration):
        try:
            url = f"http://192.168.4.1/SET/set_pump_duration?duration={new_duration}"
            response = requests.get(url)
            if response.status_code == 200:
                self.pump_duration = new_duration
                self.root.pump_duration_label.text = f"Durata Pompa: {new_duration} min"
                print("Durata della pompa aggiornata con successo.")
            else:
                print("Errore durante l'aggiornamento della durata della pompa.")
        except requests.exceptions.RequestException as e:
            print("Errore durante l'aggiornamento della durata della pompa:", e)

    def set_pause_duration(self, new_pause):
        try:
            url = f"http://192.168.4.1/SET/set_pause_duration?pause={new_pause}"
            response = requests.get(url)
            if response.status_code == 200:
                self.pause_duration = new_pause
                self.root.pause_duration_label.text = f"Durata Pausa: {new_pause} min"
                print("Durata della pausa aggiornata con successo.")
            else:
                print("Errore durante l'aggiornamento della durata della pausa.")
        except requests.exceptions.RequestException as e:
            print("Errore durante l'aggiornamento della durata della pausa:", e)

    def increment_pump_duration(self, instance):
        new_duration = self.pump_duration + 1
        self.set_pump_duration(new_duration)

    def decrement_pump_duration(self, instance):
        if self.pump_duration > 1:
            new_duration = self.pump_duration - 1
        else:
            new_duration = self.pump_duration
        self.set_pump_duration(new_duration)

    def strong_increment_pump_duration(self, instance):
        new_duration = self.pump_duration + 10
        self.set_pump_duration(new_duration)

    def strong_decrement_pump_duration(self, instance):
        if self.pump_duration > 10:
            new_duration = self.pump_duration - 10
        else:
            new_duration = self.pump_duration
        self.set_pump_duration(new_duration)

    def increment_pause_duration(self, instance):
        new_pause = self.pause_duration + 1
        self.set_pause_duration(new_pause)

    def decrement_pause_duration(self, instance):
        if self.pause_duration > 1:
            new_pause = self.pause_duration - 1
        else:
            new_pause = self.pause_duration
        self.set_pause_duration(new_pause)

    def strong_increment_pause_duration(self, instance):
        new_pause = self.pause_duration + 10
        self.set_pause_duration(new_pause)

    def strong_decrement_pause_duration(self, instance):
        if self.pause_duration > 10:
            new_pause = self.pause_duration - 10
        else:
            new_pause = self.pause_duration
        self.set_pause_duration(new_pause)
        
#**********************************
# Build e aggiornamento dati
#**********************************
    
    def build(self):
        Clock.schedule_once(self.update_data, 3)
        Clock.schedule_interval(self.update_data, 30)
        return MyGrid()
    
if __name__ == "__main__":
    MyApp().run()