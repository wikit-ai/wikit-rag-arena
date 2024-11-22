# Chatbot Arena for KG RAG pipelines

This project is a Web user interface to evaluate KG-RAG pipelines designed for Marion Schaeffer's PhD at Wikit.

This UI is powered by Streamlit and MongoDB.

## Project setup

```sh
cd wikit-kg-rag-arena
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Then create the file for Streamlit secrets (`.streamlit/secrets.toml`):

```ini
[mongo]
uri = "mongodb+srv://xxx:xxx@xxx/?retryWrites=true&w=majority"
db_name = "xxx"
collection_name = "QueryExecutions"

[eval]
eval_count_target = 2
```

## Linter

```sh
black src/*.py 
```

## Project start

```sh
streamlit run src/app.py
```
