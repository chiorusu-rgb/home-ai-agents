from crewai import Task, Crew, LLM
from agents.email_agent import create_inbox_agent

# 1. Connect to your local Ollama Brain on the Xeon server
local_llm = LLM(
    model="ollama/llama3.2:3b", 
    base_url="http://192.168.8.26:11434",
    temperature=0.2  # Low temperature keeps the summary factual and concise
)

# 2. Instantiate the Inbox Manager Agent
inbox_agent = create_inbox_agent(local_llm)

# 3. Define the specific task for the agent
check_email_task = Task(
    description=(
        'Use your Fetch Unread Emails tool to retrieve the latest unread messages. '
        'Review the senders and subjects, and write a clean, bulleted summary of what is currently in the inbox.'
    ),
    expected_output='A short, polite, and readable summary of the latest unread emails, formatted with bullet points.',
    agent=inbox_agent
)

# 4. Assemble the crew (currently just one agent)
home_ai_crew = Crew(
    agents=[inbox_agent],
    tasks=[check_email_task],
    verbose=True
)

if __name__ == "__main__":
    print("Starting the Local AI Crew...")
    print("Connecting to Ollama at 192.168.8.26...\n")
    
    # Execute the workflow
    result = home_ai_crew.kickoff()
    
    print("\n================================================")
    print("FINAL AI REPORT")
    print("================================================")
    print(result)
