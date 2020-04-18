import csv
import json
from flask import Flask, request,redirect, send_file, render_template
import requests
from requests_oauthlib import OAuth1Session
from CREDENTIAL import ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_KEY_SECRET

from janome.tokenizer import Tokenizer
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from bs4 import BeautifulSoup
from collections import Counter, defaultdict



app = Flask(__name__, static_folder='static')


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


@app.route('/')
def home():
    return render_template("./index.html")

@app.route('/analize', methods=["POST"])
def analize():
    tweet = request.form["tweet"]
    url = "https://api.twitter.com/1.1/search/tweets.json"
    params = {
              'q': tweet,
              'count':200,
              'exclude': 'retweets'}
    
    twitter = OAuth1Session(CONSUMER_KEY, CONSUMER_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    res = twitter.get(url, params = params)
    print(res)
    f_out = open('./tweet.txt', 'w')
    if res.status_code == 200:
      limit = res.headers['x-rate-limit-remaining']
      if limit == 1:
        sleep(60*15)
      n = 0
      timeline = json.loads(res.text)
      for tweet in timeline['statuses']:
        f_out.write(tweet['text']+'\n')
    f_out.close()
    #名詞だけ抽出、単語をカウント

    with open('./tweet.txt','r') as f:
        reader = csv.reader(f, delimiter='\t')
        texts = []
        for row in reader:
            if len(row)>0:
              text = row[0].split('http')
              texts.append(text[0])

    words_count, words = counter(texts)
    text = ' '.join(words)
    fpath = "./Koruri-Regular.ttf"
    wordcloud = WordCloud(background_color="white", font_path=fpath, width=900, height=500).generate(text)
    wordcloud.to_file('./static/tweet.png')
    return redirect("result")

@app.route('/result', methods=["GET"])
def result():
    return "<img src='/static/tweet.png' alt='pic01'></img><a href='/'>戻る</a>"

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)