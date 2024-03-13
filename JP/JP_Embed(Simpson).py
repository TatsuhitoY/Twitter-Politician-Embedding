import csv
import pandas as pd
import networkx as nx
from node2vec import Node2Vec

# _DEBUG_ = False
_DEBUG_ = True

#community detection   on → 1, off → 0
sign1 = 0
#Delete node with 0 edge delete → 1, retain → 0
sign2 = 0

simpson係数 = 0
print(f'simpson係数: {simpson係数}')

coefficient_adjust = 100

# JP R. Twitter Handles.csvにデータ(US)に入っているアカウント情報と収集したデータファイルの数が一致していなければならない

df = pd.read_csv("/Twitterアカウントデータ/JP R. Twitter Handles.csv", header=0)
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

#アカウントの名前のリスト
all_name_list = []
jimin_list = []
rikken_list = []
ishin_list = []
koumei_list = []
kyousan_list = []
reshin_list = []
kokumin_list = []
syamin_list = []
other_list = []
total_num = 0

num = -1
for i in range(len(identity_list)):
    num += 1
    total_num += num #全てのアカウント数をnとするとこのtotal_num= n+(n-1)+(n-2)+(n-3)+...+1+0
    all_name_list.append(str(i))
    if identity_list[i][4] == "自民":
        jimin_list.append(str(i))
    elif identity_list[i][4] == "立憲":
        rikken_list.append(str(i))
    elif identity_list[i][4] == "維新":
        ishin_list.append(str(i))
    elif identity_list[i][4] == "公明":
        koumei_list.append(str(i))
    elif identity_list[i][4] == "共産":
        kyousan_list.append(str(i))
    elif identity_list[i][4] == "れ新":
        reshin_list.append(str(i))
    elif identity_list[i][4] == "国民":
        kokumin_list.append(str(i))
    elif identity_list[i][4] == "社民党":
        syamin_list.append(str(i))
    else:
        other_list.append(str(i))

#-------------------------------------------------------------------------------------------------------------------------------

account_num = len(identity_list)
follower_list = []
filename = f'/整形済みデータ/JP_follower_count.csv'
with open(filename, encoding='utf8', newline='') as f:
    csvreader = csv.reader(f)
    lists = []
    for row in csvreader:
      lists += row
for i in lists:
    follower_list.append(i)

#-------------------------------------------------------------------------------------------------------------------------------

#Simpson係数のファイルから値を取り出す
filename = '/整形済みデータ/Simpson(JP).csv'
with open(filename, encoding='utf8', newline='') as f:
    csvreader = csv.reader(f)
    a_b_jt=[]
    for row in csvreader:
        a_b_jt += row
coefficient_m = []
for i in a_b_jt:
    coefficient_m.append(float(i))

#このmatrixが全ての係数とアカウント名を格納する最終的なリスト
matrix = [[0]*3 for i in range(total_num)]
#-------------------------------------------------------------------------------------------------------------------------------

for n in range(3):
  e = -1
  if n == 0:
    c = 0
    for i in range(len(all_name_list)):
      d = 0
      c += 1
      for k in range(len(all_name_list)):
        d += 1
        if c < d:
          e += 1
          matrix[e][0] = f'{all_name_list[c-1]}'
  elif n == 1:
    c = 0
    for i in range(len(all_name_list)):
       d = 0
       c += 1
       for k in range(len(all_name_list)):
         d += 1
         if d > c:
           e += 1
           matrix[e][1] = f'{all_name_list[d-1]}'
  else:
    for k in range(total_num):
      e += 1
      matrix[e][2] = coefficient_m[e] / coefficient_adjust

#-------------------------------------------------------------------------------------------------------------------------------
sum_engname_list1 = [jimin_list, rikken_list, ishin_list, koumei_list, kyousan_list, reshin_list, kokumin_list, syamin_list, other_list]
color_list = ['red', 'blue', 'gray', 'lightcoral', 'brown', 'lime', 'royalblue', 'slateblue', 'violet', 'fuchsia', 'cyan', 'orangered', 'gold', 'deeppink', 'darkorange', 'olivedrab', 'salmon', 'lightskyblue', 'olive', 'cornflowerblue', 'lightgreen', 'burlywood', 'turquoise', 'yellow', 'lavender', 'coral', 'lightcoral', 'lightyellow', 'bisque', 'aqua', 'chocolate', 'palegreen', 'grey', 'lightcoral', 'brown', 'lime', 'royalblue', 'slateblue', 'violet', 'fuchsia', 'cyan', 'orangered', 'gold', 'deeppink', 'darkorange', 'olivedrab', 'salmon', 'lightskyblue', 'olive', 'cornflowerblue', 'lightgreen', 'burlywood', 'turquoise', 'yellow', 'lavender', 'coral', 'red', 'blue', 'lightcoral', 'lightyellow', 'bisque', 'aqua', 'chocolate', 'palegreen', 'grey']

matrix_show = []
for i in range(len(matrix)):
  if matrix[i][2] >= simpson係数 / coefficient_adjust  and matrix[i][2] != 1:
    matrix_show.append(matrix[i])
print(f'エッジの数:{len(matrix_show)}')

H = nx.Graph() #リンクを持つノードのみの集合を作成

for n in all_name_list:
    H.add_node(n)
size =[(int(i)/800) for i in follower_list]

H.add_weighted_edges_from(matrix_show)
edge_width = [d["weight"] * 400 for (u, v, d) in H.edges(data=True)]

a = sum_engname_list1
e = len(sum_engname_list1) #2

c = []
for i in H.nodes():
  n = 0
  for j in range(e):
    if i in a[j]:
      n += 1
      c.append(color_list[j])
  if sign2 == 0:
    if n == 0:
      c.append(color_list[2])

print(f'エッジの数:{len(matrix_show)}')
print(f'ノードの数:{H.number_of_nodes()}')

# Precompute probabilities and generate walks - **ON WINDOWS ONLY WORKS WITH workers=1**
node2vec = Node2Vec(H, dimensions=64, walk_length=30, num_walks=200, workers=4)  # Use temp_folder for big graphs
# Embed nodes
model = node2vec.fit(window=10, min_count=1, batch_words=4)  # Any keywords acceptable by gensim.Word2Vec can be passed, `dimensions` and `workers` are automatically passed (from the Node2Vec constructor)

#1行目はノード数と分散表現の次元が記載されている。
model.wv.save_word2vec_format(f'/Users/yoshiharatatsuhito/Desktop/T.Yoshihara/計算社会科学/Twitter_congress/整形済みデータ/Embedding/JP_EMB_simpson={simpson係数}')

#node2vecはhttps://github.com/eliorc/node2vec

