from psaw import PushshiftAPI
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def scrape_subreddit(subreddit,
                     start_year=int(datetime.now().year),
                     start_month=int(datetime.now().month),
                     start_date=int(datetime.now().day)):
    api = PushshiftAPI()
    start_time = int(datetime(start_year, start_month, start_date).timestamp())

    submissions = api.search_submissions(after=start_time,
                                subreddit=subreddit,
                                filter=["url", "author", "title", "subreddit"])

    stock_dict = {}
    for submission in submissions:
        words = submission.title.split()
        tickers = list(set(filter(lambda word: word.lower().startswith('$'), words)))

        if len(tickers) > 0:
            print(submission.url)
            for ticker in tickers:
                if ticker.startswith('$') and ticker[1:].isalpha():
                    formatted_cashtag = ticker[1:].upper()
                    stock_dict.setdefault(formatted_cashtag, 0)
                    stock_dict[formatted_cashtag] += 1

    comments = api.search_comments(after=start_time,
                                subreddit=subreddit,
                                filter=["body"])

    for comment in comments:
        words = comment.body.split()
        tickers = list(stock_dict.keys())
        
        print(comment.body)
        for ticker in tickers:
            if ticker[1:] in comment.body.upper():
                stock_dict[ticker] += 1

    df_dict = {
        "Ticker": [ticker for ticker in stock_dict.keys()],
        "Frequency": [freq for freq in stock_dict.values()]
    }
    df = pd.DataFrame.from_dict(df_dict)
    df = df.sort_values(by="Frequency", ascending=False)
    df = df.reset_index(drop=True)

    # Save to CSV
    df.to_csv("wsb_stock_mentions.csv", index=False)
    print("CSV generated")

    # Output top 15 stocks to png
    sub_df = df[df.index < 15]
    barplot = sns.barplot(x="Ticker", y="Frequency", data=sub_df)
    plt.xticks(rotation=90)
    barplot.get_figure().savefig("output.png")
    print("PNG generated")
