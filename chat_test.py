import openai
import os

from speechgpt import PollySpeech

# Set up the OpenAI API client
openai.api_key = os.getenv('openai_API')


# Set up the model and prompt
model_engine = "gpt-3.5-turbo"
prompt = "Sag etwas schlaues!"

messages=[
        {"role": "system", "content": "Du bist ein hilfreicher Assistent."},
        {"role": "user", "content": prompt}]

# Generate a response
print("Requesting Openai Chat reponse")
chat = openai.ChatCompletion.create(
    model=model_engine,
    messages=messages,
    max_tokens=1024
)
print("done")
response = chat['choices'][0]['message']['content']
# print(response)

# Marlene
# Vicki
# Hans
# Daniel <= geht nicht

speech = PollySpeech(text=response, voice="Vicki")

speech.synthesize()