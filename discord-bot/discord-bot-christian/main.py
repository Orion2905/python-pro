#chatbot discord sul cambiamento climatico dove quando scrivi un problema, ti riesce a dare tutte le soluzioni che ci sono. (Christian)
import discord
from discord.ext import commands
import random
import requests

intents = discord.Intents.default()
intents.message_content = True

# Inizializzazione del bot
bot = commands.Bot(command_prefix='!', intents=intents)

# Lista di problemi 
soluzioni = {       
    "aumento delle temperature globali":"Riduzione delle emissioni di gas serra attraverso politiche di mitigazione come l'adozione di energie rinnovabili e l'efficienza energetica",
    "scioglimento dei ghiacciai e dei poli":"Riduzione delle emissioni di gas serra per rallentare il riscaldamento globale",
    "aumento del livello del mare":"Implementazione di misure di adattamento come la costruzione di difese costiere e la pianificazione urbana resiliente",
    "eventi metereologici estremi":"Riduzione delle emissioni di gas serra per mitigare l'intensità e la frequenza degli eventi estremi",
    "alterazioni degli ecosistemi":"Conservazione delle aree naturali e ripristino degli habitat degradati",
    "acidificazione degli oceani":"Riduzione delle emissioni di gas serra per rallentare l'acidificazione",
    "scarsità idrica":"Gestione sostenibile delle risorse idriche e investimenti in infrastrutture idriche resilienti",
    "impatti sulla sicurezza alimentare":"Promozione di pratiche agricole resilienti e sostenibili",
    "migrazioni forzate":"Cooperazione internazionale per affrontare le cause profonde della migrazione climatica",
    "impatti sulla salute umana":"Miglioramento dei sistemi sanitari per affrontare le sfide legate al cambiamento climatico",
    "perdita di biodiversità":"Riduzione della deforestazione e protezione delle specie minacciate",
    "impatti sulla pesca e l'acquacoltura":"Gestione sostenibile delle risorse ittiche e protezione degli ecosistemi marini",
    "perdita di risorse naturali":"Gestione sostenibile delle risorse naturali e riduzione dello sfruttamento eccessivo",
    "aumento dei conflitti":"Investimenti nella pace, nella sicurezza e nella diplomazia preventiva",
    "impatti sulla qualità dell'aria":"Riduzione delle emissioni inquinanti da fonti industriali, veicoli e combustibili fossili"
}


# Evento di avvio del bot
@bot.event
async def on_ready():
    print('Bot avviato come', bot.user)

@bot.command()
async def elenco_problemi(ctx):
    for soluzione in soluzioni:
        await ctx.send(soluzione)

@bot.command()
async def problemi_e_soluzioni(ctx):
    problema = random.choice(list(soluzioni.keys()))
    soluzione = soluzioni[problema]
    await ctx.send(f"la soluzione al problema {problema} è {soluzione}")

@bot.command()
async def cerca_soluzione(ctx, *, parola_chiave: str):
    parola_chiave = parola_chiave.lower()  # Converte la parola chiave in minuscolo per garantire una corrispondenza non case-sensitive
    problemi_trovati = []  # Lista per memorizzare i problemi contenenti la parola chiave

    for problema, soluzione in soluzioni.items():
        if parola_chiave in problema.lower():  # Controlla se la parola chiave è contenuta nel problema
            problemi_trovati.append((problema, soluzione))  # Aggiunge il problema alla lista dei problemi trovati

    if problemi_trovati:  # Se sono stati trovati problemi, invia i risultati all'utente
        messaggio = "\n\n".join([f"Problema: {problema}\nSoluzione: {soluzione}" for problema, soluzione in problemi_trovati])
        await ctx.send(f"Ecco i problemi che contengono '{parola_chiave}':\n\n{messaggio}")
    else:
        await ctx.send(f"Mi dispiace, non ho trovato problemi che contengono '{parola_chiave}'.")

# Gestione degli errori per il comando cerca_soluzione
@cerca_soluzione.error
async def cerca_soluzione_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Per favore, specifica un problema da cercare.")
    else:
        await ctx.send("Si è verificato un errore durante la ricerca della soluzione. Assicurati di inserire un problema valido.")



bot.run("La tua chiave discord qui")
