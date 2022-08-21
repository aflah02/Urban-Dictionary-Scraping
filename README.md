# Urban Dictionary Scraper

A scraper which scrapes every single word with every single definition present from Urban Dictionary. It generates a CSV with the columns - `'title', 'meaning', 'example', 'contributor', 'like', 'dislike'` 

Note: Since Urban Dictionary is continously updating the results will be different across multiple runs!

(Currently running, once done will add the dataset to maybe Kaggle and HF and share the link here)

Todos:
- Speed Up using Multi Threading (Tried and failed, so will have a look in the future)
- Reduce redundancy while scraping (couldn't find a way yet to avoid search hit overlaps)
- Can hit Connection Error due to prolonged requests (Workaround added with retry mechanism + sleep, I don't think there's a better method yet)
