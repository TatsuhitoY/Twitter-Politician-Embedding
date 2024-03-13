import datetime
import tweepy
tweepy.__version__
import pandas as pd
import csv


consumer_key = 'confidential'
consumer_secret = 'confidential'
access_token= 'confidential'
access_secret = 'confidential'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth, wait_on_rate_limit = True)

#---------------------------------------------------------------------------------------------

df = pd.read_csv("/Users/yoshiharatatsuhito/Desktop/US R. Twitter Handles.csv", header=0)

Fname = list(df['First Name'])
Lname = list(df['Last Name'])
Handles = list(df['Twitter Handles'])
ST = list(df['State/District'])
Party = list(df['Party'])
#422から
identity_list = [[Fname[i], Lname[i], Handles[i], ST[i], Party[i]] for i in range(len(Fname))]
#0~50, 50~100, 100~150, ... , 400~440
file_name = '/Users/yoshiharatatsuhito/Downloads/'
for i in range(len(identity_list)):
  print(f'回数:{i}')
  tz = datetime.timezone(datetime.timedelta(hours=9))
  a = datetime.datetime.now(tz)
  print(f'データ取得日時:{a}')
  print(identity_list[i])
  follower_id = tweepy.Cursor(api.followers_ids, id = identity_list[i][2]).items()
  id_list = []
  for id in follower_id:
    id_list.append(id)

  identity_list[i].append(datetime.datetime.now())
  print(f'フォロワー人数:{len(id_list)}')
  save_list = identity_list[i] + id_list
  name = f'{file_name}{identity_list[i][4]} {identity_list[i][3]}'
  print(name)
  print('\n')

  f = open(f'{name}.csv', 'w')
  writer = csv.writer(f)
  writer.writerow(save_list)
  f.close()

#csvファイルの最初の6行は政治家の情報及びデータ収集時間
