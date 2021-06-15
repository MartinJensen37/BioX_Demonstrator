import PySimpleGUI as sg
import time
import random
import sys
import firebase_admin
from firebase_admin import db
sys.path.insert(0, "..")

############################################ FIREBASE SETUP ############################################################
cred_obj = firebase_admin.credentials.Certificate('../biox_key2.json')
default_app = firebase_admin.initialize_app(cred_obj, {
	'databaseURL':'https://biox-46f4c-default-rtdb.europe-west1.firebasedatabase.app/'
	})

ref = db.reference('/project')
PLC_ref = ref.child('PLC')
plc_ids = ['STPLC_08', 'STPLC_09']

############################################ GUI SETUP #################################################################
sg.theme('Default')

def LEDIndicator(key=None, radius=30):
    return sg.Graph(canvas_size=(radius, radius),
             graph_bottom_left=(-radius, -radius),
             graph_top_right=(radius, radius),
             pad=(0, 0), key=key)

def SetLED(window, key, color):
    graph = window[key]
    graph.erase()
    graph.draw_circle((0, 0), 16, fill_color=color, line_color=color)

layout = [[sg.Text('PLC', size=(17, 1)), sg.Text('Status'), sg.Text('on/off')],
          [sg.Text('STPLC_08 Conveyor', size=(17, 1)), LEDIndicator('STPLC_08'), sg.Text('', size=(8, 1)), sg.Button('', image_filename="../on-off1.PNG", button_color='white', image_size=(28,28), key=('StartConveyor', 'STPLC_08'))],
          [sg.Text('STPLC_09 Conveyor', size=(17, 1)), LEDIndicator('STPLC_09'), sg.Text('', size=(8, 1)), sg.Button('', image_filename="../on-off1.PNG", button_color='white', image_size=(28,28), key=('StartConveyor', 'STPLC_09'))],
          [sg.Text('Stopper 1', size=(17, 1)), LEDIndicator('STPLC_08_stp'), sg.Text('', size=(8, 1)), sg.Button('', image_filename="../on-off1.PNG", button_color='white', image_size=(28,28), key=('ReleaseStopper', 'STPLC_08'))],
          [sg.Text('Stopper 2', size=(17, 1)), LEDIndicator('STPLC_09_stp'), sg.Text('', size=(8, 1)), sg.Button('', image_filename="../on-off1.PNG", button_color='white', image_size=(28,28), key=('ReleaseStopper', 'STPLC_09'))],
          [sg.Button('Exit')]]

window = sg.Window('Festo Status Interface', layout, default_element_size=(12, 1), auto_size_text=False, finalize=True)

############################################ EVENT LOOP #################################################################
flag = 0

while True:
    event, value = window.read(timeout=400)
    if event == 'Exit' or event == sg.WIN_CLOSED:
        break
    if value is None:
        break

    if event[0] is 'ReleaseStopper':
        STPLC_id = PLC_ref.child(event[1])
        STPLC_id.update({event[0]: True})
        SetLED(window, plc_id, 'green')


    if event[0] is 'StartConveyor':
        message = ref.get()
        print(message['PLC'][event[1]]['StartConveyor'])
        if message['PLC'][event[1]]['StartConveyor'] is False:
            STPLC_id = PLC_ref.child(event[1])
            STPLC_id.update({event[0]: True})
        elif message['PLC'][event[1]]['StartConveyor'] is True:
            STPLC_id = PLC_ref.child(event[1])
            STPLC_id.update({event[0]: False})

    status = ref.get()
    for plc_id in plc_ids:
        if status['PLC'][plc_id]['StartConveyor'] is True:
            SetLED(window, plc_id, 'green')
        elif status['PLC'][plc_id]['StartConveyor'] is False:
            SetLED(window, plc_id, 'red')
        if status['PLC'][plc_id]['ReleaseStopper'] is True:
            SetLED(window, plc_id + '_stp', 'green')
        elif status['PLC'][plc_id]['ReleaseStopper'] is False:
            SetLED(window, plc_id + '_stp', 'red')

window.close()



