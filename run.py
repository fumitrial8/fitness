# -*- coding: utf-8 -*-
from CREDENTIAL import ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_KEY_SECRET
import csv
import json
import requests

from flask import Flask, request,redirect, send_file, render_template
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from bs4 import BeautifulSoup
from janome.tokenizer import Tokenizer
from collections import Counter, defaultdict
from requests_oauthlib import OAuth1Session


app = Flask(__name__, static_folder='static')

fpath = "./Koruri-Regular.ttf"
output = './static/tweet.png'
def counter(texts):
    t = Tokenizer()
    words_count = defaultdict(int)
    words = []
    for text in texts:
        tokens = t.tokenize(text)
        for token in tokens:
            #品詞から名詞だけ抽出
            pos = token.part_of_speech.split(',')[0]
            if pos == '名詞':
                words_count[token.base_form] += 1
                words.append(token.base_form)
    return words_count, words


def post_request(value,CONSUMER_KEY=CONSUMER_KEY, CONSUMER_KEY_SECRET=CONSUMER_KEY_SECRET, ACCESS_TOKEN=ACCESS_TOKEN, ACCESS_TOKEN_SECRET=ACCESS_TOKEN_SECRET):
    url = "https://api.twitter.com/1.1/search/tweets.json"
    params = {
              'q': value,
              'count':200,
              'exclude': 'retweets'}
    twitter = OAuth1Session(CONSUMER_KEY, CONSUMER_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    response = twitter.get(url, params = params)
    return response


def make_corpus(timeline):
    f_out = open('./tweet.txt', 'w')
    try:
      for tweet in timeline['statuses']:
        f_out.write(tweet['text']+'\n')
    except:
      f_out.write(timeline)
    f_out.close()

@app.route('/')
def home():
    return render_template("./index.html")

@app.route('/analize', methods=["POST"])
def analize():
    tweet = request.form["tweet"]
    res = post_request(tweet)
    if res.status_code == 200:
      limit = res.headers['x-rate-limit-remaining']
      if limit == 1:
        sleep(60*15)
      n = 0
      timeline = json.loads(res.text)
    else:
      return "false"
    #名詞だけ抽出、単語をカウント
    make_corpus(timeline)
    with open('./tweet.txt','r') as f:
        reader = csv.reader(f, delimiter='\t')
        texts = []
        for row in reader:
            if len(row)>0:
              text = row[0].split('http')
              texts.append(text[0])

    words_count, words = counter(texts)
    text = ' '.join(words)
    wordcloud = WordCloud(background_color="white", font_path=fpath, width=900, height=500).generate(text)
    wordcloud.to_file(output)
    return redirect("result")

@app.route('/result', methods=["GET"])
def result():
    return "<img src='/static/tweet.png' alt='pic01'></img><a href='/'>戻る</a>"

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)