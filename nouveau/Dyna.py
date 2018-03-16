import World
import threading
import time
import matplotlib.pyplot as plt
from tkinter import Tk
from World import listescores

discount = 0.99
actions = World.actions
states = []
Q = {}
R = {}
cpteur=0
stop=False
vit=1000000000000

def init_mat():
	#on initialise tous les états possibles , soit tous les tuples (a,b) où a,b appartiennent à [|0;x|]*[|0;y|]
	for i in range(World.x):
		for j in range(World.y):
			states.append((i, j))


	for state in states:
		temp = {}
		recompense = {}
		for action in actions:
			temp[action] = 0.1
			recompense[action] = 0
		Q[state] = temp
		R[state] = recompense

	for (i, j, c, w) in World.specials:
		for action in actions:
			Q[(i, j)][action] = w
			R[(i,j)][recompense]

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


def do_action(action):
    s = World.player
    r = -World.score
    
    if action == actions[0]:
        World.try_move(0, -1)
    elif action == actions[1]:
        World.try_move(0, 1)
    elif action == actions[2]:
        World.try_move(-1, 0)
    elif action == actions[3]:
        World.try_move(1, 0)
    else:
        return
    s2 = World.player
    r += World.score
    return s, action, r, s2

def max_Q(s):
    val ,act= 0,0
    for a, q in Q[s].items():
        if val == 0 or (q > val):
            val , act = q,a
    return act, val

def amelioration_Q(s, a, discount,  max_val) :
    Q[s][a] = R[s][a] + discount*max_val

def amelioration_R(s, a, r):
    R[s][a] = (R[s][a] + r)/2
    

def run():
    global discount,cpteur,listescores
    time.sleep(1)
    t = 1
    k = 50
    while not signal_arret(listescores,1000):
        # Choix de l'action menant à la meilleure récompense
        s = World.player
        max_act, max_val = max_Q(s)
        (s, a, r, s2) = do_action(max_act)

        # Modification des matrices R et Q
        max_act, max_val = max_Q(s2)
	amelioration_R(s, a, r)
	amelioration_Q(s, a, discount, max_val)
	
	for i in range(k) :
	    s = (random.randint(0,x-1),random.randint(0,y-1))
	    if s not in walls :
		a = random.randint(0,3)
		max_act, max_val = max_Q(s)
		amelioration_R(s, a, r)
	        amelioration_Q(s, a, discount, max_val)
	    

        # vérification si le jeu a recommencé
        t += 1.0
        if World.has_restarted():
            World.restart_game()
            cpteur += 1
            time.sleep(0.001)
            t = 1.0

        # vitesse de rafraichissement de l'interface graphique
        time.sleep(1/vit)

init_mat()
t = threading.Thread(target=run)
t.daemon = True
t.start()

World.start_game()
plt.close()
plt.plot(range(cpteur),listescores)
titre= 'discount:'+str(discount)+' walk_reward:'+str(World.walk_reward)
plt.title(titre)
plt.xlabel('Nombre de générations ( matrice '+str(World.x)+'*'+str(World.y)+' )')
plt.ylabel('Score')
plt.savefig(titre+'.png')
plt.show()
