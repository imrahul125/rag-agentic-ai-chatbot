import os

from dotenv import load_dotenv
from openai import OpenAI


def main():
    load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise SystemExit("Set OPENROUTER_API_KEY in .env before listing models.")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    for model in client.models.list().data:
        print(model.id)


if __name__ == "__main__":
    main()
