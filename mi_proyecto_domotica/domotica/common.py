# EXCEPCIONES
class DatoInvalido(ValueError):
    """Un dato no cumple el formato o las reglas de negocio"""


class Duplicado(Exception):
    """Se intenta registrar/insertar un elemento con clave ya existente"""


class NoEncontrado(Exception):
    """No existe un elemento solicitado por su identificado"""


# Clase Utils
#     • Clase Utils con:
#         ○ validar_id(texto: str) -> bool
#         ○ fabricar_id(prefijo: str, n: int) -> str
#         ○ validar_version(version: str) -> bool

#     Función validar_id
#         • Valida el formato de identificador de un dispositivo.
#         • Reglas de validación (todas obligatorias):
#             ○ Texto debe ser str y no vacío (tras strip()).
#             ○ Debe comenzar por letra [A-Z, a-z].
#             ○ Por convención en la unidad: B (bombilla), S (sensor), C (cerradura)
#                 ... pero no limitar solo a estas.
#             ○ El resto de caracteres deben ser alfanuméricos o guiones: [A-Za-z0-9-].
#             ○ No se permiten espacios internos.

#     Función fabricar_id
#         Genera un nuevo ID canonizado para dispositivos, con el formato:

#         <PREFIJO><NNN>

#         donde <PREFIJO> es una letra (o varias letras) en mayúsculas
#         y <NNN> es un entero con 3 dígitos (con cero a la izquierda si procede).

#         Reglas:
#         • prefijo debe ser str, no vacío; se normaliza a mayúsculas (upper()).
#         • n debe ser int positivo (>= 1).
#         • El id_candidato debe superar validar_id(...);
#           en caso contrario, lanzar DatoInvalido con mensaje:
#             ○ "ID generado inválido: ''".

#         Ejemplos:
#             • fabricar_id("b", 1) → "B001"
#             • fabricar_id("S", 12) → "S012"
#             • fabricar_id("Hub", 7) → "HUB007"

#         Casos que deben lanzar DatoInvalido:

#             • fabricar_id("", 1) → prefijo vacío
#             • fabricar_id("B", 0) → n no positivo
#             • fabricar_id("X_", 5) → guion bajo no permitido por validar_id

#         Notas:
#             • No comprueba colisiones (IDs ya usados); eso corresponde a Hub


class Utils:
    VALID_INPUTS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-'

    @staticmethod
    def validar_id(texto: str) -> bool:
        """
        Valida el formato de identificador de un dispositivo.

        Args:
            texto (str): id del dispositivo
                Formato:
                    - Debe comenzar por letra [A-Z, a-z].
                    - El resto de caracteres deben ser alfanuméricos o guiones:
                        [A-Za-z0-9-]
                    - No se permiten espacios internos
        """
        # con patrones
        # patron = r"[A-Za-z][A-Za-z0-9-]*"
        # return re.fullmatch(patron, texto)
        texto = texto.upper()
        return (
            isinstance(texto, str)
            and texto != ''
            and 'A' <= texto[0] <= 'Z'
            and all(c in Utils.VALID_INPUTS for c in texto)
        )

    @staticmethod
    def fabricar_id(prefijo: str, n: int) -> str:
        """
        Genera un nuevo ID canonizado para dispositivos,
        con el formato: <PREFIJO><NNN>

        Args:
            prefijo (str): prefijo del dispositivo. De una a varias letras.
            n (int): número del dispositivo. De 1-999

        Returns:
            str: <PREFIJO><NNN>
                <PREFIJO>: <PREFIJO> es una letra (o varias letras) en mayúsculas
                <NNN>: es un entero con 3 dígitos (rellenado con ceros a la izquierda)

        Raises:
            DatoInvalido: ID generado inválido: ''.

        """
        if not isinstance(prefijo, str) or not prefijo:
            raise DatoInvalido('El prefijo está vacío')

        if not isinstance(n, int) or n < 1 and n > 999:
            raise DatoInvalido(f'N: {n} no es válido. Valor permitido: 1-999')

        id = prefijo.upper() + str(n)
        if not Utils.validar_id(id):
            raise DatoInvalido(f'ID generado inválido: "{id}"')

        return id

    @staticmethod
    def validar_version(version: str) -> bool:
        """ "
        Valida la version
            Args:
                version (str): X.Y.Z -> versión inválida (formato esperado X.Y.Z)
        """
        # return r"[0-9]+[.][0-9]+[.][0-9]+"
        # bool(version) o texto != '' hace falta para convertir esa parte a booleana
        # sino python como js devuelven el valor falsy
        # con not no hace falta porque ya se transforma a booleano
        res = isinstance(version, str) and bool(version)
        if res:
            versions = version.split('.')
            res = len(versions) == 3 and all(num.isdigit() for num in versions)

        return res
