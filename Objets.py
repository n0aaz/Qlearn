class Bloc:
  def __init__(self):
    self.couleur='blanc'
    self.x=0
    self.y=0
    self.taille=[1,1]
    self.prop='blanc'
  
class Obstacle(Bloc):
  def __init__(self):
    Bloc.__init__(self)
    self.couleur='noir'
    self.prop= 'obstacle'
  
class Recompense(Bloc):
  def __init__(self):
    Bloc.__init__(self)
    self.couleur='bleu'
    self.bonus=1
    self.prop='recompense'
    self.passage=False
    
    #Exemple pour johann 
    ### def deplacement(dx,dy):
    blocencours=matrice[bloc.x+dx,bloc]
    if matrice[bloc.x+dx,bloc] !=0:
      if blocencours.prop== 'obstacle' :
        pass
      elif blocencours.prop == 'recompense':
        self.score+=blocencours.bonus
        blocencours.passage=True
    else:
      self.x=self.x+dx
      bonjour
        ###
