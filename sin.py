import struct
import numpy as np

Fs = 44100                    # Sampling Rate
f = 440                       # Frequency (in Hz)
sample = 44100                # Number of samples
x = np.arange(sample)

# sine wave
y = 100 * np.sin(2 * np.pi * f * x / Fs)

f = open('sin.wav', 'wb')
# Open as Signed 8-bit on Audacity

for i in y:
    print i
    f.write(struct.pack('b', i))
f.close()
