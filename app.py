#!/usr/bin/env python
# coding: utf-8


from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
try:
    import aifc3 as aifc
except ImportError:
    try:
        import aifc
    except ImportError:
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "aifc3"])
        import aifc3 as aifc

import speech_recognition as sr

app = Flask(__name__)
#app.config['UPLOAD_FOLDER'] = "static/"

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save("static/"+filename)
#        file.save(app.config['UPLOAD_FOLDER'] + filename)
#        file = open(app.config['UPLOAD_FOLDER'] + filename,"r")
#        a = sr.AudioFile(app.config['UPLOAD_FOLDER'] + filename)
        a = sr.AudioFile("static/"+filename)
        with a as source:
            a = sr.Recognizer().record(source)
        s = sr.Recognizer().recognize_google(a)
        return(render_template("index1.html", result=s))
    elif request.method == 'GET':
        return render_template("index1.html", result="Please upload the file.")
    else:
        return(render_template("index1.html", result="error"))
    
if __name__ == "__main__":
    app.run()
