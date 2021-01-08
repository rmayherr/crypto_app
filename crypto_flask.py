from flask import Flask
from flask import url_for
from flask import render_template
from crypto_app import query_from_crypto


app = Flask(__name__)
app.secret_key = b'\xf5]\xfd\x8a\xa3/V\x91F\xe9\xbf\x1b\x84\x87\x91\x05'

# export FLASK_APP=crypto_flask.py
# flask run or python3 -m flask crypto_flask
@app.route('/')
def index(name=None):
    return render_template('base.html', name=name)

with app.test_request_context():
    print(url_for('index'))
