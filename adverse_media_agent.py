from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools

# Define the function to search for adverse media coverage of a person
def search_adverse_media(person_name):
    # Modify the agent's description and search to focus on adverse media.
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

# Prompt the user to input the name of the person they want to search for
person_name = input("Enter the name of the person or business you want to find adverse media for: ")

# Run the search function for adverse media coverage
search_adverse_media(person_name)
