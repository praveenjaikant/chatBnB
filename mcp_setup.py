import shutil
import asyncio
from datetime import datetime
from agents.mcp import MCPServer, MCPServerStdio
from agents import Agent, Runner, gen_trace_id, trace

async def run(mcp_server: MCPServer, message: str):
    agent = Agent(
        name="Assistant",
        instructions=f"""
        You are a helpful AirBnB Assistant.
        
        - Use the AirBnB MCP Tool to pull data from the AirBnB website
        - Start by running ListTools to see the available tools, then use executeTool to run the one that fits your task
        - Current Datetime is {datetime.now()}
        """,
        mcp_servers=[mcp_server],
    )

    # Ask a question that reads then reasons.
    print(f"\n\nRunning: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    return result.final_output


async def main(message):

    async with MCPServerStdio(
        name="Filesystem Server, via npx",
        params={
            "command": "npx",
            "args": ["-y", "@openbnb/mcp-server-airbnb", "--ignore-robots-txt"],

        },
    ) as server:
        trace_id = gen_trace_id()

        with trace(workflow_name="AirBnb MCP Server", trace_id=trace_id):
            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}\n")
            return await run(server, message=message)


if __name__ == "__main__":

    asyncio.run(main(message="Find me weekend stays in Brooklyn under $300 for 2 adults"))