from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
import geopy
from geopy.geocoders import Nominatim

# Define the function to get location context and compliance check, including fund type
def get_location_context_and_compliance_check(location, business_flow, fund_type):
    # Initialize the geolocator (Nominatim is a geocoding service)
    geolocator = Nominatim(user_agent="myApp")
    
    # Get the location coordinates (latitude, longitude) based on the given location
    location_data = geolocator.geocode(location, exactly_one=False)  # Now allows multiple results
    
    if location_data:
        if len(location_data) > 1:
            # If there are multiple results, ask the user to be more specific
            print("Multiple locations found. Please choose the correct address:")
            for idx, loc in enumerate(location_data):
                print(f"{idx + 1}: {loc.address}")
            
            # Ask the user to choose the correct location
            choice = int(input("Enter the number corresponding to the correct address: "))
            location_data = location_data[choice - 1]  # Get the selected address
        else:
            location_data = location_data[0]  # Use the only result
        
        # Output the chosen location information
        latitude = location_data.latitude
        longitude = location_data.longitude
        print(f"Location found: {location_data.address}")
        print(f"Latitude: {latitude}, Longitude: {longitude}")
        
        # Now, use DuckDuckGo to get additional context about the area
        search_query = f"information about {location_data.address} OR nearby attractions OR points of interest"
        
        # Setup DuckDuckGo search through the agent to find more context
        agent = Agent(
            model=OpenAIChat(id="gpt-4o"),
            description=(
                "You are an assistant tasked with providing additional context and information about locations. "
                "Search for any relevant details such as nearby attractions, restaurants, or other interesting facts about the location."
            ),
            tools=[DuckDuckGoTools()],
            show_tool_calls=True,
            markdown=True
        )
        
        # Use DuckDuckGo to search for relevant information about the location
        #agent.print_response(search_query, stream=True)
        search_result = agent.run(search_query)
        
        # Now check if a 1 million dollar flow makes sense for the area (money laundering context)
        # Add the fund type to the compliance question
        compliance_question = (
            f"Does a {business_flow} dollar business flow make sense for a small residential home in the area around {location_data.address}? "
            f"Considering that the transaction is via {fund_type}, does this make sense in money laundering compliance? "
            "For example, a bitcoin exchange might raise different questions compared to a regular credit/debit card transaction."
        )
        
        # Ask the compliance question for review
        agent.description = (
            "You are a financial crime compliance expert tasked with reviewing transactions for potential money laundering risks. "
            "Evaluate whether a large transaction, such as a 1 million dollar business flow, makes sense for a residential property in a certain area, "
            "and take into account the type of fund used (credit, debit, or cryptocurrency)."
        )
        
        # Get compliance review response
        compliance_result = agent.run(compliance_question)

        return {
            "compliance":compliance_result,
            "search":search_result
        }
    else:
        print("Location not found. Please check the input.")
        return{
            "message":"Location Not found"
        }

# Define the agent with a basic setup (not involved in map retrieval but for reference)
def search_location_info(location_name, business_flow, fund_type):
    # Use geopy to get the location info based on name
    get_location_context_and_compliance_check(location_name, business_flow, fund_type)

""" # Prompt the user to input the name of the location, business flow, and fund type
location_name = input("Enter the location or place you want to find context for: ")
business_flow = float(input("Enter the business flow amount (e.g., 1000000 for 1 million dollars): "))
fund_type = input("Enter the fund type (credit, debit, bitcoin exchange, etc.): ").lower()

# Run the function to search for the location, context, and compliance check
search_location_info(location_name, business_flow, fund_type) """