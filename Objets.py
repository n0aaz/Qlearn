from tkinter import *

class Bloc:
  def __init__(self):
    self.couleur="white"
    self.pos=[0,0]
    self.taille=[5,5]
    self.prop='blanc'
    self.bonus=-0.1
    self.objet=0
    
  def genere(self,canvas):
    #print(self.x,self.y,self.taille)
    a,b=self.pos[0]*self.taille[0],self.pos[1]*self.taille[1]
    c,d=(self.pos[0]+1)*self.taille[0], (self.pos[1]+1)*self.taille[1]
    #print(a,b,c,d)
    #matrice[self.pos[0]][self.pos[1]]
    self.objet=canvas.create_rectangle(a,b,c,d, fill=self.couleur, width=1) 
    
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
    nouveau_x,nouveau_y= self.pos[0],self.pos[1]
    nouveau_x+=dx
    nouveau_y+=dy
    x,y=self.pos
    
    print(x,nouveau_x,y,nouveau_y)
    print(matrice[self.pos[0]][self.pos[1]].objet)
    
    if (nouveau_x >= 0) and (nouveau_x <= x) and (nouveau_y >= 0) and (nouveau_y <= y) and not (matrice[nouveau_x][nouveau_y].prop=='obstacle' ):
        canvas.coords(matrice[self.pos[0]][self.pos[1]], nouveau_x*self.taille[0]+self.taille[0]*2/10, nouveau_y*self.taille[0]+self.taille[0]*2/10, nouveau_x*self.taille[0]+self.taille[0]*8/10, nouveau_y*self.taille[0]+self.taille[0]*8/10)
        self.pos = [nouveau_x, nouveau_y]
        
    self.score+=matrice[self.pos[0]][self.pos[1]].bonus  
    if matrice[self.pos[0]][self.pos[1]].prop=='recompense':
      Recompense.prop='white'
      Recompense.bonus=-0.1
      Recompense.couleur='white'
      matrice[self.pos[0]][self.pos[1]].prop='white'
      matrice[self.pos[0]][self.pos[1]].bonus=-0.1
      matrice[self.pos[0]][self.pos[1]].couleur='white'
    
