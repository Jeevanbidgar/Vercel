from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Load marks data
with open("q-vercel-python.json", "r") as file:  
    marks_list = json.load(file)
    # print(marks_list)

# Convert list to a dictionary for fast lookup
marks_data = {entry["name"]: entry["marks"] for entry in marks_list}

@app.get("/api")
def get_marks(name: list[str] = Query([])):
    result = [marks_data.get(n, None) for n in name]
    return {"marks": result}
