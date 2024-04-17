from flask import Flask, request
from google.cloud import speech
from google.oauth2 import service_account
from pydub import AudioSegment
app = Flask(__name__)

@app.route("/<mensaje>" ,methods=["GET", "POST"])
def mensaje_Llega(mensaje):
    conversa = {
        "hola": "Hola, buen dia",
        "buenos días vi una publicación sobre México y estoy interesada": "Para poder ayudarte necesitamos saber la siguiente información\nNombre:\nCorreo electrónico:\nDestino:\nFecha tentativa:\nCuantas personas viajan:\nEdades:\nSalida de Quito o Guayaquil:",
        "nombre antonella garcia correo electrónico antonella.garciacamacho@gmail.com destino cartagena fecha tentativa 25 de mayo del 2024 cuantas personas viajan 2 edades 24 y 25 salida de quito o guayaquil quito": None,
        "audio 1": "Estimada Antonella García,\n¡Gracias por ponerte en contacto con nosotros para planificar tu viaje a México ! Nos emociona mucho ayudarte a organizar una experiencia inolvidable.",
        "Gracias ☺️": "MÉXICO Y CANCÚN!\n06 NOCHES\nTicket aéreo Quito o Guayaquil / México - Cancún / Quito o Guayaquil VÍA COPA AIRLINES\nINCLUYE:\nEN CD. DE MÉXICO:\n Traslado aeropuerto / hotel / aeropuerto en servicio compartido\n 03 noches de alojamiento en HOTEL REGENTE O SIMILAR\n Desayunos diarios incluidos\n Cortesías:\n- Almuerzo en Teotihuacán\nEN CANCÚN:\n Traslado aeropuerto / hotel / aeropuerto en servicio compartido\n 03 noches de alojamiento en CANCUN BAY RESORT\n Plan alimenticio todo incluido\n$880",
        "Que actividades incluye": None,
        "audio 2": "CD. MÉXICO ACTIVIDADES\n* Visita panorámica a Plaza Garibaldi\n* Basílica de Guadalupe y Pirámides de Teotihuacán",
        "Muchas gracias": None,
        "Por favor puede decirme que no incluye el paquete": ["No incluye",
                                                            "•	Ticket aéreo interno CUN – \n•	Actividades no detalladas en el programa.\n•	Comidas y bebidas no indicadas en el programa.\n•	Extras personales en hoteles y restaurantes.\n•	Propinas.\n•	Tarjeta de asistencia médica."],
        "Muchas gracias ☺️": "•   Para mantener esta reservación en firme se requiere el pago del abono de $100, NO REEMBOLSABLE en el caso de pasajeros individuales o grupos. Aplica hasta 31 días antes del viaje para individuales y 46 días para grupos.\n•	El pago total de una reservación deberá ser realizada hasta 30 días antes de la salida.\n•	Si una reservación ingresa 30 días antes de la salida, el pago total deberá estar realizado en 24 horas luego de haber sido realizada la misma.\n•	Reservaciones que no tengan pago SE CANCELARÁN a las 24 HORAS.\n•	En el caso de grupos de pasajeros el pago total se debe realizar 45 días antes de la salida.\n•	Penalidad por cambio de nombre: USD $150 hasta 10 días antes de la salida en vuelo chárter.\n•	No se permite cambios de fecha o destino.\n•	Al momento de la facturación usted acepta estar de acuerdo con los servicios detallados y está de acuerdo con las penalidades descritas en esta liquidación de servicios sin excepción alguna.",
        "Listo cuáles serían los métodos de pago": "Claro Para completar tu reserva, te ofrecemos varias opciones de pago. Puedes realizar una transferencia bancaria, pagar con tarjeta de crédito o utilizar otras plataformas de pago en línea. Por favor, avísanos cuál prefieres y te proporcionaremos los detalles necesarios para proceder.",
        "Deseo pagar con tarjeta de crédito": "Claro para procesar el pago con tarjeta de crédito, por favor haz clic en el siguiente link: https://www.payphone.app/.",
        "Y si deseo pagar en efectivo?": "No hay problema. Para realizar el pago, por favor acérquese a nuestras oficinas ubicadas en el centro comercial Galería Plaza, Local N7.  ¿A qué hora te gustaría agendar una cita? Estamos disponibles de lunes a viernes de 9 am a 6 pm . Por favor, avísenos su preferencia para coordinar la cita. ¡Gracias!",
        "No voy a poder acercarme :( deseo que me mande su número de cuenta mejor, para hacerle el abono": "Con gusto, los datos de la cuenta bancaria son:\nCuenta Corriente Banco Guayaquil\nCuenta N°: 0041291060\nNombre: Trivai S.A\nRUC: 1793198413001",
        "Listo": ["¡Muchas gracias por realizar tu pago! En este momento procedemos a confirmar tu reserva y asegurarnos de que todo esté en orden para tu viaje. Si tienes alguna pregunta o necesitas asistencia durante el proceso de pago, no dudes en contactarnos. Puedes comunicarte con nuestro equipo de soporte al número 099926280 que te acompañara en tu viaje.",
                "Estimado/a Antonella García\n\n Queremos confirmar que hemos recibido su pago y que su reserva está ahora completa. Todos los detalles de su viaje han sido registrados y estamos emocionados de asistirlo/a en cada paso del camino.\nSi tiene alguna pregunta adicional o necesita más información, no dude en ponerse en contacto con nosotros. Estamos aquí para ayudarlo/a.\n¡Gracias por confiar en nosotros para su viaje y esperamos que tenga una experiencia memorable!"],
        "Muchísimas gracias ☺️": None
    }
    mensaje_usuario = mensaje
    mensaje_usuario = mensaje_usuario.lower()
    # Buscar el mensaje en el diccionario y devolver la respuesta correspondiente
    respuesta = conversa.get(mensaje_usuario, "No hay respuesta")
    if isinstance(respuesta, list):
        respuesta = '\n'.join(respuesta)

    return respuesta


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
    

def convert_ogg_to_wav():
    song = AudioSegment.from_ogg("temp_audio_file.ogg").set_sample_width(2)
    song.export("temp_audio_fileg.wav", format="wav")
if __name__ == "__main__":
    '''mensaje_usuario = "ayudame con informacion"
    respuesta = mensaje_Llega(mensaje_usuario)
    print(respuesta)'''
    app.run(debug=True)
