from flask import Flask, redirect, url_for
from flask import render_template
from flask import request
from flask import send_file
import os
from google.cloud import texttospeech
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="credentials.json"
app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def index():
    txt = 'ciao a tutti'
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=txt)
    voice = texttospeech.VoiceSelectionParams(
        language_code="it-IT", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open('static/output.mp3', 'wb') as out:
        out.write(response.audio_content)
    return redirect(url_for('static', filename='output.mp3'))
    #return send_file("static/output.mp3",as_attachment=True)

if __name__ == "__main__":
    app.run()