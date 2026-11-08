def sentar_grupos(restaurante, grupos):
    no_sentados = []
    for grupo in grupos:
        clientes = grupo["clientes"]
        hay_aforo = restaurante["ocupacion"] + clientes <= restaurante["capacidad"]
        hay_mesa = len(restaurante["mesas"]) < restaurante["max_mesas"]
        if hay_aforo and hay_mesa:
            restaurante["mesas"].append({"clientes": clientes, "estado":"ocupada","pedido":[]})
            restaurante["ocupacion"] = restaurante["ocupacion"] + clientes
        else:
            no_sentados.append(grupo)
    return no_sentados

def tomar_pedido(mesa, menu):
    print("Menú:")
    for plato, precio in menu.items():
        print("-", plato, ":", precio, "€")
    while True:
        plato = input("Plato (o 'fin' para terminar): ").strip()
        if plato == "fin":
            break
        elif plato in menu:
            mesa["pedido"].append(plato)
            print("Añadido:", plato)
        else:
            print("Ese plato no está en el menú.")
    if len(mesa["pedido"]) > 0:
        mesa["estado"] = "con pedido"



