
import Milieu
import threading
import time

import tkinter as tk
from tkinter import Tk

import pyscreenshot as ImageGrab

from Milieu import listescores

import marshal,random

def init_var(compteur): #initialise toutes les variables
	global gamma,actions,etats,Q,cpteur
	cpteur=compteur
	gamma = 0.9
	actions = Milieu.actions
	etats = []
	Q = {}
	#Q = Milieu.lecture('Q.txt') #On lit une matrice Q précédemment enregistrée
	cpteur=0
	

init_var(0)

def init_mat():
	#on initialise tous les états possibles , soit tous les tuples (a,b) où a,b appartiennent à [|0;x|]*[|0;y|]
	for i in range(Milieu.x):
		for j in range(Milieu.y):
			etats.append((i, j))

def decouverte(etat):
	if etat not in Q :
		temp = {}
		for action in actions:
			temp[action] = 0.1
		Q[etat] = temp

def signal_arret(liste,stop):
#cette fonction nous permet d'envoyer un signal d'arret au programme principal quand le score a convergé
#on considère qu'il y a convergence lorsqu'un même score se répète "stop" fois
	n=len(liste)
	if n<stop+1:
		return False
	aux= liste[n-1]
	
	for k in range(n-2,n-stop,-1):
		if liste[k] != aux:
			return False
		aux = liste[k]
	return True


def faire(s,action):
    r = -Milieu.score
    
    if action == actions[0]:
        Milieu.mouvement(0, -1)
    elif action == actions[1]:
        Milieu.mouvement(0, 1)
    elif action == actions[2]:
        Milieu.mouvement(-1, 0)
    elif action == actions[3]:
        Milieu.mouvement(1, 0)
    else:
        return
    s2 = Milieu.coordonnees
    r += Milieu.score
    
    #l'agent découvre la récompense r par le calcul , à aucun moment elle ne lui est pré fournie
    return s, action, r, s2

def max_Q(s):#retourne la plus grande valeur de Q[s] et l'action associée
	val ,act= 0,0
	if random.random() < 0.003:
		act= Milieu.actions[random.randint(0,3)]
		val= Q[s][act]
	else:
		for a, q in Q[s].items():
			if val == 0 or (q > val):
				val , act = q,a
	return act, val

def inc_Q(s, a, alpha, inc):
	Q[s][a] = round((1-alpha)*Q[s][a] + alpha*inc , 8) #incrémente la valeur de la matrice Q


def lancer():
	
    global cpteur,listescores,gamma,alpha
    time.sleep(1)
    alpha = 1
    t = 1
    while not signal_arret(listescores,100):
        
        s = Milieu.coordonnees
        decouverte(s) #l'agent ajoute l'état s à Q si il lui est inconnu, sinon cette fonction ne fait rien
        
        print("Q(",s,")","=",Q[s])
        
        max_act, max_val = max_Q(s) # action qui maximise la valeur de Q à partir d'un état donné
        
        print("meilleure action :",max_act)
        (s, a, r, s2) = faire(s,max_act)
        
        decouverte(s2)
        
        #print("Q("+str(s)+") =" +str(Q[s]))

        # Modification de la matrice Q
        max_act, max_val = max_Q(s2)
        
        inc_Q(s, a, alpha, r + gamma * max_val)
        print("après actualisation" ,"Q(",s,")","=",Q[s])
        

        # on verifie si le monde doit être réinitialisé
        t += 1.0
        if Milieu.etat_reinit() or abs(Milieu.score) > 10000: #limite nécessaire sinon le programme ne peut terminer dans certains cas
            Milieu.reinitialisation()
            cpteur += 1
            #time.sleep(0.001)
            t = 1.0

        # vitesse de rafraichissement de l'interface graphique
        time.sleep(5)
    
    # lignes de capture d'écran
    x = Milieu.master.winfo_rootx()
    y = Milieu.master.winfo_rooty()
    w = Milieu.master.winfo_width()
    h = Milieu.master.winfo_height()
	
    titre= "matrice "+str(Milieu.x)+"*"+str(Milieu.y)+" gamma:"+str(gamma)+ " alpha:" + str(alpha)
    img= ImageGrab.grab((x+2, y+2, x+w-2, y+h-2)).save(titre+"_grille.png") 
    # lignes de capture d'écran
   
init_mat()
#lancer()
#avec lancer: l'interface graphique n'est affichée qu'à la fin
#utilisation de threading: permet une execution en temps reel
t = threading.Thread(target=lancer)
t.daemon = True
t.start()


Milieu.gui()
 
import matplotlib.pyplot as plt
plt.close()
plt.plot(range(cpteur),listescores)
titre= "matrice "+str(Milieu.x)+"*"+str(Milieu.y)+" gamma:"+str(gamma)+ " alpha:" + str(alpha) +"(récompense immediate:mur)"
plt.title(titre)
plt.xlabel('Nombre de générations ( matrice '+str(Milieu.x)+'*'+str(Milieu.y)+' )')
plt.ylabel('Score')
plt.savefig(titre+'.png')
plt.show()

marshal.dump(Q,open("Q.txt",'wb'))






