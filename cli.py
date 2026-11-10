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

def main():
    restaurante = None
    ruta_restaurante = None

    while True:
        mostrar_menu()
        opcion=input("elige una opcion:")
        
        if opcion == "7":                      
            print("Saliendo del programa...", "\n","--OUT--")
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
                ruta_restaurante = "restaurantes/" + archivo_elegido
                restaurante = gestor_json.cargar_restaurante("restaurantes", archivo_elegido)
                restaurante["mesas"]=[]
                restaurante["ocupacion"]=0
                restaurante["ganancias"]=0
                print(restaurante)

                print("Restaurante cargado:", restaurante["nombre"])
            else:
                print("Opción no válida.")

        elif opcion =="2":
            if restaurante is None:
                print("Primero debes elegir un restaurante(opción 1).")
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
                    print(restaurante["mesas"])
                    print("Grupos recibidos:", len(grupos))
                    print("Grupos sentados:", len(grupos) - len(no_sentados))
                    print("Ocupación actual:", restaurante["ocupacion"], "de", restaurante["capacidad"])
                    if len(no_sentados) > 0:
                        print("No han podido sentarse:")
                        for grupo in no_sentados:
                            print("- grupo de", grupo["clientes"], "personas")
                    
                else:
                    print("Opción no válida.")
                
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
                        if mesa["estado"] == "socupada":
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
                print("Mesas disponibles para cobrar:")
                pendientes = 0

                for numero, mesa in enumerate(restaurante["mesas"], start=1):
                    if mesa["estado"] == "con pedido":
                        print(numero, "-", mesa["clientes"], "clientes")
                        pendientes += 1

                if pendientes == 0:
                    print("No hay mesas disponibles para cobrar.")

                else:
                    eleccion = input(
                        "Elige la mesa que quieres cobrar (número): "
                    ).strip()

                    if (
                        eleccion.isdecimal()
                        and 1 <= int(eleccion) <= len(restaurante["mesas"])
                    ):
                        mesa_elegida = restaurante["mesas"][int(eleccion) - 1]

                        if mesa_elegida["estado"] == "con pedido":
                            total = gestion_mesas.cobrar_mesa(
                                restaurante, mesa_elegida
                            )

                            print(f"Cuenta de la mesa {int(eleccion)}: {total:.2f} €")
                            print("Mesa cobrada y liberada correctamente.")
                            print("Ocupación actual:", restaurante["ocupacion"])
                            print(
                                f"Ganancias de esta noche: "
                                f"{restaurante['ganancias']:.2f} €"
                            )

                        else:
                            print("Esta mesa todavía no tiene un pedido.")

                    else:
                        print("Número de mesa no válido.")


        elif opcion == "5":

            if restaurante is None:
                print("Primero debes cargar un restaurante (opción 1).")

            else:
                plato = input("¿Qué plato desea añadir?: ").strip()

                while plato == "":
                    print("El nombre no puede estar vacío.")
                    plato = input("Nombre del plato: ").strip()

                if plato in restaurante["menu"]:
                    print("Ese plato ya existe. Se actualizará su precio.")

                while True:
                    try:
                        precio = float(
                            input("Precio del plato: ").strip().replace(",", ".")
                        )

                        if 0 < precio < float("inf"):
                            break
                        else:
                            print("Introduce un precio positivo y finito.")

                    except ValueError:
                        print("Precio no válido. Introduce un número.")

                gestion_mesas.actualizar_menu(restaurante, plato, precio)

                try:
                    gestor_json.guardar_restaurante(
                        restaurante, ruta_restaurante
                    )

                except OSError:
                    print("El menú se ha actualizado en el programa,")
                    print("pero no se ha podido guardar en el archivo JSON.")

                else:
                    print(f"Plato guardado: {plato} - {precio:.2f} €")


        elif opcion == "6":

            if restaurante is None:
                print("Primero debes cargar un restaurante (opción 1).")

            else:
                print("\nESTADO DEL RESTAURANTE")
                print("Nombre:", restaurante["nombre"])
                print("Capacidad:", restaurante["capacidad"], "personas")
                print("Ocupación actual:", restaurante["ocupacion"], "personas")

                print("\nMESAS ACTIVAS")

                if len(restaurante["mesas"]) == 0:
                    print("No hay mesas activas.")

                else:
                    for numero, mesa in enumerate(restaurante["mesas"], start=1):
                        print("Mesa", numero)
                        print("Clientes:", mesa["clientes"])
                        print("Estado:", mesa["estado"])
                        print("Pedido:", mesa["pedido"])

                print("\nMENÚ COMPLETO")

                for plato, precio in restaurante["menu"].items():
                    print(f"- {plato}: {precio:.2f} €")

                print("\nGANANCIAS")
                print(f"Total acumulado: {restaurante['ganancias']:.2f} €")

        else:
            print("Opción no válida. Escribe un número del 1 al 7")


main()
