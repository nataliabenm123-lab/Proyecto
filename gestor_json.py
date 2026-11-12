import json
from pathlib import Path

def listar_archivos(ruta):
    nombres = []
    for archivo in sorted(Path(ruta).glob("*.json")):
        nombres.append(archivo.name)
    return nombres

def cargar_restaurante(ruta,nombre_archivo):
    ruta_archivo=Path(ruta)/nombre_archivo
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        restaurante = json.load(archivo)
    return restaurante

def cargar_grupos(ruta, nombre_archivo):
    ruta_archivo= Path(ruta) / nombre_archivo
    with open (ruta_archivo, "r", encoding="utf-8") as archivo: 
        grupos = json.load(archivo)
    return grupos

def guardar_restaurante(ruta, restaurante):
    datos = {
        "nombre": restaurante["nombre"],
        "ubicacion": restaurante["ubicacion"],
        "capacidad": restaurante["capacidad"],
        "max_mesas": restaurante["max_mesas"],
        "menu": restaurante["menu"],
    }
    ruta_archivo = Path(ruta) / restaurante["archivo"]
    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

def cargar_reservas(ruta, nombre_archivo):
    ruta_archivo = Path(ruta) / nombre_archivo
    if not ruta_archivo.exists():
        return []
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        reservas = json.load(archivo)
    return reservas

def guardar_reservas(ruta, nombre_archivo, reservas):
    Path(ruta).mkdir(exist_ok=True)
    ruta_archivo = Path(ruta) / nombre_archivo
    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
        json.dump(reservas, archivo, indent=4, ensure_ascii=False)