import pytest
from models import JuegoFisico

def test_error_anio_futuro():
    """Comprueba la validación de integridad de fechas [3]."""
    from datetime import datetime
    anio_invalido = datetime.now().year + 1
    
    with pytest.raises(ValueError, match="El año no puede ser superior al actual"):
        JuegoFisico("Futuro", "PS6", anio_invalido, "Acción", "E1")

def test_tipos_datos_incorrectos():
    """Verifica que el sistema maneje errores de tipo en la entrada."""
    with pytest.raises(TypeError):
        # Falta el argumento de género requerido en el nuevo modelo
        JuegoFisico("Incompleto", "PC", 2020, "Estante")