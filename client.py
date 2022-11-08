import socket
import threading
import tkinter as tk
from tkinter import messagebox

HOST = 'localhost'
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

window = tk.Tk()
window.title('Chat Application')

message_listbox = tk.Listbox(window, height=20, width=60)
message_listbox.pack(padx=10, pady=10)

message_entry = tk.Entry(window, width=60)
message_entry.pack(padx=10, pady=10)

def send_message(event=None):
    message = message_entry.get()
    client.send(message.encode('utf-8'))
    message_entry.delete(0, tk.END)

def receive_message():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            message_listbox.insert(tk.END, message)
        except:
            print('An error occurred while receiving messages from the server.')
            client.close()
            break

def on_closing():
    if messagebox.askokcancel('Quit', 'Are you sure you want to quit?'):
        client.send('QUIT'.encode('utf-8'))
        client.close()
        window.destroy()

window.protocol('WM_DELETE_WINDOW', on_closing)
window.bind('<Return>', send_message)

receive_thread = threading.Thread(target=receive_message)
receive_thread.start()

window.mainloop()
