
import os
from dotenv import load_dotenv

from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

# Load API keys and other settings from .env
load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY is missing from .env")

model = os.getenv("MODEL")

if not os.getenv("SERPER_API_KEY"):
    raise ValueError("SERPER_API_KEY is missing from .env")

# --------------------------------------------------
# STEP 1: Create the search tool
# --------------------------------------------------

search = SerperDevTool()

# --------------------------------------------------
# STEP 2: Define the Researcher agent
# --------------------------------------------------

researcher = Agent(
    role="Technology News Researcher",
    goal=(
        "Find the three most important and recent "
        "technology news stories for today's newsletter."
    ),
    backstory=(
        "You are a technology news researcher. You use web search to verify recent developments, prefer reliable sources, and distinguish new reports from older stories."
    ),
    tools=[search],
    model=model or None,
    verbose=True
)

# --------------------------------------------------
# STEP 3: Define the Writer agent
# --------------------------------------------------

writer = Agent(
    role="Technology Newsletter Writer",
    goal=(
        "Turn the research into a concise, accurate "
        "newsletter containing exactly five lines."
    ),
    backstory=(
        "You are a professional newsletter writer. "
        "You rely exclusively on the research provided to you. "
        "You do not conduct additional research or invent facts."
    ),
    model=model or None,
    verbose=True
)

# Notice: The Writer has NO tools.

# --------------------------------------------------
# STEP 4: Create the Research task
# --------------------------------------------------

find = Task(
    description=(
        "Research today's top 3 technology news stories. "
        "Search the web for recent developments and prioritize "
        "stories published today. If fewer than three relevant "
        "stories were published today, use the most recent "
        "credible reports and state their dates. "
        "Prefer reliable sources and verify publication dates "
        "where possible. Avoid duplicate stories.\n\n"
        "For each story, provide:\n"
        "1. Headline\n"
        "2. Publisher and publication date, if available\n"
        "3. A factual summary of 1-2 sentences\n"
        "4. Source URL\n\n"
        "Return exactly three numbered stories in a clean, "
        "structured format. Do not write the newsletter."
    ),
    expected_output=(
        "Three numbered technology news stories. Each story "
        "contains a headline, publisher, publication date "
        "where available, a concise factual summary, and "
        "a source URL. Clearly identify any date that could "
        "not be verified. The output must be organized and "
        "ready for a newsletter writer to use."
    ),
    agent=researcher
)

# --------------------------------------------------
# STEP 5: Create the Writing task
# --------------------------------------------------

write = Task(
    description=(
        "Using only the Researcher's task output, write a "
        "technology newsletter in exactly FIVE lines:\n"
        "Line 1: Newsletter headline.\n"
        "Lines 2-4: One concise bullet for each of the "
        "three researched news stories.\n"
        "Line 5: One sentence explaining why these "
        "developments matter overall.\n\n"
        "Do not perform new searches. Do not invent facts, "
        "dates, or claims. Keep each line concise. "
        "Do not add an introduction, conclusion, or extra lines."
    ),
    expected_output=(
        "Exactly five non-empty lines: one headline, three "
        "news bullets based on the research, and one final "
        "'Why it matters:' sentence. No additional lines."
    ),
    agent=writer,
    context=[find]
)

# --------------------------------------------------
# STEP 6: Assemble the sequential crew
# --------------------------------------------------

crew = Crew(
    agents=[researcher, writer],
    tasks=[find, write],
    process=Process.sequential,
    verbose=True
)

# --------------------------------------------------
# STEP 7: Run the crew
# --------------------------------------------------

result = crew.kickoff()

print("\n" + "=" * 45)
print("TECH NEWSLETTER")
print("=" * 45)
print(result)
