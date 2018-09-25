#
# Basic pyaudio program playing a real time mono sine wave
#
# (ME) 2015 Marc Groenewegen
#

import pyaudio
import time
import numpy as np
import array
import keyboard

WIDTH = 2 # sample size in bytes
CHANNELS = 1 # number of samples in a frame
RATE = 44100
FRAMESPERBUFFER = 256

sineFrequency=520.0

outputDevice=0


#
# Function showDevices() lists available input- and output devices
#
def showDevices(p):
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range (0,numdevices):
        if p.get_device_info_by_host_api_device_index(0,i).get('maxInputChannels')>0:
            print "Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0,i).get('name')
        if p.get_device_info_by_host_api_device_index(0,i).get('maxOutputChannels')>0:
            print "Output Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0,i).get('name')


def setOutputDevice(p):
    global outputDevice
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range (0,numdevices):
        if p.get_device_info_by_host_api_device_index(0,i).get('maxOutputChannels')>0:
            if p.get_device_info_by_host_api_device_index(0,i).get('name').find("pulse") >= 0:
                outputDevice=i
                print "Selected device number: ", str(outputDevice)


#
# Create array of signed ints to hold one sample buffer
# Make it global so it doesn't get re-allocated for every frame
#
outbuf = array.array('h',xrange(FRAMESPERBUFFER)) # array of signed ints


#
# Create the callback function which is called by pyaudio
#   whenever it needs output-data or has input-data
#
# As we are working with 16-bit integers, the range is from -32768 to 32767
#
def callback(in_data,frame_count,time_info,status):
    global phase
    global outbuf
    for n in range(frame_count):
        outbuf[n] = int(32767 * 0.5 * np.sin(phase))
        phase += 2*np.pi*sineFrequency/RATE
    return (outbuf,pyaudio.paContinue)


    #########################
    # Start of main program #
    #########################


#
# get a handle to the pyaudio interface
#

paHandle = pyaudio.PyAudio()

# select a device
setOutputDevice(paHandle)
devinfo = paHandle.get_device_info_by_index(outputDevice)
print "Selected device name: ",devinfo.get('name')

phase=0 # sine phase


#
# open a stream with some given properties
#
stream = paHandle.open(format=paHandle.get_format_from_width(WIDTH),
                       channels=CHANNELS,
                       rate=RATE,
                       frames_per_buffer=FRAMESPERBUFFER,
                       input=False, # no input
                       output=True, # only output
#                       output_device_index=outputDevice, # choose output device
                       output_device_index=1,
                       stream_callback=callback)

stream.start_stream()

# Make sure that the main program doesn't finish until all
#  audio processing is done
while stream.is_active():
    time.sleep(0.1)

# in this example you'll never get here
stream.stop_stream()
stream.close()

paHandle.terminate()
