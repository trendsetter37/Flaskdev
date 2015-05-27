from flask import Flask
from flask import render_template
import sys

app = Flask(__name__)

@app.route('/')
@app.route('/hello/')
@app.route('/hello/<name>/')
def hello_world(name=None):
	return render_template('hello.html', name=name)

if __name__ == '__main__':
	if len(sys.argv) > 1:
		app.run(host=sys.argv[1])
	else:
		app.run(host='0.0.0.0', debug=True) # for testing purposes