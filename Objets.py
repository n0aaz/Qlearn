from tkinter import *

class Bloc:
  def __init__(self):
    self.couleur="white"
    self.x=0
    self.y=0
    self.taille=[10,10]
    self.prop='blanc'
    self.bonus=-0.1
    
  def genere(self,canvas):
    #print(self.x,self.y,self.taille)
    a,b,c,d=self.x, self.y, (self.x)+self.taille[0], (self.y)+self.taille[1]
    print(a,b,c,d)
    truc=canvas.create_rectangle(a,b,c,d, fill=self.couleur, width=3) 
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
    
  def deplacement (j,canvas,matrice,dx,dy):
    if matrice[self.x+dx][self.y+dy].prop=='obstacle':   
      return
    
    
    self.x +=dx
    self.y +=dy
    canvas.coords(j,self.x,self.y,self.x+self.taille[0],self.y+self.taille[1])
    self.score+=matrice[self.x][self.y].bonus  
    if matrice[self.x][self.y].prop=='recompense':
      Recompense.prop='white'
      Recompense.bonus=-0.1
      Recompense.couleur='white'
      matrice[self.x][self.y].prop='white'
      matrice[self.x][self.y].bonus=-0.1
      matrice[self.x][self.y].couleur='white'
    
