from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Add your settings here
    pinecone_api_key: str
    pinecone_index_name: str = "research-assistant"
    embedding_model_name: str = "all-MiniLM-L6-v2"

    class Config:
        env_file = ".env"

settings = Settings()