from app.services.llm import llm

print(
    llm.generate(
        "Explain Agentic AI in one sentence."
    )
)