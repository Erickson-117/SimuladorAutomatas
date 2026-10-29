import tkinter as tk
from tkinter import ttk, messagebox

from algoritmos.expresiones_regulares import (
    compilar_expresion, validar_cadena, generar_afn_thompson
)
from interfaz.visualizador import Visualizador


class VentanaExpresionesRegulares:
    """Ventana para probar expresiones regulares contra cadenas completas."""

    def __init__(self, ventana_padre):
        self.ventana = tk.Toplevel(ventana_padre)
        self.ventana.title("Expresiones regulares")
        self.ventana.attributes("-fullscreen", True)
        self.ventana.protocol("WM_DELETE_WINDOW", self.regresar_a_principal)
        self.ventana.bind("<Escape>", lambda _evento: self.regresar_a_principal())
        self.raiz = ventana_padre
        self.configurar_estilos()
        self.crear_interfaz()

    def configurar_estilos(self):
        estilo = ttk.Style()
        try:
            estilo.theme_use("clam")
        except tk.TclError:
            pass
        estilo.configure("Regex.Fondo.TFrame", background="#f4f6f8")
        estilo.configure("Regex.Panel.TFrame", background="white")
        estilo.configure("Regex.Titulo.TLabel", background="#f4f6f8", foreground="#17202a", font=("Segoe UI", 22, "bold"))
        estilo.configure("Regex.Subtitulo.TLabel", background="#f4f6f8", foreground="#68737d", font=("Segoe UI", 11))
        estilo.configure("Regex.Seccion.TLabel", background="white", foreground="#17202a", font=("Segoe UI", 13, "bold"))
        estilo.configure("Regex.TButton", font=("Segoe UI", 10, "bold"), padding=(16, 10))
        estilo.configure("Regex.TEntry", padding=8, font=("Consolas", 12))

    def crear_interfaz(self):
        principal = ttk.Frame(self.ventana, style="Regex.Fondo.TFrame", padding=24)
        principal.pack(fill="both", expand=True)

        barra = ttk.Frame(principal, style="Regex.Fondo.TFrame")
        barra.pack(fill="x", pady=(0, 12))
        ttk.Button(barra, text="← Pantalla principal", command=self.regresar_a_principal).pack(side="left")
        ttk.Button(barra, text="Salir del programa", command=self.salir_del_programa).pack(side="right")

        ttk.Label(principal, text="Expresiones regulares", style="Regex.Titulo.TLabel").pack(anchor="w")
        ttk.Label(
            principal,
            text="Escribe una expresión regular y comprueba si una cadena completa pertenece al lenguaje.",
            style="Regex.Subtitulo.TLabel",
        ).pack(anchor="w", pady=(4, 18))

        panel = ttk.Frame(principal, style="Regex.Panel.TFrame", padding=28)
        panel.pack(fill="both", expand=True)

        ttk.Label(panel, text="1. Expresión regular", style="Regex.Seccion.TLabel").pack(anchor="w")
        ttk.Label(
            panel,
            text="Para generar el AFN se admite: símbolos, unión |, concatenación, cerradura * y paréntesis. La prueba de cadenas usa la sintaxis de Python.",
            wraplength=1100,
        ).pack(anchor="w", pady=(6, 10))

        self.expresion_var = tk.StringVar(value="(0|1)*01")
        fila_expresion = ttk.Frame(panel, style="Regex.Panel.TFrame")
        fila_expresion.pack(fill="x")
        self.entrada_expresion = ttk.Entry(fila_expresion, textvariable=self.expresion_var, style="Regex.TEntry")
        self.entrada_expresion.pack(side="left", fill="x", expand=True, padx=(0, 12))
        ttk.Button(fila_expresion, text="Validar expresión", style="Regex.TButton", command=self.validar_expresion).pack(side="left")
        ttk.Button(
            fila_expresion, text="Generar AFN", style="Regex.TButton",
            command=self.generar_afn
        ).pack(side="left", padx=(8, 0))

        ttk.Label(panel, text="Ejemplos:  (0|1)*01   ·   a+b*   ·   [0-9]{2,4}", foreground="#68737d").pack(anchor="w", pady=(7, 20))

        ttk.Separator(panel).pack(fill="x", pady=(0, 20))
        ttk.Label(panel, text="2. Cadena de prueba", style="Regex.Seccion.TLabel").pack(anchor="w")
        fila_cadena = ttk.Frame(panel, style="Regex.Panel.TFrame")
        fila_cadena.pack(fill="x", pady=(10, 0))
        self.cadena_var = tk.StringVar(value="1101")
        self.entrada_cadena = ttk.Entry(fila_cadena, textvariable=self.cadena_var, style="Regex.TEntry")
        self.entrada_cadena.pack(side="left", fill="x", expand=True, padx=(0, 12))
        self.entrada_cadena.bind("<Return>", lambda _evento: self.probar_cadena())
        ttk.Button(fila_cadena, text="Probar cadena", style="Regex.TButton", command=self.probar_cadena).pack(side="left")

        self.resultado = ttk.Label(panel, text="Ingresa una expresión y prueba una cadena.", font=("Segoe UI", 13, "bold"), background="#f4f6f8", padding=16)
        self.resultado.pack(fill="x", pady=(20, 12))

        ttk.Label(panel, text="Cómo interpretar los resultados", style="Regex.Seccion.TLabel").pack(anchor="w", pady=(8, 6))
        ttk.Label(
            panel,
            text=(
                "• ACEPTADA: la cadena completa coincide con la expresión.\n"
                "• RECHAZADA: la cadena no coincide completamente.\n"
                "• Error de sintaxis: la expresión necesita corregirse antes de probar cadenas.\n\n"
                "Nota: la generación de AFN usa el algoritmo de Thompson y admite símbolos de un carácter, |, concatenación, *, y paréntesis."
            ),
            justify="left",
            wraplength=1200,
        ).pack(anchor="w")

    def validar_expresion(self):
        try:
            compilar_expresion(self.expresion_var.get())
        except ValueError as error:
            self.resultado.config(text=f"✗ {error}", foreground="#b42318")
            return False
        self.resultado.config(text="✓ Expresión regular válida. Ya puedes probar cadenas.", foreground="#087f5b")
        return True

    def probar_cadena(self):
        expresion = self.expresion_var.get()
        cadena = self.cadena_var.get()
        try:
            aceptada = validar_cadena(expresion, cadena)
        except ValueError as error:
            self.resultado.config(text=f"✗ {error}", foreground="#b42318")
            return
        if aceptada:
            self.resultado.config(text=f"✓ CADENA ACEPTADA: «{cadena}» coincide con la expresión.", foreground="#087f5b")
        else:
            self.resultado.config(text=f"✗ CADENA RECHAZADA: «{cadena}» no coincide con la expresión.", foreground="#b42318")


    def generar_afn(self):
        expresion = self.expresion_var.get()
        try:
            afn = generar_afn_thompson(expresion)
        except ValueError as error:
            self.resultado.config(text=f"✗ No se pudo generar el AFN: {error}", foreground="#b42318")
            return

        visor = Visualizador(self.ventana)
        visor.ventana.title(f"AFN generado por Thompson: {expresion}")
        # Mostrar primero la ventana para que el canvas tenga dimensiones
        # reales antes de calcular la distribución de los estados.
        visor.ventana.update_idletasks()
        visor.ventana.update()
        visor.dibujar_automata(
            afn.estados,
            afn.transiciones,
            afn.estado_inicial,
            afn.estados_finales,
        )
        self.resultado.config(
            text=f"✓ AFN generado: {len(afn.estados)} estados, alfabeto {sorted(afn.alfabeto)}.",
            foreground="#087f5b",
        )

    def regresar_a_principal(self):
        self.ventana.destroy()
        try:
            self.raiz.deiconify()
            self.raiz.attributes("-fullscreen", True)
            self.raiz.lift()
        except tk.TclError:
            pass

    def salir_del_programa(self):
        try:
            self.raiz.destroy()
        except tk.TclError:
            self.ventana.destroy()
