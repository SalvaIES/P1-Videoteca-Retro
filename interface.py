from datetime import datetime


class InterfazConsola:
    """Capa de interacción con el usuario mediante consola."""

    def mostrar_menu(self):
        """Muestra el menú principal y devuelve la opción elegida por el usuario.

        Returns:
            str: Carácter introducido por el usuario.
        """
        print("\n" + "=" * 55)
        print("        SISTEMA DE GESTIÓN DE VIDEOTECA RETRO")
        print("=" * 55)
        print("1. Añadir juego físico    | 2. Añadir juego digital")
        print("3. Ver colección completa | 4. Editar videojuego")
        print("5. Eliminar videojuego    | 6. Prestar videojuego")
        print("7. Devolver videojuego    | 8. Análisis estadístico")
        print("9. Salir del programa")
        return input("\nSeleccione una opción: ").strip()

    def pedir_datos_juego(self):
        """Solicita y valida los campos comunes de un videojuego.

        Valida que ningún campo quede vacío y que el año sea un número
        entero no superior al año actual.

        Returns:
            tuple: (titulo, plataforma, anio, genero) ya validados.
        """
        titulo = self._pedir_texto("Título")
        plataforma = self._pedir_texto("Plataforma")
        anio = self._pedir_anio()
        genero = self._pedir_texto("Género (RPG, Arcade, etc.)")
        return titulo, plataforma, anio, genero

    def pedir_id(self, accion):
        """Solicita un ID numérico y lo valida antes de devolverlo.

        Args:
            accion (str): Descripción de la acción (para el mensaje al usuario).

        Returns:
            int: Identificador válido introducido por el usuario.
        """
        while True:
            entrada = input(f"ID del videojuego a {accion}: ").strip()
            if entrada.isdigit() and int(entrada) > 0:
                return int(entrada)
            print("  Error: introduce un número entero positivo.")

    def pedir_texto_extra(self, tipo_juego):
        """Solicita el campo extra según el tipo de juego.

        Args:
            tipo_juego (str): 'Físico' o 'Digital'.

        Returns:
            str: Estantería o URL introducida por el usuario.
        """
        if tipo_juego == "Físico":
            return self._pedir_texto("Estantería")
        return self._pedir_texto("URL de descarga")

    def mostrar_coleccion_tabular(self, registros):
        """Muestra la colección completa agrupada por plataforma.

        Args:
            registros (list[tuple]): Filas devueltas por obtener_coleccion_completa().
        """
        if not registros:
            print("\nLa videoteca está vacía.")
            return

        plataforma_actual = None
        w_id, w_tit, w_anio, w_gen, w_est = 4, 25, 6, 15, 20

        for registro in registros:
            idx, titulo, plataforma, anio, genero, tipo, extra, dest = registro

            if plataforma != plataforma_actual:
                plataforma_actual = plataforma
                separador = "-" * 65
                print(f"\n--- PLATAFORMA: {plataforma_actual.upper()} ---")
                header = (
                    f"{'ID':<{w_id}} | {'TÍTULO':<{w_tit}} | "
                    f"{'AÑO':<{w_anio}} | {'GÉNERO':<{w_gen}} | {'ESTADO':<{w_est}}"
                )
                print(header)
                print("-" * len(header))

            estado = f"Prestado a: {dest}" if dest else "En Biblioteca"
            print(
                f"{idx:<{w_id}} | {titulo:<{w_tit}} | "
                f"{anio:<{w_anio}} | {genero:<{w_gen}} | {estado:<{w_est}}"
            )

    # ------------------------------------------------------------------
    # Métodos privados de validación
    # ------------------------------------------------------------------

    def _pedir_texto(self, campo):
        """Solicita un campo de texto y rechaza entradas vacías.

        Args:
            campo (str): Nombre del campo que se pide al usuario.

        Returns:
            str: Texto no vacío introducido por el usuario.
        """
        while True:
            valor = input(f"{campo}: ").strip()
            if valor:
                return valor
            print(f"  Error: el campo '{campo}' no puede estar vacío.")

    def _pedir_anio(self):
        """Solicita el año de lanzamiento y lo valida.

        Comprueba que sea un número entero entre 1970 y el año actual.

        Returns:
            int: Año válido introducido por el usuario.
        """
        anio_actual = datetime.now().year
        while True:
            entrada = input("Año de lanzamiento: ").strip()
            if not entrada.isdigit():
                print("  Error: introduce un número entero (ej. 1993).")
                continue
            anio = int(entrada)
            if anio < 1970:
                print("  Error: el año no puede ser anterior a 1970.")
            elif anio > anio_actual:
                print(f"  Error: el año no puede ser superior a {anio_actual}.")
            else:
                return anio
