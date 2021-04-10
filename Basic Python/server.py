import socket
import tkinter as tk
import threading

# init gui server window
server_window = tk.Tk()
server_window.title("Server")

# add buttons to start and stp server to header frame
headerFrame = tk.Frame(server_window)
btnStart = tk.Button(headerFrame, text="Start server", command=lambda: start_server())
btnStart.pack(side=tk.LEFT)
btnStop = tk.Button(headerFrame, text="Stop server", command=lambda: stop_server(), state=tk.DISABLED)
btnStop.pack(side=tk.LEFT)
headerFrame.pack(side=tk.TOP, pady=(5, 0))

# add scrollable textarea in a client frame
clientFrame = tk.Frame(server_window)
scrollBar = tk.Scrollbar(clientFrame)
scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
tkDisplay = tk.Text(clientFrame, height=15, width=30)
tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
scrollBar.config(command=tkDisplay.yview)
tkDisplay.config(yscrollcommand=scrollBar.set, background="#F4F6F7", highlightbackground="grey", state="disabled")
clientFrame.pack(side=tk.BOTTOM, pady=(5, 10))

# define server network settings
SERVER_IP = "127.0.0.1"
SERVER_PORT = 5002
clients = {}
MAX_CLIENTS = 5
MAX_MSG_SIZE = 4096
server = None


def start_server():
    global server
    btnStart.config(state=tk.DISABLED)
    btnStop.config(state=tk.NORMAL)

    # define socket server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_IP, SERVER_PORT))
    server.listen(MAX_CLIENTS)
    threading.Thread(target=accept_clients, args=(server,)).start()


def stop_server():
    btnStart.config(state=tk.NORMAL)
    btnStop.config(state=tk.DISABLED)


def accept_clients(from_server):
    while True:
        client, client_addr = from_server.accept()
        threading.Thread(target=send_receive_client_message, args=(client,)).start()


def send_client_status_message(client_name, status):
    tkDisplay.config(state=tk.NORMAL)
    tkDisplay.insert(tk.END, f"{client_name} {status}.....\n")
    tkDisplay.config(state=tk.DISABLED)


def send_receive_client_message(client_conn):
    global server, clients

    # send welcome message to client
    client_name = client_conn.recv(MAX_MSG_SIZE).decode('utf-8')
    clients[client_name] = client_conn

    # send connect message
    send_client_status_message(client_name, "connected")  # update client names display

    while True:
        client_msg = client_conn.recv(MAX_MSG_SIZE).decode('utf-8')
        if not client_msg or client_msg == "exit":
            break

        for k in clients:
            if k != client_name:
                clients[k].send(f"{k} -> {client_msg}".encode())

    # on client disconnect
    clients[client_name].send("BYE!".encode())
    clients[client_name].close()
    try:
        clients.pop(client_name)
    except KeyError:
        pass
    # send disconnect message
    send_client_status_message(client_name, "disconnected")  # update client names display


server_window.mainloop()
