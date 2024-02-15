from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from utils.text_utils import normalizar_texto
import json
import random

class AdaptadorLogicoDatosCuriosos(LogicAdapter):
    """
    Clase que implementa un adaptador lógico para proporcionar datos curiosos en una conversación.

    Atributos:
    - chatbot: El objeto ChatBot al que está asociado este adaptador.
    - datos_curiosos: Una lista de datos curiosos cargados desde un archivo JSON.

    Métodos:
    - __init__(self, chatbot, **kwargs): Constructor de la clase.
    - can_process(self, declaracion): Verifica si el adaptador puede procesar una declaración.
    - process(self, declaracion_entrada, parametros_adicionales_seleccion_respuesta): Procesa una declaración y devuelve una respuesta.
    """

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        with open('./data/datos_curiosos.json', encoding='utf-8') as archivo:
            self.datos_curiosos = json.load(archivo)["conversations"]
            
    def can_process(self, declaracion):
        texto = normalizar_texto(declaracion.text)
        return "un dato curioso" in texto

    def process(self, declaracion_entrada, parametros_adicionales_seleccion_respuesta):
        dato_curioso = random.choice(self.datos_curiosos)
        declaracion_respuesta = Statement(text=dato_curioso)
        declaracion_respuesta.confidence = 1
        return declaracion_respuesta