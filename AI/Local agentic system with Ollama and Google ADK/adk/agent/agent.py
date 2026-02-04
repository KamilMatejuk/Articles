import os
from google.adk.agents import Agent
from google.adk.tools import google_search

from ollama_llm import OllamaLLM


PORT_OLLAMA = int(os.environ["PORT_OLLAMA"])
MODEL_OLLAMA = os.environ["MODEL_OLLAMA"]

model = OllamaLLM(
    model=f"ollama/{MODEL_OLLAMA}",
    api_base=f"http://ollama:{PORT_OLLAMA}",
)

root_agent = Agent(
    name="RootAgent",
    model=model,
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
    tools=[google_search],
)
