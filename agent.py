import asyncio
import os
from dotenv import load_dotenv
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, ResultMessage

load_dotenv()

SYSTEM_PROMPT = """You are a data analyst agent. You have access to CSV files in the data/ folder.

When asked a question about data:
1. First read the relevant CSV file using the Read tool
2. Analyze the data carefully
3. Answer the question clearly with exact numbers
4. If helpful, write a small Python script to verify your answer

Always be precise. Show your reasoning step by step.
If asked to compare, show both values and the difference.
"""

async def run_agent(question: str, verbose: bool = True) -> str:
    """Run the data analyst agent with a given question."""
    
    result_text = ""
    
    async for message in query(
        prompt=question,
        options=ClaudeAgentOptions(
            system_prompt=SYSTEM_PROMPT,
            allowed_tools=["Read", "Glob", "Bash"],
            permission_mode="acceptEdits",
        ),
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text") and block.text:
                    if verbose:
                        print(block.text)
                    result_text += block.text
                elif hasattr(block, "name") and verbose:
                    print(f"\n[Using tool: {block.name}]\n")
        
        elif isinstance(message, ResultMessage):
            if verbose:
                print(f"\n✅ Done ({message.subtype})")
    
    return result_text


if __name__ == "__main__":
    question = "What is the total sales amount for each product? Which product had the highest sales overall?"
    print(f"\n📊 Question: {question}\n")
    print("=" * 60)
    asyncio.run(run_agent(question))