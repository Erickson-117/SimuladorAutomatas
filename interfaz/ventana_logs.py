import logging
import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox

from algoritmos.validador_logs import (
    validar_archivo_logs, NIVELES_LOG, clasificar_nivel_log
)

logger = logging.getLogger(__name__)


class VentanaLogs:
    """Visor de logs con pestañas por nivel y validación del formato."""

    def __init__(self, ventana_padre):
        self.ventana_padre = ventana_padre
        self.ruta_logs = Path(__file__).resolve().parent.parent / "logs.txt"
        self.ventana = tk.Toplevel(ventana_padre)
        self.ventana.title("Visor de logs - Simulador de Autómatas")
        self.ventana.geometry("1050x620")
        self.ventana.minsize(760, 440)
        self.ventana.configure(bg="#f4f6f8")
        self.ventana.transient(ventana_padre)

        self.buscar_var = tk.StringVar()
        self.estado_var = tk.StringVar(value="Listo")
        self.tablas = {}
        self.crear_interfaz()
        self.cargar_logs()
        logger.info("Se abrió el visor de logs")

    def crear_interfaz(self):
        contenedor = ttk.Frame(self.ventana, padding=16)
        contenedor.pack(fill="both", expand=True)

        encabezado = ttk.Frame(contenedor)
        encabezado.pack(fill="x", pady=(0, 12))
        ttk.Label(
            encabezado, text="Visor de logs",
            font=("Segoe UI", 18, "bold")
        ).pack(side="left")
        ttk.Label(
            encabezado, text="Registro de eventos de la aplicación",
            foreground="#667085"
        ).pack(side="left", padx=14, pady=(6, 0))

        controles = ttk.Frame(contenedor)
        controles.pack(fill="x", pady=(0, 10))
        ttk.Label(controles, text="Buscar:").pack(side="left", padx=(0, 6))
        entrada = ttk.Entry(controles, textvariable=self.buscar_var, width=34)
        entrada.pack(side="left", padx=(0, 10))
        entrada.bind("<KeyRelease>", lambda _evento: self.cargar_logs())

        ttk.Button(
            controles, text="Actualizar", command=self.cargar_logs
        ).pack(side="left", padx=4)
        ttk.Button(
            controles, text="Validar formato", command=self.validar_formato
        ).pack(side="left", padx=4)
        ttk.Button(
            controles, text="Ubicación del archivo", command=self.abrir_ubicacion
        ).pack(side="left", padx=4)

        self.notebook = ttk.Notebook(contenedor)
        self.notebook.pack(fill="both", expand=True)

        for nivel in NIVELES_LOG:
            marco = ttk.Frame(self.notebook, padding=6)
            self.notebook.add(marco, text=nivel)
            columnas = ("fecha", "hora", "modulo", "mensaje")
            tabla = ttk.Treeview(marco, columns=columnas, show="headings")
            tabla.heading("fecha", text="Fecha")
            tabla.heading("hora", text="Hora")
            tabla.heading("modulo", text="Módulo")
            tabla.heading("mensaje", text="Mensaje")
            tabla.column("fecha", width=105, anchor="center")
            tabla.column("hora", width=85, anchor="center")
            tabla.column("modulo", width=160)
            tabla.column("mensaje", width=560)
            barra_y = ttk.Scrollbar(marco, orient="vertical", command=tabla.yview)
            barra_x = ttk.Scrollbar(marco, orient="horizontal", command=tabla.xview)
            tabla.configure(yscrollcommand=barra_y.set, xscrollcommand=barra_x.set)
            tabla.grid(row=0, column=0, sticky="nsew")
            barra_y.grid(row=0, column=1, sticky="ns")
            barra_x.grid(row=1, column=0, sticky="ew")
            marco.rowconfigure(0, weight=1)
            marco.columnconfigure(0, weight=1)
            self.tablas[nivel] = tabla

        ttk.Label(
            contenedor, textvariable=self.estado_var, foreground="#667085"
        ).pack(fill="x", pady=(8, 0))

    def cargar_logs(self):
        for tabla in self.tablas.values():
            tabla.delete(*tabla.get_children())

        registros, invalidos = validar_archivo_logs(self.ruta_logs)
        filtro = self.buscar_var.get().strip()
        for registro in registros:
            # Clasificamos el registro mediante los patrones Regex definidos
            # en validador_logs.py. La línea ya pasó la validación de formato.
            nivel = clasificar_nivel_log(registro["linea"])
            if nivel not in self.tablas:
                # No mostrar un registro si no se pudo reconocer su nivel.
                logger.warning(
                    "No se pudo clasificar un registro de log: %s",
                    registro["linea"],
                )
                continue
            texto_busqueda = registro["linea"]
            if filtro and filtro.casefold() not in texto_busqueda.casefold():
                continue
            self.tablas[nivel].insert(
                "", "end",
                values=(
                    registro["fecha"], registro["hora"],
                    registro["modulo"].strip(), registro["mensaje"]
                )
            )

        total = sum(len(tabla.get_children()) for tabla in self.tablas.values())
        self.estado_var.set(
            f"{total} registro(s) mostrado(s) · "
            f"{len(invalidos)} línea(s) con formato inválido · Archivo: {self.ruta_logs.name}"
        )

    def validar_formato(self):
        registros, invalidos = validar_archivo_logs(self.ruta_logs)
        if invalidos:
            detalle = "\\n".join(
                f"Línea {numero}: {error}\\n  {contenido}"
                for numero, contenido, error in invalidos[:12]
            )
            if len(invalidos) > 12:
                detalle += f"\\n... y {len(invalidos) - 12} línea(s) más."
            messagebox.showwarning(
                "Validación de logs",
                f"Registros válidos: {len(registros)}\\n"
                f"Registros inválidos: {len(invalidos)}\\n\\n{detalle}",
                parent=self.ventana,
            )
        else:
            messagebox.showinfo(
                "Validación de logs",
                f"Formato correcto. Se encontraron {len(registros)} registro(s) válido(s).",
                parent=self.ventana,
            )
        logger.info(
            "Validación del archivo de logs completada: %s válidos, %s inválidos",
            len(registros), len(invalidos)
        )

    def abrir_ubicacion(self):
        # Se muestra la ruta completa sin depender del sistema operativo.
        messagebox.showinfo(
            "Ubicación del archivo",
            f"Los logs se guardan en:\\n{self.ruta_logs}",
            parent=self.ventana,
        )
