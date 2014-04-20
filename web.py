from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
import os

app = Flask(__name__)

DEFAULT_DIRECTORY = "C:*Users*Kaan*Desktop*"

class File:
    def __init__(self, directory=None, name=None, text=None, location=None):
        self.text = text
        self.name = name
        self.directory = directory
        self.location = location

def up_directory(directory):
    directory = directory.replace("/", "*")
    parts = directory.split("*")

    if len(parts) >= 2 and parts[1] != '':
        return "*".join(parts[:-2]) + "*"
    else:
        return directory

@app.route("/save/", methods=['POST'])
def post_save():
    with open(request.form['location'], 'w') as content:
        content.write(request.form['text'])
    return redirect("/edit/" + request.form['location'].replace("/", "*"))

@app.route("/up/<directory>", methods=['GET'])
def get_up(directory):
    return redirect("/directory/" + up_directory(directory))

@app.route("/", methods=['GET'])
def get_home():
    return redirect("/directory/" + DEFAULT_DIRECTORY)

@app.route("/edit/<file_location>", methods=['GET'])
def get_edit(file_location):
    file_location = file_location.replace("*", "/")
    
    with open(file_location, 'r') as content:
        f = File(location=file_location, text = content.read())
        return render_template('edit.html', data=f)
    
    return "Unable to access " + file_name + "."

@app.route("/directory/<directory>", methods=['GET'])
def get_directory(directory):
    fixed_directory = directory.replace("*", "/")
    
    files = [File(name=f, directory=directory) for f in os.listdir(fixed_directory) if f.endswith(".txt")]

    return render_template('directory.html', files=files, directory=directory)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
