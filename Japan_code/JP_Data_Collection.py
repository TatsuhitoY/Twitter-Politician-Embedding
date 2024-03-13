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

df = pd.read_csv("/Users/yoshiharatatsuhito/Desktop/T.Yoshihara/計算社会科学/Twitter_congress/Twitterアカウントデータ/JP R. Twitter Handles.csv", header=0)

Kname = list(df['Kanji Name'])
Hname = list(df['Hiragana Name'])
Handles = list(df['Twitter Handles'])
ST = list(df['State/District'])
Party = list(df['Party'])
for i in range(len(Kname)):
  Kname[i] = Kname[i].replace('\u3000\u3000', ' ')
  Kname[i] = Kname[i].replace('君', '')
  Hname[i] = Hname[i].replace('\u3000', '')
  Hname[i] = Hname[i].replace('君', '')
#193
identity_list = [[Kname[i], Hname[i], Handles[i], ST[i], Party[i]] for i in range(len(Kname))]
#0~50, 50~100, 100~150, ... , 400~440
file_name = '/Users/yoshiharatatsuhito/Desktop/hi/'
# for i in range(193, len(identity_list)):
# [2, 3, 4, 5, 10, 11, 12, 17, 18, 20, 21, 22, 25, 26, 29, 30, 31, 35, 36, 38, 39, 42, 47, 50, 56, 58, 60, 71, 72, 74, 76, 77, 80, 85, 93, 94, 96, 99, 101, 102, 104, 105, 115, 118, 119, 122, 136, 137, 139, 145, 149, 150, 151, 154, 157, 160, 162, 167, 168, 169, 174, 175, 176, 177, 179, 187, 188, 191, 194, 195, 196, 200, 203, 204, 205, 207, 208, 211, 212, 214, 215, 216, 218, 219, 220, 224, 226, 227, 229, 232, 233, 235, 239, 241, 246, 248, 249, 250, 251, 252, 254, 255, 257, 261, 263, 266, 268, 281, 287, 288, 291, 292, 296, 298, 303, 305, 311, 313, 315, 319, 320, 322, 325, 327, 329, 335, 337, 338, 340, 347, 348, 351, 352, 353, 355, 358, 361, 362, 364, 365, 366, 372, 373, 375, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 394, 395, 397, 400]
for i in [382, 383, 384, 385, 386, 387, 388, 389, 394, 395, 397, 400]:
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
  name = f'{file_name}{identity_list[i][4]}_{identity_list[i][3]}_{identity_list[i][1]}'
  print(name)
  print('\n')

  f = open(f'{name}.csv', 'w')
  writer = csv.writer(f)
  writer.writerow(save_list)
  f.close()

#csvファイルの最初の6行は政治家の情報及びデータ収集時間
