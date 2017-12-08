from tkinter import * 
from Objets import *

fenetre = Tk()


label = Label(fenetre, text="Qlearning")
label.pack()


large,haut=1000,1000
taille=[large,haut]
bloclarge,blochaut=10,10
matrice=[bloclarge,blochaut]
blocs=[]

canvas = Canvas(fenetre, width=large, height=haut, background='white')

j=Joueur()


def generfond():
  for i in range(matrice[0]):
    for j in range(matrice[1]):
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
        

      

fenetre.mainloop()

