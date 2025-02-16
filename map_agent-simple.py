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
            
            # Handle input safely
            choice = None
            while choice not in range(1, len(location_data) + 1):
                try:
                    choice = int(input("Enter the number corresponding to the correct address: "))
                    if choice not in range(1, len(location_data) + 1):
                        print("Invalid choice. Please select a valid number.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            
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
        search_result = agent.run(search_query)

        # Extract the search result text (if it is in a `RunResponse` object)
        search_text = search_result.get("text", "") if hasattr(search_result, "get") else str(search_result)

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

        # Analyzing the search result to identify any potential suspicious signs
        suspicious_keywords = ["money laundering", "illegal", "crime", "fraud", "unusual activity"]
        suspicious = False
        blurb = "No suspicious signs found in the search results."
        customer_profile = "The area is known for having diverse demographics, with a mix of residential homes and small businesses."

        for keyword in suspicious_keywords:
            if keyword.lower() in search_text.lower():
                suspicious = True
                blurb = f"Warning: The search results mention terms related to suspicious activities, such as {keyword}. This could indicate a potential risk."
                break
        
        # Adding a customer profile based on the location
        if "business district" in search_text.lower():
            customer_profile = "The area is a commercial hub, likely attracting businesses and professionals. High-value transactions may be common here, especially in sectors like finance or tech."
        elif "residential" in search_text.lower() or "suburban" in search_text.lower():
            customer_profile = "This area is primarily residential, and residents are likely to be families or retirees, with fewer high-volume business transactions."
        elif "tourist" in search_text.lower() or "attractions" in search_text.lower():
            customer_profile = "The location is a popular tourist destination, attracting visitors for entertainment, dining, and cultural activities. Businesses in the area may cater to tourism and hospitality."

        return {
            "compliance": compliance_result,
            "search": search_text,
            ##"suspicion": suspicious,
            "blurb": blurb,
            "customer_profile": customer_profile
        }
    else:
        print("Location not found. Please check the input.")
        return {
            "message": "Location Not found"
        }

if __name__ == "__main__":
    # Sample inputs for location, business flow, and fund type
    location = "1600 Pennsylvania Ave NW, Washington, DC 20500"
    business_flow = 1000000  # Example business flow of $1,000,000
    fund_type = "credit card"  # Example fund type
    
    # Call the function with these inputs
    result = get_location_context_and_compliance_check(location, business_flow, fund_type)
    
    # Print the result to see the output of the function
    print("Compliance Result:", result.get("compliance", "No compliance result"))
    ##print("Search Result:", result.get("search", "No search result"))
    print("Suspicion Blurb:", result.get("blurb", "No suspicion identified"))
    print("Customer Profile:", result.get("customer_profile", "No profile available"))
