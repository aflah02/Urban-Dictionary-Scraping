# Urban Dictionary Scraper

A scraper which scrapes every single word with every single definition present from Urban Dictionary. It generates CSVs for every character separately with the columns - `'title', 'meaning', 'example', 'contributor', 'like', 'dislike'` 

Features:
- Scrapes data for every single entry on Urban Dictionary
- Sleeps and retries after waiting incases of connection error
- Runs across multiple threads in parallel

Scraping Methodology:
- Instantitates one thread for each character (ideally) in the browse drop down menu (27 in total as 26 characters and one * character).
- If lesser number of threads are there on your CPU, it just uses all the threads and then waits for a thread to finish to use it for another character (Haven't tested this bit but should be the case)
- On each thread iterates over all pages with that character
- On each page iterates over all words
- For each word iterates over all pages with word meanings for that word
- Adds those word meanings in a CSV with additional data. The CSV is named data_{character}.csv and all logs are added in error_log_{char}.txt

Note: Since Urban Dictionary is continously updating the results will be different across multiple runs!

(Currently running, once done will add the dataset to maybe Kaggle and HF and share the link here)

Todos:
- Reduce redundancy while scraping (couldn't find a way yet to avoid search hit overlaps)
- Can hit Connection Error due to prolonged requests (Workaround added with retry mechanism + sleep, I don't think there's a better method yet)
