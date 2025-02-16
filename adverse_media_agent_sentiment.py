from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from textblob import TextBlob  # For sentiment analysis

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
    search_results = agent.print_response(search_query, stream=True)
    
    # Check if the search results are None before iterating
    if search_results is None:
        print("No results found or there was an issue with the search.")
        return  # Exit the function early
    
    # If there are results, perform sentiment analysis
    for result in search_results:
        text = result.get('content', '')  # Ensure this is a valid field from the result
        sentiment = TextBlob(text).sentiment
        
        # If the sentiment is negative, mark it as potentially harmful
        if sentiment.polarity < 0:
            print(f"Potentially Harmful Media: {result['url']} | Sentiment: Negative")
        else:
            print(f"Neutral or Positive Media: {result['url']} | Sentiment: Positive")


# Prompt the user to input the name of the person they want to search for
person_name = input("Enter the name of the person or business you want to find adverse media for: ")

# Run the search function for adverse media coverage
search_adverse_media(person_name)
