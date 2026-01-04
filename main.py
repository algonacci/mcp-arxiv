from mcp.server.fastmcp import FastMCP
import arxiv
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

mcp = FastMCP(
    "arxiv",
    dependencies=["arxiv", "python-dotenv"]
)

# Storage path configuration
STORAGE_PATH = Path(os.getenv("ARXIV_PAPER_STORAGE_PATH", str(Path.cwd() / "downloads")))
STORAGE_PATH.mkdir(parents=True, exist_ok=True)


@mcp.tool()
def search_papers(
    query: str, 
    max_results: int = 10,
    sort_by: str = "submitted_date",
    sort_order: str = "descending"
):
    """
    Search for papers on ArXiv.
    
    Args:
        query: Search query
        max_results: Maximum number of results to return
        sort_by: Criterion to sort by ("relevance", "last_updated_date", "submitted_date")
        sort_order: Order of results ("ascending", "descending")
    """
    client = arxiv.Client()

    # Map string parameters to arxiv enums
    sort_criterion = {
        "relevance": arxiv.SortCriterion.Relevance,
        "last_updated_date": arxiv.SortCriterion.LastUpdatedDate,
        "submitted_date": arxiv.SortCriterion.SubmittedDate
    }.get(sort_by, arxiv.SortCriterion.SubmittedDate)

    sort_order_enum = {
        "ascending": arxiv.SortOrder.Ascending,
        "descending": arxiv.SortOrder.Descending
    }.get(sort_order, arxiv.SortOrder.Descending)

    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=sort_criterion,
        sort_order=sort_order_enum,
    )

    results_data = []

    for r in client.results(search):
        affiliation = None
        if hasattr(r, "_raw") and isinstance(r._raw, dict):
            affiliation = r._raw.get("arxiv_affiliation")

        paper = {
            "title": r.title,
            "pdf_url": r.pdf_url,
            "authors": [author.name for author in r.authors],
            "summary": r.summary,
            "published": r.published.strftime("%Y-%m-%d"),
            "categories": r.categories,
            "entry_id": r.entry_id,
            "comment": r.comment,
            "affiliation": affiliation,
        }

        results_data.append(paper)

    return results_data

@mcp.tool()
def download_paper(paper_id: str) -> str:
    """
    Download a paper from ArXiv as a PDF.
    
    Args:
        paper_id: The ArXiv ID of the paper (e.g., "2301.12345" or the full URL)
    """
    # Clean paper_id if it's a URL
    clean_id = paper_id.split('/')[-1]
    if clean_id.endswith('v'): # handle version numbers
        clean_id = clean_id.split('v')[0]
        
    client = arxiv.Client()
    search = arxiv.Search(id_list=[clean_id])
    
    try:
        paper = next(client.results(search))
        
        # Create filename
        safe_title = "".join([c if c.isalnum() else "_" for c in paper.title])
        filename = f"{clean_id}_{safe_title[:50]}.pdf"
        filepath = STORAGE_PATH / filename
        
        # Download
        paper.download_pdf(dirpath=str(STORAGE_PATH), filename=filename)
        
        return f"Paper downloaded successfully to: {filepath}"
    except StopIteration:
        return f"Error: Paper with ID {paper_id} not found."
    except Exception as e:
        return f"Error downloading paper: {str(e)}"


if __name__ == "__main__":
    mcp.run()