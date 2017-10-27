from flask_cors import CORS
from datetime import datetime
from generateGraph import constructGraph
from flask import Flask, abort, flash, redirect, render_template, request, url_for

app = Flask(__name__)
CORS(app)
app.config['DEBUG'] = True
# app.config['SECRET_KEY'] = 'some_really_long_random_string_here'

@app.route('/generateGraph', methods=['POST'])
def generate_graph():
    print request.get_json()
    return constructGraph(request.get_json())

if __name__ == '__main__':
    app.run()

