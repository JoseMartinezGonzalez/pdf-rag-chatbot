from fastapi import APIRouter
from pydantic import BaseModel
from app.services.retriever import Retriever
from app.services.llm import LLM

router = APIRouter()

retriever = Retriever()
llm = LLM()

class QueryIn(BaseModel):
    question: str
    top_k: int = 4

@router.post("/query")
async def query(q: QueryIn):
    docs = retriever.retrieve(q.question, top_k=q.top_k)
    context = "\n\n---\n\n".join([f"Source: {d['source']}\n\n{d['text']}" for d in docs])
    prompt = f"""You are a helpful assistant. Use the following context to answer the question. If the answer is not in the context, say you don't know.

Context:
{context}

Question:
{q.question}
"""
    answer = llm.generate(prompt)
    return {"answer": answer, "sources": [d["source"] for d in docs]}
