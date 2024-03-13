import csv
import pandas as pd
from Community_Detection import buildG, CmtyGirvanNewmanStep, _GirvanNewmanGetModularity, UpdateDeg
import matplotlib.pyplot as plt
import networkx as nx

# _DEBUG_ = False
_DEBUG_ = True

#community detection   on → 1, off → 0
sign1 = 1
#Delete node with 0 edge delete → 1, retain → 0
sign2 = 1

simpsonk係数 = 0.3

coefficient_adjust = 50

# JP R. Twitter Handles.csvにデータ(JP)に入っているアカウント情報と収集したデータファイルの数が一致していなければならない

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
filename = f'/Users/yoshiharatatsuhito/Desktop/T.Yoshihara/計算社会科学/Twitter_congress/整形済みデータ/JP_follower_count.csv'
with open(filename, encoding='utf8', newline='') as f:
    csvreader = csv.reader(f)
    lists = []
    for row in csvreader:
      lists += row
    print(lists)
for i in lists:
    follower_list.append(i)

#-------------------------------------------------------------------------------------------------------------------------------

#Simpsonk係数のファイルから値を取り出す
filename = '/Users/yoshiharatatsuhito/Desktop/T.Yoshihara/計算社会科学/Twitter_congress/整形済みデータ/Simpsonk(JP).csv'
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
  if matrix[i][2] >= simpsonk係数 / coefficient_adjust  and matrix[i][2] != 1:
    matrix_show.append(matrix[i])
print(f'エッジの数:{len(matrix_show)}')

#########################################################################################################
if sign1 == 1:
  G = nx.Graph()  #let's create the graph first
  buildG(G, matrix_show) #ここに三次元リストを入れて実行！
  print(f'ノードの数:{G.number_of_nodes()}')

  if _DEBUG_:
    print('G nodes: {} & G no of nodes: {}'.format(G.nodes(), G.number_of_nodes()))

  n = G.number_of_nodes()    #|V|
  A = nx.adjacency_matrix(G)    #adjacenct matrix

  m_ = 0.0    #the weighted version for number of edges
  for i in range(0,n):
    for j in range(0,n):
      m_ += A[i,j]
  m_ = m_/2.0
  if _DEBUG_:
          print("m(全ての辺の重みの合計): {}".format(m_))

    #calculate the weighted degree for each node
  Orig_deg = {}
  Orig_deg = UpdateDeg(A, G.nodes())

    #run Newman alg
  BestQ = 0.0
  Q = 0.0
  while True:
      CmtyGirvanNewmanStep(G)   #エッジが減らされて分割されたGが得られる。
      Q = _GirvanNewmanGetModularity(G, Orig_deg, m_);                                                        #Gのモジュラリティーを取得
      print("Modularity of decomposed G: {}".format(Q))
      if Q > BestQ:
          BestQ = Q                                                                                           #最高値のモジュラリティー値を取得
          Bestcomps = list(nx.connected_components(G))    #Best Split
          print("Identified components: {}\n".format(Bestcomps))
      if G.number_of_edges() == 0:                                                                            #分割し終えたら処理を抜ける
          break
  if BestQ > 0.0:                                                                                             #分割作業が終わって最大のモジュラリティーを得たので表示
    print('\n')
    print("Max modularity found (Q): {} and number of communities: {}".format(BestQ, len(Bestcomps)))
    print("Graph communities: {}".format(Bestcomps))
  else:
    print("Max modularity (Q):", BestQ)                                                                         #G.nodes()でノードが並ぶリストが作られる。
#########################################################################################################

H = nx.Graph() #リンクを持つノードのみの集合を作成

if sign2 == 1: #次数0のノードを非表示
  node_list_del = []
  for i in range(len(matrix_show)): #このfor文では係数の閾値を超えたアカウント（表示するアカウント）のノードの名前を取り出している。
    node_list_del.append(matrix_show[i][0])
    node_list_del.append(matrix_show[i][1])
  node_list_first = list(set(node_list_del)) #ノードの集合をリストにしてall_name_listの順番に並び替えてsizeを作成(数行後ろのfor文で処理してる)
  node_list_final = []
  num = -1
  size = []
  #sizeリストに各アカウントのフォロワー数を格納したいので、all_name_listの順番でnode_list_firstのアカウントと合致するかを確認してフォロワー数をfollower_listから数えて格納している
  for i in all_name_list:
    num += 1
    if i in node_list_first:
      node_list_final.append(i)
      size.append(int(follower_list[num])/800)

  H.add_nodes_from(node_list_final)

if sign2 == 0: #全てのノードを表示
  for n in all_name_list:
    H.add_node(n)
  size =[(int(i)/800) for i in follower_list]

H.add_weighted_edges_from(matrix_show)
edge_width = [d["weight"] * 400 for (u, v, d) in H.edges(data=True)]

if sign1 == 1:
  a = Bestcomps
  e = len(Bestcomps)
if sign1 == 0:
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

if sign1 == 0:
  print('note : Blue = Democrats, Red = Republicans')
if sign1 == 1:
  if sign2 == 0 and BestQ != 0.0:
    print('note : nodes in color gray are not in any community as it have no edges')
  if BestQ == 0:
    print('community detection fail')

print(f'エッジの数:{len(matrix_show)}')
print(f'ノードの数:{H.number_of_nodes()}')
if sign1 == 1:
    print("m(全ての辺の重みの合計): {}".format(m_))

pos = nx.kamada_kawai_layout(H)
plt.figure(figsize=(21,14))
plt.title('Simpsonk index Threshold:{}'.format(simpsonk係数))
nx.write_gexf(H, f'/Users/yoshiharatatsuhito/Downloads/JP_Rep(Simpsonk={simpsonk係数}).gexf')
nx.draw_networkx(H, pos, node_size = size, node_color=c, arrows=False, width= edge_width, font_family='Hiragino Sans')
plt.show()
