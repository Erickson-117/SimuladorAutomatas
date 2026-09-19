class AFN:

    def __init__(self, estados, alfabeto, estado_inicial, estados_finales, transiciones):

        

        if not estados:
            raise ValueError("El AFN debe tener al menos un estado.")

        if not alfabeto:
            raise ValueError("El alfabeto no puede estar vacío.")

        if estado_inicial not in estados:
            raise ValueError("El estado inicial debe pertenecer al conjunto de estados.")

        if not estados_finales.issubset(estados):
            raise ValueError("Todos los estados finales deben pertenecer al conjunto de estados.")

        for (estado, simbolo), destinos in transiciones.items():

            if estado not in estados:
                raise ValueError(
                    f"El estado '{estado}' de una transición no existe."
                )

            if simbolo != "ε" and simbolo not in alfabeto:
                raise ValueError(
                    f"El símbolo '{simbolo}' no pertenece al alfabeto."
                )

            if not destinos.issubset(estados):
                raise ValueError(
                    "Una transición contiene un estado destino que no existe."
                )

        self.estados = estados
        self.alfabeto = alfabeto
        self.estado_inicial = estado_inicial
        self.estados_finales = estados_finales
        self.transiciones = transiciones

    def epsilon_cierre(self, estados):
        cierre = set(estados)
        pendientes = list(estados)

        while pendientes:
            estado = pendientes.pop()

            destinos = self.transiciones.get(
                (estado, "ε"),
                set()
            )

            for destino in destinos:
                if destino not in cierre:
                    cierre.add(destino)
                    pendientes.append(destino)

        return cierre

    def simular(self, cadena):

        estados_actuales = self.epsilon_cierre(
            {self.estado_inicial}
        )

        for simbolo in cadena:

            if simbolo not in self.alfabeto:
                return False

            nuevos_estados = set()

            for estado in estados_actuales:

                destinos = self.transiciones.get(
                    (estado, simbolo),
                    set()
                )

                nuevos_estados.update(destinos)

            estados_actuales = self.epsilon_cierre(
                nuevos_estados
            )

        return bool(
            estados_actuales & self.estados_finales
        )    
        