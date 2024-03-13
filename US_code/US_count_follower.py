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
# for i in range(len(identity_list)):
real_total_list = []
total_number = 0
account_num = 0
each_num = []
#以下のfor文では全ての政治家のフォロワー数を数えて、フォロワーを全てtotal_listに格納している
for i in range(len(identity_list)):
    filename = f'/Users/yoshiharatatsuhito/Desktop/T.Yoshihara/計算社会科学/Twitter_congress/データ(US)/{identity_list[i][4]} {identity_list[i][3]}.csv'
    with open(filename, encoding='utf8', newline='') as f:
        csvreader = csv.reader(f)
        lists=[]
        for row in csvreader:
          lists += row
        detail_list = identity_list[i]
        print(f'データ取得日時：{lists[5]}')
        for j in range(6):
            del lists[0]
        unique_set = set(lists)
        final_list = list(unique_set)
        real_total_list += final_list
        print(f'{i}番目の政治家')
        print(f'{identity_list[i][0]} {identity_list[i][1]}')
        print(f'{identity_list[i][4]} {identity_list[i][3]}のフォロワー数：', len(final_list), '\n')

        total_number += len(final_list)
        #total_listは全てのフォロワーの数を格納するリスト
        each_num.append(len(final_list))
        account_num += 1
total_number2 = len(set(real_total_list))
print(f'Total number of  follower:{total_number}')
print(f'Total number of  follower(dup removed)):{total_number2}')
print(f'Total number of politician account:{account_num}')

# real_number = len(list(set(real_total_list)))
# print(f'real_number:{real_number}')

f = open('/Users/yoshiharatatsuhito/Desktop/T.Yoshihara/計算社会科学/Twitter_congress/整形済みデータ/US_follower_count.csv', 'w')
data = each_num
writer = csv.writer(f)
writer.writerow(data)
f.close()
