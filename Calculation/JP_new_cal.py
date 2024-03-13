import datetime
import glob
import csv
import pandas as pd

total_number = 0
account_num = 0

l = glob.glob('/Users/yoshiharatatsuhito/Desktop/T.Yoshihara/計算社会科学/Twitter_congress/データ(Japan)2/*')
total_list2 = []
handle_list = []
for i in l:
    filename = f'{i}'
    contents = []
    with open(filename, encoding='utf8', newline='') as f:
        csvreader = csv.reader(f)
        lists = []
        for row in csvreader:
          lists += row
    for i in lists:
        contents.append(i)
    total_list2.append(contents)
    total_number += (len(contents) - 6)
    account_num += 1

    Kname = contents[0]
    Hname = contents[1]
    Handles = contents[2]
    ST = contents[3]
    Party = contents[4]
    print(Kname, Hname, ST, Party)

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
identity_list = [[Kname[i], Hname[i], Handles[i], ST[i], Party[i]] for i in range(len(Kname))]

total_list = []

for i in range(len(identity_list)):
    for j in range(len(total_list2)):
        if identity_list[i][2] == total_list2[j][2]:
            detail_list = identity_list[i]
            for k in range(6):
                del total_list2[j][0]
            unique_set = set(total_list2[j])
            final_list = list(unique_set)
            final_list.append(detail_list)
            print(f'{i}番目の政治家')
            print(f'{identity_list[i][4]}_{identity_list[i][3]}_{identity_list[i][0]}のフォロワー数：', len(final_list)-1)
            total_list.append(total_list2[j])

print(f'Total number of  follower:{total_number}')
print(f'Total number of politician account:{account_num}')

s = datetime.datetime.now()
new_cal_m = []
c = 0
#sum_listはリストインリストで全てのフォロワーが格納されている
for a in total_list:
    #上三角行列を全て埋める分の要素を作成、リストインリストではなくただのリスト
    c += 1
    d = 0
    print(f'{int(100*c/account_num)}%')
    for b in total_list:
        d += 1
        if d > c:
            common = set(a[:-1]) & set(b[:-1])
            #aとbのリストにはそれぞれ不要な要素が一つあるので（アカウント情報のリスト）その文を差し引いてる
            cal_num = ((len(common))/(len(a)-1)) * ((len(common))/(len(b)-1))
            if cal_num >= 0.9:
                print(f'{a[-1]} {b[-1]}')
            new_cal_m.append(cal_num)

e = datetime.datetime.now()
print(f'Computation Time：{e - s}')
f = open('/Users/yoshiharatatsuhito/Desktop/T.Yoshihara/計算社会科学/Twitter_congress/整形済みデータ/New_cal(JP).csv', 'w')
data = new_cal_m
writer = csv.writer(f)
writer.writerow(data)
f.close()
