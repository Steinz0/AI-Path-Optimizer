import algo
import all_ways
import progLineaire
import time
import numpy as np
import matplotlib.pyplot as plt

l1=[]
l2=[]
nodes = [k for k in range(10,50)]
rate = np.arange(0.1,1,.1)

for i in nodes:

    S,A= algo.generateGraphe(i,p=0.5)
    Gt = algo.tranfo((S,A))

    start = time.time()
    all_ways.cheminIV(Gt,'0',str((i-1)))
    end = time.time()
    l1.append(end - start)

    start = time.time()
    progLineaire.gurobi(Gt,'0',str((i-1)))
    end = time.time()
    l2.append(end - start)

figure,ax = plt.subplots()
ax.plot(nodes,l1)
ax.plot(nodes,l2)
plt.show()

l1=[]
l2=[]

for i in rate:
    S,A= algo.generateGraphe(20,p=i)
    Gt = algo.tranfo((S,A))

    start = time.time()
    all_ways.cheminIV(Gt,'0',str((20-1)))
    end = time.time()

    l1.append(end - start)

    start = time.time()
    progLineaire.gurobi(Gt,'0',str((i-1)))
    end = time.time()
    l2.append(end - start)

figure,ax = plt.subplots()
ax.plot(rate,l1)
ax.plot(rate,l2)
plt.show()
