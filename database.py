import sqlite3
from datetime import datetime


class DatabaseManager:
    """Gestiona la persistencia relacional y la integridad de los datos en SQLite."""

    def __init__(self, db_name="videoteca.db"):
        """Abre la conexión con la base de datos y crea las tablas si no existen.

        Args:
            db_name (str): Ruta al archivo de base de datos SQLite.
        """
        self.conn = sqlite3.connect(db_name)
        self._crear_tablas()

    def _crear_tablas(self):
        """Crea el esquema ERD: tablas juegos y prestamos con clave foránea."""
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS juegos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    plataforma TEXT NOT NULL,
                    anio INTEGER NOT NULL,
                    genero TEXT NOT NULL,
                    tipo TEXT NOT NULL,
                    extra TEXT
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS prestamos (
                    juego_id INTEGER PRIMARY KEY,
                    destinatario TEXT NOT NULL,
                    fecha_inicio TEXT,
                    FOREIGN KEY (juego_id) REFERENCES juegos (id)
                )
            """)

    def insertar_juego(self, titulo, plataforma, anio, genero, tipo, extra):
        """Inserta un nuevo videojuego en la base de datos (C de CRUD).

        Args:
            titulo (str): Título del videojuego.
            plataforma (str): Plataforma de la consola o PC.
            anio (int): Año de lanzamiento.
            genero (str): Género del videojuego (RPG, Shooter, etc.).
            tipo (str): Formato del juego ('Físico' o 'Digital').
            extra (str): Estantería (físico) o URL de descarga (digital).
        """
        query = """
            INSERT INTO juegos (titulo, plataforma, anio, genero, tipo, extra)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        with self.conn:
            self.conn.execute(query, (titulo, plataforma, anio, genero, tipo, extra))

    def editar_juego(self, id_juego, titulo, plataforma, anio, genero, extra):
        """Actualiza los datos de un videojuego existente (U de CRUD).

        Args:
            id_juego (int): Identificador único del juego a editar.
            titulo (str): Nuevo título.
            plataforma (str): Nueva plataforma.
            anio (int): Nuevo año de lanzamiento.
            genero (str): Nuevo género.
            extra (str): Nueva estantería o URL.
        """
        query = """
            UPDATE juegos
            SET titulo=?, plataforma=?, anio=?, genero=?, extra=?
            WHERE id=?
        """
        with self.conn:
            self.conn.execute(query, (titulo, plataforma, anio, genero, extra, id_juego))

    def eliminar_juego(self, id_juego):
        """Elimina un videojuego y sus préstamos asociados (D de CRUD).

        Args:
            id_juego (int): Identificador único del juego a eliminar.
        """
        with self.conn:
            self.conn.execute(
                "DELETE FROM prestamos WHERE juego_id = ?", (id_juego,)
            )
            self.conn.execute(
                "DELETE FROM juegos WHERE id = ?", (id_juego,)
            )

    def registrar_prestamo(self, id_juego, destinatario):
        """Registra el préstamo de un videojuego a una persona.

        Args:
            id_juego (int): Identificador del juego a prestar.
            destinatario (str): Nombre de la persona que recibe el préstamo.
        """
        fecha = datetime.now().strftime("%Y-%m-%d")
        try:
            with self.conn:
                self.conn.execute(
                    "INSERT INTO prestamos VALUES (?, ?, ?)",
                    (id_juego, destinatario, fecha)
                )
        except sqlite3.IntegrityError:
            print("\nError: El videojuego ya está marcado como prestado.")

    def eliminar_prestamo(self, id_juego):
        """Registra la devolución de un videojuego eliminando su préstamo activo.

        Args:
            id_juego (int): Identificador del juego devuelto.
        """
        with self.conn:
            self.conn.execute(
                "DELETE FROM prestamos WHERE juego_id = ?", (id_juego,)
            )

    def obtener_coleccion_completa(self):
        """Devuelve todos los juegos con su estado de préstamo mediante JOIN.

        Returns:
            list[tuple]: Lista de filas con columnas:
                (id, titulo, plataforma, anio, genero, tipo, extra, destinatario)
        """
        query = """
            SELECT j.id, j.titulo, j.plataforma, j.anio, j.genero,
                   j.tipo, j.extra, p.destinatario
            FROM juegos j
            LEFT JOIN prestamos p ON j.id = p.juego_id
            ORDER BY j.plataforma, j.titulo
        """
        return self.conn.execute(query).fetchall()
