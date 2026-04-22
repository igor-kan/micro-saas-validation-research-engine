# micro-saas-validation-research-engine

Generate paid "idea validation" reports for micro-SaaS concepts.

## What it does
- Parse ideas CSV
- Score demand, competition, and execution complexity
- Generate report cards and priority recommendations

## Quick start
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.run --input examples/ideas.csv --output out
```
