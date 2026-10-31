import logging
import tkinter as tk
from tkinter import ttk, messagebox

from interfaz.ventana_afd import VentanaAFD
from interfaz.ventana_afn import VentanaAFN
from interfaz.ventana_regex import VentanaExpresionesRegulares
from interfaz.ventana_logs import VentanaLogs
from interfaz.tema import obtener_paleta, cambiar_tema_global

logger = logging.getLogger(__name__)


class Aplicacion:
    """Panel principal con navegación lateral y temas claro/oscuro."""

    def __init__(self, ventana):
        self.ventana = ventana
        self.tema_actual = "oscuro"
        self.p = obtener_paleta(self.tema_actual)
        self._widgets_tema = []

        self.ventana.title("SimuladorAutomatas | Centro de trabajo")
        self.ventana.configure(bg=self.p["fondo"])
        self.ventana.minsize(980, 650)
        try:
            self.ventana.state("zoomed")
        except tk.TclError:
            self.ventana.geometry("1280x800")

        self.configurar_estilos()
        self.crear_interfaz()
        self.aplicar_tema()
        self.ventana.bind("<Escape>", self.alternar_maximizado)
        self.ventana.protocol("WM_DELETE_WINDOW", self.salir)

    def alternar_maximizado(self, _evento=None):
        """Permite salir del modo maximizado con Escape en equipos compatibles."""
        try:
            if self.ventana.state() == "zoomed":
                self.ventana.state("normal")
            else:
                self.ventana.state("zoomed")
        except tk.TclError:
            pass

    def configurar_estilos(self):
        estilo = ttk.Style(self.ventana)
        try:
            estilo.theme_use("clam")
        except tk.TclError:
            pass
        estilo.configure("SA.TButton", font=("Segoe UI", 10, "bold"), padding=(12, 9), relief="flat")
        estilo.configure("SA.Side.TButton", font=("Segoe UI", 10), padding=(12, 10), anchor="w", relief="flat")
        estilo.configure("SA.Small.TButton", font=("Segoe UI", 9), padding=(9, 6), relief="flat")

    def crear_interfaz(self):
        self.raiz = tk.Frame(self.ventana, bd=0)
        self.raiz.pack(fill="both", expand=True)

        # Barra lateral fija
        self.sidebar = tk.Frame(self.raiz, width=248, bd=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.marca = tk.Frame(self.sidebar, bd=0)
        self.marca.pack(fill="x", padx=18, pady=(22, 24))
        self.logo = tk.Label(self.marca, text="◈", font=("Segoe UI Symbol", 25, "bold"))
        self.logo.pack(side="left", padx=(0, 10))
        self.nombre_marca = tk.Label(self.marca, text="Simulador\nAutomatas", font=("Segoe UI", 15, "bold"), justify="left")
        self.nombre_marca.pack(side="left")

        self.lbl_menu = tk.Label(self.sidebar, text="ESPACIO DE TRABAJO", font=("Segoe UI", 8, "bold"), anchor="w")
        self.lbl_menu.pack(fill="x", padx=20, pady=(0, 8))

        self.nav_buttons = []
        self.agregar_nav("⌂", "Inicio", self.mostrar_inicio, activo=True)
        self.agregar_nav("◉", "Crear / simular AFN", self.abrir_afn)
        self.agregar_nav("◎", "Crear / simular AFD", self.abrir_afd)
        self.agregar_nav("⇄", "Expresiones regulares", self.abrir_expresiones_regulares)
        self.agregar_nav("▤", "Visor de logs", self.abrir_logs)

        self.divisor_sidebar = tk.Frame(self.sidebar, height=1)
        self.divisor_sidebar.pack(fill="x", padx=18, pady=18)
        self.lbl_herramientas = tk.Label(self.sidebar, text="HERRAMIENTAS", font=("Segoe UI", 8, "bold"), anchor="w")
        self.lbl_herramientas.pack(fill="x", padx=20, pady=(0, 8))
        self.agregar_nav("✓", "Banco de pruebas", self.abrir_banco_desde_afn)
        self.agregar_nav("⇩", "Conversión y minimización", self.ayuda_conversion)

        self.sidebar_spacer = tk.Frame(self.sidebar)
        self.sidebar_spacer.pack(fill="both", expand=True)
        self.sidebar_footer = tk.Frame(self.sidebar, bd=0)
        self.sidebar_footer.pack(fill="x", padx=18, pady=(8, 18))
        self.tema_btn = ttk.Button(self.sidebar_footer, text="☼  Cambiar a tema claro", style="SA.Small.TButton", command=self.alternar_tema)
        self.tema_btn.pack(fill="x", pady=(0, 8))
        self.salir_btn = ttk.Button(
            self.sidebar_footer,
            text="⏻  Salir del programa",
            style="SA.Small.TButton",
            command=self.salir,
        )
        self.salir_btn.pack(fill="x", pady=(0, 12))
        self.footer_text = tk.Label(self.sidebar_footer, text="", font=("Segoe UI", 8), justify="left", anchor="w")
        self.footer_text.pack(fill="x")

        # Área de contenido
        self.contenido = tk.Frame(self.raiz, bd=0)
        self.contenido.pack(side="left", fill="both", expand=True)
        self.header = tk.Frame(self.contenido, bd=0)
        self.header.pack(fill="x", padx=34, pady=(25, 12))
        self.header_kicker = tk.Label(self.header, text="CENTRO DE TRABAJO", font=("Segoe UI", 8, "bold"), anchor="w")
        self.header_kicker.pack(fill="x")
        self.header_title = tk.Label(self.header, text="Panel principal", font=("Segoe UI", 25, "bold"), anchor="w")
        self.header_title.pack(fill="x", pady=(4, 2))
        self.header_subtitle = tk.Label(self.header, text="Crea, simula, transforma y analiza autómatas desde un solo lugar.", font=("Segoe UI", 10), anchor="w")
        self.header_subtitle.pack(fill="x")

        self.body = tk.Frame(self.contenido, bd=0)
        self.body.pack(fill="both", expand=True, padx=34, pady=(8, 24))

        # Tarjeta de bienvenida
        self.hero = tk.Frame(self.body, bd=0, highlightthickness=1)
        self.hero.pack(fill="x", pady=(0, 20))
        self.hero_inner = tk.Frame(self.hero, bd=0)
        self.hero_inner.pack(fill="x", padx=24, pady=22)
        self.hero_title = tk.Label(self.hero_inner, text="Bienvenido a SimuladorAutomatas", font=("Segoe UI", 18, "bold"), anchor="w")
        self.hero_title.pack(fill="x")
        self.hero_desc = tk.Label(self.hero_inner, text="Explora autómatas finitos, prueba cadenas y compara los resultados de tus modelos.", font=("Segoe UI", 10), anchor="w", justify="left", wraplength=850)
        self.hero_desc.pack(fill="x", pady=(7, 15))
        self.hero_action = ttk.Button(self.hero_inner, text="Comenzar con un AFN  →", style="SA.TButton", command=self.abrir_afn)
        self.hero_action.pack(anchor="w")

        self.section_title = tk.Label(self.body, text="Módulos disponibles", font=("Segoe UI", 14, "bold"), anchor="w")
        self.section_title.pack(fill="x", pady=(0, 12))
        self.cards = tk.Frame(self.body, bd=0)
        self.cards.pack(fill="both", expand=True)
        self.cards.columnconfigure(0, weight=1, uniform="cards")
        self.cards.columnconfigure(1, weight=1, uniform="cards")
        self.cards.rowconfigure(0, weight=1, uniform="rows")
        self.cards.rowconfigure(1, weight=1, uniform="rows")

        self.crear_tarjeta(0, 0, "◉", "Autómata no determinista", "Define estados, transiciones ε y simula cadenas en un AFN.", "Abrir AFN", self.abrir_afn)
        self.crear_tarjeta(0, 1, "◎", "Autómata determinista", "Construye un AFD y comprueba la aceptación de cadenas.", "Abrir AFD", self.abrir_afd)
        self.crear_tarjeta(1, 0, "⇄", "Expresiones regulares", "Valida cadenas y genera autómatas para expresiones compatibles.", "Abrir regex", self.abrir_expresiones_regulares)
        self.crear_tarjeta(1, 1, "▤", "Registros y diagnósticos", "Consulta los logs de la aplicación y revisa sus eventos.", "Abrir visor", self.abrir_logs)

        self.bottom_note = tk.Label(self.body, text="Consejo: desde el módulo AFN puedes abrir el banco automático de pruebas.", font=("Segoe UI", 9), anchor="w")
        self.bottom_note.pack(fill="x", pady=(14, 0))

    def agregar_nav(self, icono, texto, comando, activo=False):
        btn = tk.Button(self.sidebar, text=f"{icono}   {texto}", command=comando, anchor="w", relief="flat", bd=0,
                        font=("Segoe UI", 10), padx=18, pady=10, cursor="hand2")
        btn.pack(fill="x", padx=10, pady=2)
        self.nav_buttons.append((btn, activo))

    def crear_tarjeta(self, fila, columna, icono, titulo, descripcion, texto_boton, comando):
        tarjeta = tk.Frame(self.cards, bd=0, highlightthickness=1)
        tarjeta.grid(row=fila, column=columna, sticky="nsew", padx=(0, 10) if columna == 0 else (10, 0), pady=(0, 10) if fila == 0 else (10, 0))
        interior = tk.Frame(tarjeta, bd=0)
        interior.pack(fill="both", expand=True, padx=19, pady=17)
        icon = tk.Label(interior, text=icono, font=("Segoe UI Symbol", 22, "bold"), anchor="w")
        icon.pack(fill="x")
        label = tk.Label(interior, text=titulo, font=("Segoe UI", 12, "bold"), anchor="w")
        label.pack(fill="x", pady=(8, 5))
        desc = tk.Label(interior, text=descripcion, font=("Segoe UI", 9), anchor="w", justify="left", wraplength=380)
        desc.pack(fill="x", pady=(0, 12))
        btn = ttk.Button(interior, text=texto_boton + "  →", style="SA.Small.TButton", command=comando)
        btn.pack(anchor="w")
        self._widgets_tema.extend([(tarjeta, "card"), (interior, "panel"), (icon, "icon"), (label, "heading"), (desc, "muted")])

    def aplicar_tema(self):
        self.p = obtener_paleta(self.tema_actual)
        p = self.p
        cambiar_tema_global(self.tema_actual)
        self.ventana.configure(bg=p["fondo"])
        self.raiz.configure(bg=p["fondo"])
        self.sidebar.configure(bg=p["panel"])
        # El espacio flexible debe usar el mismo fondo de la barra lateral;
        # de lo contrario Tkinter deja visible un bloque blanco en algunos temas.
        self.sidebar_spacer.configure(bg=p["panel"])
        self.contenido.configure(bg=p["fondo"])
        self.header.configure(bg=p["fondo"])
        self.body.configure(bg=p["fondo"])
        self.marca.configure(bg=p["panel"])
        self.logo.configure(bg=p["panel"], fg=p["acento"])
        self.nombre_marca.configure(bg=p["panel"], fg=p["texto"])
        self.lbl_menu.configure(bg=p["panel"], fg=p["texto_secundario"])
        self.lbl_herramientas.configure(bg=p["panel"], fg=p["texto_secundario"])
        self.divisor_sidebar.configure(bg=p["borde"])
        self.sidebar_footer.configure(bg=p["panel"])
        self.footer_text.configure(bg=p["panel"], fg=p["texto_secundario"])
        self.header_kicker.configure(bg=p["fondo"], fg=p["acento"])
        self.header_title.configure(bg=p["fondo"], fg=p["texto"])
        self.header_subtitle.configure(bg=p["fondo"], fg=p["texto_secundario"])
        self.hero.configure(bg=p["panel"], highlightbackground=p["borde"])
        self.hero_inner.configure(bg=p["panel"])
        self.hero_title.configure(bg=p["panel"], fg=p["texto"])
        self.hero_desc.configure(bg=p["panel"], fg=p["texto_secundario"])
        self.section_title.configure(bg=p["fondo"], fg=p["texto"])
        self.cards.configure(bg=p["fondo"])
        self.bottom_note.configure(bg=p["fondo"], fg=p["texto_secundario"])
        for widget, tipo in self._widgets_tema:
            if tipo == "card":
                widget.configure(bg=p["panel"], highlightbackground=p["borde"])
            elif tipo == "panel":
                widget.configure(bg=p["panel"])
            elif tipo == "icon":
                widget.configure(bg=p["panel"], fg=p["acento"])
            elif tipo == "heading":
                widget.configure(bg=p["panel"], fg=p["texto"])
            elif tipo == "muted":
                widget.configure(bg=p["panel"], fg=p["texto_secundario"])
        for btn, activo in self.nav_buttons:
            btn.configure(bg=p["acento"] if activo else p["panel"], fg="#FFFFFF" if activo else p["texto_secundario"],
                          activebackground=p["acento_hover"], activeforeground="#FFFFFF")
        estilo = ttk.Style(self.ventana)
        estilo.configure("SA.TButton", background=p["acento"], foreground="#FFFFFF", bordercolor=p["acento"], font=("Segoe UI", 10, "bold"), padding=(12, 9))
        estilo.map("SA.TButton", background=[("active", p["acento_hover"])], foreground=[("disabled", p["texto_secundario"])])
        estilo.configure("SA.Side.TButton", background=p["panel"], foreground=p["texto"], padding=(12, 10))
        estilo.configure("SA.Small.TButton", background=p["panel_secundario"], foreground=p["texto"], padding=(9, 6))
        estilo.map("SA.Small.TButton", background=[("active", p["borde"])])
        self.tema_btn.configure(text="☾  Cambiar a tema claro" if self.tema_actual == "oscuro" else "☼  Cambiar a tema oscuro")

    def salir(self):
        """Solicita confirmación antes de cerrar la aplicación."""
        if messagebox.askyesno(
            "Salir de SimuladorAutomatas",
            "¿Seguro que deseas cerrar el programa?",
            parent=self.ventana,
        ):
            logger.info("El usuario cerró la aplicación")
            self.ventana.destroy()

    def alternar_tema(self):
        self.tema_actual = "claro" if self.tema_actual == "oscuro" else "oscuro"
        self.aplicar_tema()
        logger.info("Tema visual cambiado a %s", self.tema_actual)

    def mostrar_inicio(self):
        logger.info("Se mostró el panel principal")
        self.aplicar_tema()

    def abrir_afd(self):
        logger.info("Se abrió el módulo de creación de AFD")
        self.ventana.withdraw()
        VentanaAFD(self.ventana)

    def abrir_afn(self):
        logger.info("Se abrió el módulo de creación de AFN")
        self.ventana.withdraw()
        VentanaAFN(self.ventana)

    def abrir_expresiones_regulares(self):
        logger.info("Se abrió el módulo de expresiones regulares")
        self.ventana.withdraw()
        VentanaExpresionesRegulares(self.ventana)

    def abrir_logs(self):
        logger.info("Se solicitó abrir el visor de logs")
        VentanaLogs(self.ventana)

    def abrir_banco_desde_afn(self):
        messagebox.showinfo(
            "Banco automático de pruebas",
            "Para ejecutar el banco de pruebas, abre primero el módulo AFN, crea un autómata y pulsa «Banco de pruebas».",
            parent=self.ventana,
        )

    def ayuda_conversion(self):
        messagebox.showinfo(
            "Conversión y minimización",
            "La conversión AFN → AFD está disponible desde el módulo AFN. La minimización se inicia con un AFD creado o convertido.",
            parent=self.ventana,
        )
