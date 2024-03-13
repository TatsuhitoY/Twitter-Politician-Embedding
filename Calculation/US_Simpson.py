import csv
import pandas as pd
import datetime

df = pd.read_csv("/Users/yoshiharatatsuhito/Desktop/T.Yoshihara/計算社会科学/Twitter_congress/Twitterアカウントデータ/US R. Twitter Handles.csv", header=0)

Fname = list(df['First Name'])
Lname = list(df['Last Name'])
Handles = list(df['Twitter Handles'])
ST = list(df['State/District'])
Party = list(df['Party'])

identity_list = [[Fname[i], Lname[i], Handles[i], ST[i], Party[i]] for i in range(len(Fname))]

total_list = []
# for i in range(len(identity_list)):
total_number = 0
account_num = 0

#以下のfor文では全ての政治家のフォロワー数を数えて、フォロワーを全てtotal_listに格納している
for i in range(len(identity_list)):
    filename = f'/Users/yoshiharatatsuhito/Desktop/T.Yoshihara/計算社会科学/Twitter_congress/データ(US)/{identity_list[i][4]} {identity_list[i][3]}.csv'
    with open(filename, encoding='utf8', newline='') as f:
        csvreader = csv.reader(f)
        lists=[]
        for row in csvreader:
          lists += row
        detail_list = identity_list[i]
        for j in range(6):
            del lists[0]
        unique_set = set(lists)
        final_list = list(unique_set)
        final_list.append(detail_list)
        print(f'{i}番目の政治家')
        print(f'{identity_list[i][4]} {identity_list[i][3]}のフォロワー数：', len(final_list)-1)
        total_number += len(final_list)-1
        #total_listは全てのフォロワーを格納するリスト
        total_list.append(final_list)
        account_num += 1
print(f'Total number of  follower:{total_number}')
print(f'Total number of politician account:{account_num}')

s = datetime.datetime.now()
simpson_m = []
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
            cal_num = (len(common))/min((len(a)-1), (len(b)-1))
            if cal_num >= 0.9:
                print(f'{a[-1]} {b[-1]}')
            simpson_m.append(cal_num)

e = datetime.datetime.now()
print(f'Computation Time：{e - s}')
f = open('/Users/yoshiharatatsuhito/Desktop/T.Yoshihara/計算社会科学/Twitter_congress/整形済みデータ/Simpson(US).csv', 'w')
data = simpson_m
writer = csv.writer(f)
writer.writerow(data)
f.close()
