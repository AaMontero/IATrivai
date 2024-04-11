from flask import Flask, request
from google.cloud import speech
from google.oauth2 import service_account
from pydub import AudioSegment
app = Flask(__name__)

@app.route("/<mensaje>" ,methods=["GET", "POST"])
def mensaje_Llega(mensaje):
    conversa = {
        "hola":"Hola, buen dia",
        "buenos dias": None,
        "ayudame con informacion": "¡Encantado! ¿Con quién tengo el gusto?",
        "me llamo antonella": "Mucho gusto, Antonella. ¿En qué puedo ayudarte?",
        "me podría ayudar con más información sobre promociones en cartagena, orlando y miami": "Para poder ayudarte necesitamos saber la siguiente información\nNombre:\nCorreo electrónico:\nDestino:\nFecha tentativa:\nCuantas personas viajan:\nEdades:\nSalida de Quito o Guayaquil:",
        "nombre antonella garcia correo electrónico antonella.garciacamacho@gmail.com destino cartagena fecha tentativa 25 de mayo del 2024 cuantas personas viajan 2 edades 24 y 25 salida de quito o guayaquil quito": ["Estimada Antonella García\n¡Gracias por ponerte en contacto con nosotros para planificar tu viaje a Cartagena! Nos emociona mucho ayudarte a organizar una experiencia inolvidable.",
                                                                                                                                                                                                                                                       "Recibimos su pedido de cotización a Cartagena para dos personas para la fecha del 25 de mayo me puede confirmar."],
        "si porfavor ☺️": ["CARTAGENA 3 NOCHES Ticket aéreo Guayaquil o Quito / Cartagena / Quito o Guayaquil Vía avianca\n\nINCLUYE:\n\n• Traslado aeropuerto / hotel / aeropuerto en servicio compartido\n• 03 noches de alojamiento en HOTEL ZALMEDINA\n• Desayunos diarios\n• Cortesía:\n- City tour + Visita al Castillo de San Felipe con entrada.\n- Chip + bolsa de café por habitación\n• Impuestos hoteleros y aéreos\n$447",
                           "CARTAGENA 3 NOCHES TODO INLUIDO Ticket aéreo Guayaquil o Quito / Cartagena / Quito o Guayaquil Vía avianca\n\nINCLUYE:\n\n• Traslado aeropuerto / hotel / aeropuerto en servicio compartido\n• 03 noches de alojamiento en HOTEL CARTAGENA PLAZA\n• Desayuno, almuerzo y cena tipo buffet\n• Snacks y bar abierto\n• Piscina panorámica\n• Bar & discoteca\n• Noches temáticas y shows de baile\n• Kids & teen clubs\n• Wifi gratuito en las instalaciones\n• CORTESÍAS:\n- City tour + Castillo de San Felipe con entrada\n- Chip celular y bolsa de café por habitación\n$565",
                           "CARTAGENA! ALL INCLUSIVE 04 NOCHES Ticket aéreo QUITO - GUAYAQUIL / CARTAGENA / GUAYAQUIL - QUITO\n\nINCLUYE:\n\n• Traslado aeropuerto / hotel / aeropuerto en servicio compartido\n• 04 noches de alojamiento en HOTEL CARTAGENA PLAZA\n• Desayuno, almuerzo y cena tipo buffet\n• Snacks y bar abierto\n• Piscina panorámica\n• Bar & discoteca\n• Noches temáticas y shows de baile\n• Kids & teen clubs\n• Wifi gratuito en las instalaciones\n$829",
                           "Te proporcionamos tres opciones de cotización para tu viaje a Cartagena.\nCon gusto ☺️ por favor, revisa la cotización adjunta para más detalles sobre vuelos, alojamiento y servicios incluidos. Si estás de acuerdo y deseas proceder con la reserva, o necesitas ajustes en el itinerario háznoslo saber. Estamos aquí para ayudarte en todo el proceso de planificación."],
        "muchas gracias ya las reviso ☺️": None,
        "me intereso cartagena 3 noches todo incluido porfavor": None,
        "cómo puedo proceder con la reserva?": "¡Por supuesto! Para proceder con la reserva, necesitaremos algunos detalles adicionales de tu parte. Por favor, proporciona los siguientes datos:\nNombres completos de los viajeros:\nNúmeros de pasaporte:\nDirección de correo electrónico y número de teléfono de contacto:\nCualquier preferencia especial o requisito dietético que necesitemos tener en cuenta durante tu estadía.\nUna vez que recibamos esta información, nuestro equipo se pondrá en contacto contigo para confirmar la reserva y proceder con los detalles de pago.\nSi tienes alguna pregunta o necesitas ayuda adicional, no dudes en hacérnoslo saber.",
        "antonella garcia 1764309854 antonella.garciacamacho@gmail.com vegetariana adrián ruiz 1845876324 adriag2345@gmail.com ninguna": "¡Perfecto, Antonella y Adrián! Hemos registrado sus detalles y preferencias. Nuestro equipo se pondrá en contacto contigo en breve para confirmar la reserva y proporcionarte todos los detalles necesarios para tu viaje a Cartagena.",
        "gracias": "• Para mantener esta reservación en firme se requiere el pago del abono de $100, NO REEMBOLSABLE en el caso de pasajeros individuales o grupos. Aplica hasta 31 días antes del viaje para individuales y 46 días para grupos.\n• El pago total de una reservación deberá ser realizada hasta 30 días antes de la salida.\n• Si una reservación ingresa 30 días antes de la salida, el pago total deberá estar realizado en 24 horas luego de haber sido realizada la misma.\n• Reservaciones que no tengan pago SE CANCELARÁN a las 24 HORAS.\n• En el caso de grupos de pasajeros el pago total se debe realizar 45 días antes de la salida.\n• Penalidad por cambio de nombre: USD $150 hasta 10 días antes de la salida en vuelo chárter.\n• No se permite cambios de fecha o destino.\n• Al momento de la facturación usted acepta estar de acuerdo con los servicios detallados y está de acuerdo con las penalidades descritas en esta liquidación de servicios sin excepción alguna.",
        "listo cuáles serían los métodos de pago": "Claro Para completar tu reserva, te ofrecemos varias opciones de pago. Puedes realizar una transferencia bancaria, pagar con tarjeta de crédito o utilizar otras plataformas de pago en línea. Por favor, avísanos cuál prefieres y te proporcionaremos los detalles necesarios para proceder.",
        "deseo pagar con tarjeta de crédito": "Claro para procesar el pago con tarjeta de crédito, por favor haz clic en el siguiente link: https://www.payphone.app/.",
        "y si deseo pagar en efectivo?": "No hay problema. Para realizar el pago, por favor acérquese a nuestras oficinas ubicadas en el centro comercial Galería Plaza, Local N7. ¿A qué hora te gustaría agendar una cita? Estamos disponibles de lunes a viernes de 9 am a 6 pm . Por favor, avísenos su preferencia para coordinar la cita. ¡Gracias!",
        "no voy a poder acercarme :( deseo que me mande su número de cuenta mejor, para hacerle el abono": "Con gusto, los datos de la cuenta bancaria son:\nCuenta Corriente Banco Guayaquil\nCuenta N°: 0041291060\nNombre: Trivai S.A\nRUC: 1793198413001",
        "listo": ["¡Muchas gracias por realizar tu pago! En este momento procedemos a confirmar tu reserva y asegurarnos de que todo esté en orden para tu viaje. Si tienes alguna pregunta o necesitas asistencia durante el proceso de pago, no dudes en contactarnos. Puedes comunicarte con nuestro equipo de soporte al número 099926280 que te acompañara en tu viaje.",
                  "Estimado/a Antonella García y Adrian Ruiz Queremos confirmar que hemos recibido su pago y que su reserva está ahora completa. Todos los detalles de su viaje han sido registrados y estamos emocionados de asistirlo/a en cada paso del camino. Si tiene alguna pregunta adicional o necesita más información, no dude en ponerse en contacto con nosotros. Estamos aquí para ayudarlo/a. ¡Gracias por confiar en nosotros para su viaje y esperamos que tenga una experiencia memorable!"],
        "muchísimas gracias ☺️": None,
        "también quería preguntarle si tiene paquetes a orlando y miami": ["ORLANDO FANTASTICO 05 NOCHES GVMCO24-002 INCLUYE: Ticket aéreo UIO/GYE – BOG – MCO – BOG – GYE/UIO vía AVIANCA AIRLINES\n• Traslado aeropuerto / hotel / aeropuerto en servicio compartido\n• 05 noches de alojamiento en HOTEL ROSEN INN LAKE BUENAVISTA\n• Desayunos Buffet diarios (07:00 a 9:00)\n• 01 día de admisión a AQUATICA\n• 01 día de admisión a SEAWORLD\n• 01 día de admisión al BUSCH GARDENS\n• CORTESÍA POR HABITACIÓN:\n- 01 almohada de viaje\n- Tour de compras PREMIUM OUTLET\n$1441",
                                                                            "¡ORLANDO FULL! 05 NOCHES GVMCO01 Ticket aéreo Quito o Guayaquil/ Orlando / Quito o Guayaquil vía COPA AIRLINES INCLUYE: Traslado aeropuerto / hotel / aeropuerto en servicio compartido\n• 05 noches de alojamiento en HOTEL ROSEN INN LAKE BUENAVISTA\n• Desayunos\n• 01 día de visita a Universal Studios park-to-park con admisión y traslados ida y vuelta\n• 01 día de visita a Isla de la aventura park-to-park, con admisión y traslados ida y vuelta\n• 01 día de tour de compras a Premium Outlet International Drive, con traslados ida y vuelta\n• 01 día libre\n• Impuestos hoteleros y aéreos\n$1528"],
        "gracias porfavor me puede enviar para miami": ["¡MIAMI SALE! 03 NOCHES Ticket aéreo Quito o Guayaquil / Miami / Quito o Guayaquil VÍA avianca INCLUYE: Traslado aeropuerto / hotel en servicio shuttle*\n• 03 noches de alojamiento en HOTEL CLARION INN & SUITES MIAMI\n• Tour de compras a Dolphin Mall\n• Impuestos aéreos y hoteleros\n$627",
                                                        "¡MIAMI SALE! 03 NOCHES Ticket aéreo Quito o Guayaquil / Miami / Quito o Guayaquil VÍA avianca INCLUYE: Traslado aeropuerto / hotel en servicio shuttle*\n• 03 noches de alojamiento en HOTEL CLARION INN & SUITES MIAMI\n• Tour de compras a Dolphin Mall\n• Impuestos aéreos y hoteleros\n$627"],
        "muchas gracias los voy a revisar para unas próximas vacaciones": "Con gusto Antonella. Por favor ten en cuenta que los precios están sujetos a disponibilidad y podrían variar hasta la confirmación final de la reserva, si deseas proceder con ella, háznoslo saber y estaremos encantados de gestionarlo todo para ti.",
        "lo entiendo gracias": None,
        "señorita de igual manera mi madre desea ir a europa porfavor me puede mandar las opciones": "Estimada Antonella para poder ayudarle necesitamos saber la siguiente información\n Nombre:\nCorreo electrónico:\nDestino:\nFecha tentativa:\nCuantas personas viajan:\nEdades:\nSalida de Quito o Guayaquil:",
        "nombre marisol camacho correo marylu3020@gmail.com destino europa fecha tentativa 15 de junio cuántas personas 1 edad 60 salida quito": "Recibimos su pedido de cotización a Europa para una persona para la fecha del 15 de junio me puede confirmar.",
        "si porfavor": ["Antonella, le adjunto la cotización del Eurotrip dorada para las fechas estipuladas",
                        "Programa Incluye\nTour 16 días - 15 noches\n* Boleto aéreo QUITO - MADRID- QUITO con Iberia\n* Traslado aeropuerto – hotel – aeropuerto\n* Alojamiento en categoría Turista\n* Desayuno diario Buffet\n* Guía acompañante durante todo el viaje\n* Guías locales en español en las visitas indicadas en el itinerario\n* SEGURO DE VIAJE (APLICA PARA VISADO SCHENGEN)\n* Impuestos aéreos\n* Impuestos Ecuatorianos\n$3422"],
        "qué ciudades se visitan?": "Madrid,Paris,Venecia,Florencia,Roma,Costa Azul,Barcelona,Zaragoza",
        "muchas gracias ☺️ ya le confirmos": None,
        "porfavor señorita pueden solo enviarme la cotización de un vuelo a madrid": "¡Por supuesto! Antonella para poder ayudarte necesitamos la siguiente información para enviarte las opciones de vuelo disponibles.\nFecha de salida:\n Destino:\n Número de pasajeros:",
        "15 de junio - 15 de julio madrid 1": ["Encontramos dos opciones buenas de viaje para ti en las fechas estipuladas",
                                              "https://www.avianca.com/es/booking/select/?departure1=2024-06-15&departure2=2024-07-15&platform=WEBB2C&origin1=UIO&destination1=MAD&adt1=1&chd1=0&inf1=0&posCode=EC&origin2=MAD&destination2=UIO&adt2=1&chd2=0&inf2=0&currency=USD&CorporateCode=&Device=Web",
                                              "https://www.latamairlines.com/ec/es/seleccion-asientos?id=LA4625048IYJY"],
        "disculpe talvez un hotel en galapagos todo incluido ya que quiero viajar a fin de este mes": ["Si Antonella contamos con el hotel Torruga Vay $321 adultos y niños $290 por persona sin ticket aéreo ya que este depende de la temporada que usted viaje.",
                                                                                                        "Incluye\n-Transfer in - Visita parte alta\n-Playa Tortuga Bay\n-Visita estación Charles Darwin\n-Visita Playa de los Alemanes y Grietas\n-Tranfer out\nIncluye alimentación completa"],
        "muchas gracias voy a conversar con mi esposo": "Gracias a ti. ¡Buen viaje!"
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
