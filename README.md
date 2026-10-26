# CrewAI Tech News Newsletter

This project demonstrates a sequential CrewAI crew with two agents:

- **Researcher**: searches the web with `SerperDevTool` and finds the top three current technology news stories.
- **Writer**: receives the Researcher's output and turns it into a five-line newsletter. The Writer has no search tools.

## Requirements

- Python 3.10+
- An OpenAI API key
- A Serper API key from [serper.dev](https://serper.dev/)

## Setup

Create and activate a virtual environment if needed:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
pip install -r requirements.txt
```

Create a `.env` file in the project directory:

```env
OPENAI_API_KEY=your-openai-api-key
SERPER_API_KEY=your-serper-api-key
MODEL=your-model-name
```

Do not commit `.env` or expose either API key.

## Run

```powershell
python news_crew.py
```

The crew runs sequentially:

1. The Researcher searches for three recent technology stories.
2. The Researcher returns structured headlines, dates, summaries, and URLs.
3. The Writer receives that output through `context=[find]`.
4. The Writer produces exactly five lines: a headline, three story bullets, and a `Why it matters:` line.

## Important design choice

The Writer does not automatically receive the previous task's output in a sequential crew. The explicit `context=[find]` on the writing task passes the Researcher's result to the Writer.

