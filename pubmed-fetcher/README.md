\# PubMed Paper Fetcher



This is a Python CLI tool to fetch PubMed research papers based on a search query and identify non-academic authors (e.g., from pharmaceutical or biotech companies).



\## Features



\- Fetches papers using PubMed API

\- Filters authors from companies using affiliation heuristics

\- Extracts PubMed ID, Title, Publication Date, Author info, Email

\- Saves results as CSV

\- CLI interface using `typer`

\- `--debug` option for development



\## Tech Stack



\- Python 3

\- requests (API fetching)

\- pandas (CSV export)

\- typer (Command-line tool)

\- poetry (dependency \& script management)



\## Usage



\### Installation

Make sure you have Python 3 and Poetry installed.



''bash

poetry install



