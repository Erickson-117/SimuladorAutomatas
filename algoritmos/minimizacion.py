"""Minimización de AFD mediante refinamiento de particiones."""
from modelos.afd import AFD


def minimizar_afd(afd):
    """Devuelve (afd_minimo, pasos) sin modificar el AFD original.

    Cada paso contiene titulo, descripcion, particiones y un AFD para dibujar.
    """
    if not isinstance(afd, AFD):
        raise TypeError("La minimización requiere un objeto AFD.")

    pasos = []

    def crear_snapshot(estados, transiciones, inicial, finales, alfabeto):
        return AFD(set(estados), set(alfabeto), inicial, set(finales), dict(transiciones))

    def agregar_paso(titulo, descripcion, automata, particiones=None):
        pasos.append({
            "titulo": titulo,
            "descripcion": descripcion,
            "automata": automata,
            "particiones": [set(g) for g in (particiones or [])],
        })

    agregar_paso(
        "1. AFD original",
        "Este es el autómata determinista que se va a minimizar. Primero identificaremos los estados alcanzables desde el estado inicial.",
        crear_snapshot(afd.estados, afd.transiciones, afd.estado_inicial, afd.estados_finales, afd.alfabeto),
    )

    # Encontrar estados accesibles desde el estado inicial.
    accesibles = {afd.estado_inicial}
    pendientes = [afd.estado_inicial]
    while pendientes:
        actual = pendientes.pop()
        for simbolo in afd.alfabeto:
            destino = afd.transiciones[(actual, simbolo)]
            if destino not in accesibles:
                accesibles.add(destino)
                pendientes.append(destino)

    transiciones_accesibles = {
        clave: destino
        for clave, destino in afd.transiciones.items()
        if clave[0] in accesibles and destino in accesibles
    }
    finales_accesibles = set(afd.estados_finales) & accesibles
    afd_accesible = crear_snapshot(
        accesibles, transiciones_accesibles, afd.estado_inicial,
        finales_accesibles, afd.alfabeto
    )
    inaccesibles = set(afd.estados) - accesibles
    detalle = (
        "Estados inaccesibles eliminados: " + ", ".join(sorted(inaccesibles)) + "."
        if inaccesibles else "No hay estados inaccesibles; todos se pueden alcanzar desde el estado inicial."
    )
    agregar_paso("2. Eliminar estados inaccesibles", detalle, afd_accesible)

    no_finales = accesibles - finales_accesibles
    particiones = [grupo for grupo in (no_finales, finales_accesibles) if grupo]
    agregar_paso(
        "3. Partición inicial",
        "Separamos los estados no finales de los finales, porque un estado final nunca puede ser equivalente a uno no final.\n\n" + _texto_particiones(particiones),
        afd_accesible,
        particiones,
    )

    # Refinamiento: separar estados que transicionan a grupos distintos.
    while True:
        indice_grupo = {
            estado: i
            for i, grupo in enumerate(particiones)
            for estado in grupo
        }
        nuevas_particiones = []
        hubo_cambio = False

        for grupo in particiones:
            subgrupos = {}
            for estado in sorted(grupo):
                firma = tuple(
                    indice_grupo[afd_accesible.transiciones[(estado, simbolo)]]
                    for simbolo in sorted(afd.alfabeto)
                )
                subgrupos.setdefault(firma, set()).add(estado)
            nuevas_particiones.extend(subgrupos.values())
            if len(subgrupos) > 1:
                hubo_cambio = True

        particiones = nuevas_particiones
        agregar_paso(
            "4. Refinamiento de particiones",
            ("Se encontraron diferencias en las transiciones y se dividieron los grupos.\n\n" if hubo_cambio else "Ningún grupo necesita dividirse más. Las particiones son estables.\n\n") + _texto_particiones(particiones),
            afd_accesible,
            particiones,
        )
        if not hubo_cambio:
            break

    # Cada partición estable se convierte en un estado del AFD mínimo.
    particiones = sorted(particiones, key=lambda grupo: (0 if afd.estado_inicial in grupo else 1, sorted(grupo)))
    nombres = {frozenset(grupo): "{" + ", ".join(sorted(grupo)) + "}" for grupo in particiones}
    nombre_de = {estado: nombres[frozenset(grupo)] for grupo in particiones for estado in grupo}
    estados_minimos = set(nombre_de.values())
    inicial_minimo = nombre_de[afd.estado_inicial]
    finales_minimos = {nombre_de[e] for e in finales_accesibles}
    transiciones_minimas = {}
    for grupo in particiones:
        representativo = next(iter(grupo))
        origen_nuevo = nombre_de[representativo]
        for simbolo in afd.alfabeto:
            destino_original = afd_accesible.transiciones[(representativo, simbolo)]
            transiciones_minimas[(origen_nuevo, simbolo)] = nombre_de[destino_original]

    minimo = AFD(estados_minimos, set(afd.alfabeto), inicial_minimo, finales_minimos, transiciones_minimas)
    agregar_paso(
        "5. AFD mínimo",
        f"Cada partición estable se fusionó en un solo estado. El AFD pasó de {len(afd.estados)} estados a {len(minimo.estados)} estados.\n\nEstados del AFD mínimo:\n" + "\n".join(sorted(minimo.estados)),
        minimo,
        particiones,
    )
    return minimo, pasos


def _texto_particiones(particiones):
    return "Particiones actuales:\n" + "\n".join(
        f"P{i + 1} = {{{', '.join(sorted(grupo))}}}"
        for i, grupo in enumerate(particiones)
    )
