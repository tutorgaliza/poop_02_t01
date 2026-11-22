# 2. Subclases (dispositivos.py)
#   Implementa tres clases derivadas de Dispositivo,
#   cada una con atributos y métodos propios:

#     SensorTemperatura
#         • Atributo adicional:
#             ○ _celsius: float
#         • Métodos:
#             ○ leer_valor(): devuelve la temperatura actual.
#             ○ tipo(): devuelve "SensorTemperatura".
#     BombillaInteligente
#         • Atributos adicionales:
#             ○ _brillo: int (0–100)
#             ○ _encendida: bool
#         • Métodos:
#             ○ encender(), apagar()
#             ○ tipo(): "BombillaInteligente"
#     CerraduraInteligente
#         • Atributos adicionales:
#             ○ _bloqueada: bool
#         • Métodos:
#             ○ bloquear(), desbloquear()
#             ○ tipo(): "CerraduraInteligente"

from .base import *
from .interfaces import *


class SensorTemperatura(Dispositivo, Medible):
    def __init__(self, id: str, nombre: str, fabricante: str, celsius: float):
        super().__init__(id, nombre, fabricante)
        self.celsius = celsius

    @property
    def celsius(self) -> str:
        return self._celsius

    @celsius.setter
    def celsius(self, val):
        if not isinstance(val, float):
            raise TypeError(f'{val} no es un número')
        self._celsius = val

    def leer_valor(self) -> str:
        return self.celsius

    # esto no haría falta si se hubiese puesto la implementación común en la base
    def tipo(self):
        return TipoDispositivo.SENSOR

    def __str__(self):
        return f'{super().__str__()}, celsius={self.celsius}ºC)'


class BombillaInteligente(Dispositivo, Conmutable, Actualizable):
    def __init__(
        self,
        id: str,
        nombre: str,
        fabricante: str,
        brillo: int = 50,
        encendida: bool = False,
    ):
        super().__init__(id, nombre, fabricante)
        self.brillo = brillo
        self.encendida = encendida

    @property
    def brillo(self) -> str:
        return self._brillo

    @brillo.setter
    def brillo(self, val):
        if not isinstance(val, int):
            raise TypeError(f'{val} no es un entero')
        if val < 0 or val > 100:
            raise ValueError(f'{val} no es un valor válido. Valores permitidos:[0-100]')
        self._brillo = val

    @property
    def encendida(self) -> str:
        return self._encendida

    @encendida.setter
    def encendida(self, val):
        if not isinstance(val, bool):
            raise TypeError(f'{val} no es un booleano')
        self._encendida = val

    def encender(self):
        self.encendida = True

    def apagar(self):
        self.encendida = False

    def alternar(self):
        self.encendida = not self.encendida

    def actualizar_firmware(self, version) -> None:
        super().actualizar_firmware(version)

    def tipo(self) -> type:
        return TipoDispositivo.BOMBILLA

    def __str__(self):
        return f'{super().__str__()}, brillo={self.brillo}, encendida={self.encendida})'


class CerraduraInteligente(Dispositivo, Conmutable):
    def __init__(self, id: str, nombre: str, fabricante: str, bloqueada: float = False):
        super().__init__(id, nombre, fabricante)
        self.bloqueada = bloqueada

    @property
    def bloqueada(self) -> str:
        return self._bloqueada

    @bloqueada.setter
    def bloqueada(self, val):
        if not isinstance(val, bool):
            raise TypeError(f'{val} no es un booleano')
        self._bloqueada = val

    def bloquear(self):
        self.bloqueada = True

    def desbloquear(self):
        self.bloqueada = False

    def encender(self):
        self.bloquear()

    def apagar(self):
        self.desbloquear()

    def alternar(self):
        self.bloqueada = not self.bloqueada

    def tipo(self) -> type:
        return TipoDispositivo.CERRADURA

    def __str__(self):
        return f'{super().__str__()}, estado={"bloqueada" if self.bloqueada else "desbloqueada"})'
