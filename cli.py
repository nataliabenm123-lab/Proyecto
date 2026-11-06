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
    while True:
        mostrar_menu()
        opcion=input("elige una opcion:")
        
        if opcion == "7":                      
            print("Saliendo del programa...")
            break
        elif opcion in ["1","2","3","4","5","6"]:
            print("has elegido la opcion:",opcion)
        else:
            print("Opción no válida. Escribe un número del 1 al 7")
main()
