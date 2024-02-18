

from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def raiz():
    return "HOla esta es la rais del projecto "

app.run()