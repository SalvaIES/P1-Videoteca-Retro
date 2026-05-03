import pytest
import os
from database import DatabaseManager

class TestDatabase:
    @pytest.fixture
    def db(self):
        test_db = "test_db_logic.db"
        manager = DatabaseManager(test_db)
        yield manager
        manager.conn.close()
        if os.path.exists(test_db):
            os.remove(test_db)

    def test_insertar_y_listar(self, db):
        db.insertar_juego("Metroid", "NES", 1986, "Acción", "Físico", "E1")
        registros = db.obtener_coleccion_completa()

        assert len(registros) > 0
        # registros es una lista de tuplas; accedemos a fila 0
        assert registros[0][1] == "Metroid"   # índice 1: título
        assert registros[0][4] == "Acción"    # índice 4: género

    def test_editar_juego(self, db):
        db.insertar_juego("Sonic", "Genesis", 1991, "Plataformas", "Físico", "E1")
        registros_pre = db.obtener_coleccion_completa()
        id_v = registros_pre[0][0]  # extraemos el ID entero de la primera fila

        db.editar_juego(id_v, "Sonic 1", "Genesis", 1991, "Plataformas", "E2")
        registros_post = db.obtener_coleccion_completa()

        assert registros_post[0][1] == "Sonic 1"  # índice 1: título actualizado
        assert registros_post[0][6] == "E2"        # índice 6: campo extra (estantería)

    def test_relacion_prestamos(self, db):
        db.insertar_juego("Zelda", "NES", 1986, "Aventura", "Físico", "E1")
        registros = db.obtener_coleccion_completa()
        id_v = registros[0][0]  # extraemos el ID entero de la primera fila

        db.registrar_prestamo(id_v, "Usuario Prueba")
        registros_con_prestamo = db.obtener_coleccion_completa()

        # índice 7: columna destinatario del LEFT JOIN con prestamos
        assert registros_con_prestamo[0][7] == "Usuario Prueba"
