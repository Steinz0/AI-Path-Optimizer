import numpy as np
from gurobipy import *
import os



def gurobi(G,depart,arrivee):



    som,matIncidence = GraphtoGurobi(G)
    nbsom = len(som)

    same_a = []
    same_d = []
    for s in som:
        if s[0] == depart:
            same_d.append(s)
        elif s[0] == arrivee:
            same_a.append(s)

    init = sorted(same_d, key=lambda tup: tup[1])[0]
    dest = sorted(same_a, key=lambda tup: tup[1], reverse=True)[0]


    indInit = som.index(init)
    indDest = som.index(dest)

    a = []
    b = []

    for i_ref in range(nbsom):
        c = np.zeros((nbsom,nbsom))
        for i in range(nbsom):
            for j in range(nbsom):
                if i == i_ref:
                    c[i,j] += 1 * matIncidence[i,j]
                    c[j,i] += -1 * matIncidence[j,i]
        a += [c.reshape(nbsom**2)]

    for i in range(nbsom):
        if i == indInit:
            b += [1]
        elif i == indDest:
            b += [-1]
        else:
            b += [0]

    m = Model("mogplex")
    os.system('echo lalamsamuel@gmail.com')

    coefObj = [matIncidence[i,j] for i in range(nbsom) for j in range(nbsom)]

    x = []
    for i in range(nbsom):
        for j in range(nbsom):
            x.append(m.addVar(vtype=GRB.BINARY, lb=0, name="x_%d,%d" % (i,j)))

    m.update()

    obj = LinExpr()
    obj = 0
    for j in range(nbsom**2):
        obj += coefObj[j] * x[j]

    m.setObjective(obj,GRB.MINIMIZE)
    a = np.array(a).astype(int)

    for i in range(len(a)):
        m.addConstr(quicksum(a[i][j]*x[j] for j in range(nbsom**2)) == b[i], "Contrainte%d" % i)

    m.optimize()

    dico = dict()
    i = 1
    for s in som:
        dico[i] = s
        i+=1
    var = []
    for j in range(nbsom**2):
        if x[j].x != 0:
            var += [x[j].x]
        else:
            var += [0]

    print("\n---------------------START GUROBI---------------------n")
    var = np.reshape(var,(nbsom,nbsom))
    print("Le chemin le plus court est :")
    for i in range(len(var)):
        for j in range(len(var[0])):
            if var[i][j]==1:
                print(dico[(j%nbsom)+1],'->',dico[(i%nbsom)+1])

    print("\n----------------------END GUROBI----------------------n")

def GraphtoGurobi(G):
    S,A = G
    matIncidence = np.zeros((len(S),len(S)))
    sommets = list(S.keys())

    sommets = sorted(sommets, key=lambda tup: (tup[0],tup[1]))

    S_sorted = dict()
    i = 0
    for s in sommets:
        S_sorted[s] = i
        i += 1

    for s in S_sorted:
        for (av,_,ap) in A:
            if av == s:
                matIncidence[S_sorted[s]][S_sorted[ap]] = 1
            elif ap == s:
                matIncidence[S_sorted[s]][S_sorted[av]] = -1

    return sommets, np.array(matIncidence)
