# 📊 Data Analyst Agent

A data analyst AI agent built with the **Claude Agent SDK** that answers questions about CSV data using multi-step reasoning and tool use.

## What This Does

You give it a question like *"Which product had the highest sales?"* and it:
1. Reads the CSV file autonomously
2. Analyzes the relevant data
3. Shows its reasoning step by step
4. Gives a precise answer

## Project Structure

data-analyst-agent/

├── agent.py          # The agent (Claude Agent SDK)

├── eval.py           # Eval harness — 5 test cases with scoring

├── optimizer.py      # Tries 3 prompt variants, finds the best

├── data/sales.csv    # Sample sales dataset

└── results/          # JSON output from evals and optimizer





## How to Run

**1. Install dependencies**
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install claude-agent-sdk python-dotenv
```

**2. Set your API key**
```bash
echo "ANTHROPIC_API_KEY=your-key-here" > .env
```

**3. Run the agent**
```bash
python agent.py
```

**4. Run evals**
```bash
python eval.py
```

**5. Run optimizer**
```bash
python optimizer.py
```

## Eval Design

Each test case checks if specific keywords/numbers appear in the agent's response.
Score per test = keywords found / total keywords expected (0.0 to 1.0).

## Optimizer Results

The optimizer tested 3 system prompt variants:

| Variant | Score |
|---|---|
| baseline | 0.XX |
| step_by_step | 0.XX |
| calculation_focused | 0.XX |

**Best: [variant name]** — improved baseline by X%

*(Fill this in after running optimizer.py)*

## Tech Stack

- Python 3.10+
- Claude Agent SDK (`claude-agent-sdk`)
- Model: claude-haiku-4-5 (cost-efficient for eval loops)