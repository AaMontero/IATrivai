from flask import Flask, request, Response 
from google.cloud import speech
from google.oauth2 import service_account
from pydub import AudioSegment
from google.cloud import texttospeech
import io
app = Flask(__name__)
@app.route("/audio", methods=["POST"])
def audioText():
    if 'audio_file' not in request.files:
        return "No se ha proporcionado ningún archivo de audio", 400
    audio_file = request.files['audio_file']
    if audio_file.filename == '':
        return "No se ha seleccionado ningún archivo", 400
    audio_path = "temp_audio_file.ogg"
    audio_file.save(audio_path)
    convert_ogg_to_wav()
    audio_pathwav = "temp_audio_fileg.wav"
    client_file = "sa_key_demo.json"
    credentials = service_account.Credentials.from_service_account_file(client_file)
    client = speech.SpeechClient(credentials=credentials)
    with open(audio_pathwav, "rb") as audio_file:
        content = audio_file.read()
        audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code="es-ES",
        audio_channel_count = 1,
    )
    response = client.recognize(config=config, audio=audio)
    if response.results:
        transcript = response.results[0].alternatives[0].transcript
        print("esta en ok")
        return transcript, 200
    else:
        return "No se encontraron resultados de transcripción", 400
@app.route("/audioToText", methods=["POST"])  
def devolver_audio():
    # Obtener el texto del cuerpo de la solicitud POST
    texto = request.form.get('texto', '')  # Acceder al texto enviado desde PHP
    client_file = "sa_key_demo.json"
    credentials = service_account.Credentials.from_service_account_file(client_file)
    client = texttospeech.TextToSpeechClient(credentials=credentials)
    synthesis_input = texttospeech.SynthesisInput(text=texto)
    voice = texttospeech.VoiceSelectionParams(
        language_code="es-US",
        name="es-US-Neural2-B",
        ssml_gender=texttospeech.SsmlVoiceGender.MALE,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    print(texto)
    return Response(response.audio_content, mimetype='audio/mpeg')

def convert_ogg_to_wav():
    song = AudioSegment.from_ogg("temp_audio_file.ogg").set_sample_width(2)
    song.export("temp_audio_fileg.wav", format="wav")
if __name__ == "__main__":
    app.run(debug=True)
    #devolver_audio("texto")
