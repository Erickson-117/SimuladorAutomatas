import tkinter as tk
from tkinter import ttk

from interfaz.ventana_afd import VentanaAFD
from interfaz.ventana_afn import VentanaAFN


class Aplicacion:

    def __init__(self, ventana):
        self.ventana = ventana

        self.ventana.title("Simulador de Autómatas")
        self.ventana.geometry("900x600")
        self.ventana.minsize(800, 550)
        self.ventana.configure(bg="#f4f6f8")

        self.configurar_estilos()
        self.crear_interfaz()

    def configurar_estilos(self):

        estilo = ttk.Style()
        estilo.theme_use("clam")

        estilo.configure(
            "Principal.TFrame",
            background="#f4f6f8"
        )

        estilo.configure(
            "Panel.TFrame",
            background="white"
        )

        estilo.configure(
            "Titulo.TLabel",
            background="white",
            foreground="#1f2937",
            font=("Segoe UI", 24, "bold")
        )

        estilo.configure(
            "Subtitulo.TLabel",
            background="white",
            foreground="#6b7280",
            font=("Segoe UI", 11)
        )

        estilo.configure(
            "Seccion.TLabel",
            background="white",
            foreground="#1f2937",
            font=("Segoe UI", 14, "bold")
        )

        estilo.configure(
            "Principal.TButton",
            font=("Segoe UI", 11, "bold"),
            padding=(20, 12)
        )

        estilo.configure(
            "Secundario.TButton",
            font=("Segoe UI", 10),
            padding=(15, 10)
        )

    def crear_interfaz(self):

        contenedor = ttk.Frame(
            self.ventana,
            style="Principal.TFrame"
        )
        contenedor.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=35
        )

        # Panel principal
        panel = ttk.Frame(
            contenedor,
            style="Panel.TFrame"
        )
        panel.pack(
            fill="both",
            expand=True
        )

        # -------------------------
        # ENCABEZADO
        # -------------------------

        encabezado = ttk.Frame(
            panel,
            style="Panel.TFrame"
        )
        encabezado.pack(
            fill="x",
            padx=45,
            pady=(40, 10)
        )

        titulo = ttk.Label(
            encabezado,
            text="Simulador de Autómatas",
            style="Titulo.TLabel"
        )
        titulo.pack()

        subtitulo = ttk.Label(
            encabezado,
            text="Crea, simula y visualiza autómatas finitos",
            style="Subtitulo.TLabel"
        )
        subtitulo.pack(pady=(8, 0))

        # -------------------------
        # SECCIÓN DE SELECCIÓN
        # -------------------------

        contenido = ttk.Frame(
            panel,
            style="Panel.TFrame"
        )
        contenido.pack(
            fill="both",
            expand=True,
            padx=45,
            pady=25
        )

        texto = ttk.Label(
            contenido,
            text="Selecciona el tipo de autómata",
            style="Seccion.TLabel"
        )
        texto.pack(pady=(10, 25))

        # -------------------------
        # BOTONES
        # -------------------------

        botones = ttk.Frame(
            contenido,
            style="Panel.TFrame"
        )
        botones.pack()

        boton_afd = ttk.Button(
            botones,
            text="Crear AFD",
            style="Principal.TButton",
            command=lambda: VentanaAFD(self.ventana)
        )
        boton_afd.grid(
            row=0,
            column=0,
            padx=15,
            pady=10
        )

        boton_afn = ttk.Button(
            botones,
            text="Crear AFN",
            style="Principal.TButton",
            command=lambda: VentanaAFN(self.ventana)
        )
        boton_afn.grid(
            row=0,
            column=1,
            padx=15,
            pady=10
        )

        # -------------------------
        # INFORMACIÓN
        # -------------------------

        informacion = ttk.Frame(
            contenido,
            style="Panel.TFrame"
        )
        informacion.pack(
            pady=(45, 10)
        )

        ttk.Label(
            informacion,
            text="AFD",
            style="Seccion.TLabel"
        ).grid(
            row=0,
            column=0,
            padx=50
        )

        ttk.Label(
            informacion,
            text="AFN",
            style="Seccion.TLabel"
        ).grid(
            row=0,
            column=1,
            padx=50
        )

        ttk.Label(
            informacion,
            text="Autómata Finito Determinista",
            style="Subtitulo.TLabel"
        ).grid(
            row=1,
            column=0,
            padx=50,
            pady=(5, 0)
        )

        ttk.Label(
            informacion,
            text="Autómata Finito No Determinista",
            style="Subtitulo.TLabel"
        ).grid(
            row=1,
            column=1,
            padx=50,
            pady=(5, 0)
        )

        # -------------------------
        # PIE DE VENTANA
        # -------------------------

        pie = ttk.Frame(
            panel,
            style="Panel.TFrame"
        )
        pie.pack(
            fill="x",
            padx=45,
            pady=(10, 30)
        )

        ttk.Label(
            pie,
            text="Proyecto - Autómatas y Lenguajes Formales",
            style="Subtitulo.TLabel"
        ).pack()