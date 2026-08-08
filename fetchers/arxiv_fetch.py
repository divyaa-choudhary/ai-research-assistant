#fetching and downloading papers before loading it
import arxiv
import os
import json
from urllib.request import urlretrieve #urllib fetches files from the internet (Internet File Streaming)
from urllib.error import URLError, HTTPError as URLLibHTTPError
from utils.logger import get_logger

logger = get_logger(__name__)

def fetch_papers(query: str, max_results: int = 5, download_dir: str = "research_papers") -> list[dict]:
    logger.info(f"Starting fetch: query = '{query}', max_results={max_results}")

    os.makedirs(download_dir, exist_ok=True)
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
    )

    client = arxiv.Client(page_size = 100, delay_seconds = 5.0, num_retries = 5,)

    try:
        results = list(client.results(search)) #this is a generator; you can iterate over its elements one by one
    except arxiv.HTTPError as e:
        logger.error(f"arxiv API request failed: {e}")
        raise

    logger.info(f"Found {len(results)} papers, starting downloads")


    papers = []
    for result in results:
        arxiv_id = result.get_short_id()

        try:
            filename = f"{result.get_short_id().replace('/','_')}.pdf"
            file_path = os.path.join(download_dir, filename)
            urlretrieve(result.pdf_url, file_path)
            logger.info(f"Downloaded: {arxiv_id} -> {file_path}")
        except (URLError, URLLibHTTPError) as e:
            logger.warning(f"Failed to download {arxiv_id}, skipping. Reason: {e}")
            continue #skip this paper, keep processing the next one

        paper_meta = {
            "arxiv_id": arxiv_id,
            "title": result.title,
            "authors": [a.name for a in result.authors], 
            "abstract": result.summary,
            "published": str(result.published.date()),
            "categories": result.categories,
            "pdf_path": file_path,
        }

        #Save metadata as a sidecar JSON File next to its own PDF
        meta_path = os.path.join(download_dir, f"{arxiv_id.replace('/','_')}.json")
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(paper_meta, f, indent=2)

        papers.append(paper_meta)

    logger.info(f"Completed: {len(papers)}/{len(results)} papers successfully downloaded.")
    return papers