from django.shortcuts import render
from django.views.generic.list import ListView
from TwitterAPI import TwitterAPI
import requests
import os

from chief_app.models import Tweet


def popular_tweets(tweeter):
    tw_consumer_key = os.getenv("tw_consumer_key")
    tw_consumer_secret = os.getenv("tw_consumer_secret")
    api = TwitterAPI(tw_consumer_key,
                     tw_consumer_secret,
                     auth_type='oAuth2')

    content = api.request('statuses/user_timeline', {'screen_name': tweeter})
    for tweet in content:
        Tweet.objects.update_or_create(
            twt_id = tweet['id'],
            defaults={
            'username': tweet['user']['screen_name'],
            'created_at': tweet['created_at'],
            'text': tweet['text'],
            'retweet_count': tweet['retweet_count'],
            'favorite_count': tweet['favorite_count'],
            'popular': (tweet['retweet_count'] + tweet['favorite_count']),
            })

    popular = []
    popular = Tweet.objects.filter(username=tweeter).order_by('-popular')[:20]

    tweet_ids = []  # collecting the IDs to feed into the twitter api
    for tweet in popular:
        tweet_ids.append(tweet.twt_id)

    popular_tweets = []
    for item in tweet_ids:
        tweet = requests.get("https://api.twitter.com/1.1/statuses/oembed.json?id={}".format(item)).json()["html"]
        popular_tweets.append(tweet)
    return popular_tweets


class TrumpTweetListView(ListView):
    model = Tweet

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        top_tweets = popular_tweets('realDonaldTrump')

        context = {

            'popular_tweets': top_tweets,
            }
        return context
