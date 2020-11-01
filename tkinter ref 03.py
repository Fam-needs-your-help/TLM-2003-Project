from tkinter import *
from tkinter import ttk
from tkinter import messagebox

root = Tk()
root.geometry("400x400")
cmb = ttk.Combobox(root, width="10", values=("prova", "ciao", "come", "stai"))


def checkCombo():
    if cmb.get() == "prova":
        messagebox.showinfo("What user choose", "you choose prova")
    elif cmb.get() == "ciao":
        messagebox.showinfo("What user choose", "you choose ciao")
    elif cmb.get() == "come":
        messagebox.showinfo("What user choose", "you choose come")
    elif cmb.get() == "stai":
        messagebox.showinfo("What user choose", "you choose stai")
    elif cmb.get() == "":
        messagebox.showinfo("nothing to show!", "you have to be choose something")


cmb.place(relx="0.1", rely="0.1")
btn = ttk.Button(root, text="Get Value", command=checkCombo)
btn.place(relx="0.5", rely="0.1")

root.mainloop()