import openai
import os

from speechgpt import PollySpeech


speech = PollySpeech(text="Hallo, das ist ein Test. Draussen schneit es!")

speech.synthesize()