import scraper

is_ready = False
year, month, date = None, None, None
subreddit = "wallstreetbets"

while not is_ready:
    subreddit = input("Which subreddit do you want to scrape?:\n")
    year = int(input("Start year: "))
    month = int(input("Start month: "))
    date = int(input("Start date: "))
    if input("Ready to scrape? (y/n): ").lower().strip() == 'y':
        is_ready = True

if len(f"{year}{month}{date}") == 0:
    scraper.scrape_subreddit(subreddit)
else:
    scraper.scrape_subreddit(subreddit, year, month, date)
