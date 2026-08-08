# my entrypoint of FASTAPI app

from fastapi import FastAPI
from routers import arxiv, pdf

app = FastAPI(title="AI Research Assistant")

app.include_router(arxiv.router)
app.include_router(pdf.router)