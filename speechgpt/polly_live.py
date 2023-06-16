from boto3 import Session
import pyaudio
import io
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir
from .sentencesplitter import SentenceSplitter
import wave
import numpy as np

import nltk
# nltk.download('punkt')
from nltk import tokenize

class PollySpeech:
    def __init__(self, text, voice, format="pcm"):
        self.session = Session(profile_name="default")
        self.polly = self.session.client("polly")
        self.text = text
        self.voice = voice
        self.format = format

        self.sentences = tokenize.sent_tokenize(self.text, language="german")

        self.p = pyaudio.PyAudio()
        self.rate = 16000

    def play_audio_stream(self, audio_stream, sentence):
        print(sentence)
        stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=self.rate, output=True)
        stream.start_stream()
        stream.write(audio_stream)
        stream.stop_stream()
        stream.close()

    def synthesize(self):

        # for sentence in self.splitter.sentence_list:
        for sentence in self.sentences:
                
            # Request speech synthesis
            response = self.polly.synthesize_speech(
                Text=sentence, 
                OutputFormat=self.format,
                SampleRate=str(self.rate),
                VoiceId=self.voice)

            
            audio = response["AudioStream"].read()

            self.play_audio_stream(audio, sentence)

