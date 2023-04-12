import tkinter as tk
from PIL import Image
import generation

def generate(SizeX, SizeY, Bordure):
    # Code to execute when the button is clicked
    print(type(Bordure))
    generation.test((int(SizeX), int(SizeY)), int(Bordure), False)


# Creation de la fenetre principale
root = tk.Tk()
root.geometry("500x250")

# Creation des widgets
label1 = tk.Label(root, text="Size X:")
entry1 = tk.Entry(root)
entry1.insert(0, "8000")  

label2 = tk.Label(root, text="Size Y:")
entry2 = tk.Entry(root)
entry2.insert(0, "8000")  


label3 = tk.Label(root, text="Bordure :")
entry3 = tk.Entry(root)
entry3.insert(0, "10")  


var = tk.IntVar()
checkbox = tk.Checkbutton(root, text="Case a cocher", variable=var)
#checkbox.pack()


button = tk.Button(root, text="Generer", command=lambda: generate(entry1.get(), entry2.get(), entry3.get()))

# Placement des widgets dans la fenetre
label1.grid(row=0, column=0, padx=10, pady=10)
entry1.grid(row=0, column=1, padx=10, pady=10)

label2.grid(row=1, column=0, padx=10, pady=10)
entry2.grid(row=1, column=1, padx=10, pady=10)

label3.grid(row=2, column=0, padx=10, pady=10)
entry3.grid(row=2, column=1, padx=10, pady=10)


checkbox.grid(row=4, column=0, padx=10, pady=10)

button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Lancement de la boucle principale
root.mainloop()