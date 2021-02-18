import os
from flask import Flask
from flask import url_for
from flask import render_template
from crypto_app import query_from_crypto
from flask_caching import Cache


# export FLASK_APP=crypto_flask.py
# flask run or python3 -m flask crypto_flask
config = {
	"DEBUG" : True,
	"CACHE_TYPE" : "simple",
	"CACHE_DEFAULT_TIMEOUT" : 60
}
app = Flask(__name__)
app.secret_key = os.urandom(32).decode('utf-8', errors='ignore')
app.config.from_mapping(config)
cache = Cache(app)

@app.route('/')
def index():
	result = get_result()
	return render_template('base.html', tables=result)

@cache.memoize(60)
def get_result():
	result = query_from_crypto()
	return result

with app.test_request_context():
    print(url_for('index'))


if __name__ == '__main__':
	app.run()
