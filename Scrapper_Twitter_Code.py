import json
import time
import requests
from ntscraper import Nitter

def search_twitter(accounts, ticker, interval_minutes):
    while True:
        total_mentions = 0
        current_time = time.strftime("%H:%M:%S", time.localtime())
        all_tweets = []  # List to store all tweets scraped

        for account in accounts:
            attempts = 3  # Number of retry attempts
            while attempts > 0:
                try:
                    # Get tweets for the entered username
                    response = Nitter().get_tweets(account, mode='user', number=100)
                    tweets = response.get('tweets', [])  # Extract tweets from the response
                    for tweet in tweets:
                        if 'text' in tweet and f'${ticker}' in tweet['text']:
                            total_mentions += 1
                        all_tweets.append(tweet)  # Add tweet to the list
                    break  # Break out of retry loop if successful
                except (requests.exceptions.RequestException, ConnectionResetError) as e:
                    print(f"Error fetching tweets: {repr(e)}. Retrying...")
                    attempts -= 1
                    time.sleep(5)  # Wait before retrying
        
        print(f"'${ticker}' was mentioned '{total_mentions}' times in the last '{interval_minutes}' minutes at '{current_time}'.")

        # Save the tweets to a JSON file
        output_file = f"{ticker}_tweets_{time.strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(output_file, 'w') as file:
                json.dump(all_tweets, file, indent=4)
            print(f"All tweets have been saved to '{output_file}'.")
        except Exception as e:
            print(f"Error saving tweets to '{output_file}': {repr(e)}")

        # Sleep for the specified interval before scraping again
        time.sleep(interval_minutes * 60)

# Example usage with predefined inputs [ with our 10 accounts provided ]
accounts = ['Mr_Derivatives', 'warrior_0719', 'ChartingProdigy', 'allstarcharts', 'yuriymatso',
            'TriggerTrades', 'AdamMancini4', 'CordovaTrades', 'Barchart', 'RoyLMattox']
ticker = 'TSLA'  # change this ticker symbol as needed
interval_minutes = 60  # change this interval as needed

search_twitter(accounts, ticker, interval_minutes)


#https://twitter.com/Mr_Derivatives 
#https://twitter.com/warrior_0719
#https://twitter.com/ChartingProdigy
#https://twitter.com/allstarcharts
#https://twitter.com/yuriymatso
#https://twitter.com/TriggerTrades
#https://twitter.com/AdamMancini4 
#https://twitter.com/CordovaTrades 
#https://twitter.com/Barchart
#https://twitter.com/RoyLMattox

