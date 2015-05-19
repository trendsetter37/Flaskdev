from flask import Flask
import sys

app = Flask(__name__)

@app.route('/')
def hello_world():
	return "Hello World"

if __name__ == '__main__':
	if len(sys.argv) > 1:
		app.run(host=sys.argv[1])
	else:
		app.run(host='0.0.0.0', debug=True) # for testing purposes