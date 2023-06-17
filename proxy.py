from flask import Flask, request, Response
import requests
from flask_cors import CORS, cross_origin

backend_server = "http://129.97.186.146:5000/"
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/", defaults={"path": ""})
@app.route('/<path:path>')
@cross_origin()
def search(path):
    res = requests.get(backend_server + request.path, params=request.args)
    response = Response(res.content, res.status_code)
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
