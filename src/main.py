from crewai import Task, Crew, LLM
from agents.email_agent import create_inbox_agent
from agents.energy_agent import create_energy_agent

# 1. Connect to your local Ollama Brain on the Xeon server
local_llm = LLM(
    model="ollama/llama3.2:3b", 
    base_url="http://192.168.8.26:11434",
    temperature=0.2
)

# 2. Instantiate both agents
inbox_agent = create_inbox_agent(local_llm)
energy_agent = create_energy_agent(local_llm)

# 3. Define tasks for both agents
check_email_task = Task(
    description=(
        'Use your Fetch Unread Emails tool to retrieve the latest unread messages. '
        'Review the senders and subjects, and write a clean, bulleted summary of the inbox.'
    ),
    expected_output='A short, bulleted summary of the latest unread emails.',
    agent=inbox_agent
)

check_energy_task = Task(
    description=(
        'Use your Fetch Energy Stats tool to check the current power and energy status. '
        'Report the current reading clearly.'
    ),
    expected_output='A concise status report of the current home energy usage.',
    agent=energy_agent
)

# 4. Assemble the multi-agent crew
home_ai_crew = Crew(
    agents=[inbox_agent, energy_agent],
    tasks=[check_email_task, check_energy_task],
    verbose=True
)

if __name__ == "__main__":
    print("Starting the Multi-Agent Local AI Crew...")
    print("Connecting to Ollama at 192.168.8.26...\n")
    
    # Execute the workflow
    result = home_ai_crew.kickoff()
    
    print("\n================================================")
    print("FINAL MULTI-AGENT REPORT")
    print("================================================")
    print(result)
