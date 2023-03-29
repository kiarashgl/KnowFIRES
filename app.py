import json

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/search/<retriever>')
@cross_origin()
def search(retriever):  # put application's code here
    query = request.args.get("query", "")
    top_k = request.args.get("k", 10)
    print(retriever)
    return retriever_result

retriever_file = 'response.json'
with open(retriever_file, 'r') as file:
    retriever_result = json.load(file)
if __name__ == '__main__':
    app.run()
