from agent import graph

while True:
    query = input("\nAsk: ")

    if query.lower() == "exit":
        break

    result = graph.invoke({"query": query})
    print("\nAnswer:\n", result["answer"])