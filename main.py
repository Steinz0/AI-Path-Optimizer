import algo
import all_ways
import progLineaire
import time

G, init, dest = algo.choiceUser()

GTranfo = algo.tranfo(G)

print("####################################################################################\n")
print("RESULTAT des differents chemins\n")
print("Sommet de depart : %s" %init)
print("Sommet d'arrivee : %s \n\n" %dest)

print("CheminType I")
debutTime = time.time()
print("Le chemin d'arrivee au plus tot est: ")
way = all_ways.cheminI(GTranfo, init, dest)
endTime = time.time()
print(algo.solution(way)+'\n')
print("Le CheminType I detaillee:")
print(way)
print("Temps : %f ms\n\n" %(endTime-debutTime))

print("CheminType II")
debutTime = time.time()
print("Le chemin de depart au plus tard est: ")
way = all_ways.cheminII(GTranfo, init, dest)
endTime = time.time()
print(algo.solution(way)+'\n')
print("Le CheminType II detaillee:")
print(way)
print("Temps : %f ms\n\n" %(endTime-debutTime))

print("CheminType III")
debutTime = time.time()
print("Le chemin le plus rapide est: ")
way = all_ways.cheminIII(GTranfo, init, dest)
endTime = time.time()
print(algo.solution(way)+'\n')
print("Le chemin detaillee:")
print(way)
print("Temps : %f ms\n\n" %(endTime-debutTime))

print("CheminType IV")
debutTime = time.time()
print("Le chemin le plus court est: ")
way = all_ways.cheminIV(GTranfo, init, dest)
endTime = time.time()
print(algo.solution(way)+'\n')
print("Le CheminType IV detaillee:")
print(way)
print("Temps : %f ms\n\n" %(endTime-debutTime))

print("CheminType IV avec GUROBI")
debutTime = time.time()
print("Le chemin le plus court avec GUROBI est: ")
way = progLineaire.gurobi(GTranfo,init,dest)
endTime = time.time()
print("Temps : %f ms\n" %(endTime-debutTime))
print("####################################################################################")
