import json 
import os
carpeta = "datos_restaurantes"

with open("datos_restaurantes.json", "r", encoding="utf-8") as archivo:
    restaurantes = json.load(archivo)

print(restaurantes)

print("Restaurantes disponibles:")

for nombre in restaurantes:
    print(nombre)

opcion = input("Elige un restaurante: ")

if opcion in restaurantes:
    datos = restaurantes[opcion]
    print("Has seleccionado:", datos["nombre"])
else:
    print("Restaurante no encontrado")


restaurante["mesas"] = []
restaurante["ocupacion"] = 0
restaurante["ganancias"] = 0

