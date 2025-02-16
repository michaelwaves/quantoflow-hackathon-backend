from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools

# Define the function to search for images of the person
def search_adverse_media_images(person_name):
    # Create the agent with a description and tool for DuckDuckGo search
    agent = Agent(
        model=OpenAIChat(id="gpt-4o"),
        description=(
            "You are an investigator tasked with finding images related to a person and analyzing those images "
            "to check how many unique people appear. Use DuckDuckGo image search results to gather relevant images."
        ),
        tools=[DuckDuckGoTools()],
        show_tool_calls=True,
        markdown=True
    )
    
    # Create a search query that focuses on finding images of the person
    search_query = f"images of {person_name}"

    # Use the agent to search for images of the person on DuckDuckGo
    agent.print_response(search_query, stream=True)

# Prompt the user to input the name of the person they want to search for
person_name = input("Enter the name of the person you want to find images for: ")

# Run the search function for the person's images
search_adverse_media_images(person_name)
