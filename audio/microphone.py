#this example records 5 seconds of microphone input and writes it to a file sound.wav
#the example is based on documentation samples

#a useful feature of the method used below is access to the live stream of data as it is being recorded
#so you could in theory modify it on the fly and/or stream the audio somewhere or route it to a speaker

#the sounddevice library is used to record from the microphone
#the wavio library is used to write the recorded data to a wav file
#   the numpy library is needed by the wavio library

#python -m pip install sounddevice
#python -m pip install wavio 
import sounddevice
import wavio
import numpy as np

#somewhere to hold accumulated recorded data
recorded_bytes = []

#this function will be called periodically (like 8 times a second in this example) while recording 
#with new recorded data from the microphone. 'indata' is the buffer of new data
def callback(indata, frame_count, time_info, status):
    global recorded_bytes
    if status:
        print(status)
    print(frame_count)
    #append the new data to the end of the output buffer
    recorded_bytes += bytes(indata)


#how many samples to record per second
sample_rate=16000
#each sample will be 2 bytes
#signed short, or two byte integer
sample_size=2 #int16

#block_size determines how many bytes must be read before callback is called each time
#this determines the frequency that the callback will be called
#and each time it is called the indata will contain this many bytes
block_size=2048
#note: as the sample rate in this example is 16000 and the block size is 2048, the callback will be called about 8 times per second (roughly 16000 / 2048)

#this is how to get the default input device
#on windows this is directly the microphone set if you go into sound settings
#this is the input device that will be used to record with if one isn't specified
default_microphone = sounddevice.query_devices(kind='input')

#now to set up a microphone input stream using these settings
stream = sounddevice.RawInputStream(
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

#the recording is now complete and recorded_bytes contains all the data

#now I would like to dump it to a wav file so it can be played back to verify it
#but it's not as simple as writing the recorded bytes straight to a file on disk. A wav file requires a file header too.

#the wavio library can do this, but it wants a numpy array as input not a plain byte array
#so first convert the recorded_bytes array to a numpy int16 array
int16_array = np.frombuffer(bytes(recorded_bytes), dtype = np.int16)
#now it can be passed to wavio.write to create a wav file 'sound.wav' in this directory
wavio.write("sound.wav", int16_array, rate=sample_rate, sampwidth=sample_size)