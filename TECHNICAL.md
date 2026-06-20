# Technical Document

## Architecture

The agent follows a tool-calling architecture where a central LLM (LLaMA 3.3 70B via Groq) receives the user's request, decides which tools to call, executes them, and synthesises the results into a response. The FastAPI layer sits handles incoming requests from the user.

## Tool Selection

I chose three tools to cover the core information needed for trip planning:

Web search via Tavily:used to find attractions, things to do, and transport options for any city. Tavily was chosen over alternatives like SerpAPI because it is built specifically for AI agents and integrates cleanly with LangChain.

Weather via OpenWeatherMap: used to get current weather conditions for the destination city. The free tier was sufficient for this use case.

Mock hotel and flight data: real travel APIs like Skyscanner and Amadeus require paid access or long approval processes. Mock data was used to simulate this tool for the assessment. In production this would be replaced with a real API.

## Memory Design

the agent maintains conversation context within a single session.

Long-term memory stores user preferences across sessions. I built this locally using FAISS with HuggingFace BAAI/bge-small-en embeddings for vector-based similarity search. For deployment, I switched to a lightweight JSON file store due to RAM constraints on Render's free tier. The architecture supports swapping this back to FAISS or a managed vector database like Pinecone when scale requires it.