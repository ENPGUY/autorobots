# news_bot.py
# -*- coding: utf-8 -*-

import feedparser
import tweepy
import json
import os
import time

# -------------------------------
# 1. 트위터 API 인증 정보
# -------------------------------
API_KEY = "YOUR_API_KEY"
API_SECRET = "YOUR_API_SECRET"
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
ACCESS_SECRET = "YOUR_ACCESS_SECRET"

auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# -------------------------------
# 2. 트윗 중복 방지용 기록 파일
# -------------------------------
TWEETED_FILE = "tweeted.json"
if os.path.exists(TWEETED_FILE):
    with open(TWEETED_FILE, "r", encoding="utf-8") as f:
        tweeted_links = set(json.load(f))
else:
    tweeted_links = set()

# -------------------------------
# 3. RSS 뉴스 수집
# -------------------------------
RSS_URL = "https://rss.nytimes.com/services/xml/rss/nyt/World.xml"
feed = feedparser.parse(RSS_URL)

for entry in feed.entries[:5]:  # 최신 5개 뉴스
    title = entry.title
    link = entry.link

    if link in tweeted_links:
        continue  # 이미 트윗한 뉴스는 건너뛰기

    tweet = f"{title}\n{link}"

    try:
        api.update_status(tweet)
        print(f"트윗 완료: {title}")
        tweeted_links.add(link)
        time.sleep(2)  # 트위터 API Rate 제한 대비
    except Exception as e:
        print(f"트윗 실패: {e}")

# -------------------------------
# 4. 트윗 기록 저장
# -------------------------------
with open(TWEETED_FILE, "w", encoding="utf-8") as f:
    json.dump(list(tweeted_links), f, ensure_ascii=False)
