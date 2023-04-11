# KnowFIRES

# How to run

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
Then, run the preprocessing script:
```bash
python preprocessing.py
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
