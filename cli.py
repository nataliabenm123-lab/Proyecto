import gestor_json
import gestion_mesas

def mostrar_menu():
    print("===== GESTIÓN DEL RESTAURANTE =====")
    print("1. Cargar restaurante")
    print("2. Cargar nuevas peticiones de grupos")
    print("3. Tomar un pedido")
    print("4. Cobrar y liberar una mesa")
    print("5. Ampliar el menú")
    print("6. Consultar estado")
    print("7. Salir")
    print("8. Reservas")

def main():
    restaurante = None
    cambios_pendientes = False
    while True:
        mostrar_menu()
        opcion=input("elige una opcion:")
        
        if opcion == "7":  
            if cambios_pendientes:
               gestor_json.guardar_restaurante("restaurantes", restaurante)
               print("Cambios del menú guardados.")
            print("Saliendo del programa...")
            break
        #agregamos esta linea para que lea json

        elif opcion =="1":
            nombres=gestor_json.listar_archivos("restaurantes")
            print("restaurantes disponibles:")

            for numero,nombre in enumerate (nombres,start=1):
                print(numero,"-",nombre)
            eleccion=input("Elige un restaurante (número): ")
            if eleccion.isdigit() and 1 <= int(eleccion) <= len(nombres):
                archivo_elegido = nombres[int(eleccion) - 1]
                
                #Esa línea de abajo lee el JSON del restaurante elegido y guarda el diccionario en restaurante, sustituyendo el None.
                # Justo debajo van las tres líneas que añaden mesas, ocupacion y ganancias.
                restaurante = gestor_json.cargar_restaurante("restaurantes", archivo_elegido)
                restaurante["mesas"]=[]
                restaurante["archivo"] = archivo_elegido
                restaurante["reservas"] = gestor_json.cargar_reservas("reservas", archivo_elegido)
                restaurante["ocupacion"]=0
                restaurante["ganancias"]=0

                print("Restaurante cargado:", restaurante["nombre"])
            else:
                print("Opción no válida.")

        elif opcion =="2":
            if restaurante is None:
                print("Primero debes cargar un restaurante(opción 1).")
            else:
                archivos = gestor_json.listar_archivos("mesas")
                print("Grupos disponibles:")
                for numero, nombre in enumerate(archivos, start=1):
                    print (numero, "-", nombre)
                eleccion = input("Elige un archivo de grupos (número):")
                if eleccion.isdigit() and 1 <= int(eleccion) <= len(archivos):
                    archivo_elegido = archivos[int(eleccion) - 1]
                    grupos = gestor_json.cargar_grupos("mesas", archivo_elegido)
                    no_sentados = gestion_mesas.sentar_grupos(restaurante, grupos)
                    print("Grupos recibidos:", len(grupos))
                    print("Grupos sentados:", len(grupos) - len(no_sentados))
                    print("Ocupación actual:", restaurante["ocupacion"], "de", restaurante["capacidad"])
                    if len(no_sentados) > 0:
                        print("No han podido sentarse:")
                        for grupo in no_sentados:
                            print("- grupo de", grupo["clientes"], "personas")
        elif opcion == "3":
            if restaurante is None:
                print("Primero debes cargar un restaurante (opción 1).")
            elif len(restaurante["mesas"]) == 0:
                print("No hay mesas ocupadas. Siéntalas primero con la opción 2.")
            else:
                continuar = "s"
                while continuar == "s":
                    pendientes = 0
                    print("Mesas pendientes de atender:")
                    for numero, mesa in enumerate(restaurante["mesas"], start=1):
                        if mesa["estado"] == "ocupada":
                            print(numero, "- grupo de", mesa["clientes"], "personas")
                            pendientes = pendientes + 1
                    if pendientes == 0:
                        print("Todas las mesas han sido atendidas.")
                        break
                    eleccion = input("Elige una mesa (número): ")
                    if eleccion.isdigit() and 1 <= int(eleccion) <= len(restaurante["mesas"]):
                        mesa_elegida = restaurante["mesas"][int(eleccion) - 1]
                        if mesa_elegida["estado"] == "ocupada":
                            gestion_mesas.tomar_pedido(mesa_elegida, restaurante["menu"])
                            print("Pedido registrado:", mesa_elegida["pedido"])
                        else:
                            print("Esa mesa ya tiene pedido.")
                    else:
                        print("Opción no válida.")
                    continuar = input("¿Quieres atender otra mesa? (s/n): ").lower()
        elif opcion == "4":
            if restaurante is None:
                    print("Primero debes cargar un restaurante (opción 1).")
            else:
                cobrables = []
                for mesa in restaurante["mesas"]:
                    if mesa["estado"] == "con pedido":
                        cobrables.append(mesa)
                if len(cobrables) == 0:
                    print("No hay mesas con pedido para cobrar.")
                else:
                    print("Mesas para cobrar:")
                    for numero, mesa in enumerate(cobrables, start=1):
                        cuenta = gestion_mesas.calcular_cuenta(mesa, restaurante["menu"])
                        print(numero, "- grupo de", mesa["clientes"], "personas -", cuenta, "€")
                    eleccion = input("Elige la mesa a cobrar (número): ")
                    if eleccion.isdigit() and 1 <= int(eleccion) <= len(cobrables):
                        mesa_elegida = cobrables[int(eleccion) - 1]
                        total = gestion_mesas.cobrar_mesa(restaurante, mesa_elegida)
                        print("Mesa cobrada. Total:", total, "€")
                        print("Ganancias de la noche:", restaurante["ganancias"], "€")
                    else:
                        print("Opción no válida.")
        elif opcion == "6":
            if restaurante is None:
                print("Primero debes cargar un restaurante (opción 1).")
            else:
                print("Restaurante:", restaurante["nombre"])
                print("Capacidad:", restaurante["capacidad"])
                print("Ocupación:", restaurante["ocupacion"])
                print("Mesas activas:")
                if len(restaurante["mesas"]) == 0:
                    print("No hay mesas activas.")
                else:
                    for numero, mesa in enumerate(restaurante["mesas"], start=1):
                        print(numero, "- grupo de", mesa["clientes"], "personas - estado:", mesa["estado"])
                        if len(mesa["pedido"]) > 0:
                            print("   Pedido:", mesa["pedido"])
                    print("Menú:")
                    for plato, precio in restaurante["menu"].items():
                        print("-", plato, ":", precio, "€")
                    print("Ganancias de la noche:", restaurante["ganancias"], "€")
        
        elif opcion == "5":
            if restaurante is None:
                print("Primero debes cargar un restaurante (opción 1).")
            else:
                nombre = input("Nombre del plato: ").strip().lower()
                precio_texto = input("Precio del plato: ").strip().replace(",", ".")
                try:
                    precio = float(precio_texto)
                except ValueError:
                    precio = None
                if nombre == "":
                    print("El nombre no puede estar vacío.")
                elif precio is None or precio <= 0:
                    print("El precio debe ser un número mayor que 0.")
                else:
                    existia = gestion_mesas.ampliar_menu(restaurante["menu"], nombre, precio)
                    cambios_pendientes = True
                    if existia:
                        print("Ese plato ya existía. Precio actualizado a", precio, "€")
                    else:
                        print("Plato añadido:", nombre, "-", precio, "€")

            if restaurante is None:
                print("primero debes cargar un restaurante (opcion 1)")
            else:
                print("has elegido la opcion:", opcion)
        
        elif opcion == "8":
            if restaurante is None:
                print("Primero debes cargar un restaurante (opción 1).")
            else:
                print("--- Reservas ---")
                print("1. Crear reserva")
                print("2. Ver reservas pendientes")
                print("3. Marcar llegada")
                print("4. Cancelar reserva")
                accion = input("Elige una acción: ")
                if accion == "1":
                    nombre = input("Nombre de la reserva: ").strip()
                    personas = input("Número de personas: ").strip()
                    cumple = input("¿Es de cumpleaños? (s/n): ").strip().lower()
                    if nombre == "":
                        print("El nombre no puede estar vacío.")
                    elif not personas.isdigit() or int(personas) < 1:
                        print("El número de personas debe ser un entero mayor que 0.")
                    elif int(personas) > restaurante["capacidad"]:
                        print("La reserva supera la capacidad del restaurante.")
                    elif cumple != "s" and cumple != "n":
                        print("Responde s o n.")
                    else:
                        gestion_mesas.crear_reserva(restaurante, nombre, int(personas), cumple == "s")
                        gestor_json.guardar_reservas("reservas", restaurante["archivo"], restaurante["reservas"])
                        print("Reserva creada para", nombre, "-", personas, "personas")
            
                elif accion == "2":
                    pendientes = []
                    for reserva in restaurante["reservas"]:
                        if reserva["estado"] == "pendiente":
                            pendientes.append(reserva)
                    if len(pendientes) == 0:
                        print("No hay reservas pendientes.")
                    else:
                        print("Reservas pendientes:")
                        for numero, reserva in enumerate(pendientes, start=1):
                            print(numero, "-", reserva["nombre"], "-", reserva["clientes"], "personas")
                            if reserva["cumpleanos"]:
                                print("   Cumpleaños: tarta de cortesía")

                elif accion == "3":
                    pendientes = []
                    for reserva in restaurante["reservas"]:
                        if reserva["estado"] == "pendiente":
                            pendientes.append(reserva)
                    if len(pendientes) == 0:
                        print("No hay reservas pendientes.")
                    else:
                        print("Reservas pendientes:")
                        for numero, reserva in enumerate(pendientes, start=1):
                            print(numero, "-", reserva["nombre"], "-", reserva["clientes"], "personas")
                        eleccion = input("¿Qué reserva ha llegado? (número): ")
                        if eleccion.isdigit() and 1 <= int(eleccion) <= len(pendientes):
                            reserva_elegida = pendientes[int(eleccion) - 1]
                            if gestion_mesas.sentar_reserva(restaurante, reserva_elegida):
                                gestor_json.guardar_reservas("reservas", restaurante["archivo"], restaurante["reservas"])
                                print("Reserva de", reserva_elegida["nombre"], "sentada.")
                                if reserva_elegida["cumpleanos"]:
                                    print("¡Cumpleaños! Se sirve una tarta de cortesía.")
                            else:
                                print("No hay sitio ahora mismo para esta reserva (aforo o mesas completas).")
                        else:
                            print("Opción no válida.")
                else:
                    print("Acción no disponible todavía.")

        else:
            print("Opción no válida. Escribe un número del 1 al 7")
main()


