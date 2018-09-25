import struct
import numpy as np
from scipy import signal as sg

Fs = 44100                    # Sampling Rate
f = 440                       # Frequency (in Hz)
sample = 44100                # Number of samples
x = np.arange(sample)

# Sawtooth wave
y = 100 * sg.sawtooth(2 * np.pi * f * x / Fs)


f = open('sawtooth.wav', 'wb')
# Open as Signed 8-bit on Audacity

for i in y:
    print i
    f.write(struct.pack('b', i))
f.close()
