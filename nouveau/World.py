from tkinter import *
import random
master = Tk()

triangle_size = 0.1
cell_score_min = -0.2
cell_score_max = 0.2
Width = 10
(x, y) = (20, 20)
actions = ["up", "down", "left", "right"]

board = Canvas(master, width=x*Width, height=y*Width)
player = (0, y-1)
score = 1
restart = False
walk_reward = -0.05
poubelle=[]
coffre={}

listescores=[]

#position des murs
walls = [(random.randint(0,x-1),random.randint(0,y-1)) for murs in range((x//2)**2)]

#cases bonus/malus
specials = [(4, 1, "red", -1),(x-1,0 , "yellow", 1) ,(random.randint(0,x-1), random.randint(0,y-1), "blue", -0.04),(random.randint(0,x-1), random.randint(0,y-1), "blue", -0.04)]

cell_scores = {}

def render_grid():
    global specials, walls, Width, x, y, player
    for i in range(x):
        for j in range(y):
            board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill="white", width=1)
            temp = {}
            cell_scores[(i,j)] = temp
    for (i, j, c, w) in specials:
        board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill=c, width=1)
    for (i, j) in walls:
        board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill="black", width=1)

render_grid()


def try_move(dx, dy):
    global player, x, y, score, walk_reward, me, restart , coffre
    if restart == True:
        restart_game()
    new_x = player[0] + dx
    new_y = player[1] + dy
    score += walk_reward
    
    if (new_x >= 0) and (new_x < x) and (new_y >= 0) and (new_y < y) and not ((new_x, new_y) in walls):
        board.coords(me, new_x*Width+Width*2/10, new_y*Width+Width*2/10, new_x*Width+Width*8/10, new_y*Width+Width*8/10)
        player = (new_x, new_y)
        
    for (i, j, c, w) in specials:
        if new_x == i and new_y == j:
            score -= walk_reward
            score += w
            if c== "yellow" or c=="red":
                for bonus in coffre:
                    score+=int(coffre[bonus])
                restart = True
                print("score=",score)
                    
            elif c== "blue":
                coffre[i,j]=True
            else:
                poubelle.append((i,j,c,w))
                walls.append(i,j)
                specials.remove((i,j,c,w))
            return
    #print "score: ", score


def call_up(event):
    try_move(0, -1)


def call_down(event):
    try_move(0, 1)


def call_left(event):
    try_move(-1, 0)


def call_right(event):
    try_move(1, 0)


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

master.bind("<Up>", call_up)
master.bind("<Down>", call_down)
master.bind("<Right>", call_right)
master.bind("<Left>", call_left)

me = board.create_rectangle(player[0]*Width+Width*2/10, player[1]*Width+Width*2/10,
                            player[0]*Width+Width*8/10, player[1]*Width+Width*8/10, fill="orange", width=1, tag="me")

board.grid(row=0, column=0)


def start_game():
    master.mainloop()
