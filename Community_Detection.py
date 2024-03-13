import networkx as nx
import math
import csv
import random as rand
import sys

_DEBUG_ = False

def buildG(G, list):
    for line in list:
       G.add_edge(line[0], line[1],weight=float(line[2]))                                                       #これでファイルから重み付き無向グラフの情報を打ち込む 元々int関数がついてたが削除
                                                                                                                #もしファイルの情報に重みが付与されていなかったら重みを自動で1とする。
                                                                                                                #この作業はGの中にある塊の数が一つ増えるまでエッジを減らし続ける。得られる成果はエッジが減ったG
                                                                                                                # This method keeps removing edges from Graph until one of the connected components of Graph splits into two
                                                                                                                # compute the edge betweenness
def CmtyGirvanNewmanStep(G): #③
    if _DEBUG_:
        print("Running CmtyGirvanNewmanStep method ...")
    init_ncomp = nx.number_connected_components(G)   #number of components　連結グループの数を取得
    ncomp = init_ncomp                                                                                          #ncompを更新し続けてある塊を分割できるまで繰り返す。
    while ncomp <= init_ncomp:
        bw = nx.edge_betweenness_centrality(G, weight='weight')                                                 #edge betweenness for G
                                                                                                     #find the edge with max centrality その段階のグラフで最大の中心性を持つエッジを取得。                                                             #bwの形式は形式は{('エッジ', 'エッジ'): edge_betweenness_centralityの値の値, ...}
        max_ = max(bw.values())
                                                                                                                #find the edge with the highest centrality and remove all of them if there is more than one!
        for k, v in bw.items():                                                                                 #この場合kはインデックスでvが中身
            if float(v) == max_:
                G.remove_edge(k[0],k[1])#remove the central edge
        ncomp = nx.number_connected_components(G)                                                               #recalculate the no of components

                                                                                                                #渡されたグラフGのモジュラリティーを計算して引数Modとして渡す
                                                                                                                # This method compute the modularity of current split
def _GirvanNewmanGetModularity(G, deg_, m_): #②
    New_A = nx.adjacency_matrix(G)                                                                              #データは['エッジ', 'エッジ', 重み]というリストが並んでいる。
    New_deg = {}
    New_deg = UpdateDeg(New_A, G.nodes())                                                                       #（重複）UpdateDegでは辞書型で{'ノード名': 重みの総和, ...}が取得できる。
                                                                                                                #Let's compute the Q
    comps = nx.connected_components(G)                                                                                                             #list of components データの形式の確認は困難
    print('Number of communities in decomposed G: {}'.format(nx.number_connected_components(G)))                #元々Noと記載されてたが、Numberに修正
    Mod = 0                                                                                                     #Modularity of a given partitionning
    for c in comps:
        EWC = 0                                                                                                 #number of edges within a community
        RE = 0                                                                                                  #number of random edges
        for u in c:
            EWC += New_deg[u]     #EWCはその連結部のノードの最新の重みの総和
            RE += deg_[u]         #REはその連結部のノードの初期の重みの総和                                           #count the probability of a random edge
        Mod += ( float(EWC) - float(RE*RE)/float(2*m_) )                                                        #モジュラリティーの計算
    Mod = Mod/float(2*m_)
    if _DEBUG_:
        print("Modularity: {}".format(Mod))
    return Mod

                                                                                                                #（重複）UpdateDegでは辞書型で{'ノード名': 重みの総和, ...}がdeg_dictに格納されている。
def UpdateDeg(A, nodes): #                                                                                      #nodes = G.nodes()でノードが並ぶリストが格納される。
    deg_dict = {}
    n = len(nodes)                                                                                              #len(A) ---> some ppl get issues when trying len() on sparse matrixes!
    B = A.sum(axis = 1)                                                                                         #グラフのノードが持つそれぞれのエッジの重みを足し合わせたものが格納され、それはノードごとにあり、ノードの番号順に並べられる。\
    i = 0
    for node_id in list(nodes):
        # deg_dict[node_id] = B[i, 0]                                                                             #Bは縦に一列なのでB[i, 0]はi番目の要素のこと。つまりdeg_dictは
        deg_dict[node_id] = B[i]
        i += 1
    return deg_dict
