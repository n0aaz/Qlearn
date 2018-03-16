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
		for action in actions:
			temp[action] = 0.1
		Q[state] = temp

	for (i, j, c, w) in World.specials:
		for action in actions:
			Q[(i, j)][action] = w

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

def inc_Q(s, a, alpha, inc):
    Q[s][a] = (1 - alpha)*Q[s][a] + alpha*inc


def run():
    global discount,cpteur,listescores
    time.sleep(1)
    alpha = 1
    t = 1
    while not signal_arret(listescores,1000):
        # Choix de l'action menant à la meilleure récompense
        s = World.player
        max_act, max_val = max_Q(s)
        (s, a, r, s2) = do_action(max_act)

        # Modification de la matrice Q
        max_act, max_val = max_Q(s2)
        inc_Q(s, a, alpha, r + discount * max_val)

        # Check if the game has restarted
        t += 1.0
        if World.has_restarted():
            World.restart_game()
            cpteur += 1
            time.sleep(0.001)
            t = 1.0

        # Update the learning rate
        alpha = pow(t, -0.001)

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
