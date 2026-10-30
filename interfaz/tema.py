"""Paletas y utilidades visuales compartidas para SimuladorAutomatas.

Este módulo centraliza los colores de la nueva interfaz principal. En las siguientes
etapas se puede reutilizar desde las ventanas de trabajo para aplicar el tema global.
"""

PALETAS = {
    "oscuro": {
        "fondo": "#17191F",
        "panel": "#22252D",
        "panel_secundario": "#2B303B",
        "borde": "#363B46",
        "texto": "#F3F4F6",
        "texto_secundario": "#A1A1AA",
        "acento": "#367BF5",
        "acento_hover": "#2563EB",
        "correcto": "#22C55E",
        "advertencia": "#F59E0B",
        "error": "#EF4444",
        "entrada": "#191C23",
    },
    "claro": {
        "fondo": "#F3F5F9",
        "panel": "#FFFFFF",
        "panel_secundario": "#F8FAFC",
        "borde": "#DDE3EC",
        "texto": "#172033",
        "texto_secundario": "#64748B",
        "acento": "#2563EB",
        "acento_hover": "#1D4ED8",
        "correcto": "#15803D",
        "advertencia": "#B45309",
        "error": "#B91C1C",
        "entrada": "#FFFFFF",
    },
}


def obtener_paleta(tema="oscuro"):
    """Devuelve la paleta solicitada, usando oscuro como valor predeterminado."""
    return PALETAS.get(tema, PALETAS["oscuro"]).copy()
