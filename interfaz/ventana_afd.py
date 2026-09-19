import tkinter as tk
from tkinter import ttk, messagebox

from modelos.afd import AFD
from interfaz.visualizador import Visualizador


class VentanaAFD:

    def __init__(self, ventana_padre, afd=None):

        self.ventana = tk.Toplevel(ventana_padre)

        self.ventana.title("Simulador de AFD")
        self.ventana.geometry("1100x720")
        self.ventana.minsize(950, 620)

        self.afd = afd

        self.configurar_estilos()
        self.crear_interfaz()

        if self.afd is not None:
            self.cargar_afd()

    # ==========================================================
    # ESTILOS
    # ==========================================================

    def configurar_estilos(self):

        estilo = ttk.Style()

        try:
            estilo.theme_use("clam")
        except tk.TclError:
            pass

        estilo.configure(
            "Principal.TFrame",
            background="#f4f6f8"
        )

        estilo.configure(
            "Titulo.TLabel",
            background="#f4f6f8",
            foreground="#17202a",
            font=("Segoe UI", 20, "bold")
        )

        estilo.configure(
            "Subtitulo.TLabel",
            background="#f4f6f8",
            foreground="#68737d",
            font=("Segoe UI", 10)
        )

        estilo.configure(
            "Principal.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=(18, 9)
        )

        estilo.configure(
            "Secundario.TButton",
            font=("Segoe UI", 10),
            padding=(15, 9)
        )

    # ==========================================================
    # INTERFAZ
    # ==========================================================

    def crear_interfaz(self):

        # Fondo principal
        principal = ttk.Frame(
            self.ventana,
            style="Principal.TFrame",
            padding=20
        )

        principal.pack(
            fill="both",
            expand=True
        )

        # ======================================================
        # ENCABEZADO
        # ======================================================

        encabezado = ttk.Frame(
            principal,
            style="Principal.TFrame"
        )

        encabezado.pack(
            fill="x",
            pady=(0, 18)
        )

        ttk.Label(
            encabezado,
            text="Simulador de AFD",
            style="Titulo.TLabel"
        ).pack(
            anchor="w"
        )

        ttk.Label(
            encabezado,
            text=(
                "Autómata Finito Determinista · "
                "Configuración y simulación"
            ),
            style="Subtitulo.TLabel"
        ).pack(
            anchor="w",
            pady=(3, 0)
        )

        # ======================================================
        # DOS COLUMNAS
        # ======================================================

        columnas = ttk.Frame(
            principal,
            style="Principal.TFrame"
        )

        columnas.pack(
            fill="both",
            expand=True
        )

        columnas.columnconfigure(
            0,
            weight=1
        )

        columnas.columnconfigure(
            1,
            weight=1
        )

        columnas.rowconfigure(
            0,
            weight=1
        )

        # ======================================================
        # COLUMNA IZQUIERDA
        # ======================================================

        izquierda = tk.Frame(
            columnas,
            bg="#ffffff",
            highlightbackground="#dfe4e8",
            highlightthickness=1
        )

        izquierda.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 8)
        )

        # ------------------------------------------------------
        # TÍTULO
        # ------------------------------------------------------

        tk.Label(
            izquierda,
            text="Configuración del AFD",
            bg="#ffffff",
            fg="#17202a",
            font=("Segoe UI", 12, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 3)
        )

        tk.Label(
            izquierda,
            text="Define los elementos del autómata.",
            bg="#ffffff",
            fg="#7b8794",
            font=("Segoe UI", 9)
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

        # ------------------------------------------------------
        # FORMULARIO
        # ------------------------------------------------------

        formulario = tk.Frame(
            izquierda,
            bg="#ffffff"
        )

        formulario.pack(
            fill="x",
            padx=20
        )

        formulario.columnconfigure(
            1,
            weight=1
        )

        self.entrada_estados = self.crear_campo(
            formulario,
            0,
            "Estados"
        )

        self.entrada_alfabeto = self.crear_campo(
            formulario,
            1,
            "Alfabeto"
        )

        self.entrada_inicial = self.crear_campo(
            formulario,
            2,
            "Estado inicial"
        )

        self.entrada_finales = self.crear_campo(
            formulario,
            3,
            "Estados finales"
        )

        # ------------------------------------------------------
        # TRANSICIONES
        # ------------------------------------------------------

        tk.Label(
            izquierda,
            text="Transiciones",
            bg="#ffffff",
            fg="#17202a",
            font=("Segoe UI", 10, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 5)
        )

        tk.Label(
            izquierda,
            text=(
                "Una transición por línea:\n"
                "estado,símbolo,destino"
            ),
            bg="#ffffff",
            fg="#7b8794",
            font=("Segoe UI", 8)
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 7)
        )

        self.entrada_transiciones = tk.Text(
            izquierda,
            height=7,
            font=("Consolas", 10),
            bg="#f8f9fa",
            fg="#17202a",
            insertbackground="#17202a",
            relief="flat",
            borderwidth=0,
            highlightbackground="#dfe4e8",
            highlightthickness=1,
            padx=10,
            pady=8
        )

        self.entrada_transiciones.pack(
            fill="x",
            padx=20
        )

        tk.Label(
            izquierda,
            text="Ejemplo: q0,0,q1    q0,1,q0",
            bg="#ffffff",
            fg="#7b8794",
            font=("Consolas", 8)
        ).pack(
            anchor="w",
            padx=20,
            pady=(5, 10)
        )

        # ======================================================
        # BOTONES
        # ======================================================

        botones = tk.Frame(
            izquierda,
            bg="#ffffff"
        )

        botones.pack(
            fill="x",
            padx=20,
            pady=(5, 18)
        )

        self.boton_crear = ttk.Button(
            botones,
            text="Crear AFD",
            style="Principal.TButton",
            command=self.crear_afd
        )

        self.boton_crear.pack(
            side="left",
            padx=(0, 8)
        )

        self.boton_visualizar = ttk.Button(
            botones,
            text="Visualizar AFD",
            style="Secundario.TButton",
            command=self.visualizar,
            state="disabled"
        )

        self.boton_visualizar.pack(
            side="left"
        )

        self.resultado = tk.Label(
            botones,
            text="",
            bg="#ffffff",
            fg="#218c74",
            font=("Segoe UI", 9, "bold")
        )

        self.resultado.pack(
            side="left",
            padx=12
        )

        # ======================================================
        # COLUMNA DERECHA
        # ======================================================

        derecha = tk.Frame(
            columnas,
            bg="#ffffff",
            highlightbackground="#dfe4e8",
            highlightthickness=1
        )

        derecha.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(8, 0)
        )

        # ------------------------------------------------------
        # TÍTULO
        # ------------------------------------------------------

        tk.Label(
            derecha,
            text="Probar cadena",
            bg="#ffffff",
            fg="#17202a",
            font=("Segoe UI", 12, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 3)
        )

        tk.Label(
            derecha,
            text=(
                "Introduce una cadena para comprobar "
                "si el AFD la acepta."
            ),
            bg="#ffffff",
            fg="#7b8794",
            font=("Segoe UI", 9)
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

        # ------------------------------------------------------
        # CADENA
        # ------------------------------------------------------

        fila_cadena = tk.Frame(
            derecha,
            bg="#ffffff"
        )

        fila_cadena.pack(
            fill="x",
            padx=20
        )

        self.entrada_cadena = tk.Entry(
            fila_cadena,
            font=("Segoe UI", 11),
            bg="#f8f9fa",
            fg="#17202a",
            insertbackground="#17202a",
            relief="flat",
            highlightbackground="#dfe4e8",
            highlightthickness=1
        )

        self.entrada_cadena.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=7
        )

        self.boton_simular = ttk.Button(
            fila_cadena,
            text="Probar cadena",
            style="Principal.TButton",
            command=self.simular
        )

        self.boton_simular.pack(
            side="left",
            padx=(10, 0)
        )

        # ------------------------------------------------------
        # RESULTADO
        # ------------------------------------------------------

        resultado_frame = tk.Frame(
            derecha,
            bg="#f8f9fa"
        )

        resultado_frame.pack(
            fill="x",
            padx=20,
            pady=18
        )

        tk.Label(
            resultado_frame,
            text="Resultado",
            bg="#f8f9fa",
            fg="#7b8794",
            font=("Segoe UI", 8)
        ).pack(
            anchor="w",
            padx=12,
            pady=(9, 2)
        )

        self.resultado_simulacion = tk.Label(
            resultado_frame,
            text="Aún no se ha probado ninguna cadena.",
            bg="#f8f9fa",
            fg="#34495e",
            font=("Segoe UI", 10, "bold")
        )

        self.resultado_simulacion.pack(
            anchor="w",
            padx=12,
            pady=(0, 9)
        )

        # ------------------------------------------------------
        # RECORRIDO
        # ------------------------------------------------------

        tk.Label(
            derecha,
            text="Recorrido de la simulación",
            bg="#ffffff",
            fg="#17202a",
            font=("Segoe UI", 10, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(5, 7)
        )

        recorrido_frame = tk.Frame(
            derecha,
            bg="#ffffff"
        )

        recorrido_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        self.ventana_recorrido = tk.Text(
            recorrido_frame,
            font=("Consolas", 9),
            bg="#f8f9fa",
            fg="#34495e",
            relief="flat",
            borderwidth=0,
            highlightbackground="#dfe4e8",
            highlightthickness=1,
            wrap="word",
            padx=10,
            pady=10,
            state="disabled"
        )

        self.ventana_recorrido.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar = ttk.Scrollbar(
            recorrido_frame,
            orient="vertical",
            command=self.ventana_recorrido.yview
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.ventana_recorrido.configure(
            yscrollcommand=scrollbar.set
        )

    # ==========================================================
    # CREAR CAMPO
    # ==========================================================

    def crear_campo(
        self,
        contenedor,
        fila,
        texto
    ):

        etiqueta = tk.Label(
            contenedor,
            text=texto,
            bg="#ffffff",
            fg="#34495e",
            font=("Segoe UI", 9)
        )

        etiqueta.grid(
            row=fila,
            column=0,
            sticky="w",
            padx=(0, 12),
            pady=5
        )

        entrada = tk.Entry(
            contenedor,
            font=("Segoe UI", 9),
            bg="#f8f9fa",
            fg="#17202a",
            insertbackground="#17202a",
            relief="flat",
            highlightbackground="#dfe4e8",
            highlightthickness=1
        )

        entrada.grid(
            row=fila,
            column=1,
            sticky="ew",
            pady=5,
            ipady=6
        )

        return entrada

    # ==========================================================
    # CARGAR AFD
    # ==========================================================

    def cargar_afd(self):

        if self.afd is None:
            return

        # ==========================================
        # ESTADOS
        # ==========================================

        self.entrada_estados.delete(0, tk.END)

        self.entrada_estados.insert(
            0,
            ", ".join(
                sorted(self.afd.estados)
            )
        )

        # ==========================================
        # ALFABETO
        # ==========================================

        self.entrada_alfabeto.delete(0, tk.END)

        self.entrada_alfabeto.insert(
            0,
            ", ".join(
                sorted(self.afd.alfabeto)
            )
        )

        # ==========================================
        # ESTADO INICIAL
        # ==========================================

        self.entrada_inicial.delete(0, tk.END)

        self.entrada_inicial.insert(
            0,
            self.afd.estado_inicial
        )

        # ==========================================
        # ESTADOS FINALES
        # ==========================================

        self.entrada_finales.delete(0, tk.END)

        self.entrada_finales.insert(
            0,
            ", ".join(
                sorted(self.afd.estados_finales)
            )
        )

        # ==========================================
        # TRANSICIONES
        # ==========================================

        self.entrada_transiciones.delete(
            "1.0",
            tk.END
        )

        for (origen, simbolo), destino in sorted(
            self.afd.transiciones.items()
        ):

            self.entrada_transiciones.insert(
                tk.END,
                f"{origen},{simbolo},{destino}\n"
            )

        # ==========================================
        # MENSAJE
        # ==========================================

        self.resultado.config(
            text="✓ AFD convertido correctamente.",
            fg="#218c74"
        )

        # ==========================================
        # HABILITAR VISUALIZACIÓN
        # ==========================================

        self.boton_visualizar.config(
            state="normal"
        )

        # ==========================================
        # LIMPIAR SIMULACIÓN ANTERIOR
        # ==========================================

        self.resultado_simulacion.config(
            text="Aún no se ha probado ninguna cadena.",
            fg="#34495e"
        )

        self.limpiar_recorrido()

    # ==========================================================
    # CREAR AFD
    # ==========================================================

    def crear_afd(self):

        try:

            # ==========================================
            # ESTADOS
            # ==========================================

            texto_estados = self.entrada_estados.get().strip()

            if not texto_estados:
                raise ValueError(
                    "Debe ingresar al menos un estado."
                )

            estados = {
                estado.strip()
                for estado in texto_estados.split(",")
                if estado.strip()
            }

            if not estados:
                raise ValueError(
                    "Debe ingresar al menos un estado válido."
                )

            # ==========================================
            # ALFABETO
            # ==========================================

            texto_alfabeto = self.entrada_alfabeto.get().strip()

            if not texto_alfabeto:
                raise ValueError(
                    "El alfabeto no puede estar vacío."
                )

            alfabeto = {
                simbolo.strip()
                for simbolo in texto_alfabeto.split(",")
                if simbolo.strip()
            }

            if not alfabeto:
                raise ValueError(
                    "Debe ingresar al menos un símbolo válido."
                )

            # ==========================================
            # ESTADO INICIAL
            # ==========================================

            estado_inicial = (
                self.entrada_inicial
                .get()
                .strip()
            )

            if not estado_inicial:
                raise ValueError(
                    "Debe ingresar el estado inicial."
                )

            if estado_inicial not in estados:
                raise ValueError(
                    f"El estado inicial '{estado_inicial}' "
                    "no pertenece al conjunto de estados."
                )

            # ==========================================
            # ESTADOS FINALES
            # ==========================================

            texto_finales = (
                self.entrada_finales
                .get()
                .strip()
            )

            if not texto_finales:
                raise ValueError(
                    "Debe ingresar al menos un estado final."
                )

            estados_finales = {
                estado.strip()
                for estado in texto_finales.split(",")
                if estado.strip()
            }

            estados_finales_invalidos = (
                estados_finales - estados
            )

            if estados_finales_invalidos:

                raise ValueError(
                    "Los siguientes estados finales "
                    "no existen:\n\n"
                    + ", ".join(
                        sorted(estados_finales_invalidos)
                    )
                )

            # ==========================================
            # TRANSICIONES
            # ==========================================

            texto_transiciones = (
                self.entrada_transiciones
                .get("1.0", tk.END)
                .strip()
            )

            if not texto_transiciones:

                raise ValueError(
                    "Debe ingresar las transiciones "
                    "del AFD."
                )

            transiciones = {}

            for numero_linea, linea in enumerate(
                texto_transiciones.splitlines(),
                start=1
            ):

                linea = linea.strip()

                # Ignorar líneas vacías
                if not linea:
                    continue

                partes = [
                    parte.strip()
                    for parte in linea.split(",")
                ]

                # --------------------------------------
                # FORMATO
                # --------------------------------------

                if len(partes) != 3:

                    raise ValueError(
                        f"Error en la línea {numero_linea}:\n\n"
                        f"{linea}\n\n"
                        "Formato correcto:\n"
                        "estado,símbolo,destino"
                    )

                origen, simbolo, destino = partes

                # --------------------------------------
                # CAMPOS VACÍOS
                # --------------------------------------

                if not origen:
                    raise ValueError(
                        f"Error en la línea {numero_linea}:\n\n"
                        "El estado de origen está vacío."
                    )

                if not simbolo:
                    raise ValueError(
                        f"Error en la línea {numero_linea}:\n\n"
                        "El símbolo está vacío."
                    )

                if not destino:
                    raise ValueError(
                        f"Error en la línea {numero_linea}:\n\n"
                        "El estado destino está vacío."
                    )

                # --------------------------------------
                # ESTADO DE ORIGEN
                # --------------------------------------

                if origen not in estados:

                    raise ValueError(
                        f"Error en la línea {numero_linea}:\n\n"
                        f"El estado de origen '{origen}' "
                        "no existe."
                    )

                # --------------------------------------
                # SÍMBOLO
                # --------------------------------------

                if simbolo not in alfabeto:

                    raise ValueError(
                        f"Error en la línea {numero_linea}:\n\n"
                        f"El símbolo '{simbolo}' "
                        "no pertenece al alfabeto."
                    )

                # --------------------------------------
                # ESTADO DESTINO
                # --------------------------------------

                if destino not in estados:

                    raise ValueError(
                        f"Error en la línea {numero_linea}:\n\n"
                        f"El estado destino '{destino}' "
                        "no existe."
                    )

                # --------------------------------------
                # TRANSICIÓN DUPLICADA
                # --------------------------------------

                clave = (
                    origen,
                    simbolo
                )

                if clave in transiciones:

                    raise ValueError(
                        f"Error en la línea {numero_linea}:\n\n"
                        f"Ya existe una transición "
                        f"para ({origen}, {simbolo}).\n\n"
                        "Un AFD solo puede tener una "
                        "transición por estado y símbolo."
                    )

                transiciones[clave] = destino

            # ==========================================
            # CREAR AFD
            # ==========================================

            self.afd = AFD(
                estados,
                alfabeto,
                estado_inicial,
                estados_finales,
                transiciones
            )

            # ==========================================
            # ÉXITO
            # ==========================================

            self.resultado.config(
                text="✓ AFD creado correctamente.",
                fg="#218c74"
            )

            self.boton_visualizar.config(
                state="normal"
            )

            self.resultado_simulacion.config(
                text="Aún no se ha probado ninguna cadena.",
                fg="#34495e"
            )

            self.limpiar_recorrido()

        # ==============================================
        # ERROR
        # ==============================================

        except ValueError as error:

            self.afd = None

            self.boton_visualizar.config(
                state="disabled"
            )

            self.resultado.config(
                text="✗ Error al crear el AFD.",
                fg="#c0392b"
            )

            messagebox.showerror(
                "Error al crear AFD",
                str(error)
            )

    # ==========================================================
    # SIMULAR
    # ==========================================================

    def simular(self):

        if self.afd is None:

            messagebox.showwarning(
                "Advertencia",
                "Primero debe crear el AFD."
            )

            return

        cadena = self.entrada_cadena.get()

        recorrido, aceptada = (
            self.afd.obtener_recorrido(cadena)
        )

        if aceptada:

            self.resultado_simulacion.config(
                text="✓ CADENA ACEPTADA",
                fg="#218c74"
            )

        else:

            self.resultado_simulacion.config(
                text="✗ CADENA RECHAZADA",
                fg="#c0392b"
            )

        self.mostrar_recorrido(
            recorrido
        )

    # ==========================================================
    # VISUALIZAR AFD
    # ==========================================================

    def visualizar(self):

        if self.afd is None:

            messagebox.showwarning(
                "Advertencia",
                "Primero debe crear el AFD."
            )

            return

        visualizador = Visualizador(
            self.ventana
        )

        visualizador.dibujar_automata(
            estados=self.afd.estados,
            transiciones=self.afd.transiciones,
            estado_inicial=self.afd.estado_inicial,
            estados_finales=self.afd.estados_finales
        )

    # ==========================================================
    # MOSTRAR RECORRIDO
    # ==========================================================

    def mostrar_recorrido(self, recorrido):

        self.ventana_recorrido.config(
            state="normal"
        )

        self.ventana_recorrido.delete(
            "1.0",
            tk.END
        )

        self.ventana_recorrido.insert(
            tk.END,
            "\n".join(recorrido)
        )

        self.ventana_recorrido.config(
            state="disabled"
        )

    # ==========================================================
    # LIMPIAR RECORRIDO
    # ==========================================================

    def limpiar_recorrido(self):

        self.ventana_recorrido.config(
            state="normal"
        )

        self.ventana_recorrido.delete(
            "1.0",
            tk.END
        )

        self.ventana_recorrido.config(
            state="disabled"
        )