import openai
import os

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_KEY

class LLM:
    def __init__(self):
        pass

    def generate(self, prompt: str, max_tokens: int = 300):
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # you can change to "gpt-4o-mini" or "gpt-4o" or "gpt-3.5-turbo"
            messages=[{"role":"system","content":"You are a helpful assistant."},
                      {"role":"user","content":prompt}],
            max_tokens=max_tokens,
            temperature=0.0,
        )
        return resp["choices"][0]["message"]["content"].strip()
