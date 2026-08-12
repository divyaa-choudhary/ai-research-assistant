from groq import Groq
from config import settings
from utils.logger import get_logger

logger = get_logger(__name__)

client = Groq(api_key=settings.groq_api_key)

def generate_answer(prompt: str, model: str="openai/gpt-oss-20b") -> str:
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user","content": prompt}],
            temperature=1,
        )
        return response.choices[0].message.content
    except Exception:
        logger.exception("Generation Failed")
        raise