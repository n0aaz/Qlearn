import random
import marshal

x=25
y=25
obstaclage=.15

def ecriture_obstacles(chemin,x,y,obstaclage):
	obstacles= [(random.randint(0,x-1),random.randint(0,y-1)) for mur in range(int(x*y*obstaclage))]
	fichier=open(chemin,"wb")
	marshal.dump(obstacles,fichier)
	fichier.close()

def lecture (chemin):
	
	fichier=open(chemin,"rb")
			
	variable= marshal.load(fichier)
	return(variable)
	
	fichier.close()
	
print(lecture("stockage.txt")))
	



