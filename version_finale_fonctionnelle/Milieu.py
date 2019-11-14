
from tkinter import *
import random
import marshal,copy


master = Tk()
taille = 22
(x, y) = (20, 20)
actions = ["haut", "bas", "gauche", "droite"]

board = Canvas(master, width=x*taille, height=y*taille+20)
coordonnees = (0, y-1)
score = 0
restart = False
walk_reward = -0.05 #malus à chaque mouvement pour minimiser le nombre de mouvements
obstaclage=.15
nombrebonus=0

poubelle=[]
coffre={}
objets={}
listescores=[]

#position des murs


def ecriture_obstacles(chemin,x,y,obstaclage): #Permet d'écrire les coordonnées des obstacles dans un fichier pour les conserver
	obstacles= [(random.randint(0,x-1),random.randint(0,y-1)) for mur in range(int(x*y*obstaclage))]
	fichier=open(chemin,"wb")
	marshal.dump(obstacles,fichier)
	fichier.close()

def lecture (chemin):
	
	fichier=open(chemin,"rb")
			
	variable= marshal.load(fichier)
	return(variable)
	
	fichier.close()
	
#ecriture_obstacles("stockage.txt",x,y,obstaclage)
obstacles= copy.copy(lecture("stockage.txt"))


obstacles.append((6,14)) #ici on teste une petite modification au chemin optimal pour voir si le programme est capab

#cases bonus/malus
special = [(4, 1, "red", -1),(x-1,0 , "yellow", 1)]

bonus_aleatoire =[(random.randint(0,x-1),random.randint(0,y-1),"blue",1) for k in range(nombrebonus)]
for bonus in bonus_aleatoire:
	special.append(bonus)

	
def rendu(special, obstacles, taille, x, y, coordonnees): #méthode graphique pour afficher le rendu de la grille
    global boitescore
    for i in range(x):
        for j in range(y):
            objets[i,j]= board.create_rectangle(i*taille, j*taille, (i+1)*taille, (j+1)*taille, fill="#fffffffff", width=1)
            
    for (i, j, c, w) in special:
        board.create_rectangle(i*taille, j*taille, (i+1)*taille, (j+1)*taille, fill=c, width=1)
    for (i, j) in obstacles:
        board.create_rectangle(i*taille, j*taille, (i+1)*taille, (j+1)*taille, fill="black", width=1)
    
    boitescore = board.create_text(40 , y*taille+10 , fill = "black" , text= "score:"+str(score))

	
rendu(special, obstacles, taille, x, y, coordonnees)
joueur = board.create_rectangle(coordonnees[0]*taille+taille*2/10, coordonnees[1]*taille+taille*2/10,coordonnees[0]*taille+taille*8/10, coordonnees[1]*taille+taille*8/10,fill="orange", width=1, tag="joueur")
board.grid(row=0, column=0)


def recup_coul(couleur):#transforme une "couleur" au format tkinter en triplet rouge vert bleu d'entiers
	coul2=""
	flag=False
	for elem in couleur:
		if elem=="#":
			flag=True
		elif flag:
			coul2+= elem.upper()
	r,g,b=int("0x"+coul2[:3],16),int("0x"+coul2[3:6],16),int("0x"+coul2[6:],16)
	return r,g,b
	
def recomp_coul(r,g,b): #retransforme un triplet d'entiers rouge vert bleu au format couleur tkinter
	triplet= [ hex(r)[2:],hex(g)[2:],hex(b)[2:] ] #codes hexadécimaux de la forme 0x... donc on slice juste après l'indicateur hexadécimal 0x
	sortie="#"
	for i in range(3):
		
		while len(triplet[i])<3:
			triplet[i] ='0'+triplet[i] 			  # correction d'erreur, sinon la sortie n'est pas sous le bon format, il manquera un caractere 
		sortie+=triplet[i]

	return sortie 
			
def edit_coul(x,y,mod): #modifie la couleur d'une case aux positions x,y
	r,g,b= recup_coul(board.itemcget(objets[x, y], "fill"))
	r,g,b= r,max(0,g-mod),b #on diminue la teneur en rouge , pour avoir une case de plus en violette
	
	board.itemconfigure( objets[x, y] , fill=recomp_coul(r,g,b))

def mouvement(dx, dy):
    global coordonnees, x, y, score, walk_reward, joueur, restart , coffre
    if restart :
        reinitialisation()
    new_x = coordonnees[0] + dx
    new_y = coordonnees[1] + dy
    score += walk_reward
    
    if (new_x >= 0) and (new_x < x) and (new_y >= 0) and (new_y < y) and not ((new_x, new_y) in obstacles):
        board.coords(joueur, new_x*taille+taille*2/10, new_y*taille+taille*2/10, new_x*taille+taille*8/10, new_y*taille+taille*8/10)
        coordonnees = (new_x , new_y)
        edit_coul(new_x , new_y , 10)
    else:
        pass #permet de pénaliser les actions inutiles comme un mouvement contre un mur
	
    board.itemconfigure(boitescore, text= "score:"+str(round(score,2))) # on actualise l'afficheur de score
	
    for (i, j, c, w) in special: # c = couleur w = récompense
        if new_x == i and new_y == j:
            
            if c== "yellow" or c=="red":
                score -= walk_reward
                score += w
                for bonus in coffre:
                    score+=w*int(coffre[bonus])
                restart = True
                print("score=",score)
                    
            elif c== "blue":
                score+=w
                coffre[i,j]=True
                #obstacles.append((i,j))
            else:
                poubelle.append((i,j,c,w)) # pour qu'on ne puisse récolter le bonus qu'une seule fois
                #obstacles.append(i,j) #pour transformer l'ancien bonus en mur
                special.remove((i,j,c,w))
            return 

def reinitialisation():
    global coordonnees, score, joueur, restart,listescores,coffre
    coordonnees = (0, y-1)
    listescores.append(score)
    score = 0
    ###############
    coffre={}
    ###############
    restart = False
    for tupls in poubelle:
         special.append(tupls)
         poubelle.remove(tupls)
    board.coords(joueur, coordonnees[0]*taille+taille*2/10, coordonnees[1]*taille+taille*2/10, coordonnees[0]*taille+taille*8/10, coordonnees[1]*taille+taille*8/10)

def etat_reinit():
    return restart


def gui():
	master.mainloop()

