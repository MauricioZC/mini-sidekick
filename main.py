from langchain.agents import create_agent
from dotenv import load_dotenv


def main():
    load_dotenv()
    agent = create_agent(
        model="openai:gpt-5-mini",
        tools=[get_weather],
        system_prompt="You are a helpful assistant",
    )

    # Run the agent
    response = agent.invoke(
        {"messages": [{"role": "user", "content": "What is the weather in San Francisco?"}]}
    )
    for m in response["messages"]:
        m.pretty_print()


def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


if __name__ == "__main__":
    main()
