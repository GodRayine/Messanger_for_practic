import time, socket, sys
import PySimpleGUI as sg

sg.theme('Dark')

socket_server = socket.socket()
server_host = socket.gethostname()
ip = socket.gethostbyname(server_host)
sport = 8080

login_form = [
                [sg.Text(f'This is your IP address: {ip}')], 
                [sg.Text('Enter your name:'), sg.InputText(key = 'NAME')], 
                [sg.Text('Enter Friend\'s ip: '), sg.InputText(key = 'FIP')],
                [sg.Button('Ok')]
             ]

send_message_form = [
    [sg.Text('Enter your mesage: '), sg.InputText(key='MESSAGE', do_not_clear=False)],
    [sg.Button('Send'), sg.Button('Close')]
]

layout1 = [
            [sg.Column(login_form)]       
         ]

window = sg.Window('Log-in', layout1)

a = True

while a:
    event, value = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == 'Ok':
        server_host = value['FIP']
        name = value['NAME']

        socket_server.connect((server_host, sport))
    
        socket_server.send(name.encode())
        server_name = socket_server.recv(1024)
        server_name = server_name.decode()
        connection_atempt = f'{server_name} has joined...'
        window.close() 
        a = False
send_window = sg.Window('message', send_message_form)
sg.Print(connection_atempt)    
while True:
    message = (socket_server.recv(1024)).decode()
    sg.Print(server_name, ":", message)
    event, value = send_window.read()
    if value['MESSAGE'] != "" and event == 'Send':
        message = value['MESSAGE']
        sg.Print(f'{name} : {message}')
    elif event == 'Close' or event == sg.WIN_CLOSED:
        break
    socket_server.send(message.encode())
# 
