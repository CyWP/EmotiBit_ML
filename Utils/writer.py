from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
import asyncio
import numpy as np
import pandas as pd
import time

class OSCSV():

    ADDRESS_PREFIX = "/EmotiBit/0/"

    #We are somehow missing: scr:amp,freq,ris , temp, hr, 
    ADDRESS_POSTFIXES = ("EDA", "T1", "SF",
                        "PPG:IR", "PPG:RED", "PPG:GRN",
                        "ACC:X", "ACC:Y", "ACC:Z",
                        "GYRO:X", "GYRO:Y", "GYRO:Z",
                        "MAG:X", "MAG:Y", "MAG:Z")
    
    BASE_METRICS = ['EA', 'T1', 'SF',
                'PI', 'PR', 'PG',
                'AX', 'AY', 'AZ',
                'GX', 'GY', 'GZ',
                'MX', 'MY', 'MZ']
    
    def __init__(self):
        self.input = None
        self.vector = np.ones(len(OSCSV.ADDRESS_POSTFIXES))
        self.stop = False
        self.classes = []

    @classmethod
    def get_presets(_cls):
        return [str(key) for key in CSVWriter.MASKS.keys()]

    def add_class(self, name):
        self.classes.append(name)

    def remove_class(self, index):
        self.classes.pop(index)

    def get_classes(self):
        return self.classes
    
    def msg_handler(self, address, args, index):
        start = time.time()
        self.vector[index] = np.mean(args[0])
        if start - self.time > self.wait:
            self.writer.write(self.vector)
        self.time = time.time()

    async def stop_writing(self):
        self.stop = True

    async def write(self, dest, name, preset='ALL', port=12345, frequency=10, ip='127.0.0.1'):

        self.stop = False  
        self.interval = max(0, 0.9/frequency-0.05*len(self.classes))
        self.wait = self.interval
        self.time = time.time() 
        self.writer = CSVWriter(dest, name, preset)
        dispatcher = Dispatcher()

        for i, postfix in enumerate(OSCSV.ADDRESS_POSTFIXES):
            dispatcher.map(OSCSV.ADDRESS_PREFIX + postfix, lambda address, *args, index=i: self.msg_handler(address, args, index))

        server = osc_server.AsyncIOOSCUDPServer((ip, port), dispatcher, asyncio.get_event_loop())
        transport, protocol = await server.create_serve_endpoint()  # Create datagram endpoint and start serving
        await self.loop(transport)
        transport.close()
        self.writer.save_and_close()

    async def loop(self, transport):
        while not self.stop:
            await asyncio.sleep(0.5)

class CSVWriter():

    MASKS = {'ALL': np.array([True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]),
             'IMU': np.array([False, False, False, False, False, False, True, True, True, True, True, True, True, True, True]),
             'BIO': np.array([True, True, True, True, True, False, False, False, False, False, False, False, False, False, False])}

    def __init__(self, dest, name, preset):
        self.dest = dest
        self.name=name
        self.mask = CSVWriter.MASKS[preset]
        self.array = np.zeros(shape=(np.sum(self.mask,)+1))
    
    def dest_file(self):
        return f'{self.dest}/{self.name}.{str(time.time())}.csv'

    def write(self, vector):
        self.array = np.vstack([self.array, np.insert(vector[self.mask], 0, time.time())])

    def save_and_close(self):
        self.array = self.array[2:]
        self.array[:, 0] -= np.min(self.array[:, 0])
        self.array[:, 0] *= 1000
        cols = np.asarray(OSCSV.BASE_METRICS)[self.mask].tolist()
        cols.insert(0, 'timestamp')
        df = pd.DataFrame(self.array, columns=cols)
        df.to_csv(self.dest_file(), index=False, header=True, mode='w')
        self.array = np.zeros(shape=(np.sum(self.mask)+1))