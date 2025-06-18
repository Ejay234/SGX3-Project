from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello, world!\n'

@app.route('/<name>/<number>', methods=['GET'])
def hello_name(name):
    return f'Hello, {name}!\n'

@app.route('/hello', methods=['GET'])
def hello():
    name = request.args.get('name')
    number = request.args.get('favnum')
    return f'Hello, {name}!\n I see that your favorite number is {number}?\n'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='8041')
