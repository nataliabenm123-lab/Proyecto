import gestor_json
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
    while True:
        mostrar_menu()
        opcion=input("elige una opcion:")
        
        if opcion == "7":                      
            print("Saliendo del programa...")
            break
        #agregamos esta linea para que lea json
        elif opcion =="1":
            nombres=gestor_json.listar_restaurantes("restaurantes")
            print("restaurantes disponibles:")
            for numero,nombre in enumerate (nombres,start=1):
                print(numero,"-",nombre)
            eleccion=input("Elige un restaurante (número): ")
            if eleccion.isdigit() and 1 <= int(eleccion) <= len(nombres):
                archivo_elegido = nombres[int(eleccion) - 1]
                restaurante = gestor_json.cargar_restaurante("restaurantes", archivo_elegido)
                restaurante["mesas"] = []
                restaurante["ocupacion"] = 0
                restaurante["ganancias"] = 0
                
                print(restaurante)
                print("Restaurante cargado:", restaurante["nombre"])
            else:
                print("Opción no válida.")
        elif opcion in ["2","3","4","5","6"]:
            if restaurante is None:
                print("primero debes cargar un restaurante (opcion 1)")
            else:
                print("has elegido la opcion:", opcion)
        else:
            print("Opción no válida. Escribe un número del 1 al 7")
main()


