from functools import lru_cache

from app.core.config import get_settings


@lru_cache
def get_groq_client():
    settings = get_settings()
    if not settings.groq_api_key:
        return None

    from groq import Groq
    return Groq(api_key=settings.groq_api_key)


def chat(system_prompt: str, user_prompt: str) -> str:
    settings = get_settings()
    client = get_groq_client()
    if client is None:
        return (
            "LLM is not configured. Add GROQ_API_KEY to generate a natural-language "
            "answer. The retrieval and routing pipeline still ran successfully."
        )

    completion = client.chat.completions.create(
        model=settings.groq_model,
        temperature=settings.groq_temperature,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return completion.choices[0].message.content or ""
