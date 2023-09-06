# import pyaudio
# import pyttsx3

import io
import time
import wave

from baron import AUDIO

chunk_size = 1024
sample_rate = 11025
channels = 1

# from io import BytesIO
# audio = pyaudio.PyAudio()


# engine = pyttsx3.init()
# voices = engine.getProperty('voices')

# engine.setProperty('rate', 120) # Speed percent (can go over 100
# engine.setProperty('volume', 0.9) # Volume 0-1
# engine.setProperty('voice', voices[0].id) # Voice ID
# engine.setProperty('pitch', (0.5, 1)) # Pitch 0-1
# # Convert text to speech
# engine.say('<pitch middle="0">Emma Emma emma</pitch>')
# # engine.say(text)

# # Play the speech
# engine.runAndWait()


def record():
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    # print "recording..."
    data = stream.read(CHUNK)
    return data

def genHeader(sampleRate: int, bitsPerSample: int, channels: int):
    """
    Generates a WAV header for a file that has the specified properties.
    """

    datasize = 2000*10**6
    o = bytes("RIFF",'ascii')                                               # (4byte) Marks file as RIFF
    o += (datasize + 36).to_bytes(4,'little')                               # (4byte) File size in bytes excluding this and RIFF marker
    o += bytes("WAVE",'ascii')                                              # (4byte) File type
    o += bytes("fmt ",'ascii')                                              # (4byte) Format Chunk Marker
    o += (16).to_bytes(4,'little')                                          # (4byte) Length of above format data
    o += (1).to_bytes(2,'little')                                           # (2byte) Format type (1 - PCM)
    o += (channels).to_bytes(2,'little')                                    # (2byte)
    o += (sampleRate).to_bytes(4,'little')                                  # (4byte)
    o += (sampleRate * channels * bitsPerSample // 8).to_bytes(4,'little')  # (4byte)
    o += (channels * bitsPerSample // 8).to_bytes(2,'little')               # (2byte)
    o += (bitsPerSample).to_bytes(2,'little')                               # (2byte)
    o += bytes("data",'ascii')                                              # (4byte) Data Chunk Marker
    o += (datasize).to_bytes(4,'little')                                    # (4byte) Data size in bytes
    return o

def generate_audio(text2wav, wav2stream):
    """Audio streaming generator function."""

    # wav_from_stream = io.BytesIO(wav2stream.get())

    wav = wave.open((AUDIO / "applause.wav").as_posix(), 'rb')
    while True:
        # text = text2wav.get()
        # wav = ... # tts magic here
        data = wav.readframes(chunk_size)
        if data == b'':
            # data = bytes(0 for i in range(int(chunk_size)))
            data = bytes(0 for i in range(2*sample_rate)) # 1 s
            wav.rewind()

        wav2stream.send_bytes(data)
        time.sleep(chunk_size / (sample_rate*channels))


def stream_audio(wav2stream):
    """Audio streaming generator function."""

    header_data = genHeader(bitsPerSample=8, sampleRate=sample_rate, channels=channels)
    yield header_data

    while True:
        data = wav2stream.recv_bytes()
        yield data

