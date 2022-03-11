from flask import Flask, render_template
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './planet_guesser'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

@app.route("/")
@app.route("/home")
def home_page():
    return render_template ('home2.html')


@app.route("/planet-guesser", methods=['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part, 404')
            return 'No file part' , 404
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            print('No selected file')
            return 'No selected file' , 404
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'Done', 201
    return render_template ('planet_guesser.html')    

app.run(
    host='0.0.0.0',
    port=5100,
    debug=True
)
#@app.route("/escape-mars", methods=['GET', 'POST'])
#def escape_mars():
#    return