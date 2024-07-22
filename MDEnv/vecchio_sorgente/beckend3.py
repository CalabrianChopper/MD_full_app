
#******************************************
# Librerie
#******************************************

import os
import network 
import usocket as socket
import json
import _thread
import time
import machine
from time import sleep
from dht import DHT11
import uasyncio as asyncio

#******************************************
# Configurazioni hardware
#******************************************

d = DHT11(machine.Pin(23))
pump = machine.Pin(22, machine.Pin.OUT)
config_file_path = 'pump_config.txt'

#******************************************
# Metodi Get
#******************************************

def get_pump_config():
    try:
        with open(config_file_path, 'r') as f:
            lines = f.readlines()
            return {'pump_duration': int(lines[0].strip()), 
                    'pause_duration': int(lines[1].strip()), 
                    'pump_state': int(lines[2].strip())}
    except OSError:
        with open(config_file_path, 'w') as f:
            f.write("1\n")  
            f.write("1\n") 
            f.write("0\n")
        return {'pump_duration': 1, 
                'pause_duration': 1,
                'pump_state': 0}
    
def get_pump_duration():
    config = get_pump_config()
    if config is not None:
        return config["pump_duration"]
    else:
        print("Configurazione durata pompa non trovata per get_pump_duration")
        
def get_pause_duration():
    config = get_pump_config()
    if config is not None:
        return config["pause_duration"]
    else:
        print("Configurazione durata pausa non trovata per get_pause_duration")
        
def get_pump_state():
    config = get_pump_config()
    if config is not None:
        return config["pump_state"]
    else:
        print("Configurazione stato pompa non trovata per get_pump_state")
        
def get_sensor_data():
    for i in range(5):
        try:
            d.measure()
            temperature = d.temperature()
            humidity = d.humidity()
            pause_duration = get_pause_duration()
            pump_duration = get_pump_duration()
            pump_state = get_pump_state()
            print('Temperatura:', temperature, '°C')
            print('Umidità:', humidity, '%')
            print('Stato della pompa:', pump_state)
            print('Durata Ciclo Pompa:', pump_duration)
            print('Durata Pausa:', pause_duration)
            break
        except OSError as e:
            print("Errore al tentativo {}: {}".format(i + 1, e))
            sleep(1)

    return {
        "temperature": temperature,
        "humidity": humidity,
        "pump_state": pump_state,
        "pump_duration": pump_duration,
        "pause_duration": pause_duration,
    }

#******************************************
# Metodi Set
#******************************************

def set_pump_duration(new_duration):
    current_config = get_pump_config()
    
    if current_config is None:
       current_config = {'pump_duration': 1, 
                         'pause_duration': 1,
                         'pump_state': 0}
       
    current_config['pump_duration'] = new_duration
    
    with open(config_file_path, 'w') as f:
        f.write(f"{current_config['pump_duration']}\n")
        f.write(f"{current_config['pause_duration']}\n")
        f.write(f"{current_config['pump_state']}\n")
        
def set_pause_duration(new_pause):
    current_config = get_pump_config()
    
    if current_config is None:
       current_config = {'pump_duration': 1, 
                         'pause_duration': 1,
                         'pump_state': 0}
       
    current_config['pause_duration'] = new_pause
    
    with open(config_file_path, 'w') as f:
        f.write(f"{current_config['pump_duration']}\n")
        f.write(f"{current_config['pause_duration']}\n")
        f.write(f"{current_config['pump_state']}\n")
        
def change_pump_state():
    global pump
    current_config = get_pump_config()

    if current_config is None:
       current_config = {'pump_duration': 1,
                         'pause_duration': 1,
                         'pump_state': 0 }

    if current_config['pump_state'] == 1:
        current_config['pump_state'] =0
        pump.off()
    else:
        current_config['pump_state'] =1
        pump.on()

    with open(config_file_path, 'w') as f:
        f.write(f"{current_config['pump_duration']}\n")
        f.write(f"{current_config['pause_duration']}\n")
        f.write(f"{current_config['pump_state']}\n")
        
def set_duration(request, action):
    try:
        start_query_string = request.find('?')
        query_string = request[start_query_string:]
        start_duration = query_string.find('duration=')
        if start_duration!= -1:
            new_duration_str = query_string[start_duration + len('duration='):].split(' ')[0]
            new_duration = int(new_duration_str)
            
            if action == 'pump':
                set_pump_duration(new_duration)
                return 'Durata della pompa cambiato con successo'
            elif action == 'pause':
                set_pause_duration(new_duration)
                return 'Durata della pausa cambiato con successo'
            else:
                raise ValueError("Azione non supportata")
        else:
            raise ValueError("Parametro 'duration' non trovato nella richiesta")
    except Exception as e:
        return f'Errore durante il cambiamento della {action}: {str(e)}'

#******************************************
# Impostazioni Access Point
#******************************************

ssid = 'QMT_TORRETTA_TEST'
password = '123456789'

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid, password=password)

while not ap.active():
    pass

print('Connection successful!!!')
print('Informazioni sulla connessione: ')
print(ap.ifconfig())

#******************************************
# Server Socket
#******************************************

def handle_client(client_socket):
    request = client_socket.recv(1024).decode('utf-8')
    print('Request:', request)

    response = 'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n'
    
    if '/GET/get_pump_duration' in request:
        response += json.dumps({"pump_duration": get_pump_duration()})
    elif '/GET/get_pause_duration' in request:
        response += json.dumps({"pause_duration": get_pause_duration()})
    elif '/GET/get_pump_state' in request:
        response += json.dumps({"pump_state":get_pump_state()})
    elif '/GET/get_sensor_data' in request:
        response += json.dumps(get_sensor_data())
    elif '/SET/set_pump_duration' in request:
        try:
            start_query_string = request.find('?')
            query_string = request[start_query_string:]
            start_duration = query_string.find('duration=')

            if start_duration != -1:
                new_duration_str = query_string[start_duration + len('duration='):].split(' ')[0]
                new_duration = int(new_duration_str)

                set_pump_duration(new_duration)
                response += 'Durata della pompa cambiata con successo'
            else:
                raise ValueError("Parametro 'duration' non trovato nella richiesta")
            
        except Exception as e:
            response += f'Errore durante il cambiamento della pompa: {str(e)}'

    elif '/SET/set_pause_duration' in request:
        try:
            start_query_string = request.find('?')
            query_string = request[start_query_string:]
            start_pause_duration = query_string.find('pause=')

            if start_pause_duration != -1:
                new_pause_str = query_string[start_pause_duration + len('pause='):].split(' ')[0]
                new_pause = int(new_pause_str)

                set_pause_duration(new_pause)
                response += 'Durata della pausa cambiata con successo'
            else:
                raise ValueError("Parametro 'pause' non trovato nella richiesta")
            
        except Exception as e:
            response += f'Errore durante il cambiamento della pausa: {str(e)}'
            
    elif '/CHANGE/change_pump_state' in request:
        try:
            change_pump_state()
            response += 'Pump state cambiato con successo'
        except Exception as e:
            response += f'Error durante il cambiamento di stato della pompa: {str(e)}'
    elif '/RESET/reset_device' in request:
        response += 'Dispositivo in fase di reset...'
        client_socket.send(response)
        client_socket.close()
        machine.reset()
    # elif '/FORCE/start_pump' in request:
    #     try:
    #         pump.on()
    #         response += 'Pompa avviata forzatamente'
    #     except Exception as e:
    #         response += f'Errore durante l\'avvio forzato della pompa: {str(e)}'
    elif '/FORCE/start_pump' in request:
        try:
            pump_state = get_pump_state()
            response += 'Avvio forzato pompa e riavvio dispositivo in corso...'
            if pump_state == 1:
                change_pump_state()
                client_socket.send(response)
                client_socket.close()
                machine.reset()
            else:
                client_socket.send(response)
                client_socket.close()
                machine.reset()
        except Exception as e:
            response += f'Errore durante l\'avvio forzato della pompa: {str(e)}'
    else:
        response = 'HTTP/1.1 404 NOT FOUND\r\nContent-Type: text/plain\r\n\r\nEndpoint not found'
    
    client_socket.send(response)
    client_socket.close()

def start_server():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    server_socket = socket.socket()
    server_socket.bind(addr)
    server_socket.listen(5)
    print('Listening on', addr)
    
    while True:
        client_socket, client_addr = server_socket.accept()
        print('Client connected from', client_addr)
        handle_client(client_socket)

#******************************************
# Gestione Automatica Pompa
#******************************************

async def auto_pump():
    while True:
        pump_state = get_pump_state()
        
        if pump_state == 1:
            pause_duration = get_pause_duration()
            print(f"Pompa spenta per {pause_duration} minuti")
            change_pump_state()
            await asyncio.sleep(get_pause_duration() * 60)
        else:
            pump_duration = get_pump_duration()
            print(f"Pompa accesa per {pump_duration} minuti")
            change_pump_state()
            await asyncio.sleep(get_pump_duration() * 60)

#******************************************
# Main
#******************************************

async def main():
    loop = asyncio.get_event_loop()
    loop.create_task(auto_pump())

    _thread.start_new_thread(start_server, ())
    
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())