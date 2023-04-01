#overview of querying the audio devices on the system

#python -m pip install sounddevice
import sounddevice

#these return a single device each
default_microphone = sounddevice.query_devices(kind='input')
print("current default input device:")
print(default_microphone)
default_speaker = sounddevice.query_devices(kind='output')
print("current default output device:")
print(default_speaker)

print("all devices:")
all_devices = sounddevice.query_devices()
print(all_devices)
#this returns a long list of audio devices, each has an index and each includes an audio API
#there might be multiple entries for the same device for each audio API

#whether it is a microphone or speaker can be determined from the number of in/out channels
#either the fullname or index can be passed into audio play/record functions to use the device
#instead of the default system device
#0 Microsoft Sound Mapper - Input, MME (2 in, 0 out)
#...
#6 Speakers (Focusrite Usb Audio), MME (0 in, 2 out)
#8 Realtek Digital Output (Realtek, MME (0 in, 2 out)
#23 Realtek Digital Output (Realtek High Definition Audio), Windows WASAPI (0 in, 2 out)

#this obtains the installed audio APIs, for example Windows DirectSound, ASIO
#as well as the devices that use each one
print(sounddevice.query_hostapis())

print(all)
print(all)