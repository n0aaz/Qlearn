from tkinter import *


class Bloc:
  def __init__(self):
    self.couleur="white"
    self.pos=[0,0]
    self.taille=[5,5]
    self.prop='blanc'
    self.bonus=-0.1
    
  def genere(self,canvas):
    #print(self.x,self.y,self.taille)
    a,b=self.pos[0]*self.taille[0],self.pos[1]*self.taille[1]
    c,d=(self.pos[0]+1)*self.taille[0], (self.pos[1]+1)*self.taille[1]
    print(a,b,c,d)
    truc=canvas.create_rectangle(a,b,c,d, fill=self.couleur, width=1) 
    return truc
    
class Obstacle(Bloc):
  def __init__(self):
    super().__init__()
    self.couleur="black"
    self.prop= 'obstacle'
  
class Recompense(Bloc):
  def __init__(self):
    super().__init__()
    self.couleur='bleu'
    self.bonus=1
    self.prop='recompense'
    
    
class Joueur(Bloc):  
  def __init__(self):
    super().__init__()
    self.couleur='green'
    self.score=0
    
  def deplacement (self,canvas,matrice,dx,dy):
    if matrice[self.pos[0]+dx][self.pos[1]+dy].prop=='obstacle':   
      return
    
    
    self.pos[0] =self.pos[0]+dx
    self.pos[1] =self.pos[1]+dy
    canvas.coords(j,self.pos[0],self.pos[1],self.pos[0]+self.taille[0],self.pos[1]+self.taille[1])
    self.score+=matrice[self.pos[0]][self.pos[1]].bonus  
    if matrice[self.pos[0]][self.pos[1]].prop=='recompense':
      Recompense.prop='white'
      Recompense.bonus=-0.1
      Recompense.couleur='white'
      matrice[self.pos[0]][self.pos[1]].prop='white'
      matrice[self.pos[0]][self.pos[1]].bonus=-0.1
      matrice[self.pos[0]][self.pos[1]].couleur='white'
    
