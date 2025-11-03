import asyncio
import os

from dotenv import load_dotenv
from google.adk.runners import Runner

# Load keys
load_dotenv()
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)
from google.adk.agents import Agent
from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.sessions import InMemorySessionService
from google.genai import types


# Utility tool: simple logger to satisfy potential LLM tool calls
def log_message(message: str) -> dict:
    print(message)
    return {"type": "log", "message": message}

def summary(_: str) -> dict:
    # Minimal no-op to satisfy LLM function call "summary".
    return {"type": "summary", "status": "ok"}

# Init Nebius model
nebius_model = LiteLlm(
    model="openai/meta-llama/Meta-Llama-3.1-8B-Instruct",
    api_base=os.getenv("NEBIUS_API_BASE"),
    api_key=os.getenv("NEBIUS_API_KEY")
)

# Tool 1: Exa
def exa_search_ipl(_: str) -> dict:
    
    return {
        "type": "exa",
        "results": [
            {
                "title": "IPL 2025: Opening Week Highlights",
                "url": "https://example.com/ipl-2025-opening-week",
                "highlights": [
                    "Defending champions start strong with back-to-back wins",
                    "Two last-over thrillers cap a dramatic weekend"
                ],
                "text": "A roundup of the first week of IPL 2025 with standout performances and close finishes."
            },
            {
                "title": "Injury Update: Star All-Rounder Set to Miss Two Matches",
                "url": "https://example.com/ipl-2025-injury-update",
                "highlights": [
                    "Hamstring strain confirmed after scans",
                    "Team monitoring recovery ahead of key fixtures"
                ],
                "text": "Medical staff confirm a minor hamstring issue; return expected next week."
            }
        ]
    }

# Tool 2: Tavily
def tavily_search_hn(_: str) -> dict:
    return {
        "type": "tavily",
        "results": [
            {
                "title": "Show HN: Lightweight LLM Serving with Rust",
                "url": "https://news.ycombinator.com/item?id=40000001",
                "snippet": "A minimal, high-performance LLM server written in Rust with batching and streaming."
            },
            {
                "title": "Ask HN: Best practices for evaluating small context LLMs?",
                "url": "https://news.ycombinator.com/item?id=40000002",
                "snippet": "Discussion on evaluation methods and datasets for models with 8k context windows."
            }
        ]
    }

# Agents 1
exa_agent = Agent(
    name="ExaAgent",
    model=nebius_model,
    description="Fetches IPL 2025 news using Exa.",
    instruction="Use the exa_search_ipl tool to fetch the latest IPL 2025 news from April 2025.",
    tools=[exa_search_ipl, log_message],
    output_key="exa_news"
)

# Agents 2
tavily_agent = Agent(
    name="TavilyAgent",
    model=nebius_model,
    description="Fetches AI news from Hacker News using Tavily.",
    instruction="Use the tavily_search_hn tool to retrieve AI-related news from Hacker News posted in the last 24 hours.",
    tools=[tavily_search_hn, log_message],
    output_key="tavily_news"
)

exa_agent_skill = AgentSkill(
    id="exa_search_ipl",
    name="Exa Search IPL",
    description="Search IPL for news",
    examples=[
        "Search IPL for news",
    ],
    input_modes=[
        "text",
    ],
    output_modes=[
        "text",
    ],
    security=[
        {
            "tags": ["ai"],
        }
    ],
    tags=["ai"],
)

travily_agent_skill = AgentSkill(
    id="tavily_search_hn",
    name="Tavily Search Hacker News",
    description="Search Hacker News for AI-related news",
    examples=[
        "Search Hacker News for AI-related news",
    ],
    input_modes=[
        "text",
    ],
    output_modes=[
        "text",
    ],
    security=[
        {
            "tags": ["ai"],
        }
    ],
    tags=["ai"],
)

# class AgentCard(
#     *,
#     additional_interfaces: list[AgentInterface] | None = None,
#     capabilities: AgentCapabilities,
#     default_input_modes: list[str],
#     default_output_modes: list[str],
#     description: str,
#     documentation_url: str | None = None,
#     icon_url: str | None = None,
#     name: str,
#     preferred_transport: str | None = 'JSONRPC',
#     protocol_version: str | None = '0.3.0',
#     provider: AgentProvider | None = None,
#     security: list[dict[str, list[str]]] | None = None,
#  signatures: list[AgentCardSignature] | None = None,
#     skills: list[AgentSkill],
#     supports_authenticated_extended_card: bool | None = None,
#     url: str,
#     version: str


travily_agent_card = AgentCard(
    id="tavily_search_hn",
    name="Tavily Search Hacker News",
    description="Search Hacker News for AI-related news",
    skills=[travily_agent_skill],
    url="https://tavily.com",
    version="0.1.0",
    default_input_modes=['text'],
    default_output_modes=['text'],
    capabilities=AgentCapabilities(streaming=True),
)

# Agents 3
summary_agent = Agent(
    name="SummaryAgent",
    model=nebius_model,
    description="Summarizes Exa and Tavily results in a fun, structured format.",
    instruction="""
You are a summarizer. Create a clean and fun summary using info from:
- 'exa_news': IPL 2025 updates
- 'tavily_news': AI news from Hacker News

Show a clean, structured summary (can use tables or emojis 🏏🤖📢). Make it easy to scan and engaging.
""",
    tools=[log_message, summary],
    output_key="final_summary"
)
# Runner setup
APP_NAME = "agents"
USER_ID = "vscode_user"
SESSION_ID = "vscode_session"


# Agent chain
pipeline = SequentialAgent(
    name="NewsPipelineAgent",
    sub_agents=[exa_agent, tavily_agent, summary_agent]
)

session_service = InMemorySessionService()
# create_session is async in ADK; ensure it's awaited when running as a script
# asyncio.run(session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID))
session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)

runner = Runner(agent=pipeline, app_name=APP_NAME, session_service=session_service)

# Run the pipeline
def run_news_pipeline():
    content = types.Content(role="user", parts=[types.Part(text="Start the news roundup")])
    events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=content)
    for event in events:
        if event.is_final_response():
            print("\n📢 Final Summary:\n")
            print(event.content.parts[0].text)

if __name__ == "__main__":
    run_news_pipeline()


root_agent = pipeline