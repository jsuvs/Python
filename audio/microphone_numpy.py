#this example records 5 seconds of microphone input and writes it to a file sound.wav
#this is the same as microphone.py except it uses sounddevice.InputStream and a numpy array

#python -m pip install sounddevice
#python -m pip install wavio 
import sounddevice
import wavio
import numpy as np

#somewhere to hold accumulated recorded data
recorded_bytes = np.ndarray(shape=(0,1), dtype = np.int16)

#this function will be called periodically (like 8 times a second in this example) while recording 
#with new recorded data from the microphone. 'indata' is the buffer of new data
def callback(indata : np.ndarray, frame_count, time_info, status):
    print(indata.shape) #shape is (2048, 1)
    print(indata.dtype) #int16
    #this means the data is [[1], [2], [3], [4], [5], etc]
    global recorded_bytes
    if status:
        print(status)
    print(frame_count)
    #append the new data to the end of the output buffer
    recorded_bytes = np.concatenate((recorded_bytes, indata))


#how many samples to record per second
sample_rate=16000
#each sample will be 2 bytes
#signed short, or two byte integer
sample_size=2 #int16
#block_size determines how many bytes must be read before callback is called each time
#this determines the frequency that the callback will be called
#and each time it is called the indata will contain this many bytes
block_size=2048
default_microphone = sounddevice.query_devices(kind='input')

#now to set up a microphone input stream using these settings
stream = sounddevice.InputStream(
        channels=1,
        samplerate=sample_rate,
        callback=callback,
        blocksize=block_size,
        dtype="int16"
    )

#during a sounddevice.sleep execution blocks and callback is periodically called with new microphone stream data.
#record for 5000 milliseconds
with stream:
    sounddevice.sleep(5000)
print(recorded_bytes.shape)
wavio.write("sound.wav", recorded_bytes, rate=sample_rate, sampwidth=sample_size)