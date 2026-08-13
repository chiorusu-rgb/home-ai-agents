from crewai import Agent
from crewai.tools import tool
from tools.energy_tools import fetch_energy_stats

@tool("Fetch Energy Stats")
def energy_tool(entity_id: str = "sensor.home_energy_power") -> str:
    """Fetches real-time power and energy metrics from the home automation server."""
    return fetch_energy_stats(entity_id)

def create_energy_agent(local_llm):
    """Creates and returns the Home Energy Assistant Agent."""
    return Agent(
        role='Home Energy Manager',
        goal='Monitor power consumption, track energy efficiency, and report real-time usage stats.',
        backstory='You are an intelligent home automation auditor running locally. Your goal is to keep track of household energy consumption and help optimize power usage.',
        tools=[energy_tool],
        llm=local_llm,
        verbose=True,
        allow_delegation=False
    )
