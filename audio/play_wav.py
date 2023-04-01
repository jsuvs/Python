#reads a wav file from disk and plays it through speakers
#https://python-sounddevice.readthedocs.io/en/0.4.6/

#python -m pip install soundfile 
#python -m pip install sounddevice
import sounddevice
import soundfile as sf

filename = 'output.wav'
# Extract data and sampling rate from file
data, fs = sf.read(filename, dtype='float32')  
sounddevice.play(data, fs)
status = sounddevice.wait()  # Wait until file is done playing

