# importazione librerie
from flask import Flask, render_template, request

app = Flask(__name__)

# La prima pagina
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/riscaldamento_globale')
def riscaldamento_globale():
    return render_template('riscaldamento_globale.html')

@app.route('/risposta', methods=["POST", "GET"])
def risposta():
    question = request.form['question']
    if "inquinamento" in question:
        return render_template("risposta.html", risposta="Può causare lo scioglimento dei ghiacciai")
    else:
        return render_template("risposta.html", risposta="Non ho capito!")

app.run(debug=True)
