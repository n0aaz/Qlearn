from tkinter import * 

fenetre = Tk()

label = Label(fenetre, text="Qlearning")
label.pack()

fenetre.mainloop()

haut,large=1000,1000
taille=[haut,large]
matrice=[10,10]
fonds=[]

def generfond():
  for i in range(matrice[0]):
    for j in range(matrice[1]):
    canvas.create_rectangle(i*large, j*haut, (i+1)*large, (j+1)*haut, fill="white", width=1)

canvas.pack()

