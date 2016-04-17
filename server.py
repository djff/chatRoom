__author__ = 'djff'

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
import socket
import threading


class Server(FloatLayout):
    def __init__(self, **kwargs):
        super(Server, self).__init__(**kwargs)
        self.online = Label(text="Available Clients:", size_hint=(.2, .2), color=(0.1, 0.9, 0.1, 1), font_size="19dp",
                            pos=(10, 480))
        self.conn = TextInput(text="NONE ", size_hint=(.7, .25), foreground_color=(0.1, 0.1, 0.9, 1), pos=(180, 410))
        self.message = Label(text="Server is currently down", font_size="19dp", size_hint=(.5, .5),
                             color=(0.9, 0.1, 0.1, 1), pos=(190, 210))
        self.start = Button(text='Start Server', size_hint=(.18, .1),
                            background_color=(0.5, 0.7, 1, 1), pos=(150, 100))
        self.port = TextInput(hint_text="Enter port no", size_hint=(.18, .1), pos=(320, 260),
                              multiline=False, foreground_color=(180, 0, 210, 200), font_size='20dp')
        self.stop = Button(text='Stop Server', size_hint=(.18, .1),
                           background_color=(1, 0, 0, 1), pos=(500, 100))
        self.stop.disabled = True
        self.start.bind(on_press=self.startserver)
        self.stop.bind(on_press=self.stopserver)
        self.add_widget(self.conn)
        self.add_widget(self.online)
        self.add_widget(self.message)
        self.add_widget(self.start)
        self.add_widget(self.port)
        self.add_widget(self.stop)
        self.socket = ''
        self.client_online = []

    def startserver(self, touch):
        port = self.port.text
        if port.isdigit():
            self.message.text = "Server Started and Listening to port {0}".format(port)
            self.message.color = '0101'
            self.start.text = "Server Started"
            self.start.disabled = True
            self.stop.disabled = False
            # starting server
            self.initserver(int(port))
            threading.Thread(target=self.listen).start()

        else:
            self.message.text = "Invalid Port Number"

    def stopserver(self, touch):
        self.message.text = 'Server is currently down'
        self.start.disabled = False
        self.stop.disabled = True
        self.port.text = ''
        self.sock.close()

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            client_name = str(client.getpeername()[0])
            self.message.text = "got connection from {0}".format(client_name)
            self.conn.text += str(client) + " , "
            self.client_online.append(client)
            threading.Thread(target=self.listenToClient, args=(client, address)).start()

    def listenToClient(self, client, address):
        size = 1024
        while True:
            try:
                data = client.recv(size)
                if data:
                    print data
                    response = str(data)
                    for cl in self.client_online:
                        cl.send(response)
                    print str(client) + " @@,## " + str(self.client_online[0])
                else:
                    raise Exception('Client disconnected')
            except:
                client.close()
                return False

    def get_online_contacts(self):
        return self.client_online

    def initserver(self, port):
        host = '0.0.0.0'
        port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((socket.gethostname(), port))


class Interface(App):
    def __init__(self, **kwargs):
        super(Interface, self).__init__(**kwargs)

    def build(self):
        return Server()


if __name__ == "__main__":
    # port_num = int(input("Port? "))
    # ThreadedServer('', port_num).listen()
    Interface().run()
