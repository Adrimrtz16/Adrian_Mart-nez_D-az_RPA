from agent.agent import build_agent

def main():
    agent = build_agent()

    thread_id = "session_1"

    print("Agente iniciado. Escribe 'exit' para salir.\n")

    while True:
        user_input = input("Tú: ")

        if user_input.lower() == "exit":
            break

        config = {
            "configurable": {
                "thread_id": thread_id
            }
        }

        result = agent.invoke(
            {
                "messages": [
                    ("user", user_input)
                ]
            },
            config=config
        )

        print(
            "\nAgente:",
            result["messages"][-1].content,
            "\n"
        )


if __name__ == "__main__":
    main()