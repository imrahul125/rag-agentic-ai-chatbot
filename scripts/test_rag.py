from app.services.rag import rag

response = rag.ask(
    "What is Agentic AI?"
)

print("\nANSWER\n")
print(response["answer"])

print("\nCONFIDENCE\n")
print(response["confidence"])

print("\nSOURCE 1\n")
print(response["sources"][0]["text"][:500])