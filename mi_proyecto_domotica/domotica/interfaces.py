# La única diferencia en funcionamiento usando protocol en vez de abc (en python)
# es que al usar isintance o issubclass se dan estos dos casos:

# 1) SIN runtime_checkable:
#   se genera un error de que no se puede comprobar tipos en runtime
#   no puedes usar los métodos citados anteriormente (isintance o issubclass)
#   es el comportamiento por defecto porque realmente no se tendría que comprobar
#   una jerarquía si se esta usando interfaces simuladas, sólo cumplir el contrato

# 2) CON runtime_checkable:
#   Puedes usar esos métodos (isintance o issubclass)
#   y te dará el mismo resultado que si hubieses heredado de abc
#   pero también te puede dar True aunque una clase no herede de otra
#   ,es decir, no mira la jerarquía, mira que tengan el mismo contrato
#   tengan los mismos métodos.
#
#   En python no se mira la firma del método al sobreescribir ni cuando
#   usa MRO, sólo mira el nombre. Por tanto, si se usa protocol, incluso
#   aunque el miembro de la clase sea una propiedad o atributo y
#   no fuese explícitamente un método cumpliría el contrato
#
#   Con esto quiero decir que en el resto del comportamiento,
#   para python Protocol es una clase que estás heredando,
#   realmente no se implementa como en otros lenguajes,
#   pero la manera en que usamo sus tipos (cuando usamos isintace,issubcalse)
#   sí difiere de otros lenguajes

# # 3. Protocols (interfaces.py)
# Define las capacidades que un dispositivo puede tener,
# sin obligar a una jerarquía rígida.
from abc import abstractmethod
from typing import Protocol, runtime_checkable

from .common import *


# Es importante, en mi caso, incluir métodos abstractos en las interfaces
# De otro modo podrías instnaciar las clases que la hereden sin realmente
# tener una definición real. Python no establece, como en otros lenguajes,
# que las interfaces tengan que ser todos métodos abstractos
# De hecho, los modernos y versiones actualizadas de los antiguos simulan
# interfaces o mixin o traits en los cuales mezclas métodos definidos o abstractos
# o das un valor por defecto al método y tu lo sobreescribes si quieres
@runtime_checkable
class Medible(Protocol):
    @abstractmethod
    def leer_valor(self) -> float: ...


@runtime_checkable
class Conmutable(Protocol):
    """Adaptar a cada tipo de dispositivo para que se puedan
    activar/desactivar utilizando polimorfismo llamando al metodo
    correspondiente si ya lo integran"""

    @abstractmethod
    def alternar(self) -> None: ...

    @abstractmethod
    def encender(self) -> None: ...

    @abstractmethod
    def apagar(self) -> None: ...


@runtime_checkable
class Actualizable(Protocol):
    @abstractmethod
    def actualizar_firmware(self, version: str) -> None:
        if not isinstance(version, str):
            raise TypeError(f'{version} no es una cadena')
        if not version:
            raise ValueError('El campo está vació')
        if not Utils.validar_version(version):
            raise DatoInvalido(f'versión:{version} inválida (formato esperado X.Y.Z)')
