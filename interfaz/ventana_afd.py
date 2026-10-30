import logging
import tkinter as tk
from tkinter import ttk, messagebox

from modelos.afd import AFD
from interfaz.visualizador import Visualizador
from interfaz.ventana_minimizacion import VentanaMinimizacion


logger = logging.getLogger(__name__)


class VentanaAFD:

    def __init__(self, ventana_padre, afd=None):

        self.ventana = tk.Toplevel(ventana_padre)

        self.ventana.title("Simulador de AFD")
        # Mantener las ventanas de trabajo a pantalla completa.
        self.ventana.attributes("-fullscreen", True)
        self.ventana.protocol("WM_DELETE_WINDOW", self.regresar_a_principal)
        self.ventana.bind("<Escape>", lambda _evento: self.regresar_a_principal())

        self.afd = afd
        self.visualizador = None
        self._after_animacion = None

        self.configurar_estilos()
        self.crear_interfaz()
        from interfaz.tema import registrar_ventana
        registrar_ventana(self.ventana)

        if self.afd is not None:
            self.cargar_afd()

    # ESTILOS

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

    # INTERFAZ

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

        # NAVEGACIÓN
        barra_navegacion = ttk.Frame(principal, style="Principal.TFrame")
        barra_navegacion.pack(fill="x", pady=(0, 8))
        ttk.Button(
            barra_navegacion,
            text="← Pantalla principal",
            style="Secundario.TButton",
            command=self.regresar_a_principal
        ).pack(side="left")
        ttk.Button(
            barra_navegacion,
            text="Salir del programa",
            style="Secundario.TButton",
            command=self.salir_del_programa
        ).pack(side="right")

        # ENCABEZADO

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

        # DOS COLUMNAS

        columnas = ttk.Frame(
            principal,
            style="Principal.TFrame"
        )

        columnas.pack(
            fill="both",
            expand=True
        )

        # Dar más espacio a la columna derecha, donde está el visualizador.
        columnas.columnconfigure(0, weight=5, uniform="columnas")
        columnas.columnconfigure(1, weight=6, uniform="columnas")

        columnas.rowconfigure(
            0,
            weight=1
        )

        # COLUMNA IZQUIERDA

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

        # TÍTULO

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

        # FORMULARIO

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

        # TRANSICIONES

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

        # BOTONES

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

        self.boton_minimizar = ttk.Button(
            botones,
            text="Minimizar AFD",
            style="Secundario.TButton",
            command=self.abrir_minimizacion,
            state="disabled"
        )
        self.boton_minimizar.pack(side="left", padx=(8, 0))

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

        # COLUMNA DERECHA

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

        # TÍTULO

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

        # CADENA

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

        # RESULTADO

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

        # RECORRIDO

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

        recorrido_frame = tk.Frame(derecha, bg="#ffffff")
        recorrido_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        texto_frame = tk.Frame(recorrido_frame, bg="#ffffff", height=125)
        texto_frame.pack(fill="x", expand=False)
        texto_frame.pack_propagate(False)

        self.ventana_recorrido = tk.Text(
            texto_frame, font=("Consolas", 9), bg="#f8f9fa", fg="#34495e",
            relief="flat", borderwidth=0, highlightbackground="#dfe4e8",
            highlightthickness=1, wrap="word", padx=10, pady=10, state="disabled"
        )
        self.ventana_recorrido.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(texto_frame, orient="vertical", command=self.ventana_recorrido.yview)
        scrollbar.pack(side="right", fill="y")
        self.ventana_recorrido.configure(yscrollcommand=scrollbar.set)

        tk.Label(
            recorrido_frame, text="Diagrama del autómata · estado activo en amarillo",
            bg="#ffffff", fg="#68737d", font=("Segoe UI", 8)
        ).pack(anchor="w", pady=(8, 3))
        self.contenedor_grafico = tk.Frame(
            recorrido_frame, bg="#ffffff", height=235,
            highlightbackground="#dfe4e8", highlightthickness=1
        )
        self.contenedor_grafico.pack(fill="both", expand=True)
        self.contenedor_grafico.pack_propagate(False)

    # CREAR CAMPO

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

    # CARGAR AFD

    def cargar_afd(self):

        if self.afd is None:
            return

        # Un AFD recibido desde la conversión AFN → AFD también puede minimizarse.
        self.boton_visualizar.config(state="normal")
        self.boton_minimizar.config(state="normal")

        # ESTADOS

        self.entrada_estados.delete(0, tk.END)

        self.entrada_estados.insert(
            0,
            ", ".join(
                sorted(self.afd.estados)
            )
        )

        # ALFABETO

        self.entrada_alfabeto.delete(0, tk.END)

        self.entrada_alfabeto.insert(
            0,
            ", ".join(
                sorted(self.afd.alfabeto)
            )
        )

        # ESTADO INICIAL

        self.entrada_inicial.delete(0, tk.END)

        self.entrada_inicial.insert(
            0,
            self.afd.estado_inicial
        )

        # ESTADOS FINALES

        self.entrada_finales.delete(0, tk.END)

        self.entrada_finales.insert(
            0,
            ", ".join(
                sorted(self.afd.estados_finales)
            )
        )

        # TRANSICIONES

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

        # MENSAJE

        self.resultado.config(
            text="✓ AFD convertido correctamente.",
            fg="#218c74"
        )

        # HABILITAR VISUALIZACIÓN

        self.boton_visualizar.config(
            state="normal"
        )

        # LIMPIAR SIMULACIÓN ANTERIOR

        self.resultado_simulacion.config(
            text="Aún no se ha probado ninguna cadena.",
            fg="#34495e"
        )

        self.limpiar_recorrido()

    # CREAR AFD

    def crear_afd(self):
        logger.info("Acción iniciada: crear_afd")

        try:

            # ESTADOS

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

            # ALFABETO

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

            # ESTADO INICIAL

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

            # ESTADOS FINALES

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

            # TRANSICIONES

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

                # FORMATO

                if len(partes) != 3:

                    raise ValueError(
                        f"Error en la línea {numero_linea}:\n\n"
                        f"{linea}\n\n"
                        "Formato correcto:\n"
                        "estado,símbolo,destino"
                    )

                origen, simbolo, destino = partes

                # CAMPOS VACÍOS

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

                # ESTADO DE ORIGEN

                if origen not in estados:

                    raise ValueError(
                        f"Error en la línea {numero_linea}:\n\n"
                        f"El estado de origen '{origen}' "
                        "no existe."
                    )

                # SÍMBOLO

                if simbolo not in alfabeto:

                    raise ValueError(
                        f"Error en la línea {numero_linea}:\n\n"
                        f"El símbolo '{simbolo}' "
                        "no pertenece al alfabeto."
                    )

                # ESTADO DESTINO

                if destino not in estados:

                    raise ValueError(
                        f"Error en la línea {numero_linea}:\n\n"
                        f"El estado destino '{destino}' "
                        "no existe."
                    )

                # TRANSICIÓN DUPLICADA

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

            # CREAR AFD

            self.afd = AFD(
                estados,
                alfabeto,
                estado_inicial,
                estados_finales,
                transiciones
            )

            # ÉXITO

            self.resultado.config(
                text="✓ AFD creado correctamente.",
                fg="#218c74"
            )

            self.boton_visualizar.config(state="normal")
            self.boton_minimizar.config(state="normal")

            self.resultado_simulacion.config(
                text="Aún no se ha probado ninguna cadena.",
                fg="#34495e"
            )

            self.limpiar_recorrido()

        # ERROR

        except ValueError as error:
            # La entrada no cumple los requisitos para crear el AFD.
            logger.warning("No se pudo crear el AFD: %s", error)
            self.afd = None

            self.boton_visualizar.config(state="disabled")
            self.boton_minimizar.config(state="disabled")

            self.resultado.config(
                text="✗ Error al crear el AFD.",
                fg="#c0392b"
            )

            messagebox.showerror(
                "Error al crear AFD",
                str(error)
            )

    # SIMULAR

    def regresar_a_principal(self):
        """Cierra la ventana actual y vuelve a la pantalla de selección."""
        try:
            if self._after_animacion is not None:
                self.ventana.after_cancel(self._after_animacion)
                self._after_animacion = None
        except (tk.TclError, AttributeError):
            pass
        raiz = self.ventana.master
        self.ventana.destroy()
        try:
            raiz.deiconify()
            raiz.attributes("-fullscreen", True)
            raiz.lift()
        except tk.TclError:
            pass

    def salir_del_programa(self):
        """Cierra toda la aplicación."""
        try:
            if self._after_animacion is not None:
                self.ventana.after_cancel(self._after_animacion)
        except (tk.TclError, AttributeError):
            pass
        raiz = self.ventana.master
        try:
            raiz.destroy()
        except tk.TclError:
            self.ventana.destroy()

    def asegurar_visualizador(self):
        if self.visualizador is None:
            self.visualizador = Visualizador(self.ventana, self.contenedor_grafico)
        self.ventana.update_idletasks()
        automata = self.afd
        if automata is not None:
            self.visualizador.dibujar_automata(
                estados=automata.estados,
                transiciones=automata.transiciones,
                estado_inicial=automata.estado_inicial,
                estados_finales=automata.estados_finales
            )

    def visualizar(self):
        if self.afd is None:
            logger.warning("No se pudo validar la cadena: primero debe crear el AFD")
            messagebox.showwarning("Advertencia", "Primero debe crear el AFD.")
            return
        self.asegurar_visualizador()

    def animar_estados(self, cuadros, indice=0):
        if not cuadros or self.afd is None:
            return
        if self._after_animacion is not None:
            try:
                self.ventana.after_cancel(self._after_animacion)
            except tk.TclError:
                pass
            self._after_animacion = None
        self.asegurar_visualizador()
        automata = self.afd
        self.visualizador.dibujar_automata(
            estados=automata.estados,
            transiciones=automata.transiciones,
            estado_inicial=automata.estado_inicial,
            estados_finales=automata.estados_finales,
            estados_activos=cuadros[indice]
        )
        if indice + 1 < len(cuadros):
            self._after_animacion = self.ventana.after(
                550, lambda: self.animar_estados_siguiente(cuadros, indice + 1)
            )

    def animar_estados_siguiente(self, cuadros, indice):
        automata = self.afd
        if automata is None or self.visualizador is None:
            return
        self.visualizador.dibujar_automata(
            estados=automata.estados,
            transiciones=automata.transiciones,
            estado_inicial=automata.estado_inicial,
            estados_finales=automata.estados_finales,
            estados_activos=cuadros[indice]
        )
        if indice + 1 < len(cuadros):
            self._after_animacion = self.ventana.after(
                550, lambda: self.animar_estados_siguiente(cuadros, indice + 1)
            )
        else:
            self._after_animacion = None

    def abrir_minimizacion(self):
        logger.info("Acción iniciada: abrir_minimizacion")
        if self.afd is None:
            messagebox.showwarning("Advertencia", "Primero debe crear o cargar un AFD.")
            return
        try:
            VentanaMinimizacion(self.ventana, self.afd)
        except (ValueError, TypeError) as error:
            logger.error("No se pudo abrir la minimización del AFD: %s", error)
            messagebox.showerror("Error de minimización", str(error))

    def simular(self):
        logger.info("Acción iniciada: simular AFD")
        if self.afd is None:
            mensaje = "No se pudo probar la cadena: primero debe crear el AFD."
            logger.warning(mensaje)
            messagebox.showwarning("Advertencia", "Primero debe crear el AFD.")
            return
        cadena = self.entrada_cadena.get()
        if not cadena.strip():
            mensaje = "No se pudo probar la cadena: el campo de cadena está vacío."
            logger.warning(mensaje)
            messagebox.showwarning("Cadena vacía", "Introduce una cadena antes de probarla.")
            return
        recorrido, aceptada = self.afd.obtener_recorrido(cadena)
        self.resultado_simulacion.config(
            text="✓ CADENA ACEPTADA" if aceptada else "✗ CADENA RECHAZADA",
            fg="#218c74" if aceptada else "#c0392b"
        )
        self.mostrar_recorrido(recorrido)
        cuadros = [{self.afd.estado_inicial}]
        actual = self.afd.estado_inicial
        for simbolo in cadena:
            if simbolo not in self.afd.alfabeto or (actual, simbolo) not in self.afd.transiciones:
                break
            actual = self.afd.transiciones[(actual, simbolo)]
            cuadros.append({actual})
        self.animar_estados(cuadros)

    # MOSTRAR RECORRIDO

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

    # LIMPIAR RECORRIDO

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
