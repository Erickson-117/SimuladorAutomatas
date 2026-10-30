import tkinter as tk
from tkinter import ttk

from algoritmos.minimizacion import minimizar_afd
from interfaz.visualizador import Visualizador


class VentanaMinimizacion:
    """Ventana didáctica para recorrer las etapas de minimización de un AFD."""

    def __init__(self, ventana_padre, afd, al_cerrar=None):
        self.ventana = tk.Toplevel(ventana_padre)
        self.ventana.title("Minimización de AFD")
        self.ventana.attributes("-fullscreen", True)
        self.ventana.configure(bg="#f4f6f8")
        self.ventana.protocol("WM_DELETE_WINDOW", self.cerrar)
        self.ventana.bind("<Escape>", lambda _e: self.cerrar())
        self.al_cerrar = al_cerrar
        self.paso_actual = 0
        self.visualizador = None
        self.afd_minimo, self.pasos = minimizar_afd(afd)
        self._construir_interfaz()
        self.mostrar_paso(0)
        from interfaz.tema import registrar_ventana
        registrar_ventana(self.ventana)

    def _construir_interfaz(self):
        base = ttk.Frame(self.ventana, padding=18)
        base.pack(fill="both", expand=True)
        barra = ttk.Frame(base)
        barra.pack(fill="x", pady=(0, 10))
        ttk.Button(barra, text="← Volver al AFD", command=self.cerrar).pack(side="left")
        ttk.Button(barra, text="Salir del programa", command=self.salir).pack(side="right")
        ttk.Label(base, text="Minimización de AFD", font=("Segoe UI", 21, "bold")).pack(anchor="w")
        ttk.Label(
            base,
            text="Método de particiones · Explora cada etapa y observa cómo se reduce el autómata.",
            style="Subtitulo.TLabel",
        ).pack(anchor="w", pady=(2, 10))
        self.progreso = ttk.Progressbar(base, mode="determinate", maximum=max(1, len(self.pasos)), value=1)
        self.progreso.pack(fill="x", pady=(0, 12))

        contenido = ttk.Frame(base)
        contenido.pack(fill="both", expand=True)
        contenido.columnconfigure(0, weight=2, uniform="min")
        contenido.columnconfigure(1, weight=5, uniform="min")
        contenido.rowconfigure(0, weight=1)

        izquierda = ttk.LabelFrame(contenido, text="  PROCESO PASO A PASO  ", padding=14)
        izquierda.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self.etiqueta_paso = ttk.Label(izquierda, text="", font=("Segoe UI", 13, "bold"), wraplength=420)
        self.etiqueta_paso.pack(anchor="w", pady=(0, 10))
        self.texto_paso = tk.Text(
            izquierda, wrap="word", font=("Segoe UI", 11), relief="flat",
            padx=14, pady=14, spacing1=2, spacing3=4, borderwidth=0,
        )
        # Reservar primero el espacio de navegación evita que los botones
        # queden ocultos cuando la ventana está maximizada o en fullscreen.
        navegacion = ttk.Frame(izquierda)
        navegacion.pack(side="bottom", fill="x", pady=(12, 0))
        self.boton_anterior = ttk.Button(navegacion, text="← Anterior", command=self.anterior)
        self.boton_anterior.pack(side="left")
        self.boton_siguiente = ttk.Button(navegacion, text="Siguiente →", command=self.siguiente)
        self.boton_siguiente.pack(side="right")
        self.texto_paso.pack(side="top", fill="both", expand=True)

        derecha = ttk.LabelFrame(contenido, text="  DIAGRAMA DEL PASO ACTUAL  ", padding=8)
        derecha.grid(row=0, column=1, sticky="nsew")
        self.marco_grafico = tk.Frame(derecha, highlightthickness=1, bd=0)
        self.marco_grafico.pack(fill="both", expand=True)
        self.visualizador = Visualizador(self.ventana, self.marco_grafico)

    def mostrar_paso(self, indice):
        self.paso_actual = max(0, min(indice, len(self.pasos) - 1))
        paso = self.pasos[self.paso_actual]
        self.etiqueta_paso.config(text=f"PASO {self.paso_actual + 1} DE {len(self.pasos)}  ·  {paso['titulo']}")
        self.progreso.configure(value=self.paso_actual + 1)
        self.texto_paso.config(state="normal")
        self.texto_paso.delete("1.0", tk.END)
        self.texto_paso.insert(tk.END, paso["descripcion"])
        if paso["particiones"]:
            self.texto_paso.insert(tk.END, "\n\nNota: el diagrama muestra el AFD alcanzable durante el refinamiento; las particiones se detallan en este panel.")
        self.texto_paso.config(state="disabled")
        automata = paso["automata"]
        self.visualizador.dibujar_automata(
            estados=automata.estados,
            transiciones=automata.transiciones,
            estado_inicial=automata.estado_inicial,
            estados_finales=automata.estados_finales,
        )
        self.boton_anterior.config(state="normal" if self.paso_actual > 0 else "disabled")
        self.boton_siguiente.config(state="normal" if self.paso_actual < len(self.pasos) - 1 else "disabled")

    def anterior(self):
        self.mostrar_paso(self.paso_actual - 1)

    def siguiente(self):
        self.mostrar_paso(self.paso_actual + 1)

    def cerrar(self):
        try:
            self.ventana.destroy()
        finally:
            if self.al_cerrar:
                self.al_cerrar()

    def salir(self):
        raiz = self.ventana._root()
        raiz.destroy()
