import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['GET'])
def board():
    return "HELLO WORLD"

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(port)
