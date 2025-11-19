import re

def clean_text(s: str) -> str:
    s = re.sub(r"\s+", " ", s)
    s = s.replace("\x0c", " ")
    return s.strip()
