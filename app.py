import json

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from pyserini.search.lucene import LuceneSearcher
import argparse
import json
dic_metadata=json.load(open("meta_data_person_instance_categorty.json",'r'))
dic_links=json.load(open("mappingbased_objects_en.json",'r'))
searcher = LuceneSearcher('index')


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/search/<retriever>')
@cross_origin()
def search(retriever):  # put application's code here
    query = request.args.get("query", "")
    top_k = request.args.get("k", 10)

    
    if 'bm25' in retriever:
        searcher.set_bm25()
    elif 'ql' in retriever:
        searcher.set_qld()
    
    if 'prf' in retriever:
        searcher.set_rm3()

    out_dic={}
    out_dic['query'] = query
    out_dic['retrieved_results'] = {}
    
    hits = searcher.search(query,k=top_k)
    for i in range(0, len(hits)):
        initial_name = hits[i].docid
        out_dic['retrieved_results'][initial_name]={}
        out_dic['retrieved_results'][initial_name]['rank'] = f'{i+1:2}'
        out_dic['retrieved_results'][initial_name]['score'] = f'{hits[i].score:.5f}' 
        if initial_name in dic_links:
            out_dic['retrieved_results'][initial_name]['links']=dic_links[initial_name]
        
        if f'{initial_name}' in dic_metadata:
            meta_data =  dic_metadata[f'{initial_name}']
        
        if args.meta_data :
            out_dic['retrieved_results'][initial_name]['meta_data'] = meta_data

    return out_dic


retriever_file = 'response.json'
with open(retriever_file, 'r') as file:
    retriever_result = json.load(file)
if __name__ == '__main__':
    app.run()
