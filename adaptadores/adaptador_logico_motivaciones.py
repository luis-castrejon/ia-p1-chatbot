from chatterbot.conversation import Statement
from chatterbot.logic import LogicAdapter
from utils.text_utils import normalizar_texto
import json
import random

class AdaptadorLogicoMotivaciones(LogicAdapter):
    """
    Clase que implementa un adaptador lógico para proporcionar frases motivacionales.

    Atributos:
    - frases_motivacionales (list): Lista de frases motivacionales cargadas desde un archivo JSON.

    Métodos:
    - __init__(self, chatbot, **kwargs): Constructor de la clase.
    - can_process(self, declaracion): Verifica si la declaración contiene la frase "frase motivacional".
    - process(self, declaracion_entrada, parametros_adicionales_seleccion_respuesta): Procesa la declaración y devuelve una respuesta motivacional.
    """

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        with open('./data/quotes.json', encoding='utf-8') as archivo:
            self.frases_motivacionales = json.load(archivo)["conversations"]

    def can_process(self, declaracion):
        """
        Verifica si la declaración contiene la frase "frase motivacional".

        Args:
        - declaracion (Statement): La declaración a verificar.

        Returns:
        - bool: True si la declaración contiene la frase "frase motivacional", False en caso contrario.
        """
        texto = normalizar_texto(declaracion.text)
        return "frase motivacional" in texto

    def process(self, declaracion_entrada, parametros_adicionales_seleccion_respuesta):
        """
        Procesa la declaración y devuelve una respuesta motivacional.

        Args:
        - declaracion_entrada (Statement): La declaración de entrada.
        - parametros_adicionales_seleccion_respuesta: Parámetros adicionales para la selección de la respuesta.

        Returns:
        - Statement: La declaración de respuesta motivacional.
        """
        frase_motivacional, autor = random.choice(self.frases_motivacionales)
        declaracion_respuesta = Statement(text=f"{frase_motivacional}\n- {autor}")
        declaracion_respuesta.confidence = 1
        return declaracion_respuesta