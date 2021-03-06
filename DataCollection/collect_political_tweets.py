import requests
import pandas as pd
from secrets import Bearer_Token
from datetime import datetime
import os

if 'political_tweets_data' not in os.listdir():
	os.mkdir("political_tweets_data")

headers = {'Content-Type': 'application/json; charset=utf-8', 'Authorization': 'Bearer ' + Bearer_Token}

# Add more mps
mp_list = [
	# 'narendramodi', 
	# 'rahulgandhi', 
	# 'nsitharaman', 
	# 'AmitShah', 
	# 'SoniaGandhi_FC', # Not enough tweets, don't uncomment
	# 'ombirlakota',  # Not enough tweets, don't uncomment
	# 'rajnathsingh',
	# 'SashiTharoor', # Not enough tweets, don't uncomment
	# 'nitin_gadkari',
	# 'DrSJaishankar',
	# 'BSYBJP',#not enough tweets,dont uncomment
    #'ArvindKejriwal'
    #'myogiadityanath'
    #'mamataofficial'
    #'PiyushGoyalOffc'
    #'smritiirani'
	#'rsprasad'
	#'CMOTamilNadu'
	#'Dev_Fadnavis'
	#'hd_kumaraswamy' Not enough tweets , dont uncomment
	#'vijayanpinarayi' Not enough tweets , dont uncomment
	#'OfficeofUT'
	'NitishKumar'
]

for mp in mp_list:

	print()
	print("------------------------------------")
	print('MP: ', mp)
	print("------------------------------------")
	print()

	# Get 2000 unique tweets per MP
	tweets_id = []
	tweets_text = []
	tweets_date = []
	tweets_time = []

	day = 31
	hour = 23

	while len(tweets_id) < 2000 and day > 25:
		hour = 23

		while len(tweets_id) < 2000 and hour > 0:
			
			response = requests.get(f"https://api.twitter.com/2/tweets/search/recent?query=(@{mp})+lang:en+-is:retweet+-has:images&max_results=100&end_time=2021-03-{day}T{hour}:30:00Z", headers=headers)

			print(response)

			tweets = response.json()

			print(f"date: 2021-03-{day}")
			print(f"time: {hour}:30:00")

			for tweet in tweets['data']:
				if tweet['id'] not in tweets_id:
					print()
					print(f"date: 2021-03-{day}")
					print(f"time: {hour}:30:00")
					print("-----------------START TWEET-------------------")
					print("id:", tweet['id'])
					print("text:", tweet['text'])
					print("-----------------END TWEET-------------------")
					print()

					tweets_id.append(str(tweet['id']))
					tweets_text.append(tweet['text'])
					tweets_date.append(f"2021-03-{day}")
					tweets_time.append(f"{hour}:30:00")

					print("Number of tweets for ", mp, ": ", len(tweets_id))
			
			
			hour -= 1
		
		day -= 1

	# save tweets to file
	df = pd.DataFrame({'mp': mp, 'tweet_date': tweets_date, 'tweet_time': tweets_time, 'tweet_id': tweets_id, 'tweet_text': tweets_text})

	print(df)

	df.to_csv(f'./political_tweets_data/{mp}_tweets.csv', index=False)
