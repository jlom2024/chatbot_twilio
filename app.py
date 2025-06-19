# -*- coding: utf-8 -*-

# ==========================================================
#                  IMPORTS NECESARIOS
# ==========================================================
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

# ==========================================================
#         INICIALIZACIÓN DE LA APLICACIÓN FLASK
# ==========================================================
app = Flask(__name__)

# ==========================================================
#    CONFIGURACIÓN CENTRALIZADA DE CLIENTES (TU "BASE DE DATOS")
# ==========================================================
#
#  - La "llave" de cada cliente es su número de teléfono de Twilio en formato E.164 (ej: "+15551112222").
#  - Dentro de cada cliente, puedes personalizar todos sus mensajes y palabras clave.
#
# ------------------------------------------------------------------------------------------------

CLIENTS_CONFIG = {
    # --- CLIENTE EJEMPLO 1: UNA PIZZERÍA ---
    "+15551112222": {
        "name": "Pizzería Don Gato",
        "welcome_message": "¡Hola! 🍕 Bienvenido a Pizzería Don Gato. ¿En qué podemos ayudarte? Escribe:\n"
                         "➡️ 'MENU' para ver nuestras pizzas.\n"
                         "➡️ 'ESTADO' para ver tu pedido.\n"
                         "➡️ 'UBICACION' para saber dónde estamos.",
        "keywords": {
            "menu": "Claro, nuestro menú es:\n"
                    "🍕 Pizza Margarita - $10\n"
                    "🍕 Pizza Pepperoni - $12\n"
                    "🍕 Pizza Hawaiana - $13\n"
                    "¿Cuál te gustaría ordenar?",
            "estado": "Por favor, para revisar el estado de tu pedido, indícanos tu número de orden.",
            "ubicacion": "Nos encontramos en la Calle Falsa 123, al lado de la tienda de resortes. ¡Te esperamos!",
            "gracias": "¡A ti! Que disfrutes tu pizza. 😊"
        },
        "default_response": "Lo siento, no entendí esa opción. Por favor, intenta con 'MENU', 'ESTADO' o 'UBICACION'."
    },

    # --- CLIENTE EJEMPLO 2: UN GIMNASIO ---
    "+15553334444": {
        "name": "Gimnasio FuerteFit",
        "welcome_message": "¡Hola! 💪 Bienvenido a FuerteFit. Te podemos ayudar con:\n"
                         "➡️ 'CLASES' para ver el horario semanal.\n"
                         "➡️ 'PRECIOS' para ver nuestras membresías.\n"
                         "➡️ 'CONTACTO' para hablar con un asesor.",
        "keywords": {
            "clases": "¡Con gusto! Nuestro horario es:\n"
                      "Lunes - Yoga 8 AM\n"
                      "Miércoles - Spinning 7 PM\n"
                      "Viernes - Boxeo 6 PM\n"
                      "¡No necesitas reservar!",
            "precios": "Nuestra membresía mensual tiene un costo de $50 USD. ¡Incluye acceso ilimitado a todas las clases y áreas del gimnasio!",
            "contacto": "Puedes llamarnos al 987-654-321 o visitarnos directamente. Nuestro personal estará feliz de atenderte.",
            "adios": "¡Gracias por contactarnos! Sigue entrenando duro."
        },
        "default_response": "Opción no reconocida. Por favor, prueba con 'CLASES', 'PRECIOS' o 'CONTACTO'."
    }
    
    # --- PARA AÑADIR UN NUEVO CLIENTE ---
    # 1. Compra un número nuevo en Twilio (ej: +15557778888)
    # 2. Copia y pega una de las plantillas de cliente de arriba.
    # 3. Pon el nuevo número como la llave.
    # 4. Personaliza todos los mensajes y palabras clave para el nuevo cliente.
    #
    # ",+15557778888": {
    #    ...configuración del nuevo cliente...
    # }
}

# ==========================================================
#     EL WEBHOOK ÚNICO E INTELIGENTE QUE GESTIONA TODO
# ==========================================================
@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Esta función se activa para CUALQUIER mensaje que llegue
    a CUALQUIERA de los números de Twilio configurados.
    """
    # 1. Identificar a qué número de cliente llegó el mensaje. ¡Esta es la clave!
    to_number = request.values.get('To', '')
    
    # 2. Obtener el mensaje que envió el usuario final.
    incoming_msg = request.values.get('Body', '').lower().strip()
    
    # Preparar el objeto de respuesta de Twilio.
    response = MessagingResponse()
    msg = response.message()

    # 3. Buscar la configuración del cliente usando su número de Twilio.
    if to_number in CLIENTS_CONFIG:
        client_data = CLIENTS_CONFIG[to_number]
        
        # 4. Usar la lógica del bot con los datos específicos del cliente.
        
        # Primero, establecemos la respuesta por defecto del cliente.
        respuesta = client_data['default_response']
        
        # Luego, buscamos si el mensaje coincide con alguna palabra clave.
        for keyword, reply in client_data['keywords'].items():
            if keyword in incoming_msg:
                respuesta = reply
                break  # Salimos del bucle en cuanto encontramos la primera coincidencia.
        
        # Finalmente, un caso especial para el saludo inicial.
        # Esto sobreescribe la respuesta si el usuario dice "hola".
        if 'hola' in incoming_msg or 'buenas' in incoming_msg or 'buenos' in incoming_msg:
            respuesta = client_data['welcome_message']

        # Asignamos la respuesta final al cuerpo del mensaje.
        msg.body(respuesta)

    else:
        # Mensaje de error si, por alguna razón, llega un mensaje a un número
        # que no hemos configurado en nuestro diccionario CLIENTS_CONFIG.
        error_message = (f"Error de configuración del sistema. "
                         f"El número {to_number} no tiene un perfil de chatbot asociado.")
        print(error_message) # Imprime el error en los logs de Render para que lo veas.
        msg.body("Lo sentimos, este servicio no está disponible en este momento. Por favor, contacte al administrador.")

    # 5. Devolver la respuesta a Twilio en formato TwiML.
    return str(response)

# ==========================================================
#  ESTÁNDAR PARA EJECUTAR LA APP (NO TOCAR PARA PRODUCCIÓN)
# ==========================================================
if __name__ == '__main__':
    # Esto es solo para probar en tu computadora local.
    # Render usa Gunicorn para ejecutar la aplicación, por lo que ignora esta parte.
    app.run(port=5000, debug=True)