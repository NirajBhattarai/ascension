import uvicorn

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill

from travily_executor import TravilyExecutor


def main():
    """Starts the Currency Agent server."""

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

    travily_agent_card = AgentCard(
        id="tavily_search_hn",
        name="Tavily Search Hacker News",
        description="Search Hacker News for AI-related news",
        skills=[travily_agent_skill],
        url="http://localhost:9999/",
        version="0.1.0",
        default_input_modes=["text"],
        default_output_modes=["text"],
        capabilities=AgentCapabilities(streaming=True),
    )

    request_handler = DefaultRequestHandler(
        agent_executor=TravilyExecutor(),
        task_store=InMemoryTaskStore(),
    )
    travily_server = A2AStarletteApplication(
        agent_card=travily_agent_card,
        http_handler=request_handler,
        extended_agent_card=travily_agent_card,
    )

    uvicorn.run(travily_server.build(), host='0.0.0.0', port=9999)


if __name__ == "__main__":
    main()