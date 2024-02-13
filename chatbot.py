from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from datetime import datetime
import pytz
import re

# Adaptador lógico para responder la hora en español
class AdaptadorLogicoTiempoEspanol(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, declaracion):
        texto = declaracion.text.lower()
        if 'hora' in texto:
            return True
        return False

    def process(self, declaracion_entrada, parametros_adicionales_seleccion_respuesta):
        zona_horaria = pytz.timezone('America/Mexico_City')
        ahora = datetime.now(zona_horaria)
        hora = ahora.strftime('%I')
        minuto = ahora.strftime('%M')
        periodo = ahora.strftime('%p').replace('AM', 'a.m.').replace('PM', 'p.m.')

        if hora == '01':
            hora_texto = f"Es la {hora}:{minuto} {periodo}"
        else:
            hora_texto = f"Son las {hora}:{minuto} {periodo}"

        declaracion_respuesta = Statement(text=hora_texto)
        declaracion_respuesta.confidence = 1
        return declaracion_respuesta

# Adaptador lógico para operaciones matemáticas en español
class AdaptadorLogicoMatematicasEspanol(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, declaracion):
        if re.search(r'\b(cuánto es|cuál es el resultado de|\d+\s+(más|mas|menos|por|entre)\s+\d+)\b', declaracion.text.lower()):
            return True
        return False

    def process(self, declaracion_entrada, parametros_adicionales_seleccion_respuesta):
        texto = declaracion_entrada.text.lower()
        numeros = re.findall(r'\b\d+\b', texto)
        resultado = 0
        texto_respuesta = "Lo siento, pero no pude realizar la operación."

        operaciones = {
            'más': lambda x, y: x + y,
            'menos': lambda x, y: x - y,
            'por': lambda x, y: x * y,
            'entre': lambda x, y: x / y if y != 0 else "No se puede dividir entre cero."
        }

        if 'mas' in texto:
            operaciones['mas'] = operaciones['más']

        for operacion, funcion_operacion in operaciones.items():
            if operacion in texto or f'{operacion} de' in texto:
                if len(numeros) >= 2:
                    resultado = funcion_operacion(int(numeros[0]), int(numeros[1]))
                    texto_respuesta = f"El resultado es {resultado}"
                break

        declaracion_respuesta = Statement(text=texto_respuesta)
        declaracion_respuesta.confidence = 1
        return declaracion_respuesta

# Configuración del chatbot
chatbot = ChatBot(
    'TerminalBot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///:memory:',
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'Lo siento, pero no entiendo.',
            'maximum_similarity_threshold': 0.90
        },
        '__main__.AdaptadorLogicoTiempoEspanol',
        '__main__.AdaptadorLogicoMatematicasEspanol',
        {
            'import_path': 'chatterbot.logic.SpecificResponseAdapter',
            'input_texto': 'Ayuda',
            'output_texto': 'Puedes preguntarme sobre cálculos matemáticos, la hora actual, o cualquier cosa general.'
        }
    ]
)

# Entrenamiento del chatbot (opcional si ya está entrenado)
entrenador = ChatterBotCorpusTrainer(chatbot)
entrenador.train("chatterbot.corpus.spanish")

# Interacción con el chatbot
print("\n¡Hola! Soy TerminalBot. ¿En qué puedo ayudarte? Escribe 'salir' para terminar.")
while True:
    try:
        entrada_usuario = input("Tú: ")
        if entrada_usuario.lower() == 'salir':
            print("TerminalBot: ¡Hasta luego!")
            break
        respuesta = chatbot.get_response(entrada_usuario)
        print(f"TerminalBot: {respuesta}")
    except (KeyboardInterrupt, EOFError, SystemExit):
        break