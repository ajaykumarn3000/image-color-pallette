from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from colorthief import ColorThief
from PIL import Image
import os

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        image = request.files['myfile']
        filename = secure_filename(image.filename)
        image.save(os.path.join("static/img/", filename))

    # Color Thief

    ct = ColorThief("static/img/image.jpg")
    palette = ct.get_palette(color_count=4)
    color_palette = []
    for color in palette:
        print(color)
        hex_color = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
        hex_color = hex_color.upper()
        color_palette.append(hex_color)


    return render_template('index.html', color_palette=color_palette)


@app.route('/save', methods=['POST'])
def save_file():
    image = request.files['file']
    filename = secure_filename(image.filename)
    type = filename.split(".")[-1]

    image.save("static/img/image." + type)
    im = Image.open("static/img/image." + type)
    rgb_im = im.convert("RGB")
    rgb_im.save("static/img/image.jpg")
    if type != "jpg":
        print(1)
        file = 'image.'+type
        location = "static\\img"
        path = os.path.join(location, file)
        os.remove(path)
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run()