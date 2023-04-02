#Microphone and Speaker class based on sounddevice and asyncio
#mic_to_speaker.py contains example using these classes

import sounddevice
import wavio
import numpy as np
import asyncio

#Encapsulates the system microphone providing an async method to read audio data from it
class Microphone:
    def __init__(self, sample_rate, block_size):
        self.__sample_rate = sample_rate
        self.__block_size = block_size
    async def get_data(self):
        loop = asyncio.get_event_loop()
        #started off using a queue here as a buffer, but don't currently have support for 
        #speeding up reading if the input data is backing up and for live playback it's better to just skip to the latest
        #anyway
        #so for now the queue is set to size one, even though that really negates the point of using a queue
        q = asyncio.Queue(maxsize = 1)
        def write(data):
            try:
                q.put_nowait(data)
            except Exception as exc:
                return
            
        #called with indata as the latest microphone data
        def callback(indata : np.ndarray, frame_count, time_info, status):
            #callback runs on a different thread so need to use threadsafe
            #call the write method which writes the data to the queue
            loop.call_soon_threadsafe(write, indata.copy())
        
        #begin streaming from the microphone. This will cause the callback above
        #to be periodically called with latest input data 
        input_stream = sounddevice.InputStream(channels=1,samplerate=self.__sample_rate,callback=callback,blocksize=self.__block_size,dtype="int16")
        with input_stream:
            while True:
                #print(q.qsize())
                data = await q.get()
                yield data

#Encapsulates system speaker, providing a method to output audio data to it
class Speaker:
    def __init__(self, sample_rate, block_size):
        self.__sample_rate = sample_rate
        self.__block_size = block_size
        self.__output_stream = sounddevice.OutputStream(channels=1,samplerate=sample_rate,blocksize=block_size,dtype="int16")
        
    def start(self):
        self.__output_stream.start()

    def send(self, data):
        if not self.__output_stream.active:
            self.__output_stream.start()
        self.__output_stream.write(data)
