from fastapi import APIRouter
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools

# Define the FastAPI router for media search
media_search_router = APIRouter(tags=["Media Search"])

@media_search_router.get("/search_adverse_media")
def search_adverse_media(person_name: str):
    """
    Search for adverse media coverage of a person or entity.
    This will look for negative or harmful news articles, reports, or stories.
    """
    
    # Modify the agent's description and search to focus on adverse media
    agent = Agent(
        model=OpenAIChat(id="gpt-4o"),
        description=(
            "You are a highly skilled investigator with expertise in finding adverse media coverage. "
            "Your task is to search for any negative or harmful news articles, reports, or stories related to the person. "
            "Use a reliable search tool like DuckDuckGo and return relevant details that highlight any potential risk or harm associated with this individual."
        ),
        tools=[DuckDuckGoTools()],
        show_tool_calls=True,
        markdown=True
    )
    
    # Create a search query that focuses on finding negative media coverage
    search_query = f"adverse media on {person_name} OR 'controversy' OR 'scandal' OR 'legal issues' OR 'criminal' OR 'fraud'"
    
    # Use the agent to search for adverse media related to the person
    agent.print_response(search_query, stream=True)
    
    return {"message": f"Searching for adverse media on {person_name}"}
