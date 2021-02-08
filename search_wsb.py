from psaw import PushshiftAPI
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

api = PushshiftAPI()

start_time = int(datetime.datetime(2021, 2, 4).timestamp())

submissions = api.search_submissions(after=start_time,
                            subreddit="wallstreetbets",
                            filter=["url", "author", "title", "subreddit"])

stock_dict = {}
for submission in submissions:
    words = submission.title.split()
    cashtags = list(set(filter(lambda word: word.lower().startswith('$'), words)))
    
    if len(cashtags) > 0:
        for cashtag in cashtags:
            if cashtag[1:].isalpha():
                formatted_cashtag = cashtag.upper()
                stock_dict.setdefault(formatted_cashtag, 0)
                stock_dict[formatted_cashtag] += 1

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

# Output to 15 stocks to png
sub_df = df[df.index < 15]
barplot = sns.barplot(x="Ticker", y="Frequency", data=sub_df)
plt.xticks(rotation=90)
barplot.get_figure().savefig("output.png")
print("PNG generated")
