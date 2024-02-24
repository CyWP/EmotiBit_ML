from pythonosc.dispatcher import Dispatcher
from pythonosc.udp_client import SimpleUDPClient
from pythonosc import osc_server
import asyncio
import numpy as np
import time

class OSCRelay():

    ADDRESS_PREFIX = "/EmotiBit/0/"

    #We are somehow missing: scr:amp,freq,ris , temp, hr, 
    ADDRESS_POSTFIXES = ("EDA",
                        "PPG:IR", "PPG:RED", "PPG:GRN"
                        "ACC:X", "ACC:Y", "ACC:Z",
                        "GYRO:X", "GYRO:Y", "GYRO:Z",
                        "MAG:X", "MAG:Y", "MAG:Z")

    @classmethod
    def get_presets(_cls):
        return RelayClient.get_presets()
    
    def __init__(self):
        self.input = None
        self.clients = []
        self.vector = np.ones(len(OSCRelay.ADDRESS_POSTFIXES))
        self.stop = False

    def add_client(self, ip, port, preset):
        self.clients.append(RelayClient(ip, port, preset))

    def remove_client(self, index):
        self.clients.pop(index)

    def get_clients(self):
        clientlist = []
        for client in self.clients:
            clientlist.append((client.ip, client.port, client.preset))
        return clientlist
    
    async def stop_dispatch(self):
        self.stop = True
    
    def msg_handler(self, address, args, index):
        self.vector[index] = np.mean(args[0]) 

    async def dispatch(self, port=12345, frequency=10, ip='127.0.0.1'):

        self.stop = False       
        dispatcher = Dispatcher()

        for i, postfix in enumerate(OSCRelay.ADDRESS_POSTFIXES):
            dispatcher.map(OSCRelay.ADDRESS_PREFIX + postfix, lambda address, *args, index=i: self.msg_handler(address, args, index))

        server = osc_server.AsyncIOOSCUDPServer((ip, port), dispatcher, asyncio.get_event_loop())
        transport, protocol = await server.create_serve_endpoint()  # Create datagram endpoint and start serving

        await self.loop(frequency)
        transport.close()

    async def loop(self, frequency):
        rest = 1/frequency
        while not self.stop:
            start = time.time()
            for client in self.clients:
                client.send_message(OSCRelay.ADDRESS_PREFIX, self.vector[client.mask])
            await asyncio.sleep(max(0, rest-time.time()+start))

class RelayClient(SimpleUDPClient):

    MASKS = {'ALL': np.array([True, True, True, True, True, True, True, True, True, True, True, True, True]),
             'IMU': np.array([False, False, False, False, True, True, True, True, True, True, True, True, True]),
             'BIO': np.array([True, True, True, True, False, False, False, False, False, False, False, False, False, False])}

    def __init__(self, ip, port, preset):

        super().__init__(ip, port)
        self.ip = ip
        self.port = port
        self.preset = preset
        self.mask = RelayClient.MASKS[preset]

    @classmethod
    def get_presets(_cls):
        return [str(key) for key in RelayClient.MASKS.keys()]