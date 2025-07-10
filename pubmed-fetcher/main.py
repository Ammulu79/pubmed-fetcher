import requests
from typing import List

def fetch_pubmed_ids(query: str, max_results: int = 10) -> List[str]:
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": max_results
    }

    response = requests.get(url, params=params)
    response.raise_for_status()  # raises error if something goes wrong

    data = response.json()
    return data["esearchresult"]["idlist"]

# For testing purpose, run this when you type: poetry run python pubmed_fetcher/main.py
if __name__ == "__main__":
    ids = fetch_pubmed_ids("covid vaccine")
    print("PubMed IDs found:", ids)
