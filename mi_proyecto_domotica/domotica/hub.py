# 4. Clase Hub (hub.py)
#     Gestiona los dispositivos registrados y realiza operaciones comunes.

#     • Atributos:
#         ○ _dispositivos: dict[str, Dispositivo] :
#             ▪ Diccionario donde se almacenan los dispositivos con clave ID y objeto.
#             ▪ Formato del ID:
#             • Formato bombillas: "B001", "B002", ...
#             • Formato sensores: "S001", "S002", ...
#             • Formato cerradura: "C001", "C002", ...
#     • Métodos:
#         ○ registrar(disp: Dispositivo): añade dispositivos evitando duplicados.
#         ○ listar(): devuelve todos los dispositivos.
#         ○ operar_todos(): Recorre la colección de dispositivos:
#             ▪ Si es Medible, muestra su lectura.
#             ▪ Si es Conmutable, alterna encendido/apagado.
#         ○ estadisticas(): devuelve un diccionario con el número de dispositivos por tipo.
from .base import *
from .common import Duplicado
from .dispositivos import *
from .interfaces import *


class Hub:
    def __init__(self):
        self._dispositivos: dict[str, Dispositivo] = {}

    def registrar(self, disp: Dispositivo) -> None:
        """Añade dispositivos evitando duplicados"""
        if disp.id not in self._dispositivos:
            self._dispositivos[disp.id] = disp
        else:
            raise Duplicado(f'El ID "{disp.id}" ya existe')

    def obtener(self, id: str) -> Dispositivo:
        if id.upper() in self._dispositivos:
            return self._dispositivos[id]
        else:
            raise NoEncontrado(f'El ID "{id}" no existe')

    def listar(self) -> list[Dispositivo]:
        """Devuelve todos los dispositivos"""
        return list(self._dispositivos.values())

    def operar_todos(self) -> None:
        """Aplica diferentes operaciones según su interfaz"""
        for id, disp in self._dispositivos.items():
            res = f'\t{id} ->'
            if isinstance(disp, Medible):
                res += f' lectura = {disp.leer_valor()}'
            elif isinstance(disp, Conmutable):
                disp.encender()
                res += ' encender()'
                res += ' (bloquear)' if disp.tipo() == TipoDispositivo.CERRADURA else ''
                res += ' -> OK;'
                disp.apagar()
                res += ' apagar()'
                res += ' (desbloquear)' if disp.tipo() == TipoDispositivo.CERRADURA else ''
            print(res)

    def estadisticas(self) -> dict[TipoDispositivo, int]:
        """devuelve un diccionario con el número de dispositivos por tipo"""
        res: dict[TipoDispositivo, int] = {}
        for disp in self._dispositivos.values():
            res[disp.tipo()] = res.get(disp.tipo(), 0) + 1
        return res
