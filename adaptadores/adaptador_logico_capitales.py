from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from utils.text_utils import normalizar_texto
import json

class AdaptadorLogicoCapitales(LogicAdapter):
    """
    Clase que implementa un adaptador lógico para obtener la capital de un país.
    Utiliza un archivo JSON que contiene las conversaciones de preguntas y respuestas
    sobre las capitales de los países.
    """

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        with open('./data/paises_y_capitales.json', encoding='utf-8') as archivo:
            conversaciones = json.load(archivo)["conversations"]
            self.capitales = {normalizar_texto(pregunta): respuesta for pregunta, respuesta in conversaciones}

    def can_process(self, declaracion):
        """
        Verifica si la declaración puede ser procesada por este adaptador.
        La declaración debe contener la frase "cual es la capital de".
        """
        texto = normalizar_texto(declaracion.text)
        return "cual es la capital de" in texto

    def process(self, declaracion_entrada, parametros_adicionales_seleccion_respuesta):
        """
        Procesa la declaración de entrada y devuelve una respuesta.
        Busca en el diccionario de capitales si la pregunta coincide con alguna clave,
        y devuelve la respuesta correspondiente.
        """
        texto_entrada = normalizar_texto(declaracion_entrada.text)
        respuesta_texto = "Lo siento, no tengo esa información."
        respuesta_confianza = 0

        for pregunta_normalizada, respuesta in self.capitales.items():
            if pregunta_normalizada in texto_entrada:
                respuesta_texto = respuesta
                respuesta_confianza = 1
                break

        declaracion_respuesta = Statement(text=respuesta_texto)
        declaracion_respuesta.confidence = respuesta_confianza
        return declaracion_respuesta