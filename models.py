from abc import ABC, abstractmethod
from datetime import datetime


class Item(ABC):
    """Clase base abstracta que modela un elemento de la videoteca.

    Aplica encapsulación total mediante atributos privados y propiedades,
    y define la interfaz polimórfica que deben implementar las subclases.
    """

    def __init__(self, titulo: str, plataforma: str, anio: int, genero: str):
        """Inicializa los atributos comunes a todo videojuego.

        Args:
            titulo (str): Título del videojuego.
            plataforma (str): Plataforma en la que se ejecuta.
            anio (int): Año de lanzamiento (no puede ser futuro).
            genero (str): Género del videojuego (RPG, Shooter, etc.).

        Raises:
            ValueError: Si el año de lanzamiento supera el año actual.
        """
        self.__titulo = titulo
        self.__plataforma = plataforma
        self.__anio = self._validar_anio(anio)
        self.__genero = genero

    @property
    def titulo(self):
        """str: Título del videojuego (solo lectura)."""
        return self.__titulo

    @property
    def plataforma(self):
        """str: Plataforma del videojuego (solo lectura)."""
        return self.__plataforma

    @property
    def anio(self):
        """int: Año de lanzamiento validado (solo lectura)."""
        return self.__anio

    @property
    def genero(self):
        """str: Género del videojuego (solo lectura)."""
        return self.__genero

    def _validar_anio(self, anio):
        """Valida que el año de lanzamiento no sea posterior al año actual.

        Args:
            anio (int): Año a validar.

        Returns:
            int: El mismo año si es válido.

        Raises:
            ValueError: Si el año supera el año actual.
        """
        if anio > datetime.now().year:
            raise ValueError("El año no puede ser superior al actual.")
        return anio

    @abstractmethod
    def mostrar_detalle(self) -> str:
        """Devuelve una cadena con los detalles específicos del videojuego.

        Cada subclase debe implementar este método para mostrar
        la información propia de su formato (físico o digital).

        Returns:
            str: Descripción detallada del videojuego.
        """
        pass


class JuegoFisico(Item):
    """Representa un videojuego en formato físico con ubicación en estantería."""

    def __init__(self, titulo: str, plataforma: str, anio: int,
                 genero: str, estanteria: str):
        """Inicializa un juego físico con su ubicación en la estantería.

        Args:
            titulo (str): Título del videojuego.
            plataforma (str): Plataforma en la que se ejecuta.
            anio (int): Año de lanzamiento.
            genero (str): Género del videojuego.
            estanteria (str): Ubicación física en la colección (ej. 'Estante A1').
        """
        super().__init__(titulo, plataforma, anio, genero)
        self.estanteria = estanteria

    def mostrar_detalle(self) -> str:
        """Devuelve los detalles del juego incluyendo su ubicación física.

        Returns:
            str: Cadena con prefijo [FÍSICO] y la estantería donde se encuentra.
        """
        return f"[FÍSICO] {self.titulo} - Estante: {self.estanteria}"


class JuegoDigital(Item):
    """Representa un videojuego en formato digital con enlace de descarga."""

    def __init__(self, titulo: str, plataforma: str, anio: int,
                 genero: str, enlace: str):
        """Inicializa un juego digital con su enlace de descarga.

        Args:
            titulo (str): Título del videojuego.
            plataforma (str): Plataforma en la que se ejecuta.
            anio (int): Año de lanzamiento.
            genero (str): Género del videojuego.
            enlace (str): URL o referencia de descarga digital.
        """
        super().__init__(titulo, plataforma, anio, genero)
        self.enlace = enlace

    def mostrar_detalle(self) -> str:
        """Devuelve los detalles del juego incluyendo su enlace de descarga.

        Returns:
            str: Cadena con prefijo [DIGITAL] y la URL de descarga.
        """
        return f"[DIGITAL] {self.titulo} - Enlace: {self.enlace}"
