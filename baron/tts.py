# import pyaudio
# import pyttsx3

import io
import wave

from baron import AUDIO

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

def genHeader(sampleRate, bitsPerSample, channels):
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

    while True:
        # text = text2wav.get()
        # wav = ... # tts magic here

        with open((AUDIO / "applause.wav").as_posix(), 'rb') as wav:
            wav2stream.put(wav.read())
            pass
        import time
        time.sleep(3)

def stream_audio(wav2stream):
    """Audio streaming generator function."""
    # data_to_stream = genHeader(44100, 32, 1, 200000) + currChunk
    # yield data_to_stream

    wav_header = genHeader(bitsPerSample=32, sampleRate=44100, channels=1)

    # while True:
        # wav = io.BytesIO(wav2stream.get())
    # with open((AUDIO / "applause.wav").as_posix(), 'rb') as wav:
        # wav2stream.put(wav.read())
    chunk_size = 1024
    first_time = True

    while True:
        wav_from_stream = io.BytesIO(wav2stream.get())
        with wave.open(wav_from_stream, 'rb') as wav_file:
            header_data = genHeader(bitsPerSample=wav_file.getsampwidth()*8, sampleRate=wav_file.getframerate(), channels=1)
            data = wav_file.readframes(chunk_size)
            while data:
                if first_time:
                    first_time = False
                    yield header_data + data
                else:
                    yield data
                data = wav_file.readframes(chunk_size)

