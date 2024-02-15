from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
import re

class AdaptadorLogicoMatematicasEspanol(LogicAdapter):
    """
    Clase que implementa un adaptador lógico para realizar operaciones matemáticas en español.

    Este adaptador puede procesar declaraciones que contengan preguntas sobre operaciones matemáticas,
    como sumas, restas, multiplicaciones y divisiones.

    Métodos:
    - can_process(declaracion): Verifica si la declaración puede ser procesada por este adaptador.
    - process(declaracion_entrada, parametros_adicionales_seleccion_respuesta): Procesa la declaración y devuelve una respuesta.
    """

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, declaracion):
        """
        Verifica si la declaración puede ser procesada por este adaptador.

        Parámetros:
        - declaracion: La declaración a ser procesada.

        Retorna:
        - True si la declaración puede ser procesada, False en caso contrario.
        """
        if re.search(r'\b(cuánto es|cuál es el resultado de|\d+\s+(más|mas|menos|por|entre)\s+\d+)\b', declaracion.text.lower()):
            return True
        return False

    def process(self, declaracion_entrada, parametros_adicionales_seleccion_respuesta):
        """
        Procesa la declaración y devuelve una respuesta.

        Parámetros:
        - declaracion_entrada: La declaración a ser procesada.
        - parametros_adicionales_seleccion_respuesta: Parámetros adicionales para seleccionar la respuesta.

        Retorna:
        - Una declaración de respuesta.
        """
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