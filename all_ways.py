import numpy as np
import algo

def transfoCheminI(G, dest):
    #soit n=(s,v),time,(s2,v2)
    #si time=0 (donc s=s2) et s=dest add n
    #sinon n=(s,v),time,(s2,v2) => n=(s,v),time-v,(s2,v2)
    S,A = G
    tranfo = set()

    for ((start,startValue),time,(end,endValue)) in A:
        if time==0 and start==dest:
            tranfo.add(((start,startValue),time,(end,endValue)))
        else:
            tranfo.add(((start,startValue),endValue-startValue,(end,endValue)))

    return S,tranfo

def cheminI(G, init, dest):
    G = transfoCheminI(G, dest)
    return algo.dijkstra(G,init,dest)

def cheminII(G,init,dest):
    #BFS du chemin le plus tard cherche si possible ainsi de suite
    S,A = G
    same_a = []
    same_d = []
    for s in S:
        if s[0] == init:
            same_a.append(s)
        elif s[0] == dest:
            same_d.append(s)

    inits = sorted(same_a, key=lambda tup: tup[1], reverse=True)
    dest = sorted(same_d, key=lambda tup: tup[1], reverse=True)[0]

    for i in inits:
        res = algo.bfs(G,i,dest)
        if res:
            return res
    return []

def cheminIII(G,init,dest):
    S,A = G
    inits = []
    dests = []
    for s in S:
        if s[0] == init:
            inits.append(s)
        elif s[0] == dest:
            dests.append(s)

    ways = []

    #Recupere toutes les combinaisons possibles de init et dest avec un temps de depart init > temps de depart dest
    for (nodeStart,nodeTime) in inits:
        for (nodeDest,DestTime) in dests:
            if (DestTime - nodeTime) > 0 :
                ways.append(((nodeStart,nodeTime),(nodeDest,DestTime),(DestTime - nodeTime)))

    #Trie les ways de maniere croissante par rapport au temps (correspond (DestTime - nodeTime))
    ways = sorted(ways, key=lambda tup: tup[2])

    #Renvoie le premier chemin possible de ways
    for initW,destW,time in ways:
        res = algo.bfs(G,initW,destW)
        if res:
            return res
    return []

def cheminIV(G, init, dest):
    return algo.dijkstra(G,init,dest)
