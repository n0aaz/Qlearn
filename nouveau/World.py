from tkinter import *
import random
master = Tk()

Width = 10
(x, y) = (20, 20)
actions = ["up", "down", "left", "right"]

board = Canvas(master, width=x*Width, height=y*Width)
player = (0, y-1)
score = 10
restart = False
walk_reward = -.05
poubelle=[]
coffre={}
objets={}
obstaclage=.15

listescores=[]

#position des murs
walls = [(random.randint(0,x-1),random.randint(0,y-1)) for murs in range(int(x*y*obstaclage))]

#cases bonus/malus
specials = [(4, 1, "red", -1),(x-1,0 , "yellow", 1) ,(random.randint(0,x-1), random.randint(0,y-1), "blue", -0.4),(random.randint(0,x-1), random.randint(0,y-1), "blue",-0.4)]

cell_scores = {}

def render_grid():
    global specials, walls, Width, x, y, player
    for i in range(x):
        for j in range(y):
            objets[i,j]= board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill="#fffffffff", width=1)
            
    for (i, j, c, w) in specials:
        board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill=c, width=1)
    for (i, j) in walls:
        board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill="black", width=1)

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
	
def recomp_coul(r,g,b):
	r2,g2,b2=hex(r)[2:],hex(g)[2:],hex(b)[2:]
	return "#"+r2+g2+b2 #retransforme un triplet d'entiers rouge vert bleu au format couleur tkinter 
			
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
        board.coords(me, new_x*Width+Width*2/10, new_y*Width+Width*2/10, new_x*Width+Width*8/10, new_y*Width+Width*8/10)
        player = (new_x , new_y)
        edit_coul(new_x , new_y , 10)
        
    for (i, j, c, w) in specials:
        if new_x == i and new_y == j:
            score -= walk_reward
            score += w
            if c== "yellow" or c=="red":
                for bonus in coffre:
                    score+=10*int(coffre[bonus])
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
    print(specials)
    board.coords(me, player[0]*Width+Width*2/10, player[1]*Width+Width*2/10, player[0]*Width+Width*8/10, player[1]*Width+Width*8/10)

def has_restarted():
    return restart

render_grid()
me = board.create_rectangle(player[0]*Width+Width*2/10, player[1]*Width+Width*2/10,
                            player[0]*Width+Width*8/10, player[1]*Width+Width*8/10, fill="orange", width=1, tag="me")

board.grid(row=0, column=0)


def start_game():
    master.mainloop()
