# Travel Planning AI Agent

A travel planning agent I built that takes a user's destination and travel period, calls a few external tools to gather relevant information, and puts together a 2-day itinerary. It checks the weather, searches for things to do, and returns hotel and flight options.

## Tech Stack

- LLM: LLaMA 3.3 70B via Groq
- Agent Framework: LangChain
- Web Search: Tavily API
- Weather: OpenWeatherMap API
- Memory: JSON file store for long-term preferences, session-based short-term memory
- API: FastAPI
- Deployment: Render

## How to run locally

1. Clone the repo
git clone https://github.com/sudharshini-data/travel-agent.git
cd travel-agent

2. Install dependencies
pip install -r requirements.txt

3. Add a .env file with the keys
GROQ_API_KEY=the_key
TAVILY_API_KEY=the_key
OPENWEATHER_API_KEY=the_key

4. Start the server
uvicorn api.main:app --reload

## API

POST /chat
Send a message and get back a travel plan.
{"message": "I want to plan a 2 day trip to Tokyo in winter"}

GET /
Health check — confirms the service is running.

## How it works

The user sends a message to the FastAPI endpoint. The agent reads it and decides which tools to call, weather, web search, or hotel/flight data. It gathers everything and writes out a day-by-day itinerary. If the user mentions any preferences, those get saved and pulled in on future requests.

## Notes

- Hotel and flight data is mocked since real travel APIs like Skyscanner require paid access. In production I'd swap this out for Amadeus or a similar service.
- I built the long-term memory layer with FAISS and HuggingFace embeddings locally, but switched to a JSON store for deployment since the embedding model exceeded Render's free tier RAM limit.
