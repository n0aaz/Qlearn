######### Ceci est une variante du fichier Milieu sans interface graphique (GUI = Graphic User Interface)

import random
import marshal , copy


taille = 10 #taille graphique, ici inutile
(x, y) = (20, 20) #taille de la grille
actions = ["haut", "bas", "gauche", "droite"]

coordonnees = (0, y-1) #l'agent commence tout en bas à gauche
score = 0
restart = False
walk_reward = -.05
obstaclage=.15

poubelle=[]
coffre={}
objets={}

#position des murs


def ecriture_obstacles(chemin,x,y,obstaclage): #permet d'enregistrer la liste d'obstacles dans un fichier pour une réutilisation future
	obstacles= [(random.randint(0,x-1),random.randint(0,y-1)) for mur in range(int(x*y*obstaclage))]
	fichier=open(chemin,"wb")
	marshal.dump(obstacles,fichier) #marshal.dump sert à enregistrer la variable dans un fichier
	fichier.close()

def lecture (chemin): #permet de retourner une variable contenue dans un fichier
	
	fichier=open(chemin,"rb")
			
	variable= marshal.load(fichier)
	return(variable)
	
	
#ecriture_obstacles("stockage.txt",x,y,obstaclage)
obstacles= copy.copy(lecture("stockage.txt"))

#cases bonus/malus
special = [(4, 1, "red", -1),(x-1,0 , "yellow", 1)]

"""bonus=10
for k in range (3):
	special.append((random.randint(0,x-1),random.randint(0,y-1),"blue",bonus))
"""

print(special)

def mouvement(dx, dy):
    global coordonnees, x, y, score, walk_reward, restart , coffre
    if restart == True:
        reinitialisation()
    new_x = coordonnees[0] + dx
    new_y = coordonnees[1] + dy
    score += walk_reward
    
    if (new_x >= 0) and (new_x < x) and (new_y >= 0) and (new_y < y) and not ((new_x, new_y) in obstacles): #on vérifie que le mouvement est possible
        coordonnees = (new_x , new_y)
    else:
        score -= .1  #sinon on décrémente tout de meme le score de l'agent pour avoir tenté une action inutile
		    
    for (i, j, c, w) in special:
        if new_x == i and new_y == j:
            score -= walk_reward
            score += w
            if c== "yellow" or c=="red":
                #for bonus in coffre:
                    #score+=10*int(coffre[bonus])
                restart = True
                #print("score=",score)
                    
            elif c== "blue":
                coffre[i,j]=True
                obstacles.append((i,j))
            else:
                poubelle.append((i,j,c,w))
                obstacles.append(i,j)
                special.remove((i,j,c,w))
            return 

def reinitialisation(liste):
    global coordonnees, score, restart,coffre
    coordonnees = (0, y-1)
    liste.append(score)
    score = 0
    ###############
    coffre={}
    ###############
    restart = False
    for tupls in poubelle:
         special.append(tupls)
         poubelle.remove(tupls)
         
def etat_reinit():
    return restart

    
