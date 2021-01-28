import os
from flask import Flask
from flask import url_for
from flask import render_template
from crypto_app import query_from_crypto


app = Flask(__name__)
app.secret_key = os.urandom(32).decode('utf-8', errors='ignore')

# export FLASK_APP=crypto_flask.py
# flask run or python3 -m flask crypto_flask

@app.route('/')
def index():
	result = query_from_crypto()
	return render_template('base.html', tables=result)

with app.test_request_context():
    print(url_for('index'))


if __name__ == '__main__':
	app.run()