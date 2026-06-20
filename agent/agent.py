import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import tool
from agent.tools import get_weather, search_attractions, get_hotels_and_flights
from agent.memory import save_preference, get_relevant_preferences

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))

@tool
def weather_tool(city: str) -> str:
    """Get the current weather for a city."""
    return get_weather(city)

@tool
def search_tool(query: str) -> str:
    """Search for attractions, things to do, transport and places to visit."""
    return search_attractions(query)

@tool
def hotel_flight_tool(city: str) -> str:
    """Get hotel and flight options for a city."""
    return get_hotels_and_flights(city)

tools = [weather_tool, search_tool, hotel_flight_tool]

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful travel planning assistant. 
    Help users plan detailed 2-day trips based on their preferences.
    Always check the weather, suggest attractions, and provide hotel and flight options.
    Be conversational and friendly."""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

def create_agent():
    
    agent = create_tool_calling_agent(llm, tools, prompt)
    
    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True
    )
    
    return executor


def run_agent(user_input: str, executor: AgentExecutor) -> str:
    preferences = get_relevant_preferences(user_input)
    
    if preferences:
        full_input = f"User preferences from past sessions:\n{preferences}\n\nUser request: {user_input}"
    else:
        full_input = user_input
    
    preference_keywords = ["i prefer", "i like", "i hate", "i don't like", "i love", "i always"]
    if any(keyword in user_input.lower() for keyword in preference_keywords):
        save_preference(user_input)
    
    result = executor.invoke({"input": full_input,"chat_history": []})
    return result["output"]