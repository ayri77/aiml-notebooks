"""Build l12-assistant-trace.jsonl from Lecture 11's recorded run (Step 13:
the assistant through MCP on Lecture 10's 60 team requests, gpt-6-luna,
2026-11-07): for each request, its id, kind and the tools the model
called, in order. No model; the input is the run's via-mcp.json."""
import json, sys
rows = json.load(open(sys.argv[1], encoding="utf-8"))
with open("l12-assistant-trace.jsonl", "w", encoding="utf-8") as out:
    for r in rows:
        out.write(json.dumps({"id": r["id"], "kind": r["kind"],
                              "tools": r["tools"]}) + "\n")
print("wrote", len(rows), "requests")
