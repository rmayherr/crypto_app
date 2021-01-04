from flask import Flask
from flask import url_for
from flask import render_template


app = Flask(__name__)

# export FLASK_APP=crypto_flask.py
# flask run or python3 -m flask crypto_flask
@app.route('/')
def index(name=None):
    return render_template('base.html', name=name)

with app.test_request_context():
    print(url_for('index'))
