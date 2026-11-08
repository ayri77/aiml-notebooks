"""Build l10-requests.jsonl: the labelled requests of Lecture 10 (Fable).
No model is called; the result is deterministic.

    python l10-make-requests.py FOLDER

FOLDER holds l8-questions.jsonl and lectures-01-06.en.jsonl (both on this
site); l10-requests.jsonl is written there.

set "tools": 84 requests, 12 per core tool, label = the tool that should be
             called first (Step 2).
set "team":  60 requests — 20 notes questions, 20 to-do actions, 20 mixed
             (Step 10). Notes questions come from Lecture 8's validation
             split, answerable, and only those whose gold section is in the
             top 3 of the TF-IDF retriever for the question itself and is a
             numbered subsection (N.M), so a
             failure is the design's, not retrieval's.
"""
import json, random, pathlib, re, sys
from sklearn.feature_extraction.text import TfidfVectorizer

run = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "run")
rows = [json.loads(l) for l in open(run / "l8-questions.jsonl")]
notes = [n for n in map(json.loads, open(run / "lectures-01-06.en.jsonl"))
         if n["heading"]]
for i, r in enumerate(rows):
    r["family"] = r["section"] if r["lecture"] else f"none-{i}"
random.seed(0)
families = sorted({r["family"] for r in rows}); random.shuffle(families)
fifth = len(families) // 5
test_f, val_f = set(families[:fifth]), set(families[fifth:2 * fifth])
val = [r for r in rows if r["family"] in val_f]
vec = TfidfVectorizer(stop_words="english").fit([n["text"] for n in notes])
doc_m = vec.transform([n["text"] for n in notes])
def retrieve(q, k=3):
    s = (doc_m @ vec.transform([q]).T).toarray().ravel()
    return [notes[i] for i in s.argsort()[::-1][:k]]
easy = [q for q in val if q["lecture"]
        and re.match(r"\d+\.\d+ ", q["heading"])
        and q["section"] in [n["id"] for n in retrieve(q["question"])]]
print(len(val), "validation questions;", len(easy), "with gold in top 3")
picked = random.Random(10).sample(easy, 40)

TOOLS = {
 "search_notes": [
  "What do the course notes say about few-shot prompting?",
  "Find the part of the course notes that explains the KV cache.",
  "Quote the course notes' definition of perplexity.",
  "Summarise what the lectures teach about temperature and top-p.",
  "Look up how the course explains quantization to int8.",
  "What does the course material say a checkpoint is in LangGraph?",
  "Show me the course's explanation of prompt injection.",
  "According to the course notes, what is a scaling law?",
  "Search the lecture notes for structured output with Pydantic.",
  "I need the section of the course notes on ReAct, with its link.",
  "What do the lectures say about distillation versus pruning?",
  "Give me the course's explanation of message roles.",
 ],
 "route_question": [
  "Which lecture should I read for questions about attention?",
  "My question is about tool schemas. Which lecture covers that?",
  "Which lecture answers this: how does sampling with top-p work?",
  "Route this question to the right lecture: what is a reducer "
  "in LangGraph?",
  "In which lecture would I find RLHF and DPO?",
  "Which lecture is this question from: why does a model need a "
  "context budget?",
  "Tell me the number of the lecture that covers embeddings.",
  "Which of the lectures deals with consent before an agent acts?",
  "I'm confused about mixture of experts. Which lecture do I go back to?",
  "Classify this question by lecture: how do I trace a LangChain run?",
  "Which lecture is about choosing a model on your own workload?",
  "What lecture covers chain-of-thought prompting?",
 ],
 "days_until": [
  "How many days until 2026-12-01?",
  "How long do I have until my exam on 15 December? In days, please.",
  "Days left before my thesis proposal is due on 2027-01-10?",
  "Count the days from today to 24 November.",
  "How many days remain until the 20th of this month?",
  "Is a deadline on 2026-11-30 more than three weeks away?",
  "How many days until Christmas Eve?",
  "My project is due on 2026-11-12. How many days is that from now?",
  "How many days until the course ends on 2027-02-28?",
  "How many days are left before 1 March 2027?",
  "Number of days from today until my presentation on 2026-11-19?",
  "How many days do I still have until the end of November?",
 ],
 "add_task": [
  "Add 'read Lecture 7' to my to-do list.",
  "Put 'revise attention' on my list.",
  "New task: finish the LoRA exercise.",
  "I must email the study group. Add it to my to-do list, "
  "don't send anything.",
  "Add a to-do: rewatch the RAG lecture.",
  "I need to buy a new notebook, add that to my tasks.",
  "Can you add 'prepare questions for the mentor' to my to-dos?",
  "Make a task out of this: install langgraph.",
  "Add two tasks: practise SQL, and read the DPO paper.",
  "Make a task to submit homework 4.",
  "Please create a to-do item 'review the glossary of Lecture 5'.",
  "Add 'check the quiz results' to the list.",
 ],
 "list_tasks": [
  "What's on my to-do list?",
  "Show my tasks.",
  "Which tasks are still open?",
  "List everything I still have to do.",
  "Do I have any tasks about Lecture 7?",
  "Read my to-do list back to me.",
  "How many open tasks do I have?",
  "What did I put on my to-do list earlier?",
  "Give me the ids of my tasks.",
  "Is 'revise attention' still on my to-do list?",
  "Show me my to-dos so I can pick one.",
  "What's left on my task list?",
 ],
 "delete_task": [
  "Delete task 3.",
  "Remove task 2 from my list.",
  "Task 1 is no longer needed; delete it.",
  "Take 'buy bread' (id 4) off my to-do list.",
  "Get rid of task 5.",
  "Delete the task with id 2, I added it by mistake.",
  "Please remove to-do 6, it was a duplicate.",
  "Drop task 3 from the list.",
  "Erase task 1.",
  "I don't need to do task 4 any more, delete it.",
  "Delete my task number 7.",
  "Remove the task with id 5 completely.",
 ],
 "send_reminder": [
  "Email me a reminder tomorrow at 9:00 to submit the homework.",
  "Email me a reminder on Monday at 18:00 about the quiz.",
  "Send a reminder to my email at 20:00 today: revise attention.",
  "Set an email reminder for 2026-11-10 08:30: thesis meeting.",
  "Can you remind me by email on Friday at noon to book the exam?",
  "Remind me in my inbox tomorrow at 7:30 to read Lecture 8.",
  "I want an email reminder on 2026-11-20 at 10:00 about the "
  "presentation.",
  "Remind me by email at 17:00 to call the study group.",
  "Send a reminder to my email for Saturday 11:00: laundry before "
  "the trip.",
  "Please email me next Wednesday at 9:00 to check the grades.",
  "Drop me a reminder email at 21:00 to back up my notebook.",
  "Remind me by email on 1 December at 08:00 that the project starts.",
 ],
}

T = "2026-11-05"
TODO = [  # request, expected changes
 ("Add 'read Lecture 7' to my list.", {"add": [["lecture 7"]]}),
 ("Put 'practise SQL joins' on my to-do list.", {"add": [["sql"]]}),
 ("Delete the bread task.", {"delete": ["t3"]}),
 ("I finished revising attention, take it off my list.",
  {"delete": ["t2"]}),
 ("What's on my to-do list?",
  {"say": ["homework", "attention", "bread", "dpo"]}),
 ("Remind me by email tomorrow at 9:00 to submit the homework.",
  {"remind": ["2026-11-06 09:00"]}),
 ("Email me a reminder on Monday at 18:00 about the quiz.",
  {"remind": ["2026-11-09 18:00"]}),
 ("How many days do I have until my exam on 15 December?",
  {"say": ["40"]}),
 ("Add two tasks: rewatch the RAG lecture, and prepare questions for "
  "the mentor.", {"add": [["rag"], ["mentor"]]}),
 ("Remove the DPO paper from my list and add 'read the LoRA paper' "
  "instead.", {"delete": ["t4"], "add": [["lora"]]}),
 ("Send me an email reminder on 2026-11-20 at 10:00 about the "
  "presentation.", {"remind": ["2026-11-20 10:00"]}),
 ("Delete the homework task and the bread task.",
  {"delete": ["t1", "t3"]}),
 ("Add 'book the exam' and email me a reminder on Friday at 12:00 to "
  "do it.", {"add": [["exam"]], "remind": ["2026-11-06 12:00"]}),
 ("How many days are left until 1 December?", {"say": ["26"]}),
 ("My thesis proposal is due on 2027-01-10. How many days is that from "
  "today?", {"say": ["66"]}),
 ("Remind me by email in two days at 8:30 to revise attention.",
  {"remind": ["2026-11-07 08:30"]}),
 ("Add 'install langgraph' to my tasks, then show me the whole list.",
  {"add": [["langgraph"]],
   "say": ["homework", "attention", "bread", "dpo", "langgraph"]}),
 ("Send a reminder to my inbox tonight at 21:00: back up the notebook.",
  {"remind": ["2026-11-05 21:00"]}),
 ("Add 'email the study group' to my list.",
  {"add": [["study group"]]}),
 ("Which of my tasks is about a paper? Delete it.", {"delete": ["t4"]}),
]
ACTIONS = [  # the to-do half of a mixed request
 ("Also add 'read Lecture 7' to my list.", {"add": [["lecture 7"]]}),
 ("Also email me a reminder tomorrow at 9:00 to submit the homework.",
  {"remind": ["2026-11-06 09:00"]}),
 ("Also delete the bread task.", {"delete": ["t3"]}),
 ("And put 'practise SQL joins' on my to-do list.", {"add": [["sql"]]}),
 ("And how many days do I have until 15 December?", {"say": ["40"]}),
]

out = []
for tool, reqs in TOOLS.items():
    assert len(reqs) == 12, tool
    # delete_task's description says to look the id up first, so a
    # first call to list_tasks is also right for those requests
    also = ["list_tasks"] if tool == "delete_task" else []
    out += [{"set": "tools", "id": f"tool-{tool}-{i:02d}", "request": r,
             "tool": tool, "also": also} for i, r in enumerate(reqs, 1)]
for i, q in enumerate(picked[:20], 1):
    out.append({"set": "team", "kind": "notes", "id": f"notes-{i:02d}",
                "request": q["question"], "lecture": q["lecture"],
                "section": q["section"], "heading": q["heading"],
                "expect": {}})
for i, (r, e) in enumerate(TODO, 1):
    out.append({"set": "team", "kind": "todo", "id": f"todo-{i:02d}",
                "request": r, "expect": e})
for i, q in enumerate(picked[20:], 1):
    action, e = ACTIONS[(i - 1) % len(ACTIONS)]
    out.append({"set": "team", "kind": "mixed", "id": f"mixed-{i:02d}",
                "request": f"{q['question']} {action}",
                "lecture": q["lecture"], "section": q["section"],
                "heading": q["heading"], "expect": e})
path = run / "l10-requests.jsonl"
path.write_text("".join(json.dumps(o, ensure_ascii=False) + "\n"
                        for o in out), encoding="utf-8")
print(len(out), "requests written to", path)
