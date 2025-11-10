from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from dotenv import load_dotenv
from .tools import make_call
from langchain.agents.structured_output import ToolStrategy
from pydantic import BaseModel
import os

load_dotenv()

VERIFIED_NUMBER = os.getenv("VERIFIED_NUMBER")
MODEL_NAME = 'gemini-2.5-flash'

SYSTEM_PROMPT = f"""
### System Prompt: AutoDialer

You are **AutoDialer**, a calling agent responsible for initiating phone calls using the `make_call` tool.

#### Behavior Rules:

1. You will be provided with:
   - A **mobile number** (which must include the **country code**)
   - A **message** to deliver

2. Before making a call:
   - **Verify** that the provided number includes a **country code**.
   - Only proceed if the number exactly matches `{VERIFIED_NUMBER}`.
   - If any **other number** is provided, **do not make a call**.
     Instead, return:
     > "Due to the trial account of Twilio, I can make calls to verified numbers only."

3. When you make a call using the `make_call` tool:
   - If the call is **successfully initiated** and you receive a `call_sid`, return:
     > "Call initiated successfully with call_sid: `call_sid`. Check Call logs for call status."
   - If the call **fails** and you receive an error, return:
     > "Failed to make call with error as: `error`"

4. Do not perform any other actions besides the above.
"""


class AgentOutput(BaseModel):
    final_response: str


class AutodialerAgent:
    def __init__(self):
        self.model = ChatGoogleGenerativeAI(model=MODEL_NAME)
        self.tools = [make_call]
        self.agent = create_agent(
            self.model,
            tools=self.tools,
            system_prompt=SYSTEM_PROMPT,
            response_format=ToolStrategy(AgentOutput)
        )

    def call_agent(self, user_input: str) -> str:
        """Invoke the agent with user input to make a call."""
        response = self.agent.invoke(
            {"messages": [{"role": "user", "content": user_input}]}
        )
        return response


if __name__ == "__main__":
    load_dotenv()
    autodialer_agent = AutodialerAgent()

    mobile_number = VERIFIED_NUMBER
    message = "Hi there! This is a quick test call to check if the autodialer is working properly."

    user_input = f"Make a call to {mobile_number} with the message: '{message}'"
    result = autodialer_agent.call_agent(user_input)
    print(result["structured_response"])
