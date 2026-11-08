# AI/ML Study Guides — notebooks

The companion notebooks of the [AI/ML Study Guides](https://aiml-study-guides.onrender.com/) site, published here so that they open in Google Colab. They are copied automatically from the site's repository; changes made here are overwritten.

Each notebook runs its lecture's steps in order. Steps marked 💳 API call a paid model and need an API key; in Colab, add it under **Secrets** (the key icon on the left) as `LLM_API_KEY` and run this cell first:

```python
import os
from google.colab import userdata

os.environ["LLM_API_KEY"] = userdata.get("LLM_API_KEY")
```

How to run the code, with costs and key safety: [Start here → How to run the code](https://aiml-study-guides.onrender.com/en/generative-agentic-ai/start-here/03-run-the-code/).

## Generative and Agentic AI

| Notebook | Open |
| --- | --- |
| `lecture-01-fable-foundations.ipynb` | [Open in Colab](https://colab.research.google.com/github/ayri77/aiml-notebooks/blob/main/notebooks/generative-agentic-ai/lecture-01-fable-foundations.ipynb) |
| `lecture-02-fable-training-and-cost.ipynb` | [Open in Colab](https://colab.research.google.com/github/ayri77/aiml-notebooks/blob/main/notebooks/generative-agentic-ai/lecture-02-fable-training-and-cost.ipynb) |
| `lecture-03-fable-choosing-the-model.ipynb` | [Open in Colab](https://colab.research.google.com/github/ayri77/aiml-notebooks/blob/main/notebooks/generative-agentic-ai/lecture-03-fable-choosing-the-model.ipynb) |
| `lecture-04-fable-context-engineering.ipynb` | [Open in Colab](https://colab.research.google.com/github/ayri77/aiml-notebooks/blob/main/notebooks/generative-agentic-ai/lecture-04-fable-context-engineering.ipynb) |
| `lecture-05-fable-langchain.ipynb` | [Open in Colab](https://colab.research.google.com/github/ayri77/aiml-notebooks/blob/main/notebooks/generative-agentic-ai/lecture-05-fable-langchain.ipynb) |
| `lecture-05-langchain.ipynb` | [Open in Colab](https://colab.research.google.com/github/ayri77/aiml-notebooks/blob/main/notebooks/generative-agentic-ai/lecture-05-langchain.ipynb) |
| `lecture-06-agents.ipynb` | [Open in Colab](https://colab.research.google.com/github/ayri77/aiml-notebooks/blob/main/notebooks/generative-agentic-ai/lecture-06-agents.ipynb) |
| `lecture-06-fable-agents.ipynb` | [Open in Colab](https://colab.research.google.com/github/ayri77/aiml-notebooks/blob/main/notebooks/generative-agentic-ai/lecture-06-fable-agents.ipynb) |
| `lecture-07-fable-rag.ipynb` | [Open in Colab](https://colab.research.google.com/github/ayri77/aiml-notebooks/blob/main/notebooks/generative-agentic-ai/lecture-07-fable-rag.ipynb) |
| `lecture-08-fable-fine-tuning.ipynb` | [Open in Colab](https://colab.research.google.com/github/ayri77/aiml-notebooks/blob/main/notebooks/generative-agentic-ai/lecture-08-fable-fine-tuning.ipynb) |
| `lecture-09-agent-evaluation.ipynb` | [Open in Colab](https://colab.research.google.com/github/ayri77/aiml-notebooks/blob/main/notebooks/generative-agentic-ai/lecture-09-agent-evaluation.ipynb) |
| `lecture-09-fable-agent-systems.ipynb` | [Open in Colab](https://colab.research.google.com/github/ayri77/aiml-notebooks/blob/main/notebooks/generative-agentic-ai/lecture-09-fable-agent-systems.ipynb) |
| `lecture-10-fable-multi-agent.ipynb` | [Open in Colab](https://colab.research.google.com/github/ayri77/aiml-notebooks/blob/main/notebooks/generative-agentic-ai/lecture-10-fable-multi-agent.ipynb) |
| `lecture-10-multi-agent.ipynb` | [Open in Colab](https://colab.research.google.com/github/ayri77/aiml-notebooks/blob/main/notebooks/generative-agentic-ai/lecture-10-multi-agent.ipynb) |
| `lecture-11-fable-mcp-a2a.ipynb` | [Open in Colab](https://colab.research.google.com/github/ayri77/aiml-notebooks/blob/main/notebooks/generative-agentic-ai/lecture-11-fable-mcp-a2a.ipynb) |
| `lecture-12-fable-progress-safety-regulation.ipynb` | [Open in Colab](https://colab.research.google.com/github/ayri77/aiml-notebooks/blob/main/notebooks/generative-agentic-ai/lecture-12-fable-progress-safety-regulation.ipynb) |

The datasets the notebooks read are in [`datasets/`](datasets/); the notebooks download them from the site, so they also run without this folder.
