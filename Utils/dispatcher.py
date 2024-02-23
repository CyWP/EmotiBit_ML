from pythonosc.dispatcher import Dispatcher
from pythonosc.udp_client import SimpleUDPClient
from pythonosc import osc_server
import asyncio

ADDRESS_PREFIX = "/EmotiBit/0/"

#We are somehow missing: scr:amp,freq,ris , temp, hr, 
ADDRESS_POSTFIXES = ("GYRO:X", "GYRO:Y", "GYRO:Z",
                     "MAG:X", "MAG:Y", "MAG:Z",
                     "ACC:X", "ACC:Y", "ACC:Z",
                     "PPG:IR", "PPG:RED", "PPG:GRN",
                     "EDA")

class OSCRelay():

    def __init__(self):
        self.input = None
        self.clients = []
        self.stop = False

    def add_client(self, ip, port):
        self.clients.append(RelayClient(ip, port))

    def remove_client(self, index):
        self.clients.pop(index)

    def get_clients(self):
        clients = []
        for client in self.clients:
            clients.append((client.ip, client.port))
        return clients
    
    async def stop_dispatch(self):
        self.stop = True

    def msg_handler(self, address, *args):
        for client in self.clients:
            client.send_message(address, args)

    async def dispatch(self, port=12345):

        self.stop = False
        
        ip = '127.0.0.1'
        dispatcher = Dispatcher()
        for i, postfix in enumerate(ADDRESS_POSTFIXES):
            dispatcher.map(ADDRESS_PREFIX + postfix, lambda address, *args: self.msg_handler(address, *args))
        server = osc_server.AsyncIOOSCUDPServer((ip, port), dispatcher, asyncio.get_event_loop())
        transport, protocol = await server.create_serve_endpoint()  # Create datagram endpoint and start serving
        await self.loop()
        transport.close()

    async def loop(self):
        while not self.stop:
            await asyncio.sleep(0.1)

class RelayClient(SimpleUDPClient):

    def __init__(self, ip, port):

        super().__init__(ip, port)
        self.ip = ip
        self.port = port