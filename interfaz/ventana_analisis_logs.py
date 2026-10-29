"""Ventana gráfica para interpretar advertencias y errores del archivo de logs."""
from __future__ import annotations

import logging
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

from algoritmos.analizador_logs import analizar_registros, resumir_diagnosticos
from algoritmos.validador_logs import validar_archivo_logs

logger = logging.getLogger(__name__)


class VentanaAnalisisLogs:
    """Presenta diagnósticos basados en reglas, sin modificar logs.txt."""

    def __init__(self, ventana_padre, ruta_logs=None):
        self.ventana_padre = ventana_padre
        self.ruta_logs = Path(ruta_logs) if ruta_logs else Path(__file__).resolve().parent.parent / "logs.txt"
        self.diagnosticos = []
        self.diagnosticos_visibles = []
        self.ventana = tk.Toplevel(ventana_padre)
        self.ventana.title("Análisis de logs - Simulador de Autómatas")
        self.ventana.geometry("1180x720")
        self.ventana.minsize(850, 560)
        self.ventana.configure(bg="#f4f6f8")
        self.ventana.transient(ventana_padre)
        self.filtro_nivel = tk.StringVar(value="Todos")
        self.buscar_var = tk.StringVar()
        self.estado_var = tk.StringVar(value="Preparado para analizar los registros")
        self._crear_interfaz()
        self.analizar()

    def _crear_interfaz(self):
        contenedor = ttk.Frame(self.ventana, padding=16)
        contenedor.pack(fill="both", expand=True)
        encabezado = ttk.Frame(contenedor)
        encabezado.pack(fill="x", pady=(0, 12))
        ttk.Label(encabezado, text="Análisis inteligente de logs", font=("Segoe UI", 18, "bold")).pack(side="left")
        ttk.Label(encabezado, text="", foreground="#667085").pack(side="left", padx=14, pady=(6, 0))

        resumen = ttk.Frame(contenedor)
        resumen.pack(fill="x", pady=(0, 12))
        self.lbl_total = ttk.Label(resumen, text="Incidencias: 0", font=("Segoe UI", 11, "bold"))
        self.lbl_total.pack(side="left", padx=(0, 20))
        self.lbl_errores = ttk.Label(resumen, text="Errores: 0", foreground="#c0392b", font=("Segoe UI", 11, "bold"))
        self.lbl_errores.pack(side="left", padx=(0, 20))
        self.lbl_advertencias = ttk.Label(resumen, text="Advertencias: 0", foreground="#b9770e", font=("Segoe UI", 11, "bold"))
        self.lbl_advertencias.pack(side="left", padx=(0, 20))
        self.lbl_sin_regla = ttk.Label(resumen, text="Sin regla específica: 0", foreground="#667085")
        self.lbl_sin_regla.pack(side="left")

        controles = ttk.Frame(contenedor)
        controles.pack(fill="x", pady=(0, 10))
        ttk.Label(controles, text="Nivel:").pack(side="left", padx=(0, 6))
        nivel = ttk.Combobox(controles, textvariable=self.filtro_nivel, values=("Todos", "WARNING", "ERROR", "CRITICAL"), state="readonly", width=14)
        nivel.pack(side="left", padx=(0, 12))
        nivel.bind("<<ComboboxSelected>>", lambda _e: self._aplicar_filtros())
        ttk.Label(controles, text="Buscar:").pack(side="left", padx=(0, 6))
        entrada = ttk.Entry(controles, textvariable=self.buscar_var, width=34)
        entrada.pack(side="left", padx=(0, 10))
        entrada.bind("<KeyRelease>", lambda _e: self._aplicar_filtros())
        ttk.Button(controles, text="Analizar / actualizar", command=self.analizar).pack(side="left", padx=4)

        panel = ttk.Panedwindow(contenedor, orient="vertical")
        panel.pack(fill="both", expand=True)
        lista = ttk.Frame(panel, padding=(0, 0, 0, 8))
        detalle = ttk.LabelFrame(panel, text="Diagnóstico de la incidencia seleccionada", padding=12)
        panel.add(lista, weight=3)
        panel.add(detalle, weight=2)
        columnas = ("nivel", "fecha", "hora", "modulo", "titulo", "coincidencia")
        self.tabla = ttk.Treeview(lista, columns=columnas, show="headings", selectmode="browse")
        titulos = {"nivel":"Nivel", "fecha":"Fecha", "hora":"Hora", "modulo":"Módulo", "titulo":"Interpretación", "coincidencia":"Tipo de regla"}
        anchos = {"nivel":90, "fecha":100, "hora":80, "modulo":180, "titulo":330, "coincidencia":125}
        for col in columnas:
            self.tabla.heading(col, text=titulos[col])
            self.tabla.column(col, width=anchos[col], minwidth=65, stretch=(col in {"modulo", "titulo"}))
        sy = ttk.Scrollbar(lista, orient="vertical", command=self.tabla.yview)
        sx = ttk.Scrollbar(lista, orient="horizontal", command=self.tabla.xview)
        self.tabla.configure(yscrollcommand=sy.set, xscrollcommand=sx.set)
        self.tabla.grid(row=0, column=0, sticky="nsew")
        sy.grid(row=0, column=1, sticky="ns")
        sx.grid(row=1, column=0, sticky="ew")
        lista.rowconfigure(0, weight=1); lista.columnconfigure(0, weight=1)
        self.tabla.bind("<<TreeviewSelect>>", self._mostrar_detalle)
        self.tabla.tag_configure("ERROR", foreground="#c0392b")
        self.tabla.tag_configure("CRITICAL", foreground="#922b21")
        self.tabla.tag_configure("WARNING", foreground="#b9770e")

        self.lbl_titulo = ttk.Label(detalle, text="Selecciona una incidencia para ver el diagnóstico.", font=("Segoe UI", 12, "bold"), wraplength=1050)
        self.lbl_titulo.pack(anchor="w", fill="x", pady=(0, 8))
        self.lbl_meta = ttk.Label(detalle, text="", foreground="#667085", wraplength=1050)
        self.lbl_meta.pack(anchor="w", fill="x", pady=(0, 8))
        self.texto_detalle = tk.Text(detalle, height=10, wrap="word", font=("Segoe UI", 10), relief="flat", bg="#ffffff", padx=10, pady=8)
        self.texto_detalle.pack(fill="both", expand=True)
        self.texto_detalle.configure(state="disabled")
        ttk.Label(contenedor, textvariable=self.estado_var, foreground="#667085").pack(fill="x", pady=(8, 0))

    def analizar(self):
        registros, invalidos = validar_archivo_logs(self.ruta_logs)
        self.diagnosticos = analizar_registros(registros)
        resumen = resumir_diagnosticos(self.diagnosticos)
        niveles = resumen["por_nivel"]
        self.lbl_total.configure(text=f"Incidencias: {resumen['total']}")
        self.lbl_errores.configure(text=f"Errores: {niveles.get('ERROR', 0) + niveles.get('CRITICAL', 0)}")
        self.lbl_advertencias.configure(text=f"Advertencias: {niveles.get('WARNING', 0)}")
        self.lbl_sin_regla.configure(text=f"Sin regla específica: {resumen['sin_regla_especifica']}")
        self._aplicar_filtros()
        self.estado_var.set(f"Análisis completado · {len(registros)} registros válidos · {len(invalidos)} líneas inválidas · Archivo: {self.ruta_logs.name}")
        logger.info("Análisis de logs completado: %s incidencias", len(self.diagnosticos))
        if not registros and not self.ruta_logs.exists():
            messagebox.showwarning("Archivo de logs no encontrado", f"No se encontró el archivo:\n{self.ruta_logs}", parent=self.ventana)

    def _aplicar_filtros(self):
        filtro_nivel = self.filtro_nivel.get()
        busqueda = self.buscar_var.get().strip().casefold()
        self.diagnosticos_visibles = []
        self.tabla.delete(*self.tabla.get_children())
        for diagnostico in self.diagnosticos:
            if filtro_nivel != "Todos" and diagnostico.get("nivel") != filtro_nivel:
                continue
            cadena = " ".join(str(diagnostico.get(c, "")) for c in ("nivel", "fecha", "hora", "modulo", "titulo", "mensaje_original", "solucion")).casefold()
            if busqueda and busqueda not in cadena:
                continue
            self.diagnosticos_visibles.append(diagnostico)
            coincidencia = "Regla conocida" if diagnostico.get("coincidencia") == "regla_conocida" else "Genérica"
            self.tabla.insert("", "end", iid=str(len(self.diagnosticos_visibles)-1), values=(diagnostico.get("nivel", ""), diagnostico.get("fecha", ""), diagnostico.get("hora", ""), diagnostico.get("modulo", ""), diagnostico.get("titulo", ""), coincidencia), tags=(diagnostico.get("nivel", ""),))
        hijos = self.tabla.get_children()
        if hijos:
            self.tabla.selection_set(hijos[0])
            self._mostrar_detalle()
        else:
            self.lbl_titulo.configure(text="No hay incidencias que coincidan con el filtro.")
            self.lbl_meta.configure(text="")
            self._escribir_detalle("")
        self.estado_var.set(f"Mostrando {len(self.diagnosticos_visibles)} de {len(self.diagnosticos)} incidencias")

    def _mostrar_detalle(self, _evento=None):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        try:
            diagnostico = self.diagnosticos_visibles[int(seleccion[0])]
        except (ValueError, IndexError):
            return
        self.lbl_titulo.configure(text=f"{diagnostico['nivel']} · {diagnostico['titulo']}")
        self.lbl_meta.configure(text=f"{diagnostico.get('fecha', '')} {diagnostico.get('hora', '')}  |  Módulo: {diagnostico.get('modulo', '')}  |  Clasificación: {'regla conocida' if diagnostico.get('coincidencia') == 'regla_conocida' else 'regla genérica'}")
        contenido = (
            f"MENSAJE ORIGINAL\n{diagnostico.get('mensaje_original', '')}\n\n"
            f"¿QUÉ SIGNIFICA?\n{diagnostico.get('interpretacion', '')}\n\n"
            f"CAUSA PROBABLE\n{diagnostico.get('causa_probable', '')}\n\n"
            f"IMPACTO\n{diagnostico.get('impacto', '')}\n\n"
            f"SOLUCIÓN RECOMENDADA\n{diagnostico.get('solucion', '')}"
        )
        self._escribir_detalle(contenido)

    def _escribir_detalle(self, contenido):
        self.texto_detalle.configure(state="normal")
        self.texto_detalle.delete("1.0", "end")
        self.texto_detalle.insert("1.0", contenido)
        self.texto_detalle.configure(state="disabled")
