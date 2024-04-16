import discord
from discord.ext import commands
import os, random
import requests

def get_random_duck():
    url = 'https://random-d.uk/api/random'
    response = requests.get(url)
    data = response.json()
    return data["url"]

intents = discord.Intents.default()
intents.message_content = True
# Inizializzazione del bot di discord test
bot = commands.Bot(command_prefix='!', intents=intents)

# Evento di avvio del bot
@bot.event
async def on_ready():
    print('Bot avviato come', bot.user)

@bot.command()
async def meme(ctx):
    images = os.listdir('images')
    random_image = random.choice(images)
    with open(f"images/{random_image}", "rb") as f:
        picture = discord.File(f)
    
    await ctx.send(file=picture)

@bot.command()
async def duck(ctx):
    image_url = get_random_duck()
    await ctx.send(image_url)


bot.run("CHIAVE DISCORD")
