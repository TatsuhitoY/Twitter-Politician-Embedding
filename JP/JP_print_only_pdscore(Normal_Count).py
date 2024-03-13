import csv
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
df = pd.read_csv("/Users/yoshiharatatsuhito/Desktop/T.Yoshihara/計算社会科学/Twitter_congress/Twitterアカウントデータ/JP R. Twitter Handles.csv", header=0)
Kname = list(df['Kanji Name'])
Hname = list(df['Hiragana Name'])
Handles = list(df['Twitter Handles'])
ST = list(df['State/District'])
Party = list(df['Party'])
for i in range(len(Kname)):
  Kname[i] = Kname[i].replace('\u3000\u3000', '')
  Kname[i] = Kname[i].replace('\u3000', '')
  Kname[i] = Kname[i].replace('君', '')
  Hname[i] = Hname[i].replace('\u3000', '')
  Hname[i] = Hname[i].replace('君', '')
identity_list = [[Kname[i], Hname[i], Handles[i], ST[i], Party[i]] for i in range(len(Kname))]

#各政治家のファイルを全て開けてそこに保存されているユーザーの集合を作成
total_number = 0
account_num = 0

l = glob.glob('/Users/yoshiharatatsuhito/Desktop/T.Yoshihara/計算社会科学/Twitter_congress/データ(Japan)2/*')
total_list2 = []
ctotal_list = []
bar = tqdm(total = 401, colour = 'green')
bar.set_description('Counting users of politician')
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
    Kname = contents[0]
    Hname = contents[1]
    Handles = contents[2]
    ST = contents[3]
    Party = contents[4]
    # print(Kname, Hname, ST, Party, f"フォロワー数：{len(contents) - 6}")
    bar.update(1)
    time.sleep(0.005)

#total_list2には全てのユーザーのTwitter Handlesが重複ありで入っている
real_list = list(set(total_list2))
print(f'\nフォロワー数（重複あり）:{total_number}')
print(f'フォロワー数（重複なし）:{len(set(total_list2))}')
print(f'政治家の数:{account_num}')

#2 create dictionary that has users as keys and politicians that each users follow as items
b = [[] for i in range(len(real_list))]
real_dict = dict(zip(real_list, b))

#sort_dictにctotal_listのi番目の数字を入れたら同じ政治家のidentity_listにおけるインデックスが出てくる
sort_dict = {}
for i in range(len(ctotal_list)):
    for j in range(len(identity_list)):
        if ctotal_list[i][0][2] == identity_list[j][2]:
            sort_dict[i] = str(j)

bar2 = tqdm(total = len(ctotal_list), colour = 'green')
#最初のfor文は各政治家の数
for i in range(len(ctotal_list)):
    bar2.update(1)
    #このjはとある政治家iをフォローしているユーザーのTwitter Handle
    for j in ctotal_list[i][1]:
        #ここでiをstrにすることでmodel[]に代入するときインデックスでなく、しっかりとノードの名称としてiが機能し、ベクトルが引き出される。
        real_dict[j].append(sort_dict[i])
        #real_dictのタイプはstr,よってmodeで使う分にはおkだがidentity_listの時はintする

#3 create a list of each political party that contains followers
jimin_list = []
rikken_list = []
ishin_list = []
koumei_list = []
kyousan_list = []
reshin_list = []
kokumin_list = []
syamin_list = []
other_list = []

bar3 = tqdm(total = len(real_dict), colour = 'green')
for i in real_dict.keys():
    bar3.update(1)
    for j in range(len(real_dict[i])):
        if identity_list[int(real_dict[i][j])][4] == "自民":
            jimin_list.append(i)
        elif identity_list[int(real_dict[i][j])][4] == "立憲":
            rikken_list.append(i)
        elif identity_list[int(real_dict[i][j])][4] == "維新":
            ishin_list.append(i)
        elif identity_list[int(real_dict[i][j])][4] == "公明":
            koumei_list.append(i)
        elif identity_list[int(real_dict[i][j])][4] == "共産":
            kyousan_list.append(i)
        elif identity_list[int(real_dict[i][j])][4] == "れ新":
            reshin_list.append(i)
        elif identity_list[int(real_dict[i][j])][4] == "国民":
            kokumin_list.append(i)
        elif identity_list[int(real_dict[i][j])][4] == "社民党":
            syamin_list.append(i)
        else:
            other_list.append(i)

print(f'\n自民 重複あり{len(jimin_list)}　重複なし{len(set(jimin_list))}　党内平均フォロー数{round(len(jimin_list)/len(set(jimin_list)), 3)}')
print(f'立憲 重複あり{len(rikken_list)}　重複なし{len(set(rikken_list))}　党内平均フォロー数{round(len(rikken_list)/len(set(rikken_list)), 3)}')
print(f'維新 重複あり{len(ishin_list)}　重複なし{len(set(ishin_list))}　党内平均フォロー数{round(len(ishin_list)/len(set(ishin_list)), 3)}')
print(f'公明 重複あり{len(koumei_list)}　重複なし{len(set(koumei_list))}　党内平均フォロー数{round(len(koumei_list)/len(set(koumei_list)), 3)}')
print(f'共産 重複あり{len(kyousan_list)}　重複なし{len(set(kyousan_list))}　党内平均フォロー数{round(len(kyousan_list)/len(set(kyousan_list)), 3)}')
print(f'れ新 重複あり{len(reshin_list)}　重複なし{len(set(reshin_list))}　党内平均フォロー数{round(len(reshin_list)/len(set(reshin_list)), 3)}')
print(f'国民 重複あり{len(kokumin_list)}　重複なし{len(set(kokumin_list))}　党内平均フォロー数{round(len(kokumin_list)/len(set(kokumin_list)), 3)}')
print(f'社民 重複あり{len(syamin_list)}　重複なし{len(set(syamin_list))}　党内平均フォロー数{round(len(syamin_list)/len(set(syamin_list)), 3)}')
print(f'その他 重複あり{len(other_list)}　重複なし{len(set(other_list))}　党内平均フォロー数{round(len(other_list)/len(set(other_list)), 3)}')

#4 calculate the diversity_score for each followers in the list made on step 3
normal_count係数 = 0

model = gensim.models.KeyedVectors.load_word2vec_format(f'/Users/yoshiharatatsuhito/Desktop/T.Yoshihara/計算社会科学/Twitter_congress/整形済みデータ/Embedding/JP_EMB_normal_count={normal_count係数}', binary=False)
model.init_sims(replace=True) #ここでベクトルが正規化された

#ここのnum_dictはmodelのインデックスとidentity_listのインデックスを合わせている
bar4 = tqdm(total = len(real_dict), colour = 'green')
real_dict2 = {}

for i in real_dict.keys():
    bar4.update(1)
    average = np.zeros_like(model[real_dict[i][0]])
    for j in range(len(real_dict[i])):
        #real_dict[i][j]はidentity_listの政治家のインデックス
        average = average + model[real_dict[i][j]]
    real_dict2[i] = average

bar5 = tqdm(total = len(real_dict), colour = 'green')
real_dict3 = {}
for i in real_dict.keys():
    bar5.update(1)
    average = real_dict2[i]
    sum = 0
    for j in range(len(real_dict[i])):
        sum = sum + np.dot(model[real_dict[i][j]], average)
    score = sum / (len(real_dict[i]) * np.linalg.norm(average))
    real_dict3[i] = score

#5 create histograms for each political party

jimin_scores = []
rikken_scores = []
ishin_scores = []
koumei_scores = []
kyousan_scores = []
reshin_scores = []
kokumin_scores = []
syamin_scores = []
other_scores = []

total_list = [jimin_list, rikken_list, ishin_list, koumei_list, kyousan_list, reshin_list, kokumin_list, syamin_list, other_list]
total_score = [jimin_scores, rikken_scores, ishin_scores, koumei_scores, kyousan_scores, reshin_scores, kokumin_scores, syamin_scores, other_scores]

#ヒストグラムに使うユーザーのDiversity Scoreを計算
for i in range(len(total_list)):
    for j in total_list[i]:
        total_score[i].append(real_dict3[j])

jimin_new_list = [[] for i in range(4)]
rikken_new_list = [[] for i in range(4)]
ishin_new_list = [[] for i in range(4)]
koumei_new_list = [[] for i in range(4)]
kyousan_new_list = [[] for i in range(4)]
reshin_new_list = [[] for i in range(4)]
kokumin_new_list = [[] for i in range(4)]
syamin_new_list = [[] for i in range(4)]
other_new_list = [[] for i in range(4)]
# new_score = [jimin_new_list, rikken_new_list, ishin_new_list, koumei_new_list, kyousan_new_list, reshin_new_list, kokumin_new_list, syamin_new_list, other_new_list]
new_score = [[[] for i in range(4)] for j in range(9)]

num1 = 2
num2 = 5
num3 = 10
num4 = 30
bar5 = tqdm(total = len(total_list[0] + total_list[1]), colour = 'green')
for i in range(len(new_score)):
    for j in total_list[i]:
        bar5.update(1)
        if len(real_dict[j]) >= num1 and len(real_dict[j]) <= (num2 - 1):
            new_score[i][0].append(real_dict3[j])
        elif len(real_dict[j]) >= num2 and len(real_dict[j]) <= (num3 - 1):
            new_score[i][1].append(real_dict3[j])
        elif len(real_dict[j]) >= num3 and len(real_dict[j]) <= (num4 - 1):
            new_score[i][2].append(real_dict3[j])
        elif len(real_dict[j]) >= num4:
            new_score[i][3].append(real_dict3[j])
        else:
            continue

e = datetime.datetime.now()
print('\nTotal Computation Time:', e - s)
a = datetime.datetime.now()

name = ['jimin', 'rikken', 'ishin', 'koumei', 'kyousan', 'reshin', 'kokumin', 'syamin', 'other']
for i in range(9):
        plt.subplot(2, 5, i+1)
        plt.hist(new_score[i][0], bins = np.linspace(0.5, 1.005, 100), color='green', alpha = 0.5, label=f"follow num: {num1} ~ {num2 - 1}")
        plt.hist(new_score[i][1], bins = np.linspace(0.5, 1.005, 100), color='red', alpha = 0.5, label=f"follow num: {num2} ~ {num3 - 1}")
        plt.hist(new_score[i][2], bins = np.linspace(0.5, 1.005, 100), color='blue', alpha = 0.5, label=f"follow num: {num3} ~ {num4 - 1}")
        plt.hist(new_score[i][3], bins = np.linspace(0.5, 1.005, 100), color='yellow', alpha = 0.5, label=f"follow num: over{num4}")
        if i == 0:
            plt.xlabel('Diversity Score')
            plt.ylabel('Number of Users')
            plt.legend(loc='upper left', fontsize=8)
        plt.title(name[i])


b = datetime.datetime.now()
print('\nSubplot Time:', b - a)
plt.suptitle(f'Japan Political Diversity Score, Normal_Count Similarity')
plt.show()

#6 calculate parameter for power of law



