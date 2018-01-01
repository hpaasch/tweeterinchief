from django.shortcuts import render
from django.views.generic.list import ListView
from TwitterAPI import TwitterAPI
import requests
import os
from datetime import datetime

from chief_app.models import Tweet


def popular_tweets(tweeter):
    tw_consumer_key = os.getenv("tw_consumer_key")
    tw_consumer_secret = os.getenv("tw_consumer_secret")
    api = TwitterAPI(tw_consumer_key,
                     tw_consumer_secret,
                     auth_type='oAuth2')

    content = api.request('statuses/user_timeline', {'screen_name': tweeter})
    for tweet in content:
        # adjusted_time = datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S %z %Y')
        # adjusted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y')) # convert Twitter format to python format
        Tweet.objects.update_or_create(
            twt_id = tweet['id'],
            defaults={
            'username': tweet['user']['screen_name'],
            'created_at': tweet['created_at'],
            'adjusted_time': datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S %z %Y'),
            'text': tweet['text'],
            'retweet_count': tweet['retweet_count'],
            'favorite_count': tweet['favorite_count'],
            'popular': (tweet['retweet_count'] + tweet['favorite_count']),
            })

    popular = []
    popular = Tweet.objects.filter(username=tweeter).order_by('-popular')[:3]

    tweet_ids = []  # collecting the IDs to feed into the twitter api
    for tweet in popular:
        tweet_ids.append(tweet.twt_id)

    popular_tweets = []
    for item in tweet_ids:
        tweet = requests.get("https://api.twitter.com/1.1/statuses/oembed.json?id={}".format(item)).json()["html"]
        popular_tweets.append(tweet)
    return popular_tweets

def current_year_popular_tweets(tweeter):
    tw_consumer_key = os.getenv("tw_consumer_key")
    tw_consumer_secret = os.getenv("tw_consumer_secret")
    api = TwitterAPI(tw_consumer_key,
                     tw_consumer_secret,
                     auth_type='oAuth2')

    content = api.request('statuses/user_timeline', {'screen_name': tweeter})
    for tweet in content:
        # adjusted_time = datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S %z %Y')
        # adjusted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y')) # convert Twitter format to python format
        Tweet.objects.update_or_create(
            twt_id = tweet['id'],
            defaults={
            'username': tweet['user']['screen_name'],
            'created_at': tweet['created_at'],
            'adjusted_time': datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S %z %Y'),
            'text': tweet['text'],
            'retweet_count': tweet['retweet_count'],
            'favorite_count': tweet['favorite_count'],
            'popular': (tweet['retweet_count'] + tweet['favorite_count']),
            })

    popular = []
    popular = Tweet.objects.filter(username=tweeter).filter(adjusted_time__range=["2018-01-01", "2018-12-31"]).order_by('-popular')[:25]

    tweet_ids = []  # collecting the IDs to feed into the twitter api
    for tweet in popular:
        tweet_ids.append(tweet.twt_id)

    current_year_popular_tweets = []
    for item in tweet_ids:
        tweet = requests.get("https://api.twitter.com/1.1/statuses/oembed.json?id={}".format(item)).json()["html"]
        current_year_popular_tweets.append(tweet)
    return current_year_popular_tweets

def popular_tweets_2017(tweeter):
    popular = []
    # TODO: add filter for only 2017 dates. remember: adjusted_time did not exist before Jan. 1, 2018
    popular = Tweet.objects.filter(username=tweeter).order_by('-popular')[:25]

    tweet_ids = []  # collecting the IDs to feed into the twitter api
    for tweet in popular:
        tweet_ids.append(tweet.twt_id)

    popular_tweets_2017 = []
    for item in tweet_ids:
        tweet = requests.get("https://api.twitter.com/1.1/statuses/oembed.json?id={}".format(item)).json()["html"]
        popular_tweets_2017.append(tweet)
    return popular_tweets_2017

def recent_tweets(tweeter):
    recent = []
    recent = Tweet.objects.filter(username=tweeter).order_by('-created_at')[:5]

    tweet_ids = []  # collecting the IDs to feed into the twitter api
    for tweet in recent:
        tweet_ids.append(tweet.twt_id)

    recent_tweets = []
    for item in tweet_ids:
        tweet = requests.get("https://api.twitter.com/1.1/statuses/oembed.json?id={}".format(item)).json()["html"]
        recent_tweets.append(tweet)
    return recent_tweets


class TrumpTweetListView(ListView):
    model = Tweet
    template_name = 'tweet_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_year_rdt_tweets = current_year_popular_tweets('realDonaldTrump')
        # realDonaldTrump_tweets = popular_tweets('realDonaldTrump')
        # POTUS_tweets = popular_tweets('POTUS')
        recent_rdt_tweets = recent_tweets('realDonaldTrump')
        # recent_potus_tweets = recent_tweets('POTUS')

        context = {
            # 'recent_potus_tweets': recent_potus_tweets,
            'recent_rdt_tweets': recent_rdt_tweets,
            # 'realDonaldTrump_tweets': realDonaldTrump_tweets,
            # 'POTUS_tweets': POTUS_tweets,
            'current_year_rdt_tweets': current_year_rdt_tweets,
            }
        return context

class Trump2017ListView(ListView):
    model = Tweet
    template_name = '2017_recap.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year_one_rdt_tweets = popular_tweets_2017('realDonaldTrump')
        year_one_potus_tweets = popular_tweets_2017('POTUS')

        context = {
            'year_one_rdt_tweets': year_one_rdt_tweets,
            'year_one_potus_tweets': year_one_potus_tweets,
        }
        return context
