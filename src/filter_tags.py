import pandas as pd
from collections import Counter

df = pd.read_csv("../data/cleaned_movies.csv")

all_tags = []

for tags in df["tags"].dropna():
    split_tags = [tag.strip() for tag in tags.split(",")]
    all_tags.extend(split_tags)

tag_counter = Counter(all_tags)

most_common = tag_counter.most_common(100)
filtered_tags = [tag for tag, count in most_common]

with open("../data/filtered_tags.txt", "w") as f:
    for tag in sorted(filtered_tags):
        f.write(tag + "\n")

print("Written Filtered Tags to data folder.")