import pytest
import pandas as pd
import sqlite3
import os
from database import DatabaseManager

class TestAnalysis:
    @pytest.fixture
    def setup_data(self):
        db_name = "test_analysis.db"
        db = DatabaseManager(db_name)
        # Insertamos con los 6 campos requeridos por insertar_juego
        db.insertar_juego("Juego A", "PC", 2000, "RPG", "Digital", "URL")
        yield db_name
        db.conn.close()
        if os.path.exists(db_name):
            os.remove(db_name)

    def test_datos_para_analisis(self, setup_data):
        conn = sqlite3.connect(setup_data)
        df = pd.read_sql_query("SELECT plataforma, anio, genero FROM juegos", conn)
        conn.close()

        assert not df.empty
        # .iloc[0] accede al valor de la primera fila (no al indexer)
        assert df["plataforma"].iloc[0] == "PC"
        assert "genero" in df.columns
