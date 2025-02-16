import asyncio
import psycopg2
from sqlalchemy import create_engine, text
from llama_index.core.agent.workflow import AgentWorkflow
from llama_index.llms.openai import OpenAI

# Connect to local PostgreSQL
engine = create_engine("postgresql+psycopg2://postgres:password@localhost:5432/quantoflow-test", echo=True)
def search_in_database(first_name: str, last_name: str):
    # Use SQLAlchemy's text() function to wrap the query
    query = text("""
        SELECT * FROM people
        WHERE first_name = :first_name AND last_name = :last_name;
    """)

    with engine.connect() as connection:
        # Execute the query with the provided parameters
        result = connection.execute(query, {"first_name": first_name, "last_name": last_name}).fetchall()
        return result

# Test the function
first_name = "Paige"
last_name = "Bailey"
search_results = search_in_database(first_name, last_name)
print(search_results)
