from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from datetime import datetime
from utils.text_utils import normalizar_texto
import pytz

class AdaptadorLogicoTiempoEspanol(LogicAdapter):
    """
    Clase que implementa un adaptador lógico para responder preguntas sobre la hora en español.

    Métodos:
    - __init__: Inicializa la instancia del adaptador lógico.
    - can_process: Verifica si el adaptador puede procesar una declaración.
    - process: Procesa una declaración y devuelve una respuesta.
    """

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, declaracion):
        """
        Verifica si el adaptador puede procesar una declaración.

        Parámetros:
        - declaracion: La declaración a procesar.

        Retorna:
        - True si el adaptador puede procesar la declaración, False en caso contrario.
        """
        texto = normalizar_texto(declaracion.text)
        return "que hora es" in texto or "dime la hora" in texto

    def process(self, declaracion_entrada, parametros_adicionales_seleccion_respuesta):
        """
        Procesa una declaración y devuelve una respuesta.

        Parámetros:
        - declaracion_entrada: La declaración a procesar.
        - parametros_adicionales_seleccion_respuesta: Parámetros adicionales para seleccionar la respuesta.

        Retorna:
        - La declaración de respuesta.
        """
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