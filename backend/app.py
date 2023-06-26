import json
from pyserini.search import FaissSearcher
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from pyserini.search.lucene import LuceneSearcher

# loading the entities meta data and 1hop nodes
dic_metadata=json.load(open("meta_data_person_instance_categorty.json",'r'))
dic_links=json.load(open("mappingbased_objects_en.json",'r'))
# reading the index for sparse rerrievers 
searcher = LuceneSearcher('index') #
searchersimple = LuceneSearcher('index')
searcherprf = LuceneSearcher('index')
searcherprf.set_rm3()

searcherColBERT = FaissSearcher(
    'colbert',
    'castorini/tct_colbert-v2-hnp-msmarco'
)

searcherSBERT = FaissSearcher(
    'sbert',
    'sentence-transformers/msmarco-distilbert-base-v3'
)

    
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/search/<retriever>')
@cross_origin()
def search(retriever):  # put application's code here
    query = request.args.get("query", "")
    top_k = request.args.get("k", 10)
    top_k=int(top_k)
    if 'bm25' in retriever:
        searchersimple.set_bm25()
        searcherprf.set_bm25()
    elif 'ql' in retriever:
        searchersimple.set_qld()
        searcherprf.set_qld()
    elif 'ColBERT' in retriever:
        searcher = searcherColBERT
    elif 'SentenceBERT' in retriever:
        searcher = searcherSBERT
    
    if 'prf' in retriever:
        searcher=searcherprf
    elif 'bm25' in retriever or 'ql' in retriever:
        searcher=searchersimple

    out_dic={}
    out_dic['query'] = query
    out_dic['retrieved_results'] = {}
    print(query)
    hits = searcher.search(query,k=top_k)
    scores=[]
    for i in range(0, len(hits)):
        initial_name = hits[i].docid.replace('http://dbpedia.org/resource/','')
        out_dic['retrieved_results'][initial_name]={}
        out_dic['retrieved_results'][initial_name]['rank'] = f'{i+1:2}'
        out_dic['retrieved_results'][initial_name]['name']=initial_name.replace('_',' ')

        print(initial_name,out_dic['retrieved_results'][initial_name]['rank'] )
        out_dic['retrieved_results'][initial_name]['score'] = f'{hits[i].score:.5f}' 
        scores.append(float(out_dic['retrieved_results'][initial_name]['score'] ))
        if initial_name in dic_links:
            out_dic['retrieved_results'][initial_name]['links']=dic_links[initial_name]
        
        if f'{initial_name}' in dic_metadata:
            meta_data =  dic_metadata[f'{initial_name}']
            out_dic['retrieved_results'][initial_name]['meta_data'] = meta_data
            
    for item in out_dic['retrieved_results']:
        out_dic['retrieved_results'][item]['score']= 6 + \
            ( float(out_dic['retrieved_results'][item]['score']) - min(scores) ) / (max(scores) - min(scores)) * 12 
        
    print('----------')
    return out_dic


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
