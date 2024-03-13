import csv
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx


simpsonk2係数 = 0.5

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

#Simpsonk2係数のファイルから値を取り出す
filename = '/Users/yoshiharatatsuhito/Desktop/T.Yoshihara/計算社会科学/Twitter_congress/整形済みデータ/Simpsonk2(JP).csv'
with open(filename, encoding='utf8', newline='') as f:
    csvreader = csv.reader(f)
    a_b_jt=[]
    for row in csvreader:
        a_b_jt += row
coefficient_m = []
for i in a_b_jt:
    coefficient_m.append(float(i))

matrix = [[0]*3 for i in range(len(all_name_list)**2)]

for n in range(3):
  if n == 0:
    for k in range(0, len(all_name_list)**2, len(all_name_list)):
      for i in range(len(all_name_list)):
        matrix[i+k][n] = all_name_list[k//len(all_name_list)]
  elif n == 1:
    for k in range(0, len(all_name_list)**2, len(all_name_list)):
      for i in range(len(all_name_list)):
        matrix[i+k][n] = all_name_list[i]
  else:
    t = -1
    for k in range(0, len(all_name_list)**2, len(all_name_list)):
      for i in range(len(all_name_list)):
        t += 1
        matrix[i+k][n] = coefficient_m[t]

sum_engname_list1 = [jimin_list, rikken_list, ishin_list, koumei_list, kyousan_list, reshin_list, kokumin_list, syamin_list, other_list]
color_list = ['red', 'blue', 'gray', 'lightcoral', 'brown', 'lime', 'royalblue', 'slateblue', 'violet', 'fuchsia', 'cyan', 'orangered', 'gold', 'deeppink', 'darkorange', 'olivedrab', 'salmon', 'lightskyblue', 'olive', 'cornflowerblue', 'lightgreen', 'burlywood', 'turquoise', 'yellow', 'lavender', 'coral', 'lightcoral', 'lightyellow', 'bisque', 'aqua', 'chocolate', 'palegreen', 'grey', 'lightcoral', 'brown', 'lime', 'royalblue', 'slateblue', 'violet', 'fuchsia', 'cyan', 'orangered', 'gold', 'deeppink', 'darkorange', 'olivedrab', 'salmon', 'lightskyblue', 'olive', 'cornflowerblue', 'lightgreen', 'burlywood', 'turquoise', 'yellow', 'lavender', 'coral', 'red', 'blue', 'lightcoral', 'lightyellow', 'bisque', 'aqua', 'chocolate', 'palegreen', 'grey']

matrix_show = []
for i in range(len(matrix)):
  if matrix[i][2] >= simpsonk2係数 and matrix[i][2] != 1:
    matrix_show.append(matrix[i])
print(f'エッジの数:{len(matrix_show)}')

H = nx.DiGraph()
for n in all_name_list:
    H.add_node(n)
print(f'ノードの数:{H.number_of_nodes()}')

H.add_weighted_edges_from(matrix_show)
edge_width = [d["weight"] * 1 for (u, v, d) in H.edges(data=True)]

# size =[((int(i))/800) for i in follower_list] #ノードの大きさはフォロワーの数に依存

size = [] #ノードの大きさはpagerankの値に依存
for i in nx.pagerank(H).values():
    size.append(i*30000)
print(size)

a = sum_engname_list1
e = len(sum_engname_list1)

c = []
for i in H.nodes():
  n = 0
  for j in range(e):
    if i in a[j]:
      n += 1
      c.append(color_list[j])

pos = nx.spring_layout(H, k=0.5)
pos = nx.kamada_kawai_layout(H)
plt.figure(figsize=(24,16))
plt.title('Enhanced Simpsonk2 index Threshold:{}'.format(simpsonk2係数))
nx.write_gexf(H, f'/Users/yoshiharatatsuhito/Downloads/JP_Rep(Simpsonk2={simpsonk2係数}).gexf')
nx.draw_networkx(H, pos, node_size = size, node_color=c, arrows=True, width = edge_width, connectionstyle="arc3, rad=0.1", font_family='Hiragino Sans')
plt.show()
