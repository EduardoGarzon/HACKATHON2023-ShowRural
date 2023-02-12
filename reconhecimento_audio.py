import pyaudio
import wave
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile

CHUNK = 1024
RATE = 44400

def audio():   
    p = pyaudio.PyAudio() 
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
        )

    print("Capturando áudio...")

    frames = []

    for i in range(0, int(RATE / CHUNK * 10)):
        data = stream.read(CHUNK)
        frames.append(np.frombuffer(data, dtype=np.int16))

    print("Concluído.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open("audio.wav", "wb")
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    fs, data = wavfile.read('audio.wav')

    plt.hist(data, bins=256, range=(-22768, 22767))
    plt.title("Histograma do áudio")
    plt.xlabel("Amplitude")
    plt.ylabel("Frequência")
    plt.show()
    plt.savefig("Histo", )
