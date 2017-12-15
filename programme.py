from tkinter import * 
from Objets import *
import numpy as np

fenetre = Tk()


label = Label(fenetre, text="Qlearning")
label.pack()


large,haut=500,500

bloclarge,blochaut=10,10

matrice=[[[] for i in range(bloclarge)]for j in range(blochaut)]

canvas = Canvas(fenetre, width=large, height=haut, background='white')

joueur=Joueur()


def generfond(canvas):
  for i in range(0,bloclarge):
    for j in range(0,blochaut):
      if i==0 or j==0 or i==bloclarge-1 or j==blochaut-1: 
        a=Obstacle()
        a.taille=(large/bloclarge),(haut/blochaut)
        a.x,a.y=i*a.taille[0],j*a.taille[0]
        a.genere(canvas)
      else:
        a=Bloc()
        a.taille=(large/bloclarge),(haut/blochaut)
        a.x,a.y=i*a.taille[0],j*a.taille[0]
        a.genere(canvas)
        
      matrice[i][j].append(int(a.prop=='obstacle'))

generfond(canvas)
canvas.pack()
joueur=Joueur()
joueur.taille=(large/bloclarge),(haut/blochaut)
j=joueur.genere(canvas)
fenetre.mainloop()

print(np.asarray(matrice))
