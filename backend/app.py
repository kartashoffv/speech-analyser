from flask import Flask

app = Flask(__name__)


@app.route('/test')
def test_api():
    return {'result': 'OK'}
