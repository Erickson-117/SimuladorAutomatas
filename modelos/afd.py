class AFD:

    def __init__(self, estados, alfabeto, estado_inicial, estados_finales, transiciones):

        if not estados:
            raise ValueError("El AFD debe tener al menos un estado.")

        if not alfabeto:
            raise ValueError("El alfabeto no puede estar vacío.")

        if estado_inicial not in estados:
            raise ValueError("El estado inicial debe pertenecer al conjunto de estados.")

        if not estados_finales.issubset(estados):
            raise ValueError("Todos los estados finales deben pertenecer al conjunto de estados.")

        for (estado, simbolo), destino in transiciones.items():

            if estado not in estados:
                raise ValueError(
                    f"El estado '{estado}' de una transición no existe."
                )

            if simbolo not in alfabeto:
                raise ValueError(
                    f"El símbolo '{simbolo}' no pertenece al alfabeto."
                )

            if destino not in estados:
                raise ValueError(
                    f"El estado destino '{destino}' no existe."
                )

        for estado in estados:
            for simbolo in alfabeto:
                if (estado, simbolo) not in transiciones:
                    raise ValueError(
                        f"Falta la transición para "
                        f"({estado}, {simbolo})."
                    )           

        self.estados = estados
        self.alfabeto = alfabeto
        self.estado_inicial = estado_inicial
        self.estados_finales = estados_finales
        self.transiciones = transiciones

    def simular(self, cadena):

        estado_actual = self.estado_inicial

        for simbolo in cadena:

            if simbolo not in self.alfabeto:
                return False

            if (estado_actual, simbolo) not in self.transiciones:
                return False

            estado_actual = self.transiciones[(estado_actual, simbolo)]

        return estado_actual in self.estados_finales

    def obtener_recorrido(self, cadena):

        recorrido = []

        estado_actual = self.estado_inicial

        recorrido.append(
            f"Estado inicial: {estado_actual}"
        )

        for simbolo in cadena:

            if simbolo not in self.alfabeto:
                return recorrido, False

            if (estado_actual, simbolo) not in self.transiciones:
                return recorrido, False

            estado_siguiente = self.transiciones[
                (estado_actual, simbolo)
            ]

            recorrido.append(
                f"{estado_actual} --{simbolo}--> {estado_siguiente}"
            )

            estado_actual = estado_siguiente

        aceptada = estado_actual in self.estados_finales

        recorrido.append(
            f"Estado final: {estado_actual}"
        )

        recorrido.append(
            f"Resultado: {'ACEPTADA' if aceptada else 'RECHAZADA'}"
        )

        return recorrido, aceptada