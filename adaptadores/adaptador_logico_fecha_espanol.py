from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from datetime import datetime
from utils.text_utils import normalizar_texto
import config

class AdaptadorLogicoFechaEspanol(LogicAdapter):
    """
    Clase que representa un adaptador lógico para obtener la fecha actual en español.

    Métodos:
    - __init__: Inicializa la instancia del adaptador lógico.
    - can_process: Verifica si puede procesar una declaración.
    - process: Procesa una declaración y devuelve la respuesta.
    - obtener_fecha_texto_espanol: Obtiene la fecha actual en formato de texto en español.
    """

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, declaracion):
        """
        Verifica si puede procesar una declaración.

        Parámetros:
        - declaracion: La declaración a procesar.

        Retorna:
        - True si puede procesar la declaración, False en caso contrario.
        """
        texto = normalizar_texto(declaracion.text)
        return "dia" in texto or "fecha" in texto

    def process(self, declaracion_entrada, parametros_adicionales_seleccion_respuesta):
        """
        Procesa una declaración y devuelve la respuesta.

        Parámetros:
        - declaracion_entrada: La declaración de entrada a procesar.
        - parametros_adicionales_seleccion_respuesta: Parámetros adicionales para seleccionar la respuesta.

        Retorna:
        - La declaración de respuesta.
        """
        fecha_texto = self.obtener_fecha_texto_espanol()
        declaracion_respuesta = Statement(text=f"Hoy es {fecha_texto}.")
        declaracion_respuesta.confidence = 1
        return declaracion_respuesta

    def obtener_fecha_texto_espanol(self):
        """
        Obtiene la fecha actual en formato de texto en español.

        Retorna:
        - La fecha actual en formato de texto en español.
        """
        zona_horaria = config.ZONA_HORARIA
        ahora = datetime.now(zona_horaria)
        
        # Usar las traducciones definidas para convertir la fecha al español
        dia_semana = config.TRADUCCIONES_DIAS[ahora.strftime('%A')]
        mes = config.TRADUCCIONES_MESES[ahora.strftime('%B')]
        fecha_texto = f"{dia_semana}, {ahora.day} de {mes} de {ahora.year}"
        
        return fecha_texto