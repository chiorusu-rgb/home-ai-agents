import os
from crewai import LLM
from dotenv import load_dotenv

load_dotenv()

# Your existing local model for simple tasks
local_llm = LLM(
    model="ollama/llama3.2:3b", 
    base_url="http://192.168.8.26:11434",
    temperature=0.2
)

# Your new Gemini model for heavy lifting
gemini_llm = LLM(
    model="gemini/gemini-2.5-flash", # Or gemini-2.5-pro for complex reasoning
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.2
)

# Now, simply pass `gemini_llm` to the agent you want to upgrade:
# inbox_agent = create_inbox_agent(gemini_llm)
