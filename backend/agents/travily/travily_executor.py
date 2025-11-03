from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
import os

from google.genai import types

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

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

    # Utility tool: simple logger to satisfy potential LLM tool calls
def log_message(message: str) -> dict:
    print(message)
    return {"type": "log", "message": message}

nebius_model = LiteLlm(
    model="openai/meta-llama/Meta-Llama-3.1-8B-Instruct",
    api_base=os.getenv("NEBIUS_API_BASE"),
    api_key=os.getenv("NEBIUS_API_KEY")
)

travily_agent = Agent(
    name="TavilyAgent",
    model=nebius_model,
    description="Fetches AI news from Hacker News using Tavily.",
    instruction="Use the tavily_search_hn tool to retrieve AI-related news from Hacker News posted in the last 24 hours.",
    tools=[tavily_search_hn, log_message],
    output_key="tavily_news"
)

# Initialize session and runner
session_service = InMemorySessionService()
runner = Runner(
    agent=travily_agent,
    app_name="tavily_app",
    session_service=session_service
)
    

# --8<-- [start:HelloWorldAgent]
class HelloWorldAgent:
    """Hello World Agent."""

    async def invoke(self) -> str:
        return 'Travily Agent is running'

class TravilyExecutor(AgentExecutor):
    """Test AgentProxy Implementation."""

    def __init__(self):
        self.agent = travily_agent

    # --8<-- [end:HelloWorldAgentExecutor_init]
    # --8<-- [start:HelloWorldAgentExecutor_execute]
    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        # Create a session
        session = await session_service.create_session(
            app_name="tavily_app",
            user_id="user_1"
        )
        
        # Create a user message
        user_message = types.Content(
            role="user",
            parts=[types.Part(text="Find me AI news from Hacker News")]
        )
        
        # Run the agent using Runner
        async for event in runner.run_async(
            user_id="user_1",
            session_id=session.id,
            new_message=user_message
        ):
            if event.is_final_response():
                # Extract the response text
                response_text = event.content.parts[0].text
                # Enqueue the response as an A2A event
                await event_queue.enqueue_event(
                    new_agent_text_message(response_text)
                )


    async def cancel(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        raise Exception('cancel not supported')
