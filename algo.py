from os import replace
import sys
import random
import numpy as np


def dijkstra(G, init, dest):
    S,A = G
    same_d = []
    same_a = []
    #Recuperation de tous les sommets de departs et arrivees
    for s in S:
        if s[0] == init:
            same_d.append(s)
        elif s[0] == dest:
            same_a.append(s)

    #init : Le depart le plus tot dest : l'arrivee la plus tard
    init = sorted(same_d, key=lambda tup: tup[1])[0]
    dest = sorted(same_a, key=lambda tup: tup[1], reverse=True)[0]
    pred = [None for i in range(len(S))]

    #tab de dists initisaliser a inf sauf pour l'init a 0
    dists = np.zeros(len(S))+np.inf
    dists[G[0][init]] = 0

    visite = set()
    notVisite = S.copy()
    #d_notViste permet de recup toutes les distances des sommets non visite
    d_notVisite = dists[list(notVisite.values())]

    #Tant qu'il reste des sommets a regarder et le min des restes n'est pas un dest
    while len(notVisite)!=0 and (list(notVisite.keys())[np.argmin(d_notVisite)] != dest):

        s,value = list(notVisite.keys())[np.argmin(d_notVisite)]
        visite.add(s)
        notVisite.pop((s,value))

        for ((start,startValue),time,(end,endValue)) in A:
            if (start,startValue) == (s,value):
                if dists[S[(end,endValue)]] > (dists[S[(s,value)]]+time):
                    dists[S[(end,endValue)]] = dists[S[(s,value)]]+time
                    pred[S[(end,endValue)]] = (s,value)

        d_notVisite = dists[list(notVisite.values())]

    #Retrouve le chemin pris et le retourne
    sommet = dest
    path = [sommet]
    while (sommet !=init):
        if not(sommet):
            return []
        sommet = pred[S[sommet]]
        path = [sommet] + path

    return path


class Node:
    def __init__(self,value=None,pere=None):
        self.value = value
        self.pere = pere

    def setPere(self,pere):
        self.pere = pere

    def getValue(self):
        return self.value

    def getPere(self):
        return self.pere

    def getSolution(self):
        if not(self.pere):
            return [self.value]
        else :
            return self.getPere().getSolution()+[self.value]

def getSuccesseur(G,value):
    S,A = G
    successeurs = set()

    for a in A:
        if a[0] == value:
            successeurs.add(a)

    return successeurs

def bfs(G,init,dest):

    visite = []
    frontiere = []
    frontiere.append(Node(init))
    
    #Tant que y'a des noeuds dans la frontiere
    while len(frontiere) != 0 :
        sommetAct = frontiere[0]
        #Si le sommet est final alors on envoie la solution
        if sommetAct.value == dest:
            return sommetAct.getSolution()
        else :
            #sinon on met le sommet dans les visiter et on l'enleve de la frontiere, auquel on va ajouter les voisins du sommet actuel
            visite.append(sommetAct)
            frontiere.remove(sommetAct)
            successeurs = getSuccesseur(G,sommetAct.getValue())
            for s in successeurs:
                frontiere.append(Node(s[-1],sommetAct))

def graphFile(filename):
    A = set()
    S = dict()

    f = open(filename,'r')

    nbSommets = int(f.readline())
    nbAretes = int(f.readline())

    i = 0
    for i in range(nbSommets):
        value = f.readline()
        value = value.replace('\n',' ')

        S[value.split()[0]] = i
        i+=1

    for i in range(nbAretes):
        value = f.readline()
        value = value.replace(',',' ').replace('(',' ').replace(')',' ').replace('\n',' ')

        A.add(tuple(value.split()))

    return (S,A)


def choiceUser():
    mode = ''
    S = []
    A = []
    filename = ''
    while not(mode=='1' or mode=='2' or mode=='3'):
        print("Choissisez le mode d'entree du graphe:")
        print("Via un fichier -> 1")
        print("Via le terminal -> 2")
        print("Generer un graphe -> 3")
        mode = input()

    if mode=='1':
        success = False
        while not(success):
            filename = input("Le nom du fichier: ")
            try:
                f = open(filename,'r')
                success = True
            except FileNotFoundError:
                print("Le fichier %s n'existe pas" % filename)

        S,A = graphFile(filename)
    elif mode=='2':
        A = set()
        S = dict()

        sommets = input("Quels sont les sommets ? : Respectez le format suivant => sommet1;sommet2;... :\n")
        sommets = sommets.split(';')

        for i in range(len(sommets)):
            S[sommets[i]] = i
            i+=1

        aretes = input("Quels sont les aretes ? : Respectez le format suivant =>  (u,v,t,lambda);(u,v,t,lambda);... :\n")
        aretes = aretes.split(';')
        for a in range(len(aretes)):
            u,v,t,lam = tuple(aretes[a][1:-1].split(','))
            A.add((u,v,int(t),int(lam)))
            print(A)
    elif mode=='3':
        nbSom = input("Combien de sommets souhaitez-vous ? : ")

        S,A = generateGraphe(int(nbSom))

    print("Voici les sommets: ")
    print(S)
    success = False
    while not(success):
        d = input("Le sommet de depart: ")
        a = input("Le sommet d'arrivee: ")
        if d in S and a in S:
            success = True
        else:
            print("\nL'un ou les deux sommets n'existe pas! Reessayez.\n")

    return (S,A),d,a

def tranfo(G):
    S,A = G
    i = 0
    sommets = dict()
    arcs = set()
    tab = np.zeros((len(S),2),dtype=object)

    #On creer le tableau des Vin et Vout comme expliquer dans le sujet
    for s in S:
        v_out_for_s = set([(arete[0],int(arete[2])) for arete in A if arete[0] == s])
        v_in_for_s = set([(arete[1],int(arete[2])+1) for arete in A if arete[1] == s])
        tab[i][0] = v_in_for_s
        tab[i][1] = v_out_for_s
        i+=1

    i = 0
    #On ajoute tous les elements a sommets
    for elem in tab.reshape(len(S)*2):
        if elem != set():
            for e in elem:
                if e not in sommets:
                    sommets[e] = i
                    i+=1
    
    #Pour chaque sommet on prend les sommets aux memes label et on ajoute a arcs
    for s in S:
        same = [a for a in sommets if a[0] == s]
        same = sorted(same, key=lambda tup: tup[1])
        for i in range(len(same)-1):
            arcs.add((same[i],0,same[i+1]))

    #Enfin pour tout a = (u,v,t,l) de arcs , on ajoute a arcs ((u,t),l,(v,t+l)) 
    for a in A:
        arcs.add(((a[0],int(a[2])),int(a[3]),(a[1],int(a[2])+int(a[3]))))


    return sommets,arcs

def solution(res):
    #Permet de recontruire le chemin sans tout les noeuds intermediares
    if not(res) or res==[]:
        return "Aucun chemin"
    way = res[0][0]
    for i in range(len(res)-1):
        if res[i][0] != res[i+1][0]:
            way += ' --' + str(res[i][1]) + '--> ' + res[i+1][0]
    return way

def generateGraphe(n,p=0.5,lambd=1):
    S = []
    A = set()
    for i in range(n):
        S.append(str(i))
    for i in range(len(S)):
        sommetRestants = S[(i+1):]
        for j in sommetRestants:
            tirage = random.random()
            if tirage <= p:
                A.add((str(i),j,random.randint(1,np.ceil(n/2)),lambd))
    Sommets = {}
    for i in range(len(S)):
        Sommets[S[i]] = i
    return Sommets,A
