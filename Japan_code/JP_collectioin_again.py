import glob
import csv
import pandas as pd

l = glob.glob('/Users/yoshiharatatsuhito/Desktop/T.Yoshihara/計算社会科学/Twitter_congress/データ(Japan)2/*')

handle_list = []
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
    Kname = contents[0]
    Hname = contents[1]
    Handles = contents[2]
    ST = contents[3]
    Party = contents[4]
    # print(Kname, Hname, Handles, ST, Party)
    handle_list.append(Handles)
    # file_name = '/Users/yoshiharatatsuhito/Desktop/T.Yoshihara/計算社会科学/Twitter_congress/データ(Japan)2/'
    # name = f'{file_name}{Party}_{ST}_{Kname}'
    # f = open(f'{name}.csv', 'w')
    # writer = csv.writer(f)
    # writer.writerow(contents)
    # f.close()

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
#193
identity_list = [[Kname[i], Hname[i], Handles[i], ST[i], Party[i]] for i in range(len(Kname))]
number = 0
again_list = []
for i in range(len(identity_list)):
    if identity_list[i][2] in handle_list:
        continue
    else:
        number += 1
        print(i)
        again_list.append(i)
        print(identity_list[i])

# lists = []　何かを確認しようとしてた
# for i in range(len((identity_list))):
#     if '比' in identity_list[i][3]:
#         print(identity_list[i][0])
#         print(identity_list[i][1])
#         lists.append(i)
#
# print(again_list)
# print(number)
# print(lists)
