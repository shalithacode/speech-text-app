from flask import Flask

app = Flask(__name__)

# Imports the Google Cloud client library
import sys, os

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "lib")
# insert at position 1 in the path, as 0 is the path of this file.
sys.path.insert(1, filename)
from google.cloud import speech

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "shalithatestproject-4399094c0dde.json"
# Instantiates a client
client = speech.SpeechClient()

# The name of the audio file to transcribe
gcs_uri = "gs://cloud-samples-data/speech/brooklyn_bridge.raw"

audio = speech.RecognitionAudio(uri=gcs_uri)

config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=16000,
    language_code="en-US",
)

# Detects speech in the audio file
response = client.recognize(config=config, audio=audio)

for result in response.results:
    print("Transcript: {}".format(result.alternatives[0].transcript))


@app.route("/")
def main():
    return '<form action="/text"><input type="submit" value="Submit" /></form>'


@app.route("/text")
def speech_text():
    for result in response.results:
        text = result.alternatives[0].transcript
        return f'<h2>{text}</h2><form action="/text"><input type="submit" value="Submit" /></form>'


if __name__ == "__main__":
    app.run()
