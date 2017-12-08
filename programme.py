from tkinter import * 
from Objets import *

fenetre = Tk()


label = Label(fenetre, text="Qlearning")
label.pack()


large,haut=1000,1000

bloclarge,blochaut=10,10

matrice=[[[] for i in range bloclarge]for j in range blochaut]

canvas = Canvas(fenetre, width=large, height=haut, background='white')

joueur=Joueur()


def generfond():
  for i in range(bloclarge):
    for j in range(blochaut):
      if i==1 or j==1 or i==bloclarge-1 or i==blochaut-1:
        a=Obstacle()
        a.x=i*(large/bloclarge)
        a.y=i*(haut/blochaut)
        a.genere(canvas)
      else:
        a=Bloc()
        a.x=i*(large/bloclarge)
        a.y=i*(haut/blochaut)
        a.genere(canvas)
        
      matrice[i][j].append(a)
       

      

fenetre.mainloop()

