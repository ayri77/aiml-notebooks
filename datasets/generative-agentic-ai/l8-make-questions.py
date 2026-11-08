"""Generate the Lecture 8 training data: student questions for every subsection of Lectures 1-6,
plus questions the notes do not answer. Run once with a key; prints a summary, writes l8-questions.jsonl.

    LLM_API_KEY=... python make_questions.py        (PowerShell: $env:LLM_API_KEY = "..."; python make_questions.py)
"""
import json, os, re, urllib.request
from openai import OpenAI

CORPUS_URL = "https://aiml-study-guides.onrender.com/corpus/generative-agentic-ai/lectures-01-06.en.jsonl"
MODEL = os.environ.get("LLM_MODEL", "gpt-4o-mini")
client = OpenAI(api_key=os.environ["LLM_API_KEY"], base_url=os.environ.get("LLM_BASE_URL"))

sections = [json.loads(l) for l in urllib.request.urlopen(CORPUS_URL).read().decode().splitlines() if l]
sections = [s for s in sections if s["heading"] and s["words"] >= 60]

PROMPT = """Below is a passage from a university course's study notes.
Write 4 different questions a student might ask that this passage answers.
Rules: one question per line; no numbering; 6-20 words each; vary the wording;
do not copy the heading; at least one question should paraphrase with no shared rare words.

Heading: {heading}
Passage:
{text}"""

def ask(prompt, temperature=0.7):
    r = client.chat.completions.create(model=MODEL, temperature=temperature,
                                       messages=[{"role": "user", "content": prompt}])
    return r.choices[0].message.content

rows = []
for i, s in enumerate(sections, 1):
    reply = ask(PROMPT.format(heading=s["heading"], text=s["text"][:3000]))
    qs = [re.sub(r"^\s*(?:[-•*]|\d+[.)])\s*", "", q).strip() for q in reply.splitlines()]
    for q in [q for q in qs if q.endswith("?")][:4]:
        rows.append({"question": q, "lecture": s["lecture"], "section": s["id"], "heading": s["heading"]})
    if i % 20 == 0:
        print(f"{i}/{len(sections)} sections, {len(rows)} questions")

OUT_OF_SCOPE = """Write 90 different questions a computer-science student might ask that are NOT about
generative AI, language models, prompting, LangChain, agents or diffusion models. Mix topics:
DevOps and Kubernetes, databases and SQL, web front-end, networking, operating systems, statistics,
classic algorithms, cloud billing, university administration, everyday life. One per line, no numbering."""
for q in ask(OUT_OF_SCOPE, temperature=0.9).splitlines():
    q = re.sub(r"^\s*(?:[-•*]|\d+[.)])\s*", "", q).strip()
    if q.endswith("?"):
        rows.append({"question": q, "lecture": 0, "section": "none", "heading": ""})

with open("l8-questions.jsonl", "w", encoding="utf-8") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
from collections import Counter
print(len(rows), "questions;", dict(sorted(Counter(r["lecture"] for r in rows).items())), "(0 = not in the notes)")
