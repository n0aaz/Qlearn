
from tkinter import *
#from Learner import x,y,walk_reward,obstaclage
import random

master = Tk()
taille = 10
(x, y) = (10, 10)
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

walls = [(random.randint(0,x-1),random.randint(0,y-1)) for murs in range(int(x*y*obstaclage))]

#cases bonus/malus
specials = [(4, 1, "red", -1),(x-1,0 , "yellow", 1) ,(random.randint(0,x-1), random.randint(0,y-1), "blue", walk_reward),(random.randint(0,x-1), random.randint(0,y-1), "blue",walk_reward)]

cell_scores = {}
