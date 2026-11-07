def sentar_grupos(restaurante, grupos):
    no_sentados = []
    for grupo in grupos:
        clientes = grupo["clientes"]
        hay_aforo = restaurante["ocupacion"] + clientes <= restaurante["capacidad"]
        hay_mesa = len(restaurante["mesas"]) < restaurante["mesas_max"]
        if hay_aforo and hay_mesa:
            restaurante["mesas"].append({"clientes": clientes})
            restaurante["ocupacion"] = restaurante["ocupacion"] + clientes
        else:
            no_sentados.append(grupo)
    return no_sentados
