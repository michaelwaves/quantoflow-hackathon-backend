from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from  basic_agent import search_adverse_media
from map_api import search_location_info
from dotenv import load_dotenv
from sanctions_agent import simple_fuzzy_search

load_dotenv()

app = FastAPI()

# Enable CORS for all origins, methods, and headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


@app.get("/adverse_media_search")
def adverse_media_search(entity):
    return search_adverse_media(entity)

@app.get("/search_location_info")
def location_search(address):
    return search_location_info(address)

@app.get("/sanctions")
def simple_search_sanctions(firstName, lastName):
    res = simple_fuzzy_search(
        firstName, 
        lastName,
    ) 
    return res
""" 
@app.get("/sanctions_embeddings")
def embeddings_search_sanctions(firstName, lastName):
    res = embeddings_sanctions_search(
        firstName, 
        lastName,
    ) 
    return res """

if __name__ =="__main__":
    uvicorn.run("api:app", port=8000, host="0.0.0.0", reload=True)