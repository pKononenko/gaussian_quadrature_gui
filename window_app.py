import PySimpleGUI as sg
from integral_backend import integrate_f      


layout = [ [sg.Txt('Enter values to calculate')],      
            [sg.In(size=(5,1), key='upper_lim')],
            [sg.Text('∫', font=("Helvetica", 80)), sg.In(size=(12,1), key='f'), sg.Txt('dx = ', size=(8,1), key='output')],  
            [sg.In(size=(5,1), key='lower_lim')],      
            [sg.Button('Calculate', bind_return_key=True)]]      

window = sg.Window('Integral calculator', layout)      

while True:
    event, values = window.read()

    if event != sg.WIN_CLOSED:
        try:  
            b = float(values['upper_lim'])
            a = float(values['lower_lim'])
            f_str = str(values['f'])
            calc = integrate_f(a, b, f_str)
        except:
            calc = 'Invalid'

        window['output'].update("dx = " + str(calc))
    else:
        break
