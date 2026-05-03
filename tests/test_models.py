import pytest
from models import JuegoFisico, JuegoDigital

class TestModels:
    """Pruebas unitarias para validar la lógica de negocio y POO [4, 6]."""

    def test_creacion_juego_fisico(self):
        """Verifica que un juego físico se cree con todos sus atributos privados."""
        # Ahora necesitamos 5 argumentos: titulo, plataforma, anio, genero, estanteria
        juego = JuegoFisico("DOOM", "PC", 1993, "Shooter", "A1")
        assert juego.titulo == "DOOM"
        assert juego.genero == "Shooter"
        assert juego.estanteria == "A1"

    def test_validacion_anio(self):
        """Verifica que no se permitan años de lanzamiento futuros [2, 6]."""
        with pytest.raises(ValueError, match="El año no puede ser superior al actual"):
            # Intentamos crear un juego con un año inválido
            JuegoFisico("GTA VI", "PS5", 2030, "Acción", "S1")

    def test_polimorfismo_mostrar_detalle(self):
        """Verifica el comportamiento polimórfico del método mostrar_detalle [7]."""
        fisico = JuegoFisico("Tetris", "GameBoy", 1989, "Puzzle", "Cajon1")
        digital = JuegoDigital("Zelda", "Switch", 2017, "Aventuras", "http://nintendo.es")
        
        assert "[FÍSICO]" in fisico.mostrar_detalle()
        assert "[DIGITAL]" in digital.mostrar_detalle()