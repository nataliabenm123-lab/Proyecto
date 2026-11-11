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
        print("-", plato, ":", precio, "€")

    while True:
        plato = input("Plato (o 'fin' para terminar): ").strip()

        if plato.lower() == "fin":
            break
        elif plato in menu:
            mesa["pedido"].append(plato)
            print("Añadido:", plato)
        else:
            print("Ese plato no está en el menú.")

    if len(mesa["pedido"]) > 0:
        mesa["estado"] = "con pedido"
        print("Mesa atendida correctamente.")
        print("Número de clientes:", mesa["clientes"])
        
    else:
        print("No se ha registrado ningún plato.")

def calcular_cuenta (mesa, menu):
    total= 0

    for plato in mesa ["pedido"]:
        total += menu[plato]

    return total

def cobrar_mesa(restaurante, mesa):
    total = calcular_cuenta(mesa, restaurante["menu"])

    restaurante["ganancias"] += total
    restaurante["ocupacion"] -= mesa["clientes"]
    restaurante["mesas"].remove(mesa)

    return total 

def ampliar_menu(menu, nombre, precio):
    existia = nombre in menu
    menu[nombre] = precio
    return existia
#menu[nombre] = precio es la línea clave. Si el plato no existe, lo crea; si ya existe, sobrescribe el precio. Un solo comando hace las dos cosas que pide el PDF, y por eso no necesitamos un if.
#return existia devuelve True si ya estaba, para que cli.py pueda avisar al usuario.