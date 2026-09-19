import tkinter as tk
import math


class Visualizador:

    def __init__(self, ventana_padre):
        self.ventana = tk.Toplevel(ventana_padre)
        self.ventana.title("Visualización del Autómata")
        self.ventana.geometry("1100x750")
        self.ventana.minsize(800, 600)
        self.ventana.configure(bg="#f4f6f8")

        # Colores
        self.color_fondo = "#f4f6f8"
        self.color_canvas = "#ffffff"
        self.color_estado = "#ffffff"
        self.color_estado_inicial = "#e8f1ff"
        self.color_estado_final = "#e8f7ee"
        self.color_borde = "#374151"
        self.color_linea = "#4b5563"
        self.color_texto = "#1f2937"
        self.color_etiqueta = "#2563eb"

        # -----------------------------
        # ENCABEZADO
        # -----------------------------

        encabezado = tk.Frame(
            self.ventana,
            bg=self.color_fondo
        )
        encabezado.pack(
            fill="x",
            padx=25,
            pady=(20, 10)
        )

        tk.Label(
            encabezado,
            text="Visualización del Autómata",
            font=("Segoe UI", 18, "bold"),
            bg=self.color_fondo,
            fg=self.color_texto
        ).pack()

        tk.Label(
            encabezado,
            text="Representación gráfica de estados y transiciones",
            font=("Segoe UI", 10),
            bg=self.color_fondo,
            fg="#6b7280"
        ).pack(pady=(3, 0))

        # -----------------------------
        # CONTENEDOR DEL CANVAS
        # -----------------------------

        contenedor = tk.Frame(
            self.ventana,
            bg=self.color_canvas,
            highlightbackground="#d1d5db",
            highlightthickness=1
        )

        contenedor.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(5, 25)
        )

        self.canvas = tk.Canvas(
            contenedor,
            bg=self.color_canvas,
            highlightthickness=0
        )

        self.canvas.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

    # ==================================================
    # DIBUJAR AUTOMATA
    # ==================================================

    def dibujar_automata(
        self,
        estados,
        transiciones,
        estado_inicial,
        estados_finales
    ):

        self.canvas.delete("all")

        estados = sorted(estados)
        estados_finales = set(estados_finales)

        if not estados:
            return

        ancho = self.canvas.winfo_width()
        alto = self.canvas.winfo_height()

        # Si Tkinter todavía no ha calculado el tamaño,
        # utilizamos dimensiones aproximadas.
        if ancho < 400:
            ancho = 1000

        if alto < 300:
            alto = 600

        posiciones = self.calcular_posiciones(
            estados,
            ancho,
            alto
        )

        grupos = self.agrupar_transiciones(
            transiciones
        )

        # Primero las transiciones
        self.dibujar_transiciones(
            grupos,
            posiciones,
            estados
        )

        # Después los estados
        self.dibujar_estados(
            posiciones,
            estado_inicial,
            estados_finales
        )

        # Finalmente el indicador inicial
        self.dibujar_estado_inicial(
            posiciones,
            estado_inicial
        )

    # ==================================================
    # CALCULAR POSICIONES
    # ==================================================

    def calcular_posiciones(
        self,
        estados,
        ancho,
        alto
    ):

        posiciones = {}

        cantidad = len(estados)

        centro_x = ancho / 2
        centro_y = alto / 2

        if cantidad == 1:

            posiciones[estados[0]] = (
                centro_x,
                centro_y
            )

            return posiciones

        if cantidad == 2:

            separacion = min(
                260,
                ancho / 3
            )

            posiciones[estados[0]] = (
                centro_x - separacion,
                centro_y
            )

            posiciones[estados[1]] = (
                centro_x + separacion,
                centro_y
            )

            return posiciones

        # Para 3 o más estados dejamos un margen
        # amplio para que los bucles y etiquetas
        # no queden pegados al borde.

        radio_x = min(
            350,
            ancho / 2 - 170
        )

        radio_y = min(
            210,
            alto / 2 - 150
        )

        for indice, estado in enumerate(estados):

            angulo = (
                2 * math.pi * indice / cantidad
                - math.pi / 2
            )

            x = centro_x + radio_x * math.cos(angulo)
            y = centro_y + radio_y * math.sin(angulo)

            posiciones[estado] = (
                x,
                y
            )

        return posiciones

    # ==================================================
    # AGRUPAR TRANSICIONES
    # ==================================================

    def agrupar_transiciones(
        self,
        transiciones
    ):

        grupos = {}

        for (origen, simbolo), destinos in transiciones.items():

            # AFD
            if isinstance(destinos, str):

                destinos = [destinos]

            # AFN
            elif isinstance(
                destinos,
                (set, list, tuple)
            ):

                destinos = list(destinos)

            else:
                continue

            for destino in destinos:

                clave = (
                    origen,
                    destino
                )

                if clave not in grupos:
                    grupos[clave] = []

                if simbolo not in grupos[clave]:
                    grupos[clave].append(
                        simbolo
                    )

        return grupos

    # ==================================================
    # DIBUJAR TRANSICIONES
    # ==================================================

    def dibujar_transiciones(
        self,
        grupos,
        posiciones,
        estados
    ):

        for (
            origen,
            destino
        ), simbolos in grupos.items():

            if origen not in posiciones:
                continue

            if destino not in posiciones:
                continue

            etiqueta = ", ".join(
                sorted(simbolos)
            )

            # --------------------------
            # BUCLE
            # --------------------------

            if origen == destino:

                self.dibujar_bucle(
                    posiciones[origen],
                    etiqueta
                )

            # --------------------------
            # DOS DIRECCIONES
            # --------------------------

            elif (
                destino,
                origen
            ) in grupos:

                indice_origen = estados.index(
                    origen
                )

                indice_destino = estados.index(
                    destino
                )

                if indice_origen < indice_destino:
                    desplazamiento = 50
                else:
                    desplazamiento = -50

                self.dibujar_curva(
                    posiciones[origen],
                    posiciones[destino],
                    etiqueta,
                    desplazamiento
                )

            # --------------------------
            # UNA DIRECCIÓN
            # --------------------------

            else:

                self.dibujar_recta(
                    posiciones[origen],
                    posiciones[destino],
                    etiqueta
                )

    # ==================================================
    # TRANSICIÓN RECTA
    # ==================================================

    def dibujar_recta(
        self,
        origen,
        destino,
        etiqueta
    ):

        x1, y1 = origen
        x2, y2 = destino

        dx = x2 - x1
        dy = y2 - y1

        distancia = math.hypot(
            dx,
            dy
        )

        if distancia == 0:
            return

        radio = 40

        ux = dx / distancia
        uy = dy / distancia

        inicio_x = x1 + ux * radio
        inicio_y = y1 + uy * radio

        final_x = x2 - ux * radio
        final_y = y2 - uy * radio

        self.canvas.create_line(
            inicio_x,
            inicio_y,
            final_x,
            final_y,
            fill=self.color_linea,
            width=2,
            arrow=tk.LAST,
            arrowshape=(12, 14, 6)
        )

        # Posición de la etiqueta
        medio_x = (
            inicio_x + final_x
        ) / 2

        medio_y = (
            inicio_y + final_y
        ) / 2

        # Separación perpendicular
        px = -uy
        py = ux

        etiqueta_x = medio_x + px * 15
        etiqueta_y = medio_y + py * 15

        self.dibujar_etiqueta(
            etiqueta_x,
            etiqueta_y,
            etiqueta
        )

    # ==================================================
    # TRANSICIÓN CURVA
    # ==================================================

    def dibujar_curva(
        self,
        origen,
        destino,
        etiqueta,
        desplazamiento
    ):

        x1, y1 = origen
        x2, y2 = destino

        dx = x2 - x1
        dy = y2 - y1

        distancia = math.hypot(
            dx,
            dy
        )

        if distancia == 0:
            return

        ux = dx / distancia
        uy = dy / distancia

        px = -uy
        py = ux

        radio = 40

        inicio_x = x1 + ux * radio
        inicio_y = y1 + uy * radio

        final_x = x2 - ux * radio
        final_y = y2 - uy * radio

        control_x = (
            (x1 + x2) / 2
            + px * desplazamiento
        )

        control_y = (
            (y1 + y2) / 2
            + py * desplazamiento
        )

        self.canvas.create_line(
            inicio_x,
            inicio_y,
            control_x,
            control_y,
            final_x,
            final_y,
            fill=self.color_linea,
            width=2,
            smooth=True,
            splinesteps=30,
            arrow=tk.LAST,
            arrowshape=(12, 14, 6)
        )

        self.dibujar_etiqueta(
            control_x,
            control_y - 15,
            etiqueta
        )

    # ==================================================
    # BUCLE
    # ==================================================

    def dibujar_bucle(
        self,
        posicion,
        etiqueta
    ):

        x, y = posicion

        # Bucle ubicado encima del estado
        # con suficiente separación.
        self.canvas.create_arc(
            x - 32,
            y - 95,
            x + 32,
            y - 32,
            start=20,
            extent=300,
            style=tk.ARC,
            outline=self.color_linea,
            width=2
        )

        # Flecha del bucle
        self.canvas.create_line(
            x + 23,
            y - 45,
            x + 31,
            y - 32,
            fill=self.color_linea,
            width=2,
            arrow=tk.LAST,
            arrowshape=(10, 12, 5)
        )

        # Etiqueta
        self.dibujar_etiqueta(
            x,
            y - 112,
            etiqueta
        )

    # ==================================================
    # ETIQUETA DE TRANSICIÓN
    # ==================================================

    def dibujar_etiqueta(
        self,
        x,
        y,
        texto
    ):

        # Fondo para que la línea no atraviese
        # visualmente el texto.
        fondo = self.canvas.create_text(
            x,
            y,
            text=texto,
            font=("Segoe UI", 10, "bold"),
            fill=self.color_canvas
        )

        caja = self.canvas.bbox(
            fondo
        )

        if caja:

            self.canvas.create_rectangle(
                caja[0] - 5,
                caja[1] - 3,
                caja[2] + 5,
                caja[3] + 3,
                fill=self.color_canvas,
                outline=""
            )

        self.canvas.create_text(
            x,
            y,
            text=texto,
            font=("Segoe UI", 10, "bold"),
            fill=self.color_etiqueta
        )

    # ==================================================
    # DIBUJAR ESTADOS
    # ==================================================

    def dibujar_estados(
        self,
        posiciones,
        estado_inicial,
        estados_finales
    ):

        radio = 40

        for estado, (
            x,
            y
        ) in posiciones.items():

            # Color del estado
            if estado in estados_finales:

                relleno = self.color_estado_final

            elif estado == estado_inicial:

                relleno = self.color_estado_inicial

            else:

                relleno = self.color_estado

            # Estado final
            if estado in estados_finales:

                self.canvas.create_oval(
                    x - radio - 7,
                    y - radio - 7,
                    x + radio + 7,
                    y + radio + 7,
                    outline=self.color_borde,
                    width=2,
                    fill=self.color_canvas
                )

            # Estado principal
            self.canvas.create_oval(
                x - radio,
                y - radio,
                x + radio,
                y + radio,
                outline=self.color_borde,
                width=2,
                fill=relleno
            )

            # Nombre
            self.canvas.create_text(
                x,
                y,
                text=estado,
                font=("Segoe UI", 11, "bold"),
                fill=self.color_texto
            )

    # ==================================================
    # INDICADOR DE ESTADO INICIAL
    # ==================================================

    def dibujar_estado_inicial(
        self,
        posiciones,
        estado_inicial
    ):

        if estado_inicial not in posiciones:
            return

        x, y = posiciones[
            estado_inicial
        ]

        radio = 40

        inicio_x = x - 105
        final_x = x - radio - 5

        self.canvas.create_line(
            inicio_x,
            y,
            final_x,
            y,
            fill=self.color_linea,
            width=2,
            arrow=tk.LAST,
            arrowshape=(12, 14, 6)
        )

        self.canvas.create_text(
            inicio_x,
            y - 18,
            text="Inicio",
            font=("Segoe UI", 9),
            fill="#6b7280"
        )