import tkinter
from tkinter import ttk
root = tkinter.Tk()
''' 
widgets are added here 
'''
brands = ["Bugatti","VW","Opel","Porsche"]

models = [["Veyron","Chiron"],
          ["Golf","Passat","Polo","Caddy"],
          ["Insignia","Corsa","Astra"],
          ["Taycan","Cayenne","911"]]

car_brand = ttk.Combobox(root, width=37, value=(brands))
car_brand.grid(row=3, column=1, columnspan=2, padx=10, pady=2, sticky='w')

def callback(eventObject):
    abc = eventObject.widget.get()
    car = car_brand.get()
    index=brands.index(car)
    car_model.config(values=models[index])

car_model = ttk.Combobox(root, width=37)
car_model.grid(row=4, column=1, columnspan=2, padx=10, pady=2, sticky='w')
car_model.bind('<Button-1>', callback)

root.mainloop()