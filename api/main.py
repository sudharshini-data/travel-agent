from fastapi import FastAPI
from pydantic import BaseModel
from agent.agent import create_agent, run_agent

app = FastAPI()
executor = create_agent()

class TripRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: TripRequest):
    response = run_agent(request.message, executor)
    return {"response": response}

@app.get("/")
async def root():
    return {"message": "Travel Planning Agent is running"}