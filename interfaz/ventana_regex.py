import tkinter as tk
from tkinter import ttk, messagebox

from algoritmos.expresiones_regulares import (
    compilar_expresion, validar_cadena, generar_afn_thompson
)
from interfaz.visualizador import Visualizador
from algoritmos.conversion import convertir_afn_a_afd
from algoritmos.minimizacion import minimizar_afd
from interfaz.ventana_minimizacion import VentanaMinimizacion


class VentanaExpresionesRegulares:
    """Ventana para probar expresiones regulares contra cadenas completas."""

    def __init__(self, ventana_padre):
        self.ventana = tk.Toplevel(ventana_padre)
        self.ventana.title("Expresiones regulares")
        self.ventana.attributes("-fullscreen", True)
        self.ventana.protocol("WM_DELETE_WINDOW", self.regresar_a_principal)
        self.ventana.bind("<Escape>", lambda _evento: self.regresar_a_principal())
        self.raiz = ventana_padre
        self.ultimo_afn = None
        self.ultimo_afd = None
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
        ttk.Button(
            fila_expresion, text="Convertir a AFD", style="Regex.TButton",
            command=self.convertir_a_afd
        ).pack(side="left", padx=(8, 0))
        ttk.Button(
            fila_expresion, text="Minimizar AFD", style="Regex.TButton",
            command=self.minimizar_afd
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
        ttk.Button(
            fila_cadena,
            text="Comparar AFN, AFD y mínimo",
            style="Regex.TButton",
            command=self.comparar_automatas,
        ).pack(side="left", padx=(8, 0))

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


    def comparar_automatas(self):
        """Simula una cadena en el AFN, el AFD y el AFD minimizado.

        Presenta un resumen visual y separa cada recorrido en una pestaña.
        """
        expresion = self.expresion_var.get().strip()
        cadena = self.cadena_var.get()

        try:
            afn = generar_afn_thompson(expresion)
            afd = convertir_afn_a_afd(afn)
            afd_minimo, _pasos = minimizar_afd(afd)

            recorrido_afn, acepta_afn = afn.obtener_recorrido(cadena)
            recorrido_afd, acepta_afd = afd.obtener_recorrido(cadena)
            recorrido_minimo, acepta_minimo = afd_minimo.obtener_recorrido(cadena)
        except (ValueError, TypeError, KeyError) as error:
            self.resultado.config(
                text=f"✗ No se pudo comparar los autómatas: {error}",
                foreground="#b42318",
            )
            return

        coinciden = acepta_afn == acepta_afd == acepta_minimo
        estado = "✓ Los tres autómatas coinciden." if coinciden else "⚠ Hay resultados diferentes."
        color = "#087f5b" if coinciden else "#b42318"
        self.resultado.config(
            text=(
                f"{estado} Cadena «{cadena}»: "
                f"AFN={'ACEPTADA' if acepta_afn else 'RECHAZADA'}, "
                f"AFD={'ACEPTADA' if acepta_afd else 'RECHAZADA'}, "
                f"AFD mínimo={'ACEPTADA' if acepta_minimo else 'RECHAZADA'}."
            ),
            foreground=color,
        )

        ventana = tk.Toplevel(self.ventana)
        ventana.title("Comparación de simulación de autómatas")
        ventana.geometry("1050x760")
        ventana.minsize(780, 560)
        ventana.configure(bg="#f4f6f8")

        estilo = ttk.Style(ventana)
        try:
            estilo.theme_use("clam")
        except tk.TclError:
            pass
        estilo.configure("Comparacion.TFrame", background="#f4f6f8")
        estilo.configure("Comparacion.TLabel", background="#f4f6f8", foreground="#17202a")
        estilo.configure("Comparacion.Titulo.TLabel", background="#f4f6f8", foreground="#17202a", font=("Segoe UI", 17, "bold"))
        estilo.configure("Comparacion.Subtitulo.TLabel", background="#f4f6f8", foreground="#586574", font=("Segoe UI", 10))
        estilo.configure("Comparacion.TNotebook", padding=5)
        estilo.configure("Comparacion.TNotebook.Tab", padding=(18, 9), font=("Segoe UI", 10, "bold"))

        contenedor = ttk.Frame(ventana, style="Comparacion.TFrame", padding=18)
        contenedor.pack(fill="both", expand=True)

        ttk.Label(
            contenedor,
            text="Comparación de autómatas",
            style="Comparacion.Titulo.TLabel",
        ).pack(anchor="w")
        ttk.Label(
            contenedor,
            text=f"Expresión regular:  {expresion}     |     Cadena evaluada:  {cadena!r}",
            style="Comparacion.Subtitulo.TLabel",
        ).pack(anchor="w", pady=(4, 14))

        # Resumen en tres tarjetas para distinguir rápidamente cada resultado.
        tarjetas = ttk.Frame(contenedor, style="Comparacion.TFrame")
        tarjetas.pack(fill="x", pady=(0, 12))
        resultados = (
            ("AFN", acepta_afn),
            ("AFD", acepta_afd),
            ("AFD mínimo", acepta_minimo),
        )
        for columna, (nombre, aceptada) in enumerate(resultados):
            tarjetas.columnconfigure(columna, weight=1, uniform="resultado")
            tarjeta = tk.Frame(
                tarjetas,
                bg="white",
                highlightbackground="#d7dee7",
                highlightthickness=1,
                padx=14,
                pady=12,
            )
            tarjeta.grid(row=0, column=columna, sticky="nsew", padx=(0 if columna == 0 else 6, 6 if columna < 2 else 0))
            tk.Label(
                tarjeta, text=nombre, bg="white", fg="#344054",
                font=("Segoe UI", 10, "bold"),
            ).pack(anchor="w")
            tk.Label(
                tarjeta,
                text="✓ ACEPTADA" if aceptada else "✗ RECHAZADA",
                bg="white", fg="#087f5b" if aceptada else "#b42318",
                font=("Segoe UI", 13, "bold"),
            ).pack(anchor="w", pady=(5, 0))

        estado_texto = (
            "VERIFICACIÓN CORRECTA · Los tres autómatas dieron el mismo resultado."
            if coinciden else
            "ATENCIÓN · Los resultados no coinciden. Revisa la conversión y la minimización."
        )
        aviso = tk.Frame(
            contenedor,
            bg="#e8f6ef" if coinciden else "#fff0ef",
            padx=12,
            pady=10,
        )
        aviso.pack(fill="x", pady=(0, 12))
        tk.Label(
            aviso,
            text=estado_texto,
            bg="#e8f6ef" if coinciden else "#fff0ef",
            fg="#087f5b" if coinciden else "#b42318",
            font=("Segoe UI", 10, "bold"),
            anchor="w",
            justify="left",
            wraplength=950,
        ).pack(fill="x")

        ttk.Label(
            contenedor,
            text="Recorridos de la simulación",
            style="Comparacion.TLabel",
            font=("Segoe UI", 11, "bold"),
        ).pack(anchor="w", pady=(0, 6))

        pestañas = ttk.Notebook(contenedor, style="Comparacion.TNotebook")
        pestañas.pack(fill="both", expand=True)
        secciones = (
            ("AFN", recorrido_afn, acepta_afn),
            ("AFD", recorrido_afd, acepta_afd),
            ("AFD mínimo", recorrido_minimo, acepta_minimo),
        )
        for titulo, recorrido, aceptada in secciones:
            pagina = ttk.Frame(pestañas, padding=8)
            pestañas.add(pagina, text=titulo)
            pagina.rowconfigure(0, weight=1)
            pagina.columnconfigure(0, weight=1)

            texto = tk.Text(
                pagina,
                wrap="word",
                font=("Consolas", 10),
                bg="white",
                fg="#202938",
                relief="flat",
                padx=14,
                pady=12,
                spacing1=2,
                spacing3=5,
                state="normal",
            )
            barra_scroll = ttk.Scrollbar(pagina, orient="vertical", command=texto.yview)
            texto.configure(yscrollcommand=barra_scroll.set)
            texto.grid(row=0, column=0, sticky="nsew")
            barra_scroll.grid(row=0, column=1, sticky="ns")
            texto.tag_configure("titulo", font=("Segoe UI", 11, "bold"), foreground="#175cd3", spacing3=8)
            texto.tag_configure("resultado_ok", font=("Consolas", 10, "bold"), foreground="#087f5b")
            texto.tag_configure("resultado_error", font=("Consolas", 10, "bold"), foreground="#b42318")

            texto.insert(tk.END, f"RECORRIDO DEL {titulo.upper()}\n", "titulo")
            texto.insert(tk.END, "─" * 42 + "\n\n")
            for numero, paso in enumerate(recorrido, start=1):
                texto.insert(tk.END, f"{numero:02d}.  {paso}\n")
            texto.insert(tk.END, "\n")
            texto.insert(
                tk.END,
                f"RESULTADO FINAL: {'ACEPTADA' if aceptada else 'RECHAZADA'}",
                "resultado_ok" if aceptada else "resultado_error",
            )
            texto.configure(state="disabled")

        pie = ttk.Frame(contenedor, style="Comparacion.TFrame")
        pie.pack(fill="x", pady=(10, 0))
        ttk.Button(pie, text="Cerrar", command=ventana.destroy).pack(side="right")

    def generar_afn(self):
        expresion = self.expresion_var.get()
        try:
            afn = generar_afn_thompson(expresion)
        except ValueError as error:
            self.resultado.config(text=f"✗ No se pudo generar el AFN: {error}", foreground="#b42318")
            return

        self.ultimo_afn = afn
        self.ultimo_afd = None
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


    def convertir_a_afd(self):
        """Genera el AFN actual si hace falta y lo convierte a AFD."""
        expresion = self.expresion_var.get()
        try:
            # Siempre construir desde la expresión actual para evitar convertir
            # por accidente un AFN generado con una expresión anterior.
            afn = generar_afn_thompson(expresion)
            afd = convertir_afn_a_afd(afn)
        except (ValueError, TypeError) as error:
            self.resultado.config(
                text=f"✗ No se pudo convertir a AFD: {error}",
                foreground="#b42318",
            )
            return
        self.ultimo_afn = afn
        self.ultimo_afd = afd
        visor = Visualizador(self.ventana)
        visor.ventana.title(f"AFD convertido desde expresión: {expresion}")
        visor.ventana.update_idletasks()
        visor.ventana.update()
        visor.dibujar_automata(
            afd.estados, afd.transiciones, afd.estado_inicial, afd.estados_finales
        )
        self.resultado.config(
            text=(f"✓ AFD generado: {len(afd.estados)} estados, "
                  f"alfabeto {sorted(afd.alfabeto)}."),
            foreground="#087f5b",
        )

    def minimizar_afd(self):
        """Convierte la expresión actual a AFD y abre la minimización paso a paso."""
        expresion = self.expresion_var.get()
        try:
            afn = generar_afn_thompson(expresion)
            afd = convertir_afn_a_afd(afn)
        except (ValueError, TypeError) as error:
            self.resultado.config(
                text=f"✗ No se pudo preparar el AFD para minimizar: {error}",
                foreground="#b42318",
            )
            return
        self.ultimo_afn = afn
        self.ultimo_afd = afd
        self.resultado.config(
            text=(f"✓ AFD preparado para minimización: {len(afd.estados)} estados."),
            foreground="#087f5b",
        )
        try:
            VentanaMinimizacion(self.ventana, afd)
        except (ValueError, TypeError) as error:
            self.resultado.config(
                text=f"✗ No se pudo minimizar el AFD: {error}",
                foreground="#b42318",
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
