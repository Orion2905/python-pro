from flask import Flask, render_template, request, redirect, url_for

from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np

def model_(image_path):
    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)

    # Load the model
    model = load_model("keras_model.h5", compile=False)

    # Load the labels
    class_names = open("labels.txt", "r").readlines()

    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Replace this with the path to your image
    image = Image.open(image_path).convert("RGB")

    # resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    # turn the image into a numpy array
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # Predicts the model
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    print("Class:", class_name[2:], end="")
    print("Confidence Score:", confidence_score)

    return [class_name[2:], confidence_score]

app = Flask(__name__)

articles = [
    {"id": 0, "title": "Articolo 1 sul cambiamento climatico", "content": "Contenuto dell'articolo 1..."},
    {"id": 1, "title": "Articolo 2 sul cambiamento climatico", "content": "Contenuto dell'articolo 2..."},
    {"id": 2, "title": "Articolo 3 sul cambiamento climatico", "content": "Contenuto dell'articolo 3..."}
    # Aggiungi altri articoli qui
]

@app.route('/')
def index():
    return render_template('index.html', articles=articles)

@app.route('/model', methods=['POST'])
def model():
    risposta = model_(request.form['url'])
    return render_template('risposta.html', risposta=risposta)

@app.route('/submit_article', methods=['POST'])
def submit_article():
    title = request.form['title']
    content = request.form['content']
    new_article = {"title": title, "content": content}
    articles.append(new_article)
    return redirect(url_for('index'))

@app.route('/article/<int:article_id>')
def article(article_id):
    # L'ID dell'articolo fornito nell'URL sarà 1 in più dell'indice dell'articolo nella lista
    article_index = article_id - 1
    # Verifica se l'indice dell'articolo è valido
    if 0 <= article_index < len(articles):
        return render_template('article.html', article=articles[article_index])
    else:
        return "Articolo non trovato"




if __name__ == '__main__':
    app.run(debug=True)
