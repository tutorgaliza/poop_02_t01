# Identifica al directorio, aunque ahora ya no hace falta, como paquete
# Sirve para inicializar cuando este paquete es importado

# la primera linea se necesita para acceder a los modulos listados justo debajo
# las siguientes líneas para importar todas las clases dentro de cada módulo
from . import *
from .base import *
from .common import *
from .dispositivos import *
from .hub import *
from .interfaces import *

__all__ = [
    nombre
    for modulo in (base, common, dispositivos, hub, interfaces)
    # vars devuelve un diccionario
    # con las propiedades de instancia,
    # en este caso son las clases contenidas en un módulo
    # las claves son las propiedades
    for nombre in vars(modulo)
    if not nombre.startswith("_")
]