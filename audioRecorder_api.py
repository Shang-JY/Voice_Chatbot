import pyaudio
import wave


class AudioRecorder:
    def __init__(self, channels=1, filename="upload_buffer.wav", rate=16000, chunk_size=1024):
        self.CHANNELS = channels
        self.CHUNK_SIZE = chunk_size  # Record in chunks of n samples
        self.RATE = rate  # Record at n samples per second
        self.FORMAT = pyaudio.paInt16  # n bits per sample
        self.RECORD_SECONDS = 5
        self.WAVE_OUTPUT_FILENAME = filename

    def record_by_timer(self):
        p = pyaudio.PyAudio()  # Create an interface to PortAudio
        print("Starting.")
        stream = p.open(format=self.FORMAT,
                        channels=1,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK_SIZE,
                        )

        frames = []  # Initialize array to store frames

        # Store data in chunks for n seconds
        print("Recording...")
        for i in range(0, int(self.RATE / self.CHUNK_SIZE * self.RECORD_SECONDS)):
            data = stream.read(self.CHUNK_SIZE)
            frames.append(data)

        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        print("Recording complete.")
        # Terminate the PortAudio interface
        p.terminate()

        # Save the recorded data as a WAV file
        wf = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

    def record_by_detection(self):  # At least record 5 seconds, and use the average loudness to detect the end.
        pass

    def record_by_control(self):  # Version A, using the callback function and a input function to control
        audio = pyaudio.PyAudio()  # Create an interface to PortAudio
        print("Starting.")
        frames = []  # Initialize array to store frames

        def audio_callback(in_data, frame_count, time_info, status):
            frames.append(in_data)
            return None, pyaudio.paContinue

        stream = audio.open(format=self.FORMAT,
                            channels=1,
                            rate=self.RATE,
                            input=True,
                            frames_per_buffer=self.CHUNK_SIZE,
                            stream_callback=audio_callback,
                            )
        stream.start_stream()
        # Store data in chunks for n seconds
        print("Recording...")
        input("Press enter to stop recording: ")

        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        print("Recording complete.")
        # Terminate the PortAudio interface
        audio.terminate()

        # Save the recorded data as a WAV file
        with wave.open(self.WAVE_OUTPUT_FILENAME, 'wb') as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(audio.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(frames))
        print("Audio saved to: ", self.WAVE_OUTPUT_FILENAME)

    # def record_by_control(self):  # Version B, using the read function and the KeyboardInterrupt to control
    #     p = pyaudio.PyAudio()  # Create an interface to PortAudio
    #     print("Starting.")
    #     stream = p.open(format=self.FORMAT,
    #                     channels=1,
    #                     rate=self.RATE,
    #                     input=True,
    #                     frames_per_buffer=self.CHUNK_SIZE,
    #                     )
    #
    #     frames = []  # Initialize array to store frames
    #     stream.start_stream()
    #     # Store data in chunks for n seconds
    #     print("Recording...")
    #
    #     try:
    #         while stream.is_active():
    #             data = stream.read(self.CHUNK_SIZE)
    #             frames.append(data)
    #     except KeyboardInterrupt:
    #         pass
    #
    #     # Stop and close the stream
    #     stream.stop_stream()
    #     stream.close()
    #     print("Recording complete.")
    #     # Terminate the PortAudio interface
    #     p.terminate()
    #
    #     # Save the recorded data as a WAV file
    #     wf = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
    #     wf.setnchannels(self.CHANNELS)
    #     wf.setsampwidth(p.get_sample_size(self.FORMAT))
    #     wf.setframerate(self.RATE)
    #     wf.writeframes(b''.join(frames))
    #     wf.close()

    def play_wav(self, wav_path='output_buffer.wav'):
        wf = wave.open(wav_path, 'rb')
        # print("samplewidth:", wf.getsampwidth())
        # print("channles:",wf.getnchannels())
        # print("framerate:",wf.getframerate())
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
        data = wf.readframes(self.CHUNK_SIZE)
        while len(data) > 0:
            stream.write(data)
            data = wf.readframes(self.CHUNK_SIZE)
        stream.stop_stream()
        stream.close()
        wf.close()
        p.terminate()
