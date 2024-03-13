import datetime
import glob
import csv
import pandas as pd

total_number = 0
account_num = 0

l = glob.glob('/Users/yoshiharatatsuhito/Desktop/T.Yoshihara/計算社会科学/Twitter_congress/データ(Japan)2/*')
total_list2 = []
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
each_num = []
real_total_list = []

tri = []
for i in range(len(identity_list)):
    for j in range(len(total_list2)):
        if identity_list[i][2] == total_list2[j][2]:
            detail_list = identity_list[i]
            print(f'データ取得日時：{total_list2[j][5]}')
            for k in range(6):
                del total_list2[j][0]
            unique_set = set(total_list2[j])
            #ここの処理でTwitter特有の同じユーザーというバグを直している
            final_list = list(unique_set)
            #total_list2の順番はidentity_listと一致していないけどfor文とif文のおかげでここのtotal_list2の抽出される要素の順番はidentity_listと同じ
            each_num.append(len(final_list))
            #eachnumの数字はIdentity_listの順番と一致している
            real_total_list += final_list
            final_list.append(detail_list)
            tri.append(identity_list[i][4])
            print(f'{i}番目の政治家')
            print(f'{identity_list[i][4]}_{identity_list[i][3]}_{identity_list[i][0]}のフォロワー数：', len(final_list)-1, '\n')
            total_list += total_list2[j]
tri = list(set(tri))
print('hi', tri)

total_number2 = len(set(total_list))
print(f'Total number of  follower(重複あり):{total_number}')
print(f'Total number of  follower:{total_number2}')
print(f'Total number of politician account:{account_num}')

jimin = 0
rikken = 0
ishin = 0
koumei = 0
kyousan = 0
reshin = 0
kokumin = 0
syamin = 0
other = 0


for i in range(len(identity_list)):
    if identity_list[i][4] == '自民':
        jimin += each_num[i]
    elif identity_list[i][4] == '立憲':
        rikken += each_num[i]
    elif identity_list[i][4] == '維新':
        ishin += each_num[i]
    elif identity_list[i][4] == '公明':
        koumei += each_num[i]
    elif identity_list[i][4] == '共産':
        kyousan += each_num[i]
    elif identity_list[i][4] == 'れ新':
        reshin += each_num[i]
    elif identity_list[i][4] == '国民':
        kokumin += each_num[i]
    elif identity_list[i][4] == '社民党':
        syamin += each_num[i]
    else:
        other += each_num[i]

print('自民', jimin)
print('立憲', rikken)
print('維新', ishin)
print('公明', koumei)
print('共産', kyousan)
print('れ新', reshin)
print('国民', kokumin)
print('社民', syamin)
print('その他', other)

real_number = len(set(real_total_list))
print(f'real_number:{real_number}')
print(len(each_num))
# f = open('/Users/yoshiharatatsuhito/Desktop/T.Yoshihara/計算社会科学/Twitter_congress/整形済みデータ/JP_follower_count.csv', 'w')
# data = each_num
# writer = csv.writer(f)
# writer.writerow(data)
# f.close()
