from unidecode import unidecode
import re

def normalizar_texto(texto):
    texto = unidecode(texto.lower())  # Convertir a minúsculas y eliminar acentos
    texto = re.sub(r'[^\w\s]', '', texto)  # Remover puntuación
    texto = re.sub(r'\s+', ' ', texto).strip()  # Remover espacios extra y espacios al inicio y final
    return texto
