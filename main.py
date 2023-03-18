from fastapi import FastAPI
from pymongo import MongoClient
from fastapi.responses import JSONResponse
from bson import ObjectId
from datetime import datetime 
import pytz 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


client = MongoClient("mongodb://localhost:27017/")
db = client["news_data"]
collection = db["Articles_collection"]

@app.get("/api/data")
async def get_data():
    articles = []
    for doc in collection.find():
        doc["_id"] = str(doc["_id"])  # convert ObjectId to string
        doc["date"] = str(doc["date"])
        articles.append(doc)
    return JSONResponse(content={"data": articles })

@app.get("/api/data/topic/{topic}")
async def get_data_by_topic(topic: str):
    data = []
    for doc in collection.find({"topic": topic}):
        doc["_id"] = str(doc["_id"])  # convert ObjectId to string
        doc["date"] = str(doc["date"])

        data.append(doc)
    return JSONResponse(content={"data": data})

@app.get("/api/data/countsarticlesbytopic/{topic}")
async def get_data_by_topic(topic: str):
    data = []
    for doc in collection.find({"topic": topic}):
        doc["_id"] = str(doc["_id"])  # convert ObjectId to string
        data.append(doc)
    return JSONResponse(content={"data": len(data)})


@app.get("/api/data/author/{authors}")
async def get_data_by_author(authors: str):
    data = []
    for doc in collection.find({"authors": authors}):
        doc["_id"] = str(doc["_id"])  # convert ObjectId to string
        doc["date"] = str(doc["date"])

        data.append(doc)
    return JSONResponse(content={"data": data})

@app.get("/api/data/countsarticlesbyauthor/{authors}")
async def get_data_by_author(authors: str):
    data = []
    for doc in collection.find({"authors": authors}):
        doc["_id"] = str(doc["_id"])  # convert ObjectId to string
        data.append(doc)
    return JSONResponse(content={"data": len(data)})


@app.get("/api/data/before/{date}")
async def get_data_before_date(date: str):
    # Convert date strings to datetime objects
    #date = datetime.strptime(date, '%Y-%m-%d ')
    date = datetime.strptime(date, '%Y-%m-%d')
    print(date)
    #post_date = datetime.strptime(post_date, '%Y-%m-%d')

    # Create the query dictionary
    query = {"date": {"$lte": date}}

    # Retrieve the data from MongoDB
    data = []
    for doc in collection.find(query):
        doc["_id"] = str(doc["_id"])  # convert ObjectId to string
        doc["date"] = doc["date"].strftime("%Y-%m-%d")
        data.append(doc)

    return JSONResponse(content={"data": data})

@app.get("/api/data/after/{date}")
async def get_data_after_date(date: str):
    # Convert date strings to datetime objects
    date = datetime.strptime(date, '%Y-%m-%d')
    print(date)
    # Create the query dictionary
    query = {"date": {"$gte": date}}
    # Retrieve the data from MongoDB
    data = []
    for doc in collection.find(query):
        doc["_id"] = str(doc["_id"])  # convert ObjectId to string
        doc["date"] = doc["date"].strftime("%Y-%m-%d")
        data.append(doc)

    return JSONResponse(content={"data": data})