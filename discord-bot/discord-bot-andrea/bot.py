import discord
import random
from discord.ext import commands
import asyncio  # Aggiungi questa riga
import os

# Definisci il token del tuo bot
TOKEN = 'Inserisci la tua chiave qui'

def add_users(username):
    with open("points.txt", "r+", encoding="UTF-8") as f:
        users = [line.split("=")[0] for line in f.readlines()]
        if username not in users:
            f.write(f"{username}=0\n")
        else:
            print("Username già registrato")
 

# Funzione per incrementare il punteggio
def edit_user_points(username, points_delta):
    updated_lines = []
    with open("points.txt", "r", encoding="UTF-8") as f:
        for line in f:
            if username in line:
                user, points = line.strip().split("=")
                new_points = int(points) + points_delta
                line = f"{user}={new_points}\n"
            updated_lines.append(line)

    with open("points.txt", "w", encoding="UTF-8") as f:
        f.writelines(updated_lines)

    return new_points

# Funzione per creare il file del punteggio
def create_points_file():
    files = os.listdir(".")
    if "points.txt" not in files:
        print(files)
        with open("points.txt", "w", encoding="UTF-8") as f:
            pass
    else:
        print("File già esistente")

create_points_file()

# Lista di domande e risposte per i quiz ambientali
environmental_quizzes = [
    {
        "domanda": "Quale gas è principalmente responsabile dell'effetto serra?",
        "risposte": ["Anidride carbonica (CO2)", "Metano (CH4)", "Ozono (O3)"],
        "risposta_corretta": "Anidride carbonica (CO2)"
    },
    {
        "domanda": "Quale fenomeno è associato al progressivo riscaldamento del pianeta?",
        "risposte": ["Scioglimento dei ghiacciai", "Aumento del livello del mare", "Entrambi"],
        "risposta_corretta": "Entrambi"
    },
    {
        "domanda": "Qual è la principale fonte di energia rinnovabile utilizzata nel mondo?",
        "risposte": ["Solare", "Eolica", "Idroelettrica"],
        "risposta_corretta": "Solare"
    },
    {
        "domanda": "Qual è il principale inquinante dell'aria nelle città?",
        "risposte": ["PM2.5", "Ozono", "Monossido di carbonio"],
        "risposta_corretta": "PM2.5"
    }
]

intents = discord.Intents.default()
intents.message_content = True
# Definisci i comandi del bot
bot = commands.Bot(command_prefix='!', intents=intents)

# Comando per avviare un quiz ambientale
@bot.command()
async def quiz(ctx):
    # Ottieni il nome dell'utente che ha inviato il comando
    username = ctx.author.name
    add_users(username)

    quiz = random.choice(environmental_quizzes)
    domanda = quiz["domanda"]
    risposte = quiz["risposte"]
    risposta_corretta = quiz["risposta_corretta"]

    # Manda la domanda
    await ctx.send(domanda)

    # Manda le opzioni di risposta
    for risposta in risposte:
        await ctx.send(risposta)

    # Funzione per controllare se la risposta data dall'utente è corretta
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        # Aspetta la risposta dell'utente
        risposta_utente = await bot.wait_for('message', timeout=30, check=check)
         
        # Controlla se la risposta dell'utente è corretta
        if risposta_utente.content == risposta_corretta:
            points = edit_user_points(username, 1)
            await ctx.send(f"Risposta corretta!\nIl tuo punteggio attuale è di: {points}")
        else:
            await ctx.send(f"Risposta sbagliata! La risposta corretta è: {risposta_corretta}")
    except asyncio.TimeoutError:
        await ctx.send("Tempo scaduto! Il quiz è terminato.")

# Evento quando il bot è pronto
@bot.event
async def on_ready():
    print(f'{bot.user.name} è online!')

# Avvia il bot
bot.run(TOKEN)
