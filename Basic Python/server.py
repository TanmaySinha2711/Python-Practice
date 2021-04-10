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


def start_server():
    pass


def stop_server():
    pass


server_window.mainloop()
