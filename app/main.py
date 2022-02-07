"""
FastAPI application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import db


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/search")
async def search(subtext: str, amount: int = 10):
    """
    Search for a given subtext in a given amount of documents.
    """
    with db.TableResults() as table:
        result = table.search(subtext, amount)
    if result:
        return {"subtext": subtext, "results": result}, 200

    with db.TablePastas() as table:
        result = table.search(subtext, amount)
    if not result:
        return {"error": "No results found."}, 404

    return {"subtext": subtext, "results": result}, 200



@app.get("/stats/{number}")
async def stats(number: str):
    """
    Get the stats for the user with the number.
    """
    with db.TablePastas() as table:
        result = table.get_sent_by(number)
    if not result:
        return {"error": "No results found."}, 404
    return {"number": number, "results": result}, 200


@app.get("/health-check")
async def health_check():
    """
    Check if the application is running
    """
    return {"message": "I'm alive!"}
