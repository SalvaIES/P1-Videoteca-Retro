from database import DatabaseManager
from interface import InterfazConsola
from analysis import AnalizadorColeccion


def ejecutar_app():
    """Punto de entrada principal de la aplicación de videoteca retro.

    Coordina las capas de base de datos, interfaz de usuario y análisis,
    manteniendo el bucle principal del menú de consola.
    """
    db = DatabaseManager()
    ui = InterfazConsola()
    analizador = AnalizadorColeccion()

    while True:
        opcion = ui.mostrar_menu()

        try:
            if opcion in ["1", "2"]:
                tipo = "Físico" if opcion == "1" else "Digital"
                titulo, plataforma, anio, genero = ui.pedir_datos_juego()
                extra = ui.pedir_texto_extra(tipo)
                db.insertar_juego(titulo, plataforma, anio, genero, tipo, extra)
                print("  Videojuego añadido con éxito.")

            elif opcion == "3":
                ui.mostrar_coleccion_tabular(db.obtener_coleccion_completa())

            elif opcion == "4":
                id_juego = ui.pedir_id("editar")
                titulo, plataforma, anio, genero = ui.pedir_datos_juego()
                extra = input("Nuevo Estante/URL: ").strip()
                db.editar_juego(id_juego, titulo, plataforma, anio, genero, extra)
                print("  Registro actualizado con éxito.")

            elif opcion == "5":
                id_juego = ui.pedir_id("eliminar")
                db.eliminar_juego(id_juego)
                print("  Registro borrado con éxito.")

            elif opcion == "6":
                id_juego = ui.pedir_id("prestar")
                destinatario = input("Nombre del prestatario: ").strip()
                if destinatario:
                    db.registrar_prestamo(id_juego, destinatario)
                else:
                    print("  Error: el nombre del prestatario no puede estar vacío.")

            elif opcion == "7":
                db.eliminar_prestamo(ui.pedir_id("devolver"))
                print("  Devolución registrada con éxito.")

            elif opcion == "8":
                analizador.ejecutar_analisis_completo()

            elif opcion == "9":
                print("\nCerrando el sistema. ¡Hasta pronto!")
                break

            else:
                print("  Opción no válida. Elige un número del 1 al 9.")

        except Exception as e:
            print(f"\nERROR INESPERADO: {e}")


if __name__ == "__main__":
    ejecutar_app()
