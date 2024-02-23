from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
import asyncio
import numpy as np

ADDRESS_PREFIX = "/EmotiBit/0/"

#We are somehow missing: scr:amp,freq,ris , temp, hr, 
ADDRESS_POSTFIXES = ("GYRO:X", "GYRO:Y", "GYRO:Z",
                     "MAG:X", "MAG:Y", "MAG:Z",
                     "ACC:X", "ACC:Y", "ACC:Z",
                     "PPG:IR", "PPG:RED", "PPG:GRN",
                     "EDA")

VECTOR = np.ones(len(ADDRESS_POSTFIXES))

def msg_handler(address, args, index):
    #print(args)
    VECTOR[index] = np.mean(args[0])

async def loop():
    for i in range(10):
        print(VECTOR)
        await asyncio.sleep(0.1)

async def start_listening_server(custom_port=False, port=12345):

    dispatcher = Dispatcher()

    ip = "127.0.0.1"

    for i, postfix in enumerate(ADDRESS_POSTFIXES):
        dispatcher.map(ADDRESS_PREFIX + postfix, lambda address, *args, index=i: msg_handler(address, args, index))

    server = osc_server.AsyncIOOSCUDPServer((ip, port), dispatcher, asyncio.get_event_loop())
    print("Serving on {}".format(server._server_address))
    transport, protocol = await server.create_serve_endpoint()  # Create datagram endpoint and start serving

    await loop()

    transport.close()

if __name__ == "__main__":
    
    asyncio.run(start_listening_server())