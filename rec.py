import time
import pyaudio
import numpy as np


CHUNK_SIZE = 4096 * 10
FMT = pyaudio.paInt32
CHANNELS = 2
RATE = 122100 * 2

# Define the pitch shift factor (1.0 means no shift, 2.0 means double the pitch)
PITCH_SHIFT_FACTOR = 0.97


def main():
    p = pyaudio.PyAudio()
    stream_in = create_stream(p)
    stream_out = create_stream(p, 'output')

    while True:
        data = stream_in.read(CHUNK_SIZE)
        audio = np.frombuffer(data, dtype=np.int64)

        # Apply the pitch shift
        shifted_audio = pitch_shift(audio, PITCH_SHIFT_FACTOR)
        time.sleep(0.02)

        stream_out.write(shifted_audio.tobytes())


def create_stream(p: pyaudio.PyAudio, type='input'):
    return p.open(
        format=FMT,
        channels=CHANNELS,
        rate=RATE,
        input=type == 'input',
        output=type == 'output',
        frames_per_buffer=CHUNK_SIZE
    )


def pitch_shift(audio, pitch_shift_factor):
    # Determine the number of samples to shift based on the pitch shift factor
    num_samples = len(audio)
    shift_samples = int(num_samples * pitch_shift_factor)

    # Use linear interpolation to resample the audio at the shifted pitch
    indices = np.round(np.arange(0, num_samples, pitch_shift_factor) * (shift_samples / num_samples)).astype(np.int64)
    shifted_audio = np.interp(indices, np.arange(num_samples), audio).astype(np.int64)

    return shifted_audio


if __name__ == '__main__':
    main()
