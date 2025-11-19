Setup
1.	Clone / create project folder.
2.	Create & activate a virtualenv:
o	macOS/Linux:
o	python3 -m venv venv
o	source venv/bin/activate
o	Windows:
o	python -m venv venv
o	venv\Scripts\activate
3.	Install deps:
4.	pip install -r requirements.txt
5.	Set your OpenAI key:
o	macOS/Linux:
o	export OPENAI_API_KEY="sk-..."
o	Windows (PowerShell):
o	$env:OPENAI_API_KEY="sk-..."
6.	Run FastAPI:
7.	uvicorn app.main:app --reload --port 8001
Usage
•	Upload a PDF:
•	POST http://127.0.0.1:8001/api/upload
•	Body: form-data file: yourfile.pdf
•	Query:
•	POST http://127.0.0.1:8001/api/query
•	JSON:
•	{"question":"What is the refund policy?","top_k":4}
Notes & Testing
•	After first upload, vector_store/index.faiss and vector_store/meta.pkl are created.
•	If embeddings fail due to model or key, check OPENAI_API_KEY and quota.
•	For large PDFs you may want to tune chunk_size and overlap.

