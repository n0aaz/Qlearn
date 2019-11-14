######### Ceci est une variante du fichier Apprentissage sans interface graphique (GUI = Graphic User Interface)
import Milieu_nogui
import threading
import time
import marshal
import math
import matplotlib.pyplot as plt


def init_var(n):
	global actions,etats,Q,cpteur,listescores
	import Milieu_nogui
	Milieu_nogui.x=n
	Milieu_nogui.y=n
	listescores=[]
	cpteur=0
	actions = Milieu_nogui.actions
	etats = []
	Q = {}
	
def init_mat():
	#on initialise tous les états possibles , soit tous les tuples (a,b) où a,b appartiennent à [|0;x|]*[|0;y|]
	for i in range(Milieu_nogui.x):
		for j in range(Milieu_nogui.y):
			etats.append((i, j))

def decouverte(etat):
	if etat not in Q :
		temp = {}
		for action in actions:
			temp[action] = 0.1
		Q[etat] = temp
		
def signal_arret(liste,stop):
#cette fonction nous permet d'envoyer un signal d'arret au programme principal quand le score a convergé
#on considère qu'il y a convergence lorsqu'un même score se répète 10 fois
	n=len(liste)
	if n<stop+1:
		return False
	aux= liste[n-1]
	
	for k in range(n-2,n-stop,-1):
		if liste[k] != aux:
			return False
		aux = liste[k]
	return True

def faire(action):
    s = Milieu_nogui.coordonnees
    r = -Milieu_nogui.score
    
    if action == actions[0]: #up
        Milieu_nogui.mouvement(0, -1)
    elif action == actions[1]: #down
        Milieu_nogui.mouvement(0, 1)
    elif action == actions[2]: #left
        Milieu_nogui.mouvement(-1, 0)
    elif action == actions[3]: #right
        Milieu_nogui.mouvement(1, 0)
    else:
        return
    s2 = Milieu_nogui.coordonnees
    r += Milieu_nogui.score
    return s, action, r, s2

def max_Q(s): #retourne la plus grande valeur de Q[s] et l'action associée
    val ,act= 0,0
    for a, q in Q[s].items():
        if val == 0 or (q > val):
            val , act = q,a
    return act, val

def inc_Q(s, a, alpha, inc):
    Q[s][a] = round((1-alpha)*Q[s][a] + alpha*inc , 5) #incrémente la valeur de la matrice Q

def lancer(gamma,alpha):
	
    global cpteur,listescores
    time.sleep(1)
    t = 1
    while not signal_arret(listescores,5):
        # Choix de l'action menant à la meilleure récompense
        s = Milieu_nogui.coordonnees
        decouverte(s)
        
        max_act, max_val = max_Q(s)
        (s, a, r, s2) = faire(max_act)
        decouverte(s2)

        # Modification de la matrice Q
        max_act, max_val = max_Q(s2)
        inc_Q(s, a, alpha, r + gamma * max_val)
        #print(Q[s],Milieu_nogui.score)

        # on veut savoir si le jeu a redémarré
        t += 1.0
        if Milieu_nogui.etat_reinit() or abs(Milieu_nogui.score) > 10000: #la deuxieme condition est nécessaire en cas de blocage sur une case non terminale
            Milieu_nogui.reinitialisation(listescores)
            cpteur += 1
            #time.sleep(0.001)
            t = 1.0

        # vitesse de rafraichissement de l'interface graphique
        #time.sleep(1/vit)
  
######## Methodes de tracé ##########


def moyenne(l):
	s=0
	for elem in l:
		s+=elem
	return s/len(l)

nombre_iterations=1
#for taillematrice in range(15,21):
listegamma,listegen=[],[[],[]]
#Milieu_nogui.ecriture_obstacles("stockage.txt",taillematrice,taillematrice,Milieu_nogui.obstaclage)
taillematrice=20

gamma=[99,100]

for gamma_var in [0.01*i for i in range(gamma[0],gamma[1])]:   
	liste_lissage=[[],[]]
	for k in range(nombre_iterations):
		t0=time.time() #référence de temps, suivi du temps d'exécution
		
		init_var(taillematrice)
		init_mat()
		alpha=1

		lancer(gamma_var,alpha)
		#thr= threading.Thread(target=lancer(gamma,1))
		#thr.daemon=True
		#thr.start
		liste_lissage[0].append(listescores[len(listescores)-1])
		liste_lissage[1].append(len(listescores))
		
		print("taillematrice=",taillematrice,"g=",gamma_var," t=",round(time.time()-t0,3))
		
	listegamma.append(gamma_var)
	listegen[0].append(moyenne(liste_lissage[0]))
	listegen[1].append(moyenne(liste_lissage[1]))


marshal.dump([listegamma,listegen],open("resultats.txt","wb")) #exportation des résultats pour analyse ultérieure
marshal.dump(Q,open("Q.txt","wb"))	#Exportation de la matrice Q apres calculs : chemin optimal
		

plt.subplot(211)
titre= "matrice "+str(Milieu_nogui.x)+"x"+str(Milieu_nogui.y)+" alpha:" + str(alpha)# + "(dégréssif en e^-0,1)"
plt.title(titre)
plt.xlabel("gamma")
plt.ylabel("score final")
plt.plot(listegamma,listegen[0],label="n="+ str(taillematrice))

plt.subplot(212)
#titre= "matrice "+str(Milieu_nogui.x)+"x"+str(Milieu_nogui.y)+" alpha:" + str(alpha) #+ "(dégréssif en e^-0,001)"
#plt.title(titre)
plt.xlabel("alpha")
plt.ylabel("nombre de générations")
plt.plot(listegamma,listegen[1],label="n= "+ str(taillematrice))#+ " d/da="+str(round((listegen[1][-1]-listegen[1][0])/(listegamma[-1]-listegamma[0]),2)))

plt.legend()

manager = plt.get_current_fig_manager()
manager.resize(*manager.window.maxsize())

#plt.savefig(titre+'.png')
plt.show()


 






