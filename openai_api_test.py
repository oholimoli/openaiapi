import openai
import os

from speechgpt import PollySpeech

# Set up the OpenAI API client
openai.api_key = os.getenv('openai_API')


# Set up the model and prompt
model_engine = "text-davinci-003"
prompt = "Sag drei kluge Sätze!"

# Generate a response
completion = openai.Completion.create(
    engine=model_engine,
    prompt=prompt,
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.5,
)

response = completion.choices[0].text
print(response)


speech = PollySpeech(text=response)

speech.synthesize()