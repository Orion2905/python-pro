from flask import Flask, render_template, request, redirect, url_for
import os
import random

app = Flask(__name__)

# Definizione dei livelli e dei rispettivi percorsi delle cartelle
livelli = {
    "livello1": "static/livello1/",
    "livello2": "static/livello2/",
    "livello3": "static/livello3/"
}

# Definizione dei secchi disponibili
secchi = ["alluminio", "carta", "plastica", "vetro"]

livello_corrente = "livello1"  # Livello di partenza
livello_max = len(livelli)  # Numero massimo di livelli

@app.route('/')
def index():
    global livello_corrente
    livello_corrente = "livello1"  # Reset del livello a quello di partenza
    return render_template('index.html', livello=livello_corrente, secchi=secchi)

@app.route('/seleziona_secchio', methods=['POST'])
def seleziona_secchio():
    global livello_corrente
    selezione_utente = request.form['secchio']

    # Ottenere la lista delle immagini nel livello corrente
    lista_immagini = os.listdir(livelli[livello_corrente])

    # Selezionare casualmente una nuova immagine
    immagine_da_indovinare = random.choice(lista_immagini)
    nome_rifiuto = immagine_da_indovinare.split('_')[0]  # Ottenere il nome del rifiuto dall'immagine

    # Verifica se il secchio selezionato è corretto
    if selezione_utente == nome_rifiuto:
        if livello_corrente != "livello3":
            # Se l'utente ha indovinato e non è al livello massimo, passa al livello successivo
            livello_corrente = "livello" + str(int(livello_corrente[-1]) + 1)
        else:
            return "Complimenti, hai completato tutti i livelli!"
    # Reindirizza l'utente alla pagina del gioco con tutte le variabili necessarie
    return redirect(url_for('game'))

@app.route('/game', methods=['GET', 'POST'])
def game():
    global livello_corrente
    
    if request.method == 'GET':
        lista_immagini = os.listdir(livelli[livello_corrente])
        immagine_da_indovinare = random.choice(lista_immagini)
        return render_template('game.html', livello=livello_corrente, immagine_da_indovinare=immagine_da_indovinare, secchi=secchi)
    
    elif request.method == 'POST':
        selezione_utente = request.form['secchio']
        lista_immagini = os.listdir(livelli[livello_corrente])
        immagine_da_indovinare = random.choice(lista_immagini)
        nome_rifiuto = immagine_da_indovinare.split('_')[0]

        if selezione_utente == nome_rifiuto:
            if livello_corrente != "livello3":
                livello_corrente = "livello" + str(int(livello_corrente[-1]) + 1)
                return redirect(url_for('game'))  # Reindirizza alla stessa pagina per mostrare il nuovo livello
            else:
                return "Complimenti, hai completato tutti i livelli!"
        else:
            return redirect(url_for('game'))  # Reindirizza alla stessa pagina per mostrare la nuova immagine




if __name__ == '__main__':
    app.run(debug=True)
