from crewai import Agent
from crewai.tools import tool
from tools.email_tools import fetch_unread_emails

@tool("Fetch Unread Emails")
def email_reader_tool(limit: int = 5) -> str:
    """Connects to the IMAP server and fetches the subjects and senders of the latest unread emails. Use this tool whenever you need to check the inbox."""
    
    # Safety Net: Force the AI's input into a valid positive integer
    try:
        safe_limit = int(limit)
        if safe_limit <= 0:
            safe_limit = 5 # Default to 5 if it asks for 0 or negative emails
    except (ValueError, TypeError):
        safe_limit = 5 # Default to 5 if it passes weird text
        
    return fetch_unread_emails(safe_limit)

def create_inbox_agent(local_llm):
    """Creates and returns the Inbox Manager Agent."""
    return Agent(
        role='Local Inbox Manager',
        goal='Securely read and summarize unread emails from the user inbox.',
        backstory='You are a highly secure, offline AI assistant running on a local homelab server. Your primary duty is to monitor the inbox, extract important updates, and present them clearly to the user while keeping all data private.',
        tools=[email_reader_tool],
        llm=local_llm,
        verbose=True,
        allow_delegation=False
    )
