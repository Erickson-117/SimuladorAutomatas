from modelos.afd import AFD


def convertir_afn_a_afd(afn):
    """
    Convierte un AFN a un AFD utilizando el método
    de construcción por subconjuntos.

    El AFN puede contener transiciones epsilon (ε).
    """

    # --------------------------------------------------
    # CIERRE-EPSILON
    # --------------------------------------------------

    def epsilon_cierre(estados):

        cierre = set(estados)
        pendientes = list(estados)

        while pendientes:

            estado = pendientes.pop()

            destinos = afn.transiciones.get(
                (estado, "ε"),
                set()
            )

            for destino in destinos:

                if destino not in cierre:

                    cierre.add(destino)
                    pendientes.append(destino)

        return frozenset(cierre)

    # --------------------------------------------------
    # MOVIMIENTO
    # --------------------------------------------------

    def mover(estados, simbolo):

        destinos = set()

        for estado in estados:

            estados_destino = afn.transiciones.get(
                (estado, simbolo),
                set()
            )

            destinos.update(estados_destino)

        return epsilon_cierre(destinos)

    # --------------------------------------------------
    # ESTADO INICIAL DEL AFD
    # --------------------------------------------------

    estado_inicial = epsilon_cierre(
        {afn.estado_inicial}
    )

    # --------------------------------------------------
    # CONSTRUCCIÓN DE SUBCONJUNTOS
    # --------------------------------------------------

    estados_afd = set()

    estados_pendientes = [
        estado_inicial
    ]

    transiciones_afd = {}

    while estados_pendientes:

        estado_actual = estados_pendientes.pop()

        if estado_actual in estados_afd:
            continue

        estados_afd.add(estado_actual)

        for simbolo in sorted(afn.alfabeto):

            siguiente_estado = mover(
                estado_actual,
                simbolo
            )

            transiciones_afd[
                (estado_actual, simbolo)
            ] = siguiente_estado

            if siguiente_estado not in estados_afd:

                if siguiente_estado not in estados_pendientes:

                    estados_pendientes.append(
                        siguiente_estado
                    )

    # --------------------------------------------------
    # ESTADOS FINALES
    # --------------------------------------------------

    estados_finales_afd = set()

    for estado in estados_afd:

        if estado & afn.estados_finales:

            estados_finales_afd.add(
                estado
            )

    # --------------------------------------------------
    # CONVERTIR LOS SUBCONJUNTOS A NOMBRES
    # --------------------------------------------------

    def nombre_estado(estado):

        if not estado:
            return "∅"

        elementos = sorted(estado)

        return "{" + ",".join(elementos) + "}"

    nombres_estados = {
        estado: nombre_estado(estado)
        for estado in estados_afd
    }

    # --------------------------------------------------
    # TRANSICIONES DEL AFD
    # --------------------------------------------------

    transiciones_finales = {}

    for (origen, simbolo), destino in transiciones_afd.items():

        transiciones_finales[
            (
                nombres_estados[origen],
                simbolo
            )
        ] = nombres_estados[destino]

    # --------------------------------------------------
    # CONJUNTO DE ESTADOS
    # --------------------------------------------------

    estados_finales_nombres = {
        nombres_estados[estado]
        for estado in estados_finales_afd
    }

    estados_nombres = set(
        nombres_estados.values()
    )

    # --------------------------------------------------
    # ESTADO INICIAL
    # --------------------------------------------------

    estado_inicial_nombre = nombres_estados[
        estado_inicial
    ]

    # --------------------------------------------------
    # CREAR AFD
    # --------------------------------------------------

    afd = AFD(
        estados=estados_nombres,
        alfabeto=set(afn.alfabeto),
        estado_inicial=estado_inicial_nombre,
        estados_finales=estados_finales_nombres,
        transiciones=transiciones_finales
    )

    return afd