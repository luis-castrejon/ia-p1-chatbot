from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from unidecode import unidecode
from datetime import datetime
import pytz
import re
import json
import random

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

class AdaptadorLogicoCapitales(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        # Cargar el archivo JSON con las conversaciones
        with open('./data/paises_y_capitales.json', encoding='utf-8') as archivo:
            self.capitales = json.load(archivo)["conversations"]

    def can_process(self, declaracion):
        texto = unidecode(declaracion.text.lower())
        if "cual es la capital de" in texto:
            return True
        return False

    def process(self, declaracion_entrada, parametros_adicionales_seleccion_respuesta):
        texto_entrada = unidecode(declaracion_entrada.text.lower()) 
        texto_entrada = re.sub(r'[^\w\s]', '', texto_entrada)  # Remover puntuación

        respuesta_confianza = 0
        respuesta_texto = "Lo siento, no tengo esa información."

        # Buscar en el archivo JSON la capital del país preguntado
        for pregunta, respuesta in self.capitales:
            pregunta_normalizada = unidecode(pregunta.lower())  # Normalizar para remover acentos y convertir a minúsculas
            pregunta_normalizada = re.sub(r'[^\w\s]', '', pregunta_normalizada)  # Remover puntuación
            if pregunta_normalizada == texto_entrada:
                respuesta_texto = respuesta
                respuesta_confianza = 1
                break

        declaracion_respuesta = Statement(text=respuesta_texto)
        declaracion_respuesta.confidence = respuesta_confianza
        return declaracion_respuesta

class AdaptadorLogicoFechaEspanol(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, declaracion):
        texto = declaracion.text.lower()
        if any(frase in texto for frase in ['fecha', 'día es', 'dia es']):
            return True
        return False

    def process(self, declaracion_entrada, parametros_adicionales_seleccion_respuesta):
        zona_horaria = pytz.timezone('America/Mexico_City')
        ahora = datetime.now(zona_horaria)
        fecha_texto = ahora.strftime('%A, %d de %B de %Y')
        
        # Traducción de los días de la semana y meses al español
        traducciones = {
            "Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles",
            "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado",
            "Sunday": "Domingo", "January": "Enero", "February": "Febrero",
            "March": "Marzo", "April": "Abril", "May": "Mayo", "June": "Junio",
            "July": "Julio", "August": "Agosto", "September": "Septiembre",
            "October": "Octubre", "November": "Noviembre", "December": "Diciembre"
        }
        for ingles, espanol in traducciones.items():
            fecha_texto = fecha_texto.replace(ingles, espanol)

        declaracion_respuesta = Statement(text=f"Hoy es {fecha_texto}.")
        declaracion_respuesta.confidence = 1
        return declaracion_respuesta

class AdaptadorLogicoMotivacional(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        with open('./data/quotes.json', encoding='utf-8') as archivo:
            self.frases_motivacionales = json.load(archivo)["conversations"]

    def can_process(self, declaracion):
        texto = declaracion.text.lower()
        if 'frase motivacional' in texto:
            return True
        return False

    def process(self, declaracion_entrada, parametros_adicionales_seleccion_respuesta):
        frase_motivacional, autor = random.choice(self.frases_motivacionales)
        declaracion_respuesta = Statement(text=f"{frase_motivacional}\n- {autor}")
        declaracion_respuesta.confidence = 1
        return declaracion_respuesta

class AdaptadorLogicoDatosCuriosos(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        with open('./data/datos_curiosos.json', encoding='utf-8') as archivo:
            self.datos_curiosos = json.load(archivo)["conversations"]

    def can_process(self, declaracion):
        texto = declaracion.text.lower()
        if 'dato curioso' in texto:
            return True
        return False

    def process(self, declaracion_entrada, parametros_adicionales_seleccion_respuesta):
        dato_curioso = random.choice(self.datos_curiosos)
        declaracion_respuesta = Statement(text=dato_curioso)
        declaracion_respuesta.confidence = 1
        return declaracion_respuesta

# Adaptador lógico para contar cuántos días faltan hasta una fecha específica
class AdaptadorLogicoConteoDias(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, declaracion):
        texto = declaracion.text.lower()
        return bool(re.search(r'\b(cuántos días faltan para el \d{1,2} de \w+ del \d{4})\b', texto))

    def process(self, declaracion_entrada, parametros_adicionales_seleccion_respuesta):
        meses = {
            'enero': 'January',
            'febrero': 'February',
            'marzo': 'March',
            'abril': 'April',
            'mayo': 'May',
            'junio': 'June',
            'julio': 'July',
            'agosto': 'August',
            'septiembre': 'September',
            'octubre': 'October',
            'noviembre': 'November',
            'diciembre': 'December'
        }

        try:
            fecha_match = re.search(r'\bpara el (\d{1,2}) de (\w+) del (\d{4})\b', declaracion_entrada.text)
            if fecha_match:
                dia, mes_espanol, ano = fecha_match.groups()
                mes_ingles = meses.get(mes_espanol.lower())
                if mes_ingles:
                    zona_horaria = pytz.timezone('America/Mexico_City')
                    fecha_texto = f"{dia} {mes_ingles} {ano}"
                    fecha_objetivo = zona_horaria.localize(datetime.strptime(fecha_texto, '%d %B %Y'))
                    ahora = datetime.now(zona_horaria)

                    diferencia_total = fecha_objetivo - ahora
                    dias = diferencia_total.days
                    horas = diferencia_total.seconds // 3600
                    minutos = (diferencia_total.seconds % 3600) // 60

                    if dias > 0 or (dias == 0 and diferencia_total.seconds > 0):
                        respuesta_texto = f"Faltan {dias} días, {horas} horas y {minutos} minutos para el {dia} de {mes_espanol} del {ano}."
                    elif dias == 0 and diferencia_total.seconds == 0:
                        respuesta_texto = "Hoy es el día indicado."
                    else:
                        respuesta_texto = f"El {dia} de {mes_espanol} del {ano} ya pasó."
                else:
                    respuesta_texto = "Por favor, proporciona un nombre de mes válido."
            else:
                respuesta_texto = "Por favor, proporciona la fecha en el formato 'dd de mm del aaaa'."
            declaracion_respuesta = Statement(text=respuesta_texto)
            declaracion_respuesta.confidence = 1
        except Exception as e:
            print(f"Error al procesar la solicitud: {e}")
            declaracion_respuesta = Statement(text="Lo siento, hubo un error al procesar tu solicitud.")
            declaracion_respuesta.confidence = 0
        return declaracion_respuesta

chatbot = ChatBot(
    'TerminalBot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///:memory:',
    logic_adapters=[
        # Tu AdaptadorLogicoConteoDias va primero para darle la mayor prioridad
        '__main__.AdaptadorLogicoConteoDias',

        # Luego, coloca otros adaptadores personalizados que has mencionado
        '__main__.AdaptadorLogicoTiempoEspanol',
        '__main__.AdaptadorLogicoMatematicasEspanol',
        '__main__.AdaptadorLogicoCapitales',
        '__main__.AdaptadorLogicoFechaEspanol',
        '__main__.AdaptadorLogicoMotivacional',
        '__main__.AdaptadorLogicoDatosCuriosos',

        # El adaptador para respuestas específicas
        {
            'import_path': 'chatterbot.logic.SpecificResponseAdapter',
            'input_text': 'Ayuda',
            'output_text': 'Puedes preguntarme sobre cálculos matemáticos, la hora actual, o cualquier cosa general.'
        },
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'Lo siento, pero no entiendo.',
            'maximum_similarity_threshold': 0.95
        }
    ]
)

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