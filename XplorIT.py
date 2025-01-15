from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import csv
import os


message = input('message: ')

analyzer = SentimentIntensityAnalyzer()

def get_sentiment(text):
    sentiment = analyzer.polarity_scores(text)
    compound_score = sentiment['compound']
    return compound_score

sentiment_entry = get_sentiment(message)

output_file = 'SeafarerSentiment.csv'

with open(output_file, mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Message', 'Sentiment Score'])
    writer.writerow([message, sentiment_entry])

print(f"Saved to {output_file}.")
