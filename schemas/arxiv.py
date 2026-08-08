from pydantic import BaseModel

class ArxivFetchIn(BaseModel):
    query: str
    max_results: int = 5

class PaperOut(BaseModel):
    """A single paper's metadata """
    arxiv_id: str
    title: str
    authors: list[str]
    abstract: str
    published: str
    categories: list[str]
    pdf_path: str

class ArxivFetchOut(BaseModel):
    """ Full response - list of fetched papers"""
    count: int
    papers: list[PaperOut]