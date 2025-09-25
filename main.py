from modules import logs
import threading
from modules.mainloop import main_loop
from pythonosc.udp_client import SimpleUDPClient
from config import *

client1 = SimpleUDPClient(IP1, PORT)
client2 = SimpleUDPClient(IP2, PORT)

threading.Thread(target=main_loop, daemon=True).start()

logs.initui()
mainloop.main_loop()
