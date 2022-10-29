from multiprocessing import Event
import time, socket, sys
import PySimpleGUI as sg

sg.theme('Dark')

new_socket = socket.socket()
host_name = socket.gethostname()
s_ip = socket.gethostbyname(host_name)
port = 8080

login_form = [
                [sg.Text('Enter your name:'), sg.InputText(key = 'NAME')], 
                [sg.Button('Ok')]
             ]
send_message_form = [
    [sg.Text('Enter your mesage: '), sg.InputText(key='MESSAGE', do_not_clear=False)],
    [sg.Button('Send'), sg.Button('Close')]
]
new_socket.bind((host_name, port))
sg.Print( "Binding successful!")
sg.Print("This is your IP: ", s_ip)

window = sg.Window('Log-in', login_form)
a=True
while a:
    event, value = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == 'Ok':
        name = value['NAME']
        new_socket.listen(1) 
        conn, add = new_socket.accept()
        sg.Print("Received connection from ", add[0])
        sg.Print('Connection Established. Connected From: ',add[0])
        client = (conn.recv(1024)).decode()
        sg.Print(client + ' has connected.')
        conn.send(name.encode())
        window.close()
window = sg.Window('Message', send_message_form)
while True:
    event, value = window.read()
    if value['MESSAGE'] != "" and event == 'Send':
        message = value['MESSAGE']
        sg.Print(f'{name} : {message}')
    elif event == 'Close' or event == sg.WIN_CLOSED:
        break
    conn.send(message.encode())
    message = conn.recv(1024)
    message = message.decode()
    sg.Print(client, ':', message)
