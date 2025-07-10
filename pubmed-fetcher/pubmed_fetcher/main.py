import requests
import pandas as pd
from typing import List, Dict
import xml.etree.ElementTree as ET

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
def fetch_paper_details(pubmed_ids: List[str]) -> List[Dict]:
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(pubmed_ids),
        "retmode": "xml"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    papers = []
    root = ET.fromstring(response.content)

    for article in root.findall(".//PubmedArticle"):
        paper = {}

        # Extract PubMed ID
        pmid_elem = article.find(".//PMID")
        paper["PubmedID"] = pmid_elem.text if pmid_elem is not None else ""

        # Extract Title
        title_elem = article.find(".//ArticleTitle")
        paper["Title"] = title_elem.text if title_elem is not None else ""

        # Extract Publication Date
        date_elem = article.find(".//PubDate")
        if date_elem is not None:
            year = date_elem.findtext("Year") or "Unknown"
            paper["Publication Date"] = year
        else:
            paper["Publication Date"] = "Unknown"

        # Extract Author Info
        non_academic_authors = []
        affiliations = []
        email = ""

        for author in article.findall(".//Author"):
            affil_info = author.find(".//AffiliationInfo")
            if affil_info is not None:
                affil = affil_info.findtext("Affiliation", "")
                if affil:
                    affiliations.append(affil)
                    if any(keyword in affil.lower() for keyword in ["pharma", "inc", "ltd", "company", "biotech"]):
                        # Heuristic to detect company
                        name = author.findtext("LastName", "") + " " + author.findtext("ForeName", "")
                        non_academic_authors.append(name)
                        if "@" in affil:
                            email = affil.split()[-1]  # try to pick email from end

        paper["Non-academic Author(s)"] = ", ".join(non_academic_authors)
        paper["Company Affiliation(s)"] = ", ".join(affiliations)
        paper["Corresponding Author Email"] = email

        papers.append(paper)

    return papers
# For testing purpose, run this when you type: poetry run python pubmed_fetcher/main.py

if __name__ == "__main__":
    query = "covid vaccine"  # You can change this search term later
    ids = fetch_pubmed_ids(query)
    print(f"✅ Found {len(ids)} PubMed IDs")

    papers = fetch_paper_details(ids)
    print(f"✅ Fetched details for {len(papers)} papers")

    # Save to CSV
    df = pd.DataFrame(papers)
    df.to_csv("output.csv", index=False)
    print("📄 Saved results to output.csv")


