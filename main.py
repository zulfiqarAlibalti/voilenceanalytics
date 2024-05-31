import pandas as pd
import nltk
import newspaper
from newspaper import Article, Config
import pymongo
from datetime import datetime

def main():
    nltk.download('punkt')

    # Connect to MongoDB
    client = pymongo.MongoClient("mongodb://localhost:27017/")  # Update with your MongoDB connection string
    db = client["dashboard"]  # Use the desired database name
    collection = db["news"]

    # Create a compound index on 'Title' and 'Publish Date' fields
    collection.create_index([('Title', pymongo.ASCENDING), ('Publish Date', pymongo.ASCENDING)], unique=True)

    # Define the URL and build the newspaper
    url = 'https://www.dawn.com/'
    config = Config()
    config.memoize_articles = False
    paper = newspaper.build(url, language="en", config=config)

    # Keywords to filter articles
    keywords_to_filter = ["blasphemy", "terrorism", "violence"]  
    filtered_data_dict = {keyword: [] for keyword in keywords_to_filter}

    # Extracting news articles' details
    for article in paper.articles:
        try:
            article.download()
            article.parse()
            article.nlp()

            # Filter articles containing any of the keywords
            for keyword in keywords_to_filter:
                if keyword.lower() in article.text.lower() or keyword.lower() in article.title.lower():
                    # Prepare data
                    data = {
                        'Title': article.title,
                        'URL': article.url,
                        'Authors': article.authors,
                        'Publish Date': article.publish_date,
                        'Text': article.text,
                        'Keywords': article.keywords,
                        'Top Image': article.top_image,
                        'Summary': article.summary
                    }

                    try:
                        # Try to insert the data into MongoDB
                        collection.insert_one(data)
                        filtered_data_dict[keyword].append(data)  # Append to filtered data dict
                    except pymongo.errors.DuplicateKeyError as e:
                        # Handle duplicate key error (article with same title and publish date already exists)
                        print(f"Duplicate article found: {article.title} - {article.publish_date}")
                        continue
        except Exception as e:
            print(e)
            continue

    # Convert the filtered data to CSV files for each keyword
    for keyword, filtered_data in filtered_data_dict.items():
        if filtered_data:
            keyword_csv_filename = f"{keyword}.csv"
            pd.DataFrame(filtered_data).to_csv(keyword_csv_filename, index=False)
            print(f"Filtered data for '{keyword}' saved as '{keyword_csv_filename}' in the current directory.")

if __name__ == "__main__":
    main()
