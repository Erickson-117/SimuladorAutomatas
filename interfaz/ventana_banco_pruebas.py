import tkinter as tk
from tkinter import ttk, messagebox

from algoritmos.banco_pruebas import ejecutar_banco_pruebas


class VentanaBancoPruebas:
    """Interfaz para ejecutar un banco exhaustivo de cadenas de longitud acotada."""

    def __init__(self, ventana_padre, afn):
        self.afn = afn
        self.ventana = tk.Toplevel(ventana_padre)
        self.ventana.title("Banco automático de pruebas")
        self.ventana.geometry("1050x680")
        self.ventana.minsize(800, 500)
        self.ventana.configure(bg="#f4f6f8")

        estilo = ttk.Style(self.ventana)
        estilo.configure("Banco.TLabel", background="#f4f6f8", font=("Segoe UI", 10))
        estilo.configure("BancoTitulo.TLabel", background="#f4f6f8", foreground="#17202a", font=("Segoe UI", 18, "bold"))
        estilo.configure("Banco.TButton", font=("Segoe UI", 10, "bold"), padding=(12, 7))

        contenedor = ttk.Frame(self.ventana, padding=18)
        contenedor.pack(fill="both", expand=True)
        ttk.Label(contenedor, text="Banco automático de pruebas", style="BancoTitulo.TLabel").pack(anchor="w")
        ttk.Label(
            contenedor,
            text="Compara el AFN original, su AFD convertido y el AFD mínimo con todas las cadenas hasta la longitud elegida.",
            style="Banco.TLabel", wraplength=950,
        ).pack(anchor="w", pady=(5, 14))

        controles = ttk.Frame(contenedor)
        controles.pack(fill="x", pady=(0, 14))
        ttk.Label(controles, text=f"Alfabeto: {{{', '.join(sorted(self.afn.alfabeto))}}}").pack(side="left", padx=(0, 18))
        ttk.Label(controles, text="Longitud máxima:").pack(side="left")
        self.longitud = tk.IntVar(value=3)
        ttk.Spinbox(controles, from_=0, to=8, width=5, textvariable=self.longitud).pack(side="left", padx=8)
        self.incluir_vacia = tk.BooleanVar(value=True)
        ttk.Checkbutton(controles, text="Incluir cadena vacía (ε)", variable=self.incluir_vacia).pack(side="left", padx=8)
        ttk.Button(controles, text="Ejecutar pruebas", style="Banco.TButton", command=self.ejecutar).pack(side="right")

        self.resumen = ttk.Label(
            contenedor, text="Configura las pruebas y pulsa «Ejecutar pruebas».",
            style="Banco.TLabel", wraplength=980,
        )
        self.resumen.pack(anchor="w", fill="x", pady=(0, 12))

        tabla_frame = ttk.Frame(contenedor)
        tabla_frame.pack(fill="both", expand=True)
        columnas = ("cadena", "afn", "afd", "minimo", "estado")
        self.tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=16)
        encabezados = {
            "cadena": ("Cadena", 200), "afn": ("AFN", 130), "afd": ("AFD", 130),
            "minimo": ("AFD mínimo", 150), "estado": ("Comparación", 170),
        }
        for columna, (titulo, ancho) in encabezados.items():
            self.tabla.heading(columna, text=titulo)
            self.tabla.column(columna, width=ancho, minwidth=90, anchor="center", stretch=(columna == "cadena"))
        self.tabla.tag_configure("coincide", foreground="#176b3a")
        self.tabla.tag_configure("discrepancia", foreground="#b42318")
        barra = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=barra.set)
        self.tabla.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")

        separador = ttk.Separator(contenedor, orient="horizontal")
        separador.pack(fill="x", pady=(10, 8))
        self.nota = ttk.Label(
            contenedor,
            text="Nota: una ejecución sin discrepancias confirma la concordancia para estas cadenas, no constituye una demostración formal para todas las cadenas posibles.",
            style="Banco.TLabel", wraplength=950,
        )
        self.nota.pack(anchor="w", pady=(10, 0))
        from interfaz.tema import registrar_ventana
        registrar_ventana(self.ventana)

    @staticmethod
    def texto_resultado(aceptada):
        return "Aceptada" if aceptada else "Rechazada"

    def ejecutar(self):
        try:
            longitud = self.longitud.get()
            if longitud < 0 or longitud > 8:
                raise ValueError("Elige una longitud entre 0 y 8 para mantener el tiempo de ejecución razonable.")
            resultado = ejecutar_banco_pruebas(self.afn, longitud, self.incluir_vacia.get())
        except (ValueError, tk.TclError) as error:
            messagebox.showerror("No se pudieron ejecutar las pruebas", str(error), parent=self.ventana)
            return
        except Exception as error:
            messagebox.showerror("Error al ejecutar el banco", f"Ocurrió un error inesperado:\n{error}", parent=self.ventana)
            return

        for elemento in self.tabla.get_children():
            self.tabla.delete(elemento)
        for fila in resultado["resultados"]:
            cadena = "ε (vacía)" if fila["cadena"] == "" else fila["cadena"]
            coincide = fila["coincide"]
            self.tabla.insert("", "end", values=(
                cadena,
                self.texto_resultado(fila["afn"]),
                self.texto_resultado(fila["afd"]),
                self.texto_resultado(fila["afd_minimo"]),
                "Coinciden" if coincide else "¡DISCREPANCIA!",
            ), tags=("coincide" if coincide else "discrepancia",))

        resumen = resultado["resumen"]
        estado = "Todos los resultados coinciden" if resumen["equivalencia_observada"] else "Se encontraron discrepancias"
        self.resumen.configure(text=(
            f"{estado} · {resumen['coincidentes']}/{resumen['total']} cadenas coincidentes · "
            f"{resumen['discrepancias']} discrepancias · Longitud máxima: {longitud}"
        ))
