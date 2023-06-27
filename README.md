# KnowFIRES
A Knowledge-graph Framework for Interpreting Retrieved Entities from Search
# How to run

After cloning this repo, you need to download and extract the relevant metadata for the knowledge graph, was well as the indexed dbpedia from [here](https://drive.google.com/drive/folders/1uBGISKdQhHDEfG6ma6HpccSYD8LOiEak?usp=share_link). 

```
tar -xf dbpedia.tar.gz
tar -xf index.tar.gz
```

Further, you shall run the preprocessing scripts to prepare the meta data for all the entities in the knowledge graph as follows:
```
python backend/preprocessing.py
```
This step, might take a few minutes.

In case you do not want to do the preprocessing, download the processed indices and [necessary files from here](https://www.dropbox.com/s/nuenb83ixub6x6p/knowfires_data.tar.gz?dl=0) and extract them as follows : 
```
tar -xf knowfires_data.tar.gz
mv knowfires_data/* .
rm -r knowfires_data
```
After that, you can proceed to running the backend stage.
## Backend
First, extract the index and metadata files in the backend folder. Then, create and activate a virtual environment using
```bash
virtualenv venv
source venv/bin/activate
```
After that, install the requirements:
```bash
cd backend
pip install -r requirements.txt
```

Finally, the web app could be run:
```bash
python app.py
```

## Frontend
First, you should have node.js and npm installed. Then, install the packages:
```
npm install
```
For compiling and running the development server (with hot reload enabled), use:
```
npm run serve
```

For Compiling and minifying the code for production, run:
```
npm run build
```

For deployment on server:
```bash
npm install -g serve
serve -d dist
```
