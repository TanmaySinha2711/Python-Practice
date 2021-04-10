import tkinter as tk
from tkinter import messagebox
import socket
import threading

# init UI window
window = tk.Tk()
window.title("Client")
username = " "

topFrame = tk.Frame(window)
lblName = tk.Label(topFrame, text="Name:").pack(side=tk.LEFT)
entered_name = tk.Entry(topFrame)
entered_name.pack(side=tk.LEFT)
btnConnect = tk.Button(topFrame, text="Connect", command=lambda: connect())
btnConnect.pack(side=tk.LEFT)
topFrame.pack(side=tk.TOP)

displayFrame = tk.Frame(window)
scrollBar = tk.Scrollbar(displayFrame)
scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
tkDisplay = tk.Text(displayFrame, height=20, width=55)
tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
tkDisplay.tag_config("tag_your_message", foreground="blue")
scrollBar.config(command=tkDisplay.yview)
tkDisplay.config(yscrollcommand=scrollBar.set, background="#F4F6F7", highlightbackground="grey", state="disabled")
displayFrame.pack(side=tk.TOP)

bottomFrame = tk.Frame(window)
tkMessage = tk.Text(bottomFrame, height=2, width=55)
tkMessage.pack(side=tk.LEFT, padx=(5, 13), pady=(5, 10))
tkMessage.config(highlightbackground="grey", state="disabled")
tkMessage.bind("<Return>", (lambda event: get_chat_message(tkMessage.get("1.0", tk.END))))
bottomFrame.pack(side=tk.BOTTOM)


def connect():
    global username, client
    if len(entered_name.get()) < 1:
        tk.messagebox.showerror(title="ERROR!", message="You MUST enter a name for this session")
    else:
        username = entered_name.get()
        connect_to_server(username)


# network client
client = None
SERVER_IP = "127.0.0.1"
HOST_PORT = 5002
MAX_MSG_SIZE = 4096


def connect_to_server(name):
    global client, HOST_PORT, SERVER_IP
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((SERVER_IP, HOST_PORT))
        client.send(name.encode())  # Send name to server after connecting

        entered_name.config(state=tk.DISABLED)
        btnConnect.config(state=tk.DISABLED)
        tkMessage.config(state=tk.NORMAL)

        # start a thread to keep receiving message from server
        threading.Thread(target=receive_message_from_server, args=(client,)).start()
    except Exception as e:
        tk.messagebox.showerror(title="ERROR!", message=f"Cannot connect to host: {SERVER_IP} on port:{str(HOST_PORT)}"
                                                          f"\nServer may be Unavailable. "
                                                          f"Try again later")


def receive_message_from_server(sck):
    while True:
        from_server = sck.recv(MAX_MSG_SIZE).decode('utf-8')

        if not from_server:
            break

        # display message from server on the chat window
        # enable the display area and insert the text and then disable.
        tkDisplay.config(state=tk.NORMAL)
        tkDisplay.insert(tk.END, f"\n\n{from_server}")
        tkDisplay.config(state=tk.DISABLED)
        tkDisplay.see(tk.END)

    sck.close()
    window.destroy()


def get_chat_message(msg):
    msg = msg.replace('\n', '')

    tkDisplay.config(state=tk.NORMAL)
    tkDisplay.insert(tk.END, f"\n\nYou -> {msg}")
    tkDisplay.config(state=tk.DISABLED)
    send_message_to_server(msg)
    tkDisplay.see(tk.END)


def send_message_to_server(msg):
    global client
    client.send(msg.encode())
    if msg == "exit":
        client.close()
        window.destroy()


window.mainloop()
