from flask import Flask, request, render_template

app = Flask(__name__, template_folder="template")


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/result", methods=["GET", "POST"])
def speech():
    transcript = ""

    from google.cloud import speech

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
        transcript = format(result.alternatives[0].transcript)
        return render_template("index.html", transcript=transcript)


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
