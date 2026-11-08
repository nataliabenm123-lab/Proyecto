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

    print("Menú del restaurante:")
    for plato, precio in menu.items():
        print(plato, "-", precio, "€")

    pedidos = []

    for cliente in range(1, mesa["clientes"] + 1):
        pedido = input(f"¿Qué desea pedir el cliente {cliente}? ")

        while pedido not in menu:
            print("Ese plato no está en el menú.")
            pedido = input(f"¿Qué desea pedir el cliente {cliente}? ")

        pedidos.append(pedido)

    mesa["pedido"] = pedidos
    mesa["estado"] = "con pedido"

    print("Pedido registrado correctamente.")
    print("Platos pedidos:", pedidos)



