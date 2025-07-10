import typer
from pubmed_fetcher.main import fetch_pubmed_ids, fetch_paper_details
import pandas as pd

app = typer.Typer()

@app.command()
def get(query: str, file: str = "output.csv", debug: bool = False):
    """Fetch PubMed papers for a query and save to CSV"""
    ids = fetch_pubmed_ids(query)
    typer.echo(f" Found {len(ids)} PubMed IDs")

    papers = fetch_paper_details(ids)
    typer.echo(f" Fetched {len(papers)} paper details")

    if debug: 
         typer.echo("Full Paper Data:")
         for paper in papers:
            typer.echo(paper)

    df = pd.DataFrame(papers)
    df.to_csv(file, index=False)
    typer.echo(f" Saved results to {file}")

if __name__ == "__main__":
    app()
