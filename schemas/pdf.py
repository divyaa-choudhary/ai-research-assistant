from pydantic import BaseModel

class LoadedDocOut(BaseModel):
    file_name: str
    char_count: int
    preview: str # fisrst ~400 chars, not the full text

class LoadAllOut(BaseModel):
    count: int
    documents: list[LoadedDocOut]