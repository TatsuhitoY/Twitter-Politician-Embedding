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
print(len(identity_list))

#各政治家のファイルを全て開けてそこに保存されているユーザーの集合を作成
total_number = 0
account_num = 0

l = glob.glob('/Users/yoshiharatatsuhito/Desktop/T.Yoshihara/計算社会科学/Twitter_congress/データ(US)/*')
total_list2 = []
ctotal_list = []
# bar = tqdm(total = 439, colour = 'green')
# bar.set_description('Counting users of politician')
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
    # bar.update(1)
    time.sleep(0.005)

#total_list2には全てのユーザーのTwitter Handlesが重複ありで入っている
real_list = list(set(total_list2))
print(f'\nフォロワー数（重複あり）:{total_number}')
print(f'フォロワー数（重複なし）:{len(set(total_list2))}')
print(f'政治家の数:{account_num}')


#4 calculate the diversity_score for each followers in the list made on step 3
normal_count係数 = 0

model = gensim.models.KeyedVectors.load_word2vec_format(f'/Users/yoshiharatatsuhito/Desktop/T.Yoshihara/計算社会科学/Twitter_congress/整形済みデータ/Embedding/US_EMB_normal_count={normal_count係数}', binary=False)
model.init_sims(replace=True) #ここでベクトルが正規化された

def save_embedding_projector_files(model, vector_file, metadata_file):
    """ Generate a vector file and a metadata file for Embedding Projector.
    You can upload the generated files to Embedding Projector
    (http://projector.tensorflow.org/), and get vizualization of
    the trained vector space.
    """
    with open(vector_file, 'w', encoding='utf-8') as f, \
         open(metadata_file, 'w', encoding='utf-8') as g:

        # metadata file needs header
        # g.write('Word\n')

        for i in range(439):
            embedding = model[str(i)]

            # Save vector TSV file
            f.write('\t'.join([('%f' % x) for x in embedding]) + '\n')

            # Save metadata TSV file
            g.write(identity_list[i][4] + '\n')


save_embedding_projector_files(model, f'/Users/yoshiharatatsuhito/Desktop/T.Yoshihara/計算社会科学/Twitter_congress/整形済みデータ/tensor_flow_projector/vector_file_US_normalc={normal_count係数}',f'/Users/yoshiharatatsuhito/Desktop/T.Yoshihara/計算社会科学/Twitter_congress/整形済みデータ/tensor_flow_projector/metadata_file_US_normalc={normal_count係数}')
