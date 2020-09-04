import os
import tweepy


def tweet(text):
    CONSUMER_KEY = os.getenv("TWITTER_UoA_BOT_API_KEY")
    CONSUMER_SECRET = os.getenv("TWITTER_UoA_BOT_API_SECRET_KEY")
    ACCESS_TOKEN = os.getenv("TWITTER_UoA_BOT_ACCESS_TOKEN")
    ACCESS_TOKEN_SECRET = os.getenv("TWITTER_UoA_BOT_ACCESS_TOKEN_SECRET")

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    api.update_status(text)

    return text


if __name__ == "__main__":
    tweet("test")
