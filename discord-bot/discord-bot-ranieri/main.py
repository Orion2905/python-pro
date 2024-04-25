import discord
from discord.ext import commands
import requests

from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np

# Token del bot
TOKEN = 'la tua chiave discord qui'

# Prefix del bot
PREFIX = '!'

# Categorie di rifiuti
categories = ['Plastica', 'Carta', 'Vetro', "Organico", "Piccione", "Indifferenziato"]

# Funzione per classificare l'immagine usando il modello Teachable Machine
def elabora_rispota(risposta):
    for category in categories:
        print((category, risposta[0]))
        if category in risposta[0]:
            return f"Questo oggetto va buttato in {category} [sicurezza del {round(float(risposta[1]), 2)} %]"
    else:
        return f"Questo oggetto va buttato in {categories[-1]}"

def get_class(model_path, labels_path, image_path):
    np.set_printoptions(suppress=True)
    model = load_model(model_path, compile=False)
    class_names = open(labels_path, "r", encoding="utf-8").readlines()
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = Image.open(image_path).convert("RGB")
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data[0] = normalized_image_array
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]
    return(class_name[2:], confidence_score*100)


intents = discord.Intents.default()
intents.message_content = True

# Inizializza il bot
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# Evento di avvio del bot
@bot.event
async def on_ready():
    print('Bot pronto')

# Comando per analizzare un'immagine
@bot.command()
async def analizza(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            file_name = attachment.filename
            file_url = attachment.url
            await attachment.save(f"./{file_name}")
            message = elabora_rispota(get_class(model_path="./keras_model.h5", labels_path="labels.txt", image_path=f"./{attachment.filename}"))
            await ctx.send(
                message
                )
    else:
        await ctx.send("Hai dimenticato di inserire un'immagine 😢")

# Avvia il bot
bot.run(TOKEN)
