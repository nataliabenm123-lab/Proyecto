#opcion 1 de cargar restaurante
from pathlib import Path

def listar_restaurantes(ruta):
    nombres = []
    for archivo in sorted(Path(ruta).glob("*.json")):
        nombres.append(archivo.name)
    return nombres