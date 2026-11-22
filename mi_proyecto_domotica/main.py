# Demostración completa del funcionamiento
# • Crear una lista de dispositivos de distintos tipos.
# • Registrarlos en el Hub.
# • Mostrar su información y estadísticas.
# • Utilizar bucles, condicionales, listas y diccionarios.
# • Mostrar manejo de excepciones controladas.

# Presentación e inicio
#   1. Mostrar un encabezado breve indicando que comienza la demo del sistema de domótica.
#   2. Crear una instancia del Hub (registro interno vacío).

# Preparación de datos (entrada)
#     1. Preparar una lista de diccionarios con la definición de dispositivos a crear.
#         ○ Cada elemento define: id, tipo (sensor/bombilla/cerradura),
#         nombre, fabricante y los parámetros específicos:
#             ▪ SensorTemperatura: celsius inicial.
#             ▪ BombillaInteligente: brillo inicial (0–100).
#             ▪ CerraduraInteligente: estado inicial (bloqueada por defecto, opcional).
#         ○ Incluir al menos dos dispositivos
#           por tipo para que las estadísticas sean significativas.
#         ○ Incluir casos problemáticos para probar validaciones:
#             ▪ Un id inválido (por ejemplo, que no empiece por letra).
#             ▪ Un id duplicado (repetir uno existente).

# Creación e inyección en el Hub
#     1. Recorrer con un bucle la lista de definiciones:
#         ○ Según el tipo, instanciar la subclase correspondiente:
#             ▪ SensorTemperatura(...)
#             ▪ BombillaInteligente(...)
#             ▪ CerraduraInteligente(...)
#         • Validar previamente el id con Utils.validar_id;
#           si es inválido, avisar y saltar ese elemento.
#     2. Registrar cada dispositivo en el Hub con hub.registrar(disp):
#         ○ Si el id ya existe, capturar Duplicado y mostrar un mensaje indicando el fallo.
#         ○ Si algún dato fuese inválido en el constructor,
#           capturar DatoInvalido y continuar con el siguiente.

# Operaciones polimórficas masivas
#     1. Llamar a hub.operar_todos() (recorre todos los dispositivos):
#         ○ Para cada Medible: llamar a leer_valor() y mostrar la lectura.
#         ○ Para cada Conmutable: ejecutar encender() y luego apagar();
#           mostrar mensajes de acción (o estado resultante)

# Acciones específicas por tipo
#     1. Localizar una BombillaInteligente y:
#         ○ Cambiar su brillo (p. ej., 50 → 90) y mostrar el nuevo valor.
#         ○ Ejecutar una actualización de firmware con
#           Actualizable.actualizar_firmware("1.2.3"),
#           validando versión con Utils.validar_version.
#             ▪ Si la versión es inválida, capturar DatoInvalido y mostrar mensaje.
#     2. Localizar una CerraduraInteligente y:
#          ○ Mostrar su estado (bloqueada/desbloqueada).
#          ○ Llamar a bloquear() y luego a desbloquear() (y viceversa)
#            para evidenciar la conmutación

# Estadísticas y resúmenes
#     1. Obtener hub.estadisticas() y mostrar el diccionario con recuento por tipo
#     (p. ej., {'SensorTemperatura': 2, 'BombillaInteligente': 2, 'CerraduraInteligente': 1}).
#     2. Mostrar un resumen final: total de dispositivos, cuántos son medibles,
#        cuántos conmutables y cuántos actualizables
#        (se puede calcular sobre hub.listar() con contadores).

# Manejo de errores y casos límite (demostración explícita)
#     1. Intentar registrar de nuevo un id existente para mostrar el mensaje de Duplicado.
#     2. Probar a validar una versión incorrecta (por ejemplo "1.0")
#        para evidenciar validar_version == False y el lanzamiento de DatoInvalido
#        si se intenta actualizar con ella.
#     3. Intentar consultar un dispositivo inexistente para ilustrar NoEncontrado

from domotica import *

if __name__ == '__main__':
    # Mostrar un encabezado indicando que comienza la demo del sistema de domótica.
    print(f'\n{"=" * 5} DEMO DOMÓTICA - INICIO {"=" * 5}')

    # crear hub
    print('\nCreando Hub... OK')
    hub = Hub()

    # crear lista de datos
    # Dispositivo:
    #   id, tipo (sensor/bombilla/cerradura), nombre, fabricante
    #   ▪ SensorTemperatura: celsius inicial.
    #   ▪ BombillaInteligente: brillo inicial (0–100).
    #   ▪ CerraduraInteligente: estado inicial (bloqueada por defecto, opcional).
    print('\nCargando definiciones de dispositivos (lista de diccionarios)...')
    data = [
        {
            'id': 'S001',
            'tipo': 'sensor',
            'nombre': 'Sensor Cocina',
            'fabricante': 'Acme',
            'celsius': 22.5,
        },
        {
            'id': 'B001',
            'tipo': 'bombilla',
            'nombre': 'Bombilla Salón',
            'fabricante': 'Lumen',
            'brillo': 80,
        },
        {
            'id': 'C001',
            'tipo': 'cerradura',
            'nombre': 'Puerta Principal',
            'fabricante': 'SafeCo',
            'bloqueada': True,
        },
        {
            'id': 'S002',
            'tipo': 'sensor',
            'nombre': 'Sensor Dormitorio',
            'fabricante': 'Acme',
            'celsius': 19.3,
        },
        {
            'id': 'B002',
            'tipo': 'bombilla',
            'nombre': 'Bombilla Pasillo',
            'fabricante': 'Lumen',
            'brillo': 50,
        },
        {
            'id': '001',
            'tipo': 'cerradura',
            'nombre': 'Cerradura Baño',
            'fabricante': 'SafeCo',
            'bloqueada': False,
        },
        {
            'id': 'B001',
            'tipo': 'bombilla',
            'nombre': 'Bombilla Entrada',
            'fabricante': 'Lumen',
            'brillo': 60,
        },
    ]

    # Registro de los dispositivos,
    # recordad que validar_id se llama en el setter (tambien constructor)
    print('\nValidando e instanciando:\n')
    for dis in data:
        try:
            dispositivo: Dispositivo = None
            match str(dis.get('tipo', '')).lower():
                case TipoDispositivo.BOMBILLA:
                    dispositivo = BombillaInteligente(
                        id=dis.get('id', ''),
                        nombre=dis.get('nombre', ''),
                        fabricante=dis.get('fabricante', ''),
                        brillo=dis.get('brillo', ''),
                    )
                case TipoDispositivo.CERRADURA:
                    dispositivo = CerraduraInteligente(
                        id=dis.get('id', ''),
                        nombre=dis.get('nombre', ''),
                        fabricante=dis.get('fabricante', ''),
                        bloqueada=dis.get('bloqueada', ''),
                    )

                case TipoDispositivo.SENSOR:
                    dispositivo = SensorTemperatura(
                        id=dis.get('id', ''),
                        nombre=dis.get('nombre', ''),
                        fabricante=dis.get('fabricante', ''),
                        celsius=dis.get('celsius', ''),
                    )
            if dispositivo:
                hub.registrar(dispositivo)
                print(f'\tOK: {dispositivo.id} ({dispositivo.tipo()}) -> {dispositivo}')
        except Duplicado as e:
            print(f'\tDUPLICADO: {e}')
        except DatoInvalido as e:
            print(f'\tERROR: {e}')

    list_disp = hub.listar()
    print(f'\nRegistro en Hub completado: {len(list_disp)} dispositivos.')

    print('\nListado de dispositivos:\n')
    for d in list_disp:
        print(f'\t{d}')

    print('\nCapacidades detectadas:\n')
    # voy a usar este contador para un apartado que nos piden mas abajo
    # esto si quires todas las interfaces
    # capacidades = {k:0 for k in vars(interfaces)}
    # si quires puedes mirar por string
    capacidades = {k: 0 for k in (Medible, Conmutable, Actualizable)}
    for d in list_disp:
        res = f'\t{d.id} ->'
        for c in capacidades:
            if isinstance(d, c):
                res += f' {c.__name__},'
                capacidades[c] += 1
        print(res.removesuffix(','))

    print('\nOperar todos (polimorfismo):\n')
    hub.operar_todos()

    print('\nAcciones específicas\n')
    checks = [False for i in range(3)]
    for d in list_disp:
        res = f'\t{d.id}:'
        if not checks[0] and isinstance(d, BombillaInteligente):
            # cambiar brillo
            res += f' brillo previo = {d.brillo}'
            d.brillo = 90
            res += f' -> brillo nuevo = {d.brillo}'
            # actualizar firmware
            try:
                res += f'\n\t{d.id}:'
                res += 'actualizar_firmware("1.2.3") -> OK'
                d.actualizar_firmware('1.2.3')
                res += f'\n\t{d.id}:'
                res += 'actualizar_firmware("1.0")'
                d.actualizar_firmware('1.0')
            except DatoInvalido as e:
                res += f' -> {e}'
        elif not checks[1] and isinstance(d, CerraduraInteligente):
            # ver estado, apagarlo y encenderlo
            res += f'estado -> {"bloqueada" if d.bloqueada else "desbloqueada"};'
            res += ' desbloquear() -> OK;'
            d.desbloquear()
            res += ' bloquear() -> OK;'
            d.bloquear()
        elif not checks[2] and isinstance(d, SensorTemperatura):
            offset = 0.70
            res += f' Calibrar con offset {offset:+.2f}'
            d.celsius += offset
            res += f' -> nueva lectura = {d.celsius} ºC'

        print(res)

        if all(checks):
            break

    print('\nEstadísticas por tipo:\n')
    total = 0
    for tipo, val in hub.estadisticas().items():
        print(f'\t{tipo}: {val}')
        total += val
    print(f'\tTotal de dispositivos: {total}')

    print('\nResumen de capacidades:\n')

    for cap, val in capacidades.items():
        print(f'\t{cap.__name__}: {val}')

    print('\nPruebas de errores controlados:\n')
    # Registrar de nuevo B001 → ERROR: Duplicado (el ID ya existe)
    try:
        id = 'B001'
        res = f'\tRegistrar de nuevo {id}'
        hub.registrar(BombillaInteligente(id, 'bombilla', 'acme'))
    except Duplicado as e:
        res += f' -> ERROR: {type(e).__name__} ({e})'
    print(res)

    # Validar id "A_01" → False (carácter '_' no permitido)
    id = 'A_01'
    print(f'\tValidar id "{id}" -> {Utils.validar_id("")} (caracter "_" no permitido)')

    # Actualizar firmware B002 a "v1.2.3" → ERROR: versión inválida
    id = 'B002'
    firmware = 'v1.2.3'
    actualizada = Utils.validar_version(firmware)
    res = f'\tActualizar firmware {id} a "{firmware}"'
    res += '-> ERROR: versión inválida' if not actualizada else ''
    print(res)

    # Obtener "X999" → ERROR: NoEncontrado (no existe)
    # me he tenido que inventar el método para poder tirar el error
    try:
        id = 'X999'
        res = f'\tObtener {id}'
        d = hub.obtener(id)
    except NoEncontrado as e:
        res += f' -> ERROR: {type(e).__name__} ({e})'
    print(res)

    print(f'\n{"=" * 5} DEMO DOMÓTICA - FIN {"=" * 5}')
