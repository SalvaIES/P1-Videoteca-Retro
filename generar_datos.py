import sqlite3

def inicializar_base_de_datos():
    conn = sqlite3.connect("videoteca.db")
    cursor = conn.cursor()

    # Eliminamos tablas previas para asegurar la nueva estructura con 'genero'
    cursor.execute("DROP TABLE IF EXISTS prestamos")
    cursor.execute("DROP TABLE IF EXISTS juegos")

    # Crear tabla juegos (CRUD completo y campo genero para análisis)
    cursor.execute("""
        CREATE TABLE juegos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            plataforma TEXT NOT NULL,
            anio INTEGER NOT NULL,
            genero TEXT NOT NULL,
            tipo TEXT NOT NULL,
            extra TEXT
        )
    """)

    # Crear tabla prestamos (Esquema ERD relacional)
    cursor.execute("""
        CREATE TABLE prestamos (
            juego_id INTEGER PRIMARY KEY,
            destinatario TEXT NOT NULL,
            fecha_inicio TEXT,
            FOREIGN KEY (juego_id) REFERENCES juegos (id)
        )
    """)

    # Lista de videojuegos de diversas épocas y plataformas para el análisis estadístico
    videojuegos = [
        # PC
        ("DOOM", "PC", 1993, "Shooter", "Físico", "Estante Retro 1"),
        ("Baldur's Gate 3", "PC", 2023, "RPG", "Digital", "Steam Library"),
        ("Half-Life 2", "PC", 2004, "Shooter", "Físico", "Caja PC-04"),
        
        # PlayStation
        ("Metal Gear Solid 4", "PS3", 2008, "Acción", "Físico", "Estante Sony-1"),
        ("Uncharted 2", "PS3", 2009, "Aventuras", "Digital", "PSN Store"),
        ("Bloodborne", "PS4", 2015, "RPG", "Físico", "Estante Sony-2"),
        ("God of War", "PS4", 2018, "Acción", "Digital", "PSN Store"),
        
        # Nintendo
        ("Zelda: Breath of the Wild", "Switch", 2017, "Aventuras", "Físico", "Maletín Switch"),
        ("Super Mario Odyssey", "Switch", 2017, "Plataformas", "Digital", "eShop"),
        ("Metroid Prime 4", "Switch2", 2024, "Aventuras", "Físico", "Estante Switch2"),
        ("Mario Kart 9", "Switch2", 2024, "Carreras", "Digital", "eShop"),
        
        # Otros géneros para correlación
        ("Street Fighter II", "Arcade", 1991, "Lucha", "Físico", "Placa JAMMA"),
        ("Tetris", "GameBoy", 1989, "Puzzle", "Físico", "Cajón Portátiles")
    ]

    # Inserción masiva de datos
    cursor.executemany("""
        INSERT INTO juegos (titulo, plataforma, anio, genero, tipo, extra) 
        VALUES (?, ?, ?, ?, ?, ?)
    """, videojuegos)

    # Insertamos algunos préstamos para probar la consulta relacional
    prestamos = [
        (1, "Salvador Martínez", "2026-04-10"),
        (8, "Aleix Peiró", "2026-04-15")
    ]
    cursor.executemany("INSERT INTO prestamos VALUES (?, ?, ?)", prestamos)

    conn.commit()
    conn.close()
    print("Archivo 'videoteca.db' generado con éxito con datos de prueba profesionales.")

if __name__ == "__main__":
    inicializar_base_de_datos()