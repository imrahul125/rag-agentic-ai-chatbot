from app.graph.workflow import graph

response = graph.invoke(
    {
        "question": "What is Agentic AI?"
    }
)

print(response["answer"])
print()
print(response["confidence"])