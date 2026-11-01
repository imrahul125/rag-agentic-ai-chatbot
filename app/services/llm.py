from openai import OpenAI

from app.config import (
    OPENROUTER_BASE_URL,
    OPENROUTER_MODEL,
    get_openrouter_api_key,
)


APP_URL = "https://github.com/imrahul125/rag-agentic-ai-chatbot"


class LLMService:
    def __init__(self):
        self._client: OpenAI | None = None

    @property
    def client(self) -> OpenAI:
        if self._client is None:
            api_key = get_openrouter_api_key()
            if not api_key:
                raise ValueError(
                    "Add OPENROUTER_API_KEY to your .env file or hosting secrets."
                )
            self._client = OpenAI(
                base_url=OPENROUTER_BASE_URL,
                api_key=api_key,
                default_headers={
                    "HTTP-Referer": APP_URL,
                    "X-Title": "Document Chat",
                },
            )
        return self._client

    def generate(self, prompt: str):
        response = self.client.chat.completions.create(
            model=OPENROUTER_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        answer = response.choices[0].message.content
        if not answer:
            raise RuntimeError("The language model returned an empty response.")
        return answer.strip()


llm = LLMService()
