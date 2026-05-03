import sqlite3

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MaxNLocator


class AnalizadorColeccion:
    """Realiza análisis exploratorio (EDA) y visualización de la colección."""

    def __init__(self, db_name="videoteca.db"):
        """Inicializa el analizador apuntando a la base de datos indicada.

        Args:
            db_name (str): Ruta al archivo de base de datos SQLite.
        """
        self.db_name = db_name

    def _cargar_datos(self):
        """Carga y devuelve los datos de juegos desde la base de datos.

        Realiza una limpieza básica eliminando filas con valores nulos
        en las columnas clave para el análisis.

        Returns:
            pd.DataFrame: DataFrame con columnas plataforma, anio y genero,
                          o un DataFrame vacío si no hay datos.
        """
        conn = sqlite3.connect(self.db_name)
        df = pd.read_sql_query(
            "SELECT plataforma, anio, genero FROM juegos", conn
        )
        conn.close()

        # Limpieza: eliminar filas con nulos en columnas críticas
        df = df.dropna(subset=["plataforma", "anio", "genero"])

        # Normalización: quitar espacios extra en campos de texto
        df["plataforma"] = df["plataforma"].str.strip()
        df["genero"] = df["genero"].str.strip()

        # Asegurar tipo entero en el año tras la limpieza
        df["anio"] = df["anio"].astype(int)

        return df

    def ejecutar_analisis_completo(self):
        """Genera y muestra tres gráficas de análisis de la colección.

        Las gráficas muestran:
            1. Distribución de juegos por plataforma (barras).
            2. Evolución temporal acumulada de la colección (línea).
            3. Correlación entre género y año de lanzamiento (dispersión).

        Si la colección está vacía, informa al usuario y no genera gráficas.
        """
        df = self._cargar_datos()

        if df.empty:
            print("\nNo hay datos suficientes para el análisis estadístico.")
            return

        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5))
        fig.suptitle("Análisis de la Colección de Videojuegos Retro", fontsize=14)

        # 1. Distribución por plataforma
        conteo = df["plataforma"].value_counts()
        conteo.plot(kind="bar", ax=ax1, color="skyblue")
        ax1.set_title("Juegos por plataforma")
        ax1.set_xlabel("Plataforma")
        ax1.set_ylabel("Número de juegos")
        ax1.tick_params(axis="x", rotation=45)
        ax1.yaxis.set_major_locator(MaxNLocator(integer=True))

        # 2. Evolución temporal acumulada
        temporal = df.groupby("anio").size().cumsum()
        temporal.plot(kind="line", ax=ax2, marker="o", color="green")
        ax2.set_title("Evolución de la colección")
        ax2.set_xlabel("Año")
        ax2.set_ylabel("Total acumulado")
        ax2.xaxis.set_major_locator(MaxNLocator(integer=True, nbins=10))
        ax2.yaxis.set_major_locator(MaxNLocator(integer=True))

        # 3. Correlación género / año de lanzamiento
        ax3.scatter(df["anio"], df["genero"], alpha=0.6, color="purple")
        ax3.set_title("Correlación género / lanzamiento")
        ax3.set_xlabel("Año")
        ax3.set_ylabel("Género")
        ax3.xaxis.set_major_locator(MaxNLocator(integer=True, nbins=5))
        ax3.tick_params(axis="y", labelsize=8)

        plt.tight_layout()
        plt.show()
