from sqlalchemy import select, Table, create_engine, MetaData
from dotenv import load_dotenv
import os 


load_dotenv()

def simple_fuzzy_search(firstName=None, lastName=None, dateOfBirth=None, sourceId=None, limit=10, offset=0):
    """
    Perform a fuzzy search on the sanctions table. Matches substrings for firstName and lastName.
    All parameters are optional.

    
    """
    engine = create_engine(os.getenv("POSTGRES_URL"),echo=True)
    db_metadata = MetaData()
    sanctions_table = Table("sanctions",db_metadata,autoload_with=engine)
    db_metadata.create_all(engine)
    # Initialize the base query
    query = select(sanctions_table).limit(limit).offset(offset)
    
    # Build a list of conditions
    conditions = []
    if firstName:
        conditions.append(sanctions_table.c.firstName.ilike(f"%{firstName}%"))
    if lastName:
        conditions.append(sanctions_table.c.lastName.ilike(f"%{lastName}%"))
    if dateOfBirth:
        conditions.append(sanctions_table.c.dateOfBirth.ilike(f"%{dateOfBirth}%"))
    if sourceId:
        conditions.append(sanctions_table.c.sourceId.ilike(f"%{sourceId}%"))
    
    # Add conditions to the query if any exist
    if conditions:
        query = query.where(*conditions)
    
    print(query)
    # Execute the query
    data = []
    with engine.connect() as conn:
        for row in conn.execute(query):
            data.append(row._asdict())  # Convert rows to dictionaries for easier handling
    
    print(data)
    return data