__author__ = 'djff'

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from functools import partial
from kivy.lang import Builder
from kivy.app import App
import socket
import threading

# Builder.load.string("""
#     <AnimWidget@Widget>:
#     canvas:
#         Color:
#             rgba: 0.7, 0.3, 0.9, 1
#         Rectangle:
#             pos: self.pos
#             size: self.size
#     size_hint: None, None
#     size: 400, 30
#     """)


class Client(FloatLayout):
    heading = """
       Client-Server GUI is a project based on socket programming.
    It is developed in kivy using Python, sockets and multithreading\n
    """
    home_text = """
    Basic Features include:
    [+]   Connect To Server
    [+]   View Online clients
    [+]   Chat with contacts
    [+]   Disconnect from server  \n\n
    Future Features to be Include:
    [+]   Zero Configuation
    [+]   File Transfering
    [+]   File Sharing
    [+]   Notifications

    """

    def __init__(self, **kwargs):
        super(Client, self).__init__(**kwargs)
        self.Mainlabel = Label(text="Client-Server GUI CEF508", color=(0.6, 0.7, 0.2, 1), font_size="50sp",
                               pos=(280, 450),
                               size_hint=(.3, .3))
        self.add_widget(self.Mainlabel)
        self.cont_but = Button(text="Cont...", background_color=(0.2, 0.3, 0.88, 1), pos=(700, 30), size_hint=(.12, .1))
        self.add_widget(self.cont_but)
        self.INFO = Label(size_hint=(.3, .3), pos=(270, 300), color=(0.6, 0.3, 0.1, 1), font_size="21dp")
        self.INFO2 = Label(size_hint=(.3, .3), pos=(230, 80), color=(0.3, 0.3, 0.7, 1), font_size="20dp")
        self.INFO.text += self.heading
        self.INFO2.text += self.home_text
        self.add_widget(self.INFO)
        self.add_widget(self.INFO2)
        self.anim_info2 = Animation(x=80, y=150, opacity=0.4, d=0.4, t='in_quad') + \
                          Animation(x=230, y=80, opacity=1, d=0.5)
        self.anim_info2.start(self.INFO2)
        self.cont_but.bind(on_press=self.connectpage)
        self.sock = ''
        self.cport = ''
        self.sendarea = ''

    def connectpage(self, touch):
        chost = TextInput(text="localhost", hint_text="Enter host", size_hint=(.2, .1), pos=(50, 350),
                          multiline=False, background_color=(0.4, 0.5, 1, 0.9), foreground_color=(255, 255, 255, 1))
        self.cport = TextInput(text="8000", hint_text="Enter port", size_hint=(.2, .1), pos=(50, 250),
                               multiline=False, background_color=(0.4, 0.5, 1, .9), foreground_color=(255, 255, 255, 1))
        button = Button(text="Start Client", size_hint=(.2, .1), background_color=(0.1, 0.7, 0.3, 1), pos=(50, 100))
        self.clear_widgets()
        self.add_widget(chost)
        self.add_widget(self.cport)
        self.add_widget(button)
        self.add_widget(self.Mainlabel)
        self.cport.bind(on_text_validate=partial(self.connect))


    def connect(self, test):
        port = self.cport.text
        if port.isdigit():
            try:
                self.sock = socket.socket()
                host = socket.gethostname()
                self.sock.connect((host, int(port)))
            except:
                print "error connecting"
                return

            self.clear_widgets()
            self.sendarea = Label(text="", size_hint=(.2, .2), pos=(80, 400), font_size="19dp", color=(0.7, 0.5, 0.6, 1))
            update = Button(text="Refresh", background_color=(0.3, 0.3, 0.9, 1), size_hint=(.25, .1), pos=(600, 550))

            self.chat_lid = TextInput(hint_text="Send msg",pos=(100,50),size_hint=(.6,.1),multiline=False)
            self.add_widget(self.chat_lid)
            self.chat_lid.bind(on_text_validate=partial(self.send_to_server))
            self.add_widget(update)
            self.add_widget(self.sendarea)
            threading.Thread(target=self.listenserver).start()
        else:
            pass

    def send_to_server(self, touch):
        msg = self.chat_lid.text
        if msg:
            self.sock.send(msg)
            self.chat_lid.text = ''

    def listenserver(self):
        while True:
            msg = self.sock.recv(1024)
            self.sendarea.text += str(msg) + '\n'

class Interface(App):
    def __init__(self, **kwargs):
        super(Interface, self).__init__(**kwargs)

    def build(self):
        return Client()


if __name__ == "__main__":
    # port_num = int(input("Port? "))
    # ThreadedServer('', port_num).listen()
    Interface().run()
