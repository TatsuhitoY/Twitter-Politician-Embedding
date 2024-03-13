import csv
import pickle
import numpy as np
import pandas as pd
import glob
from tqdm import tqdm
import time
import matplotlib.pyplot as plt
import gensim
import datetime
s = datetime.datetime.now()
#------------------------------------------------------------
#1 create a set of all users
#2 create dictionary that has users as keys and politicians that each users follow as items
#3 create a list of each political party that contains followers
#4 calculate the diversity_score for each followers in the list made on step 3
#5 create histograms for each political party
#6 calculate parameter for power of law
#7 do the steps 3~6 but remove followers with just one politician
#------------------------------------------------------------

#1 create a set of all users
df = pd.read_csv("/Users/yoshiharatatsuhito/Desktop/T.Yoshihara/計算社会科学/Twitter_congress/Twitterアカウントデータ/US R. Twitter Handles.csv", header=0)
Fname = list(df['First Name'])
Lname = list(df['Last Name'])
Handles = list(df['Twitter Handles'])
ST = list(df['State/District'])
Party = list(df['Party'])
identity_list = [[Fname[i], Lname[i], Handles[i], ST[i], Party[i]] for i in range(len(Fname))]

#各政治家のファイルを全て開けてそこに保存されているユーザーの集合を作成
total_number = 0
account_num = 0

l = glob.glob('/Users/yoshiharatatsuhito/Desktop/T.Yoshihara/計算社会科学/Twitter_congress/データ(US)/*')
total_list2 = []
ctotal_list = []
bar1 = tqdm(total = 439, colour = 'green')
bar1.set_description('bar1 Counting users of politician')
#以下のfor文で出てくるcontentsというのは各政治家のフォロワーのuser_id、これを全ての政治家について集めたものがtotal_list2
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

    #ctotal_listには----(大事)最初のファイルの順番で----[政治家のidentity_list, [フォロワー1, フォロワー2, フォロワー3, ....]]が格納される。
    #contentsは各政治家について作り[firstname, lastname, handles, st, party, user1, user2...]
    for k in identity_list:
        if k[2] == contents[2]:
            ctotal_list.append([k, list(set(contents[6:]))])

    total_list2 += contents[6:]
    total_number += (len(contents) - 6)
    account_num += 1
    #ここから先は各政治家の情報をprintするための処理
    Fname = contents[0]
    Lname = contents[1]
    Handles = contents[2]
    ST = contents[3]
    Party = contents[4]
    # print(Fname, Lname, ST, Party, f"フォロワー数：{len(contents) - 6}")
    bar1.update(1)
    time.sleep(0.005)

print('\npoint -3 pass', datetime.datetime.now() - s)
#total_list2には全てのユーザーのTwitter Handlesが重複ありで入っている
real_list = list(set(total_list2))
print('\npoint -2 pass', datetime.datetime.now() - s)
print(f'\nフォロワー数（重複あり）:{total_number}')
print('\npoint -1 pass', datetime.datetime.now() - s)
print(f'フォロワー数（重複なし）:{len(set(total_list2))}')
print('\npoint 0 pass', datetime.datetime.now() - s)
print(f'政治家の数:{account_num}')

simpson係数 = 0
print('\npoint 1 pass', datetime.datetime.now() - s)
with open(f'/Users/yoshiharatatsuhito/Desktop/T.Yoshihara/計算社会科学/Twitter_congress/整形済みデータ/Embedding/US_EMB_simpson={simpson係数}_real_dict.pkl', "rb") as tf:
    real_dict = pickle.load(tf)
#real_dictの形は ...'1451524260107853857': ['314'], '119507717': ['314'], '907544341136265216': ['314'], '1110248788575293445': ['314'], '31516782': ['326', '29', '314']}
print('\npoint 2 pass', datetime.datetime.now() - s)
with open(f'/Users/yoshiharatatsuhito/Desktop/T.Yoshihara/計算社会科学/Twitter_congress/整形済みデータ/Embedding/US_EMB_simpson={simpson係数}_real_dict2.pkl', "rb") as tf:
    real_dict2 = pickle.load(tf)
print('\npoint 3 pass', datetime.datetime.now() - s)
with open(f'/Users/yoshiharatatsuhito/Desktop/T.Yoshihara/計算社会科学/Twitter_congress/整形済みデータ/Embedding/US_EMB_simpson={simpson係数}_real_dict3.pkl', "rb") as tf:
    real_dict3 = pickle.load(tf)
print('\npoint 4 pass', datetime.datetime.now() - s)
#3 create a list of each political party that contains followers
d_list = []
r_list = []
dr_list = []

# bar2 = tqdm(total = len(real_dict), colour = 'green')
# bar2.set_description('bar2 Checking political party')
# for i in real_dict.keys():
#     bar2.update(1)
#     for j in range(len(real_dict[i])):
#         if identity_list[int(real_dict[i][j])][4] == "D":
#             d_list.append(i)
#         else:
#             r_list.append(i)

total_list_a = []
total_score_a = []
bar2 = tqdm(total = len(real_dict), colour = 'green')
bar2.set_description('bar2 Checking political party')
for i in real_dict.keys():
    bar2.update(1)
    for j in range(len(real_dict[i])):
        total_list_a.append(i)

# 旧
# bar2 = tqdm(total = len(real_dict), colour = 'green')
# bar2.set_description('bar2 Checking political party')
# for i in real_dict.keys():
#     bar2.update(1)
#     for j in range(len(real_dict[i])):
#         if identity_list[int(real_dict[i][j])][4] == "D":
#             d_list.append(i) #ここでiはフォロワーのID、このリストの内容はdemocratic partyをフォローしている人のユーザーID
#         else:
#             r_list.append(i)

# 新
# bar3 = tqdm(total = len(total_list_a), colour = 'green')
# bar3.set_description('bar3 Calculating user diversity score')
# #ヒストグラムに使うユーザーのDiversity Scoreを計算
# for j in total_list_a:
#     bar3.update(1)
#     total_score_a.append(real_dict3[j]) #total_scoreの中には二つのリスト、それぞれのリストの中にその政党をフォローしている人のIDがある


# d_scores = []
# r_scores = []
#
# total_list = [d_list, r_list]
# total_score = [d_scores, r_scores]
#
# bar3 = tqdm(total = len(total_list[0] + total_list[1]), colour = 'green')
# bar3.set_description('bar3 Calculating user diversity score')
# #ヒストグラムに使うユーザーのDiversity Scoreを計算
# for i in range(len(total_list)):
#     for j in total_list[i]:
#         bar3.update(1)
#         total_score[i].append(real_dict3[j]) #total_scoreの中には二つのリスト、それぞれのリストの中にその政党をフォローしている人のIDがある

new_score_a = [[] for i in range(4)]

num1 = 3
num2 = 5
num3 = 10
num4 = 30
bar4 = tqdm(total = len(total_list_a), colour = 'green')
bar4.set_description('bar4 Checking bin')

for j in total_list_a:
        bar4.update(1)
        if len(real_dict[j]) >= num1 and len(real_dict[j]) <= (num2 - 1):
            new_score_a[0].append(real_dict3[j])
        elif len(real_dict[j]) >= num2 and len(real_dict[j]) <= (num3 - 1):
            new_score_a[1].append(real_dict3[j])
        elif len(real_dict[j]) >= num3 and len(real_dict[j]) <= (num4 - 1):
            new_score_a[2].append(real_dict3[j])
        elif len(real_dict[j]) >= num4:
            new_score_a[3].append(real_dict3[j])
        else:
            continue
print('\npoint 5 pass', datetime.datetime.now() - s)
# num1 = 2
# num2 = 5
# num3 = 10
# num4 = 30
# bar4 = tqdm(total = len(total_list[0] + total_list[1]), colour = 'green')
# bar4.set_description('bar4 Checking bin')
# for i in range(len(new_score)):
#     for j in total_list[i]:
#         bar4.update(1)
#         if len(real_dict[j]) >= num1 and len(real_dict[j]) <= (num2 - 1):
#             new_score[i][0].append(real_dict3[j])
#         elif len(real_dict[j]) >= num2 and len(real_dict[j]) <= (num3 - 1):
#             new_score[i][1].append(real_dict3[j])
#         elif len(real_dict[j]) >= num3 and len(real_dict[j]) <= (num4 - 1):
#             new_score[i][2].append(real_dict3[j])
#         elif len(real_dict[j]) >= num4:
#             new_score[i][3].append(real_dict3[j])
#         else:
#             continue


e = datetime.datetime.now()
print('\nTotal Computation Time:', e - s)
a = datetime.datetime.now()

plt.hist(new_score_a[0], bins = np.linspace(0.7, 1.005, 200), color='green', alpha = 0.5, label=f"follow num: {num1} ~ {num2 - 1}")
plt.hist(new_score_a[1], bins = np.linspace(0.7, 1.005, 200), color='red', alpha = 0.5, label=f"follow num: {num2} ~ {num3 - 1}")
plt.hist(new_score_a[2], bins = np.linspace(0.7, 1.005, 200), color='blue', alpha = 0.5, label=f"follow num: {num3} ~ {num4 - 1}")
plt.hist(new_score_a[3], bins = np.linspace(0.7, 1.005, 200), color='yellow', alpha = 0.5, label=f"follow num: over{num4}")
plt.xlabel('GS-score')
plt.ylabel('Number of Users')
plt.title('Democratic Party & Republican Party')
plt.legend(loc='upper left')

b = datetime.datetime.now()
print('\nSubplot Time:', b - a)
plt.suptitle(f'US Political Diversity Score, Simpson Similarity')
plt.show()

#6 calculate parameter for power of law
