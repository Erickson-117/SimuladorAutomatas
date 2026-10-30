"""Sistema visual compartido y temas globales para SimuladorAutomatas."""
from __future__ import annotations
import tkinter as tk
from tkinter import ttk

PALETAS = {
    "oscuro": {
        "fondo": "#17191F", "panel": "#22252D", "panel_secundario": "#2B303B",
        "borde": "#363B46", "texto": "#F3F4F6", "texto_secundario": "#A1A1AA",
        "acento": "#367BF5", "acento_hover": "#2563EB", "correcto": "#22C55E",
        "advertencia": "#F59E0B", "error": "#EF4444", "entrada": "#191C23",
        "seleccion": "#294A80", "texto_seleccion": "#FFFFFF",
    },
    "claro": {
        "fondo": "#F3F5F9", "panel": "#FFFFFF", "panel_secundario": "#F8FAFC",
        "borde": "#DDE3EC", "texto": "#172033", "texto_secundario": "#64748B",
        "acento": "#2563EB", "acento_hover": "#1D4ED8", "correcto": "#15803D",
        "advertencia": "#B45309", "error": "#B91C1C", "entrada": "#FFFFFF",
        "seleccion": "#DCEAFE", "texto_seleccion": "#172033",
    },
}
_TEMA_ACTUAL = "oscuro"
_VENTANAS = []


def obtener_paleta(tema=None):
    """Devuelve una copia de la paleta actual o de la solicitada."""
    return PALETAS.get(tema or _TEMA_ACTUAL, PALETAS["oscuro"]).copy()


def obtener_tema_actual():
    return _TEMA_ACTUAL


def registrar_ventana(ventana):
    """Registra una raíz Tk/Toplevel para que el cambio de tema sea global."""
    global _VENTANAS
    _VENTANAS = [w for w in _VENTANAS if _existe(w)]
    if not any(w is ventana for w in _VENTANAS):
        _VENTANAS.append(ventana)
    aplicar_tema_ventana(ventana, _TEMA_ACTUAL)


def _existe(widget):
    try:
        return bool(widget.winfo_exists())
    except (tk.TclError, AttributeError):
        return False


def _configurar_estilos(root, p):
    """Configura estilos ttk estándar y los estilos con nombre del proyecto."""
    try:
        estilo = ttk.Style(root)
        try:
            estilo.theme_use("clam")
        except tk.TclError:
            pass

        estilo.configure(".", background=p["fondo"], foreground=p["texto"], font=("Segoe UI", 10))
        estilo.configure("TFrame", background=p["fondo"])
        estilo.configure("TLabel", background=p["fondo"], foreground=p["texto"])
        estilo.configure("TLabelFrame", background=p["panel"], foreground=p["texto"], bordercolor=p["borde"])
        estilo.configure("TLabelFrame.Label", background=p["panel"], foreground=p["texto"])
        estilo.configure("TButton", background=p["panel_secundario"], foreground=p["texto"], bordercolor=p["borde"], padding=(10, 7))
        estilo.map("TButton", background=[("disabled", p["panel"]), ("active", p["acento_hover"])], foreground=[("disabled", p["texto_secundario"]), ("active", "#FFFFFF")])
        estilo.configure("TEntry", fieldbackground=p["entrada"], foreground=p["texto"], insertcolor=p["texto"], bordercolor=p["borde"])
        estilo.map("TEntry", fieldbackground=[("disabled", p["panel"])], foreground=[("disabled", p["texto_secundario"])])
        estilo.configure("TCombobox", fieldbackground=p["entrada"], background=p["panel_secundario"], foreground=p["texto"], arrowcolor=p["texto"])
        estilo.map("TCombobox", fieldbackground=[("readonly", p["entrada"])], foreground=[("readonly", p["texto"])], selectbackground=[("readonly", p["seleccion"])], selectforeground=[("readonly", p["texto_seleccion"])])
        estilo.configure("TCheckbutton", background=p["fondo"], foreground=p["texto"])
        estilo.map("TCheckbutton", background=[("active", p["fondo"])])
        estilo.configure("TRadiobutton", background=p["fondo"], foreground=p["texto"])
        estilo.configure("TNotebook", background=p["fondo"], bordercolor=p["borde"])
        estilo.configure("TNotebook.Tab", background=p["panel_secundario"], foreground=p["texto"], padding=(10, 6))
        estilo.map("TNotebook.Tab", background=[("selected", p["panel"])], foreground=[("selected", p["texto"])])
        estilo.configure("Treeview", background=p["entrada"], fieldbackground=p["entrada"], foreground=p["texto"], bordercolor=p["borde"], rowheight=25)
        estilo.configure("Treeview.Heading", background=p["panel_secundario"], foreground=p["texto"], relief="flat")
        estilo.map("Treeview", background=[("selected", p["seleccion"])], foreground=[("selected", p["texto_seleccion"])])
        for orientacion in ("Vertical", "Horizontal"):
            estilo.configure(f"{orientacion}.TScrollbar", background=p["panel_secundario"], troughcolor=p["fondo"], arrowcolor=p["texto"])

        # Estilos personalizados definidos por las distintas ventanas.
        # Al redefinirlos aquí, sus colores dejan de quedar fijados al tema claro.
        estilos_frame = {
            "Principal.TFrame": p["fondo"],
            "Regex.Fondo.TFrame": p["fondo"],
            "Regex.Panel.TFrame": p["panel"],
            "Comparacion.TFrame": p["fondo"],
        }
        for nombre, fondo in estilos_frame.items():
            estilo.configure(nombre, background=fondo)

        estilos_label = {
            "Titulo.TLabel": (p["fondo"], p["texto"]),
            "Subtitulo.TLabel": (p["fondo"], p["texto_secundario"]),
            "Regex.Titulo.TLabel": (p["fondo"], p["texto"]),
            "Regex.Subtitulo.TLabel": (p["fondo"], p["texto_secundario"]),
            "Regex.Seccion.TLabel": (p["panel"], p["texto"]),
            "Comparacion.TLabel": (p["fondo"], p["texto"]),
            "Comparacion.Titulo.TLabel": (p["fondo"], p["texto"]),
            "Comparacion.Subtitulo.TLabel": (p["fondo"], p["texto_secundario"]),
            "Banco.TLabel": (p["panel"], p["texto"]),
            "BancoTitulo.TLabel": (p["fondo"], p["texto"]),
        }
        for nombre, (fondo, texto) in estilos_label.items():
            estilo.configure(nombre, background=fondo, foreground=texto)

        for nombre in ("Principal.TButton", "Secundario.TButton", "Regex.TButton", "Banco.TButton", "SA.TButton", "SA.Small.TButton"):
            estilo.configure(nombre, background=p["panel_secundario"], foreground=p["texto"], bordercolor=p["borde"])
            estilo.map(nombre, background=[("active", p["acento_hover"]), ("disabled", p["panel"])], foreground=[("active", "#FFFFFF"), ("disabled", p["texto_secundario"])])
        estilo.configure("Regex.TEntry", fieldbackground=p["entrada"], foreground=p["texto"], insertcolor=p["texto"], bordercolor=p["borde"])
        estilo.configure("Comparacion.TNotebook", background=p["fondo"], bordercolor=p["borde"])
        estilo.configure("Comparacion.TNotebook.Tab", background=p["panel_secundario"], foreground=p["texto"])
        estilo.map("Comparacion.TNotebook.Tab", background=[("selected", p["panel"])], foreground=[("selected", p["texto"])])
    except tk.TclError:
        pass


def aplicar_tema_ventana(ventana, tema=None):
    """Aplica la paleta recursivamente a controles Tk y ttk de una ventana."""
    global _TEMA_ACTUAL
    if tema in PALETAS:
        _TEMA_ACTUAL = tema
    p = obtener_paleta(tema)
    _configurar_estilos(ventana, p)
    _recorrer(ventana, p)


def _recorrer(widget, p):
    if not _existe(widget):
        return
    try:
        clase = widget.winfo_class()
        if clase in ("Toplevel", "Tk"):
            widget.configure(bg=p["fondo"])
        elif isinstance(widget, ttk.Label):
            # Las opciones directas de algunos ttk.Label prevalecen sobre el estilo.
            try:
                estilo_widget = str(widget.cget("style"))
                fondo = p["panel"] if estilo_widget in ("Regex.Seccion.TLabel", "Banco.TLabel") else p["fondo"]
                widget.configure(background=fondo, foreground=p["texto"])
            except tk.TclError:
                pass
        elif isinstance(widget, tk.Canvas):
            widget.configure(bg=p["panel"], highlightbackground=p["borde"])
        elif isinstance(widget, (tk.Frame, tk.LabelFrame)):
            widget.configure(bg=p["fondo"], highlightbackground=p["borde"])
        elif isinstance(widget, tk.Label):
            widget.configure(bg=p["fondo"], fg=p["texto"])
        elif isinstance(widget, tk.Button):
            widget.configure(bg=p["panel_secundario"], fg=p["texto"], activebackground=p["acento_hover"], activeforeground="#FFFFFF")
        elif isinstance(widget, (tk.Entry, tk.Spinbox)):
            widget.configure(bg=p["entrada"], fg=p["texto"], insertbackground=p["texto"], selectbackground=p["seleccion"], selectforeground=p["texto_seleccion"])
        elif isinstance(widget, tk.Text):
            widget.configure(bg=p["entrada"], fg=p["texto"], insertbackground=p["texto"], selectbackground=p["seleccion"], selectforeground=p["texto_seleccion"])
        elif isinstance(widget, (tk.Checkbutton, tk.Radiobutton)):
            widget.configure(bg=p["fondo"], fg=p["texto"], activebackground=p["fondo"], activeforeground=p["texto"], selectcolor=p["entrada"])
        elif isinstance(widget, tk.Listbox):
            widget.configure(bg=p["entrada"], fg=p["texto"], selectbackground=p["seleccion"], selectforeground=p["texto_seleccion"])
    except (tk.TclError, TypeError):
        pass
    try:
        children = widget.winfo_children()
    except (tk.TclError, AttributeError):
        children = []
    for child in children:
        _recorrer(child, p)


def cambiar_tema_global(tema):
    """Actualiza el tema de todas las ventanas registradas que sigan abiertas."""
    global _TEMA_ACTUAL, _VENTANAS
    if tema not in PALETAS:
        return
    _TEMA_ACTUAL = tema
    _VENTANAS = [w for w in _VENTANAS if _existe(w)]
    for ventana in list(_VENTANAS):
        aplicar_tema_ventana(ventana, tema)
