import csv
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx


simpsonk2係数 = 0.5

#"/Users/yoshiharatatsuhito/Desktop/US R. Twitter Handles(2023:2:12).csv"に入っているアカウント情報と収集したデータファイルの数が一致していなければならない

df = pd.read_csv("/Users/yoshiharatatsuhito/Desktop/T.Yoshihara/計算社会科学/Twitter_congress/Twitterアカウントデータ/US R. Twitter Handles.csv", header=0)
Fname = list(df['First Name'])
Lname = list(df['Last Name'])
Handles = list(df['Twitter Handles'])
ST = list(df['State/District'])
Party = list(df['Party'])
identity_list = [[Fname[i], Lname[i], Handles[i], ST[i], Party[i]] for i in range(len(Fname))]

#アカウントの名前のリスト
all_name_list = []
d_list = []
r_list = []
total_num = 0

num = -1
for i in identity_list:
    num += 1
    total_num += num #全てのアカウント数をnとするとこのtotal_num= n+(n-1)+(n-2)+(n-3)+...+1+0
    # all_name_list.append(f'{i[4]} {i[3]} {i[0]} {i[1]}')
    all_name_list.append(f'{i[4]} {i[3]}')
    if i[4] == "D":
        # d_list.append(f'{i[4]} {i[3]} {i[0]} {i[1]}')
        d_list.append(f'{i[4]} {i[3]}')
    else:
        # r_list.append(f'{i[4]} {i[3]} {i[0]} {i[1]}')
        r_list.append(f'{i[4]} {i[3]}')

#-------------------------------------------------------------------------------------------------------------------------------

account_num = len(identity_list)
follower_list = []
filename = f'/Users/yoshiharatatsuhito/Desktop/T.Yoshihara/計算社会科学/Twitter_congress/整形済みデータ/US_follower_count.csv'
with open(filename, encoding='utf8', newline='') as f:
    csvreader = csv.reader(f)
    lists = []
    for row in csvreader:
      lists += row
for i in lists:
    follower_list.append(i)

#-------------------------------------------------------------------------------------------------------------------------------

#Simpsonk2係数のファイルから値を取り出す
filename = '/Users/yoshiharatatsuhito/Desktop/T.Yoshihara/計算社会科学/Twitter_congress/整形済みデータ/Simpsonk2(US).csv'
with open(filename, encoding='utf8', newline='') as f:
    csvreader = csv.reader(f)
    a_b_jt=[]
    for row in csvreader:
        a_b_jt += row
simpsonk2_m = []
for i in a_b_jt:
    simpsonk2_m.append(float(i))

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
        matrix[i+k][n] = simpsonk2_m[t]

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


c = []
for i in H.nodes():
  if i in r_list:
    c.append('red')
  elif i in d_list:
    c.append('blue')
  else:
    c.append('green')

pos = nx.spring_layout(H, k=0.5)
pos = nx.kamada_kawai_layout(H)
plt.figure(figsize=(24,16))
plt.title('Enhanced Simpsonk2 index Threshold:{}'.format(simpsonk2係数))
nx.write_gexf(H, f'/Users/yoshiharatatsuhito/Downloads/US_Rep(Simpsonk2={simpsonk2係数}).gexf')
nx.draw_networkx(H, pos, node_size = size, node_color=c, arrows=True, width = edge_width, connectionstyle="arc3, rad=0.1")
plt.show()
