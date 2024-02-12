from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

chatbot = ChatBot("Bot")

conversation = [
    "Hola",
    "¡Hola!",
    "¿Cómo estás?",
    "Estoy muy bien.",
    "Me alegro.",
    "Gracias.",
    "De nada."
]

trainer = ListTrainer(chatbot)
trainer.train(conversation)

#response = chatbot.get_response("¡Buenos días!")
#print(response)

def converse():
    user_input = ""
    while user_input != "adiós":
        try:
            user_input = input("Tú: ")
            if user_input.lower() == "adiós":
                break
            if user_input:
                response = chatbot.get_response(user_input)
                print(f"Bot: {response}")
        except EOFError:
            break

converse()