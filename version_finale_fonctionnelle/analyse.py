import matplotlib.pyplot as plt
import math
import marshal
from World_nogui import lecture,x,y

listegamma,listegen= lecture("resultats.txt")

taillematrice=x
alpha=1
plt.subplot(211)
titre= "matrice "+str(x)+"x"+str(y)+" alpha:" + str(alpha)# + "(dégréssif en e^-0,1)"
plt.title(titre)
plt.xlabel("alpha")
plt.ylabel("score final")
plt.plot(listegamma,listegen[0],label="n= "+ str(taillematrice))


plt.subplot(212)
#titre= "matrice "+str(World_nogui.x)+"x"+str(World_nogui.y)+" alpha:" + str(alpha) #+ "(dégréssif en e^-0,001)"
#plt.title(titre)
plt.xlabel("alpha")
plt.ylabel("nombre de générations)")
plt.plot(listegamma,listegen[1],label="n= "+ str(taillematrice)+ " d/da="+str(round((listegen[1][-1]-listegen[1][0])/(listegamma[-1]-listegamma[0]),2)))

#plt.legend()

manager = plt.get_current_fig_manager()
manager.resize(*manager.window.maxsize())

#plt.savefig(titre+'.png')
plt.show()

