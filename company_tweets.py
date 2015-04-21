#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from tweepy import Cursor
from datetime import datetime, timedelta
import sys
import os

#Variables that contains the user credentials to access Twitter API
access_token = "438661609-gUgTPlL5MGJzTFmqihDcl88HQEofSeuMgOzD7X6s"
access_token_secret = "8APdMTZipYyfqdKRrWhHvRplN0gwDGWnlfn9IactTZF3w"
consumer_key = "sFa6HYiNyNao4zFHBwN1xUVD6"
consumer_secret = "M8gF6W6kxTPAlAufkFcmZqNiWPYCAsaiCRR3U6Rrftky5GJ6ba"

def log(file, output):
    file.write("\n" + output)
    print output


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = API(auth)

    now = datetime.now()
    companies = ["TeslaMotors", "Zynga", "SpaceX"]

    for company in companies:
        for lag in range(4):
            midnight = now.replace(hour=00, minute=00, second=00, microsecond=00) - timedelta(days=lag) # modify this to get past info
            cutoff = midnight + timedelta(days=1)
            today = midnight.date()
            print 'Collecting tweets for ' + company + 'for ' + str(today)

            directory = "company_tweet_logs/" + company + "/"
            if not os.path.exists(directory):
                os.makedirs(directory)

            filename = directory + str(today)
            file = open(filename, 'w')

            count = 1
            total_retweets = 0.0
            total_favorites = 0.0
            max_retweet = 0
            max_favorite = 0
            for tweet in Cursor(api.user_timeline, screen_name=company, include_rts=False, lang='en').items(100):
                created = tweet.created_at
                if created > midnight and created < cutoff and tweet.lang == 'en':
                    log(file, "Tweet #" + str(count))
                    log(file, str(tweet._json) + "\n")
                    if(hasattr(tweet, 'retweeted_status')):
                        log(file, "IT'S A RETWEET")
                    total_retweets += tweet.retweet_count
                    total_favorites += tweet.favorite_count
                    if tweet.retweet_count > max_retweet:
                        max_retweet = tweet.retweet_count
                    if tweet.favorite_count > max_favorite:
                        max_favorite = tweet.favorite_count
                    count += 1

            count -= 1
            if count != 0:
                avg_retweet = total_retweets / count
                avg_favorite = total_favorites / count
            else:
                avg_retweet = 0
                avg_favorite = 0
            log(file, "-----------------Daily Statistics-------------------")
            log(file, "Tweets: " + str(count))
            log(file, "Average retweets: " + str(avg_retweet))
            log(file, "Average favorites: " + str(avg_favorite))
            log(file, "Max retweets: " + str(max_retweet))
            log(file, "Max favorites: " + str(max_favorite))