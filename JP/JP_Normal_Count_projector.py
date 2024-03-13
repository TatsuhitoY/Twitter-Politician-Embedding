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
print(len(identity_list))

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

real_list = list(set(total_list2))
b = [[] for i in range(len(real_list))]
real_dict = dict(zip(real_list, b))

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


#ここから先のコードのみで良いのでは？関数のreal_dictを省略できるから
normal_count係数 = 0
model = gensim.models.KeyedVectors.load_word2vec_format(f'/Users/yoshiharatatsuhito/Desktop/T.Yoshihara/計算社会科学/Twitter_congress/整形済みデータ/Embedding/JP_EMB_normal_count={normal_count係数}', binary=False)
model.init_sims(replace=True) #ここでベクトルが正規化された

def save_embedding_projector_files(model,real_dict, vector_file, metadata_file):
    """ Generate a vector file and a metadata file for Embedding Projector.
    You can upload the generated files to Embedding Projector
    (http://projector.tensorflow.org/), and get vizualization of
    the trained vector space.
    """
    with open(vector_file, 'w', encoding='utf-8') as f, \
         open(metadata_file, 'w', encoding='utf-8') as g:

        # metadata file needs header
        # g.write('Word\n')

        for i in range(401):
            print(i, type(i))
            embedding = model[str(i)]

            # Save vector TSV file
            f.write('\t'.join([('%f' % x) for x in embedding]) + '\n')

            # Save metadata TSV file
            g.write(identity_list[i][4] + '\n')


save_embedding_projector_files(model, real_dict, f'/Users/yoshiharatatsuhito/Desktop/T.Yoshihara/計算社会科学/Twitter_congress/整形済みデータ/tensor_flow_projector/vector_file_JP_normal_count={normal_count係数}',f'/Users/yoshiharatatsuhito/Desktop/T.Yoshihara/計算社会科学/Twitter_congress/整形済みデータ/tensor_flow_projector/metadata_file_JP_normal_count={normal_count係数}')




