# Urban Dictionary Scraper

Uses beautifulsoup to scrape data for every single word on Urban Dictionary and stores it in an output CSV

Todos:
- Speed Up using Multi Threading
- Reduce redundancy while scraping (couldn't find a way yet to avoid search hit overlaps)
- Can hit Connection Error due to prolonged requests (Workaround added with retry mechanism + sleep)