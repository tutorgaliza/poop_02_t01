# 1. Clase base (abstracta) Dispositivo (base.py)
#     Define la estructura común de todos los dispositivos.
#
#     • Atributos protegidos:
#         ○ _id: str
#         ○ _nombre: str
#         ○ _fabricante: str
#     • Métodos:
#         ○ __init__: constructor con validaciones.
#         ○ Métodos setters y getters para los atributos.
#         ○ __str__: representación legible del objeto.
#         ○ tipo(): método abstracto que devuelva el tipo de dispositivo.

from abc import ABC, abstractmethod
from enum import StrEnum

from .common import DatoInvalido, Utils


class TipoDispositivo(StrEnum):
    BOMBILLA = "bombilla"
    CERRADURA = "cerradura"
    SENSOR = "sensor"

class Dispositivo(ABC):
    # las validaciones se hacen en las propiedades
    # sino no pasarían por el mismo flujo al setearlas,
    # ya que no pasan por el constructor
    def __init__(self, id: str, nombre: str, fabricante: str):
        super().__init__()
        self.id = id
        self.nombre = nombre
        self.fabricante = fabricante

    @property
    def classname(self) -> str:
        return type(self).__name__

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, val):
        if not isinstance(val, str):
            raise TypeError(f'{val} no es una cadena')
        if not val:
            raise ValueError('El campo está vació')
        if not Utils.validar_id(val) or len(val) == 1 and self.classname != val[0]:
            raise DatoInvalido(f'El ID "{val}" no es válido.')
        self._id = val

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, val):
        if not isinstance(val, str):
            raise TypeError(f'{val} no es una cadena')
        if not val:
            raise ValueError('El campo está vació')
        self._nombre = val

    @property
    def fabricante(self) -> str:
        return self._fabricante

    @fabricante.setter
    def fabricante(self, val):
        if not isinstance(val, str):
            raise TypeError(f'{val} no es una cadena')
        if not val:
            raise ValueError('El campo está vació')
        self._fabricante = val

    # formato: [SensorTemperatura] Sensor Cocina (id=S001, fabricante=Acme)
    def __str__(self) -> str:
        return (
            f'[{self.classname}]'
            f'{self.nombre}'
            f'(id={self.id}'
            f',tipo={self.tipo()})'
            f'(fabricante={self.fabricante}'
        )

    @abstractmethod
    def tipo(self) -> TipoDispositivo:...
