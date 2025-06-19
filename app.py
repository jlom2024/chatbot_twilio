from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

# Inicializa la aplicación Flask
app = Flask(__name__)

# Define la ruta (endpoint) que Twilio usará. 
# Twilio enviará una petición POST a esta URL cada vez que reciba un mensaje.
@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Esta función se activa cuando Twilio recibe un mensaje.
    """
    # Obtenemos el mensaje que el usuario envió
    incoming_msg = request.values.get('Body', '').lower().strip()
    
    # Preparamos la respuesta que vamos a enviar
    response = MessagingResponse()
    msg = response.message()

    # --- Lógica del Chatbot ---
    # Aquí es donde decides qué responder.
    
    if 'hola' in incoming_msg:
        respuesta = "¡Hola! 👋 Soy un bot de prueba. ¿En qué puedo ayudarte? Puedes preguntar por el 'precio' o decir 'adiós'."
        msg.body(respuesta)
        
    elif 'precio' in incoming_msg:
        respuesta = "El precio de nuestro servicio estrella es de $10 USD. ¡Una ganga! 😉"
        msg.body(respuesta)

    elif 'adios' in incoming_msg or 'adiós' in incoming_msg:
        respuesta = "¡Hasta luego! Que tengas un excelente día. 😊"
        msg.body(respuesta)
        
    else:
        # Mensaje por defecto si no entendemos la palabra clave
        respuesta = "Lo siento, no entendí tu mensaje. Intenta con 'hola', 'precio' o 'adiós'."
        msg.body(respuesta)
        
    # Devolvemos la respuesta a Twilio en el formato que espera (TwiML)
    return str(response)

# Esta parte es solo para probar en tu computadora local, no es necesaria para Hostinger.
if __name__ == '__main__':
    app.run(debug=True)