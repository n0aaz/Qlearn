class Bloc:
  def __init__(self):
    self.couleur="white"
    self.x=0
    self.y=0
    self.taille=[1,1]
    self.prop='blanc'
    self.bonus=-0.1
    
  def generer(canvas):
    canvas.create_rectangle(self.x*large, self.y*haut, (self.x +1)*large, (self.y+1)*haut, fill=self.couleur, width=1)
  
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
    
    
class Joueur(Bloc):   #joueur est il considéré comme un bloc comme les autres ? superposition possible ?
  def __init__(self):
    super().__init__()
    self.couleur='vert'
    self.score=0
    
  def deplacement (dx,dy):
    if matrice[self.x+dx][self.y+dy].prop='obstacle':   #devrait on créer la map avec des obstacles tout autour pour ne pas avoir de problèmes de limites ?
      return
    self.x+=dx
    self.y+=dy
    self.score+=matrice[self.x][self.y].bonus  #est ce que  ça écrase le bloc sous le joueur ? bonus de la case de départ ou  d'arrivée ?
    if matrice[self.x][self.y].prop='recompense':
      Recompense.prop='blanc'  #ça change les propriétés de la classe ou juste de ce bloc ?
      Recompense.bonus=-0.1
      Recompense.couleur='blanc'
      #autre proposition
      matrice[self.x][self.y].prop='blanc'
      matrice[self.x][self.y].bonus=-0.1
      matrice[self.x][self.y].couleur='blanc'
    
        
    
   ###tkinter : module graphique (à regarder)
