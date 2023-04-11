import collections, json

person_data_file=open('dbpedia/persondata_en.ttl','r').readlines()

outdic=collections.defaultdict(dict)
for line in person_data_file:
    if '/ontology/' not in line:
        continue
    entity,predicate,value,_=line.split('>')
    if 'dbpedia' not in value:
        continue
    entity=entity.replace('<','').replace('http://dbpedia.org/resource/', '')
    predicate = predicate.replace('>','').replace(' <http://dbpedia.org/ontology/','')
    if entity not in outdic:
        outdic[entity]=collections.defaultdict(dict)
    outdic[entity]['person_data'][predicate]= value.replace('<http:','http').replace('^^','').replace('"','').replace('http://dbpedia.org/resource/', '').replace('http//dbpedia.org/resource/', '').strip()

print('person done')
    
article_category_file=open('dbpedia/article_categories_en.ttl','r').readlines()
for line in article_category_file:
    try:
        entity,predicate,value,_=line.split('>')
    except:
        print(line)
        continue
    entity=entity.replace('<','').replace('http://dbpedia.org/resource/', '')
    value=value.split('Category:')[-1]  
    if entity not in outdic or 'subject' not in outdic[entity]:
        outdic[entity]['subject']=[]
    outdic[entity]['subject'].append(value.replace('http://dbpedia.org/resource/', ''))
    
print('category done')
instance_type_file=open('dbpedia/instance_types_en.ttl','r').readlines()
for line in instance_type_file:
    try:
        entity,predicate,value,_=line.split('>')
    except:
        print(line)
        continue
    
    entity=entity.replace('<','').replace('http://dbpedia.org/resource/', '')
    if 'dbpedia' not in value:
        continue
    
    value=value.split('/')[-1].split('>')[0]  
    
    if entity not in outdic or 'type' not in outdic[entity]:
        outdic[entity]['type']=[]
    outdic[entity]['type'].append(value)

print('instance done')

image_file=open('dbpedia/images_en.ttl','r').readlines()
for line in image_file:
    try:
        entity,predicate,value,_=line.split('>')
    except:
        print(line)
        continue
    
    if 'thumbnail' not in predicate:
        continue
    
    entity=entity.replace('<','').replace('http://dbpedia.org/resource/', '')
    value=value.replace('<','').replace('http://dbpedia.org/resource/', '')
    outdic[entity]['image']=value
    
print('images done')

with open("meta_data_person_instance_categorty.json", "w") as write_file:
    json.dump(outdic, write_file, indent=4)
    
import collections, json

person_data_file=open('dbpedia/mappingbased_objects_en.ttl','r').readlines()
dic=collections.defaultdict(list)
for line in person_data_file:
    try:
        entity,predicate,value,_=line.split('>')
    except:
        print(line)
        continue
    if 'dbpedia.org' not in predicate:
        continue
    
    entity=entity.replace( '<','').replace('"','').replace('http://dbpedia.org/resource/', '')
    value=value.split('<')[1].replace('"','')
    predicate = predicate.split('/')[-1]
    dic[entity].append({'p':predicate ,'v':value.replace('http://dbpedia.org/resource/', '')})
    
print(len(dic))

with open("mappingbased_objects_en.json", "w") as write_file:
    json.dump(dic, write_file, indent=4)
    
