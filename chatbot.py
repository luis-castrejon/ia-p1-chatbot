from chatterbot import ChatBot
from adaptadores.adaptador_logico_conteo_dias import AdaptadorLogicoConteoDias
from adaptadores.adaptador_logico_tiempo_espanol import AdaptadorLogicoTiempoEspanol
from adaptadores.adaptador_logico_matematicas_espanol import AdaptadorLogicoMatematicasEspanol
from adaptadores.adaptador_logico_capitales import AdaptadorLogicoCapitales
from adaptadores.adaptador_logico_fecha_espanol import AdaptadorLogicoFechaEspanol
from adaptadores.adaptador_logico_motivaciones import AdaptadorLogicoMotivaciones
from adaptadores.adaptador_logico_datos_curiosos import AdaptadorLogicoDatosCuriosos
from utils.text_utils import normalizar_texto

# Utilidad para normalizar texto, como quitar acentos y caracteres especiales.
from utils.text_utils import normalizar_texto

# Crea una instancia del chatbot con un nombre y configuraciones específicas.
chatbot = ChatBot(
    'Bot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',  # Especifica el adaptador de almacenamiento para guardar las conversaciones.
    database_uri='sqlite:///:memory:',  # Usa una base de datos en memoria, lo que significa que los datos se pierden al reiniciar.
    logic_adapters=[  # Lista de adaptadores lógicos para manejar diferentes tipos de preguntas.
        # Cada adaptador lógico personalizado se especifica con su ruta de importación.
        {'import_path': 'adaptadores.adaptador_logico_conteo_dias.AdaptadorLogicoConteoDias'},
        {'import_path': 'adaptadores.adaptador_logico_tiempo_espanol.AdaptadorLogicoTiempoEspanol'},
        {'import_path': 'adaptadores.adaptador_logico_matematicas_espanol.AdaptadorLogicoMatematicasEspanol'},
        {'import_path': 'adaptadores.adaptador_logico_capitales.AdaptadorLogicoCapitales'},
        {'import_path': 'adaptadores.adaptador_logico_fecha_espanol.AdaptadorLogicoFechaEspanol'},
        {'import_path': 'adaptadores.adaptador_logico_motivaciones.AdaptadorLogicoMotivaciones'},
        {'import_path': 'adaptadores.adaptador_logico_datos_curiosos.AdaptadorLogicoDatosCuriosos'},
        # Un adaptador para proporcionar una respuesta específica a una entrada exacta.
        {
            'import_path': 'chatterbot.logic.SpecificResponseAdapter',
        },
        # Adaptador para encontrar la mejor coincidencia de respuesta, con un umbral de similitud y respuesta por defecto.
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'Lo siento, pero no entiendo.',
            'maximum_similarity_threshold': 0.95
        }
    ]
)

# Loop principal para interactuar con el chatbot desde la línea de comando.
print("\n¡Hola! ¿En qué puedo ayudarte? Escribe 'salir' para terminar.")
while True:
    try:
        entrada_usuario = input("> ")
        if entrada_usuario.lower() == 'salir':  # Permite al usuario salir del programa.
            print("¡Hasta luego!")
            break
        # Normaliza la entrada del usuario para mejorar la consistencia en la respuesta.
        entrada_normalizada = normalizar_texto(entrada_usuario)
        respuesta = chatbot.get_response(entrada_normalizada)
        print(f"{respuesta}")
    except UnicodeEncodeError as e:
        # Maneja posibles errores de codificación en la entrada del usuario.
        print("Se encontró un error de codificación. Intenta formular tu pregunta de otra manera.")
    except (KeyboardInterrupt, EOFError, SystemExit):
        break