from datetime import datetime
from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from utils.text_utils import normalizar_texto
import config
import re

# Utilizando pytz desde config directamente para establecer la zona horaria
TRADUCCIONES_MESES_NORMALIZADOS = {normalizar_texto(espanol): ingles for ingles, espanol in config.TRADUCCIONES_MESES.items()}

class AdaptadorLogicoConteoDias(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        # Uso directo de config.ZONA_HORARIA que ya tiene pytz.timezone aplicado
        self.zona_horaria = config.ZONA_HORARIA

    def can_process(self, declaracion):
        texto_normalizado = normalizar_texto(declaracion.text)
        return "cuantos dias faltan para el" in texto_normalizado

    def process(self, declaracion_entrada, parametros_adicionales_seleccion_respuesta):
        texto_normalizado = normalizar_texto(declaracion_entrada.text)
        try:
            fecha_match = re.search(r'cuantos dias faltan para el (\d{1,2}) de (\w+)(?: del (\d{4}))?', texto_normalizado)
            if fecha_match:
                dia, mes_normalizado, ano = fecha_match.groups()
                if not ano:
                    ano = str(datetime.now().year)
                
                mes_ingles = None
                for espanol, ingles in TRADUCCIONES_MESES_NORMALIZADOS.items():
                    if mes_normalizado == espanol:
                        mes_ingles = ingles
                        break
                
                if mes_ingles:
                    fecha_texto = f"{dia} {mes_ingles} {ano}"
                    fecha_objetivo = config.ZONA_HORARIA.localize(datetime.strptime(fecha_texto, '%d %B %Y'))
                    ahora = datetime.now(config.ZONA_HORARIA)
                    diferencia = fecha_objetivo - ahora
                    
                    if diferencia.total_seconds() > 0:
                        dias = diferencia.days
                        horas = diferencia.seconds // 3600
                        minutos = (diferencia.seconds % 3600) // 60
                        segundos = diferencia.seconds % 60
                        respuesta_texto = f"Faltan {dias} días, {horas} horas, {minutos} minutos y {segundos} segundos para el {dia} de {mes_normalizado.capitalize()} del {ano}."
                    else:
                        dias = abs(diferencia.days)
                        respuesta_texto = f"El {dia} de {mes_normalizado.capitalize()} del {ano} ya pasó hace {dias} días."
                else:
                    respuesta_texto = "No se reconoce el mes. Asegúrate de escribirlo correctamente."
            else:
                respuesta_texto = "Por favor, proporciona la fecha en el formato correcto."
        except Exception as e:
            respuesta_texto = f"Error al procesar la solicitud: {e}"
        
        declaracion_respuesta = Statement(text=respuesta_texto)
        declaracion_respuesta.confidence = 1
        return declaracion_respuesta