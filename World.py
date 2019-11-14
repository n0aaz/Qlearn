
from tkinter import *
import random


master = Tk()
taille = 10
(x, y) = (30, 30)
actions = ["up", "down", "left", "right"]

board = Canvas(master, width=x*taille, height=y*taille)
player = (0, y-1)
score = 0
restart = False
walk_reward = -.05
obstaclage=.15

poubelle=[]
coffre={}
objets={}
listescores=[]

#position des murs

walls = [(random.randint(0,x-1),random.randint(0,y-1)) for mur in range(int(x*y*obstaclage))]

#cases bonus/malus
specials = [(4, 1, "red", -1),(x-1,0 , "yellow", 1) ,(random.randint(0,x-1), random.randint(0,y-1), "blue", walk_reward),(random.randint(0,x-1), random.randint(0,y-1), "blue",walk_reward)]

cell_scores = {}

	
def render_grid(specials, walls, taille, x, y, player):
    for i in range(x):
        for j in range(y):
            objets[i,j]= board.create_rectangle(i*taille, j*taille, (i+1)*taille, (j+1)*taille, fill="#fffffffff", width=1)
            
    for (i, j, c, w) in specials:
        board.create_rectangle(i*taille, j*taille, (i+1)*taille, (j+1)*taille, fill=c, width=1)
    for (i, j) in walls:
        board.create_rectangle(i*taille, j*taille, (i+1)*taille, (j+1)*taille, fill="black", width=1)

def creation(specials, walls, taille, x, y, player):
	
	render_grid(specials, walls, taille, x, y, player)
	me = board.create_rectangle(player[0]*taille+taille*2/10, player[1]*taille+taille*2/10,player[0]*taille+taille*8/10, player[1]*taille+taille*8/10,fill="orange", width=1, tag="me")
	board.grid(row=0, column=0)
	return me

me= creation(specials, walls, taille, x, y, player)

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


def try_move(dx, dy):
    global player, x, y, score, walk_reward, me, restart , coffre
    if restart == True:
        restart_game()
    new_x = player[0] + dx
    new_y = player[1] + dy
    score += walk_reward
    
    if (new_x >= 0) and (new_x < x) and (new_y >= 0) and (new_y < y) and not ((new_x, new_y) in walls):
        board.coords(me, new_x*taille+taille*2/10, new_y*taille+taille*2/10, new_x*taille+taille*8/10, new_y*taille+taille*8/10)
        player = (new_x , new_y)
        edit_coul(new_x , new_y , 10)
        
    for (i, j, c, w) in specials:
        if new_x == i and new_y == j:
            score -= walk_reward
            score += w
            if c== "yellow" or c=="red":
                #for bonus in coffre:
                    #score+=10*int(coffre[bonus])
                restart = True
                print("score=",score)
                    
            elif c== "blue":
                coffre[i,j]=True
                walls.append((i,j))
            else:
                poubelle.append((i,j,c,w))
                walls.append(i,j)
                specials.remove((i,j,c,w))
            return

def restart_game():
    global player, score, me, restart,listescores,coffre
    player = (0, y-1)
    listescores.append(score)
    score = 1
    ###############
    coffre={}
    ###############
    restart = False
    for tupls in poubelle:
         specials.append(tupls)
         poubelle.remove(tupls)
    board.coords(me, player[0]*taille+taille*2/10, player[1]*taille+taille*2/10, player[0]*taille+taille*8/10, player[1]*taille+taille*8/10)

def has_restarted():
    return restart



def start_game():
    master.mainloop()
    
