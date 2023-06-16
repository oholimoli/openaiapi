from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir
from .sentencesplitter import SentenceSplitter


class PollySpeech:
    def __init__(self, text, voice="Hans", format="mp3"):
        self.session = Session(profile_name="default")
        self.polly = self.session.client("polly")
        self.text = text
        self.voice = voice
        self.format = format
        self.splitter = SentenceSplitter(text)

    def synthesize(self):
        for sentence in self.splitter.sentence_list:
            try:
                # Request speech synthesis
                response = self.polly.synthesize_speech(Text=sentence, OutputFormat=self.format,
                                                        VoiceId=self.voice)
            except (BotoCoreError, ClientError) as error:
                # The service returned an error, exit gracefully
                print(error)
                sys.exit(-1)

            # Access the audio stream from the response
            if "AudioStream" in response:
                # Note: Closing the stream is important because the service throttles on the
                # number of parallel connections. Here we are using contextlib.closing to
                # ensure the close method of the stream object will be called automatically
                # at the end of the with statement's scope.
                with closing(response["AudioStream"]) as stream:
                    output = os.path.join(gettempdir(), "speech.mp3")

                    try:
                        # Open a file for writing the output as a binary stream
                        with open(output, "wb") as file:
                            file.write(stream.read())
                    except IOError as error:
                        # Could not write to file, exit gracefully
                        print(error)
                        sys.exit(-1)

            else:
                # The response didn't contain audio data, exit gracefully
                print("Could not stream audio")
                sys.exit(-1)

            # Play the audio using the platform's default player
            if sys.platform == "win32":
                # Use Windows Media Player to play the audio
                subprocess.call(["cmd", "/c", "start", "", output], shell=True)
                # Wait for the audio to finish playing
                subprocess.call(["powershell", "-Command", "(New-Object Media.SoundPlayer '"+output+"').PlaySync();"])
            else:
                # The following works on macOS and Linux. (Darwin = mac, xdg-open = linux).
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, output])
                # Wait for the audio to finish playing
                subprocess.call(["afplay", "-d", str(get_audio_length(output)), output])
