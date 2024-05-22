from google.cloud import texttospeech
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials.json'


# Instantiates a client
client = texttospeech.TextToSpeechClient()

# Set the text input to be synthesized

txt = '''L'immagine mostra un uomo che si trova di fronte a una Tesla Cybertruck. 
L'uomo è vestito con una camicia bianca e dei jeans, e ha un sorriso sul volto. 
La Cybertruck è un veicolo elettrico prodotto da Tesla, Inc. 
È stato presentato per la prima volta nel 2019 e ha un design futuristico e accattivante'''

synthesis_input = texttospeech.SynthesisInput(text=txt)

# Build the voice request, select the language code ("en-US") and the ssml
# voice gender ("neutral")
voice = texttospeech.VoiceSelectionParams(
    language_code="it-IT", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
)

# Select the type of audio file you want returned
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

# Perform the text-to-speech request on the text input with the selected
# voice parameters and audio file type
response = client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio_config
)

# The response's audio_content is binary.
with open("output.mp3", "wb") as out:
    # Write the response to the output file.
    out.write(response.audio_content)
    print('Audio content written to file "output.mp3"')