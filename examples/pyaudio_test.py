import pyaudio
import numpy as np

# Create PyAudio object
pa = pyaudio.PyAudio()

# Set parameters
sample_rate = 44100
duration = 5
frequency = 440

# Generate sine wave
t = np.linspace(0, duration, int(sample_rate * duration), False)
waveform = np.sin(frequency * 2 * np.pi * t)

# Play audio
stream = pa.open(format=pyaudio.paFloat32,
                 channels=1,
                 rate=sample_rate,
                 output=True)
stream.write(waveform.astype(np.float32).tobytes())
stream.stop_stream()
stream.close()

# Terminate PyAudio
pa.terminate()