import discord
from discord.ext import commands
import requests
from model import get_class

# Token del bot
TOKEN = 'La tua chiave discord'

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
