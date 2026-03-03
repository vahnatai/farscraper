# Farscraper

A web scraper that calculates watch orders for Farscape by scraping the Farscape Encyclopedia Project wiki.

## Requirements

- Python 3.9+
- internet access
- `fandom` library (need my fixed fork of fandom-py)

```bash
pip install git+https://github.com/vahnatai/fandom-py-fixes.git
```

## Usage

```bash
python farscraper.py [page_title] [count]
```

### Arguments

- `page_title` (optional): The starting page title. Defaults to 'Premiere' (first episode).
- `count` (optional): Number of episodes to retrieve. Defaults to 3.

### Examples

```bash
# Get the first 3 episodes
python farscraper.py

# Get 5 episodes starting from "Premiere"
python farscraper.py Premiere 5

# Get 10 episodes starting from a specific episode
python farscraper.py "Exodus from Genesis" 10
```

## Output

Episodes are displayed in the format:
- Episodes: `FAR <season>x<episode> "<title>"`
- Movies: `MOV "<title>"`

## Notes

- Comic series listing is not yet implemented
- The script stops when it encounters the "Return of the King" comic
