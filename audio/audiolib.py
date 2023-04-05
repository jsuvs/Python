#Microphone and Speaker class based on sounddevice and asyncio
#mic_to_speaker.py contains example using these classes

import sounddevice
import numpy as np
import asyncio
import queue
import librosa
import soundfile as sf

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

#Encapsulates system speaker
#provides methods to play, pause and stop
class Speaker:
    def __init__(self, sample_rate, block_size):
        self.__sample_rate = sample_rate
        self.__block_size = block_size
        self.__output_stream = sounddevice.OutputStream(channels=1,samplerate=sample_rate,blocksize=block_size, callback=self.__callback,dtype="int16")
        self.__queue = queue.Queue()
        self.__buffer = None
        self.__state="stopped"
        self.speed=1.0
    def __callback(self, outdata, frames, time, status):
        while True:
            if self.__state == "stopped" or self.__state == "paused":
                #this causes execution of the callback to cease until output stream start is run
                raise sounddevice.CallbackAbort()
            #if there are enough frames in the buffer to return a full block
            if self.__buffer.shape[0] >= frames:
                outdata[:] = self.__buffer[:frames,:]
                self.__buffer = self.__buffer[frames:,:]
                break
            #only play remaining data if there is none queued
            #if will have to be padded with zeroes
            if self.__buffer.shape[0] > 0 and self.__queue.qsize() == 0:
                outdata[self.__buffer.shape[0]:].fill(0)
                self.__buffer = np.empty((0, 1))
                raise sounddevice.CallbackAbort()
            data = self.__queue.get()
            if data.shape[0] > 0:
                self.__buffer=np.concatenate((self.__buffer, data))

    #play or resume 
    #If speaker is already playing the samples will be 
    #appended to the existing buffer
    def play(self, samples=None):
        if samples is not None:
            self.__send_samples(samples)
        self.__state="playing"
        if not self.__output_stream.active:
            self.__output_stream.stop()
            self.__output_stream.start()

    def __send_samples(self, samples):
        samples = samples.astype(np.float32).transpose()
        samples = librosa.effects.time_stretch(samples, rate=self.speed)
        samples = samples.transpose()

        #if samples are a 1D array convert them to single channel 2D array
        if len(samples.shape) == 1:
            samples = samples.reshape((samples.shape[0], 1))
        #clear the buffer before starting from stopped
        if self.__state == "stopped":
            self.__buffer = np.empty((0, samples.shape[1]))
        self.__queue.put(samples)
    
    def pause(self):
        self.__state = "paused"

    def stop(self):
        self.__state = "stopped"
        self.__queue.empty()

async def test():
    filename = 'audio/output.wav'
    data, fs = sf.read(filename, dtype='int16')
    speaker = Speaker(16000, 1024)
    speaker.play(data)
    speaker.play(data)
    await asyncio.sleep(11)
    speaker.play(data)
    await asyncio.sleep(4)
    speaker.stop()
    await asyncio.sleep(1)
    speaker.play()
    await asyncio.sleep(1)
    speaker.stop()
    await asyncio.sleep(1)
    speaker.play(data)
    await asyncio.sleep(8)

async def test2():
    sample_rate=8000
    block_size=4000
    speaker = Speaker(sample_rate, 2000)
    t = np.arange(0, block_size/sample_rate*2.4, 1/sample_rate)
    freq = 1500
    while True:
        freq+=100
        n = 100 * np.sin(2 * np.pi * freq * t)
        n = n.astype('int16')
        speaker.play(n)
        await asyncio.sleep(10)
        #break

#asyncio.run(test())
