from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
import geopy
from geopy.geocoders import Nominatim

# Define the function to get location context
def get_location_context(location):
    print(f"Looking up location: {location}")
    # Initialize the geolocator (Nominatim is a geocoding service)
    geolocator = Nominatim(user_agent="myApp")
    
    # Get the location coordinates (latitude, longitude) based on the given location
    location_data = geolocator.geocode(location, exactly_one=False)  # Now allows multiple results
    
    if location_data:
        print(f"Found {len(location_data)} location(s).")
        if len(location_data) > 1:
            # If there are multiple results, ask the user to be more specific
            print("Multiple locations found. Please choose the correct address:")
            for idx, loc in enumerate(location_data):
                print(f"{idx + 1}: {loc.address}")
            
            # Choose the first result for now
            choice = 1  # Just select the first result
            location_data = location_data[choice - 1]  # Get the selected address
        else:
            location_data = location_data[0]  # Use the only result
        
        # Output the chosen location information
        latitude = location_data.latitude
        longitude = location_data.longitude
        print(f"Location found: {location_data.address}")
        print(f"Latitude: {latitude}, Longitude: {longitude}")
        
        # Now, use DuckDuckGo to get additional context about the area
        search_query = f"Brief context and historical background about {location_data.address} OR nearby landmarks or points of interest"
        
        # Setup DuckDuckGo search through the agent to find more context
        agent = Agent(
            model=OpenAIChat(id="gpt-4o"),
            description=(
                "You are an assistant tasked with providing a brief context of the location. "
                "Search for any relevant details such as historical background, local landmarks, "
                "or any important characteristics of the location."
            ),
            tools=[DuckDuckGoTools()],
            show_tool_calls=True,
            markdown=True
        )
        
        # Use DuckDuckGo to search for relevant information about the location
        search_result = agent.run(search_query)

        return {
            "location_info": location_data.address,
            "latitude": latitude,
            "longitude": longitude,
            "context": search_result
        }
    else:
        print("Location not found. Please check the input.")
        return {
            "message": "Location Not found"
        }

# Define the function to search location info
def search_location_info(location_name):
    # Use geopy to get the location info based on name
    result = get_location_context(location_name)
    return result
    # Output the result
    print("Location Information:", result)

# Assign a fixed location value
location_name = "New York City"  # Example location

# Run the function to search for the location context
search_location_info(location_name)
