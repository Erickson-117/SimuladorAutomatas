"""Utilidades iniciales para validar expresiones regulares y cadenas.

La implementación usa la sintaxis de expresiones regulares de Python (módulo re).
La validación de cadenas es completa: la cadena entera debe coincidir.
"""

import re


def compilar_expresion(expresion: str):
    """Compila una expresión regular o lanza ValueError con un mensaje claro."""
    if not isinstance(expresion, str):
        raise ValueError("La expresión regular debe ser texto.")
    if not expresion:
        raise ValueError("Ingresa una expresión regular.")

    try:
        return re.compile(expresion)
    except re.error as error:
        raise ValueError(f"La expresión regular no es válida: {error}") from error


def validar_cadena(expresion: str, cadena: str) -> bool:
    """Devuelve True si toda la cadena coincide con la expresión regular."""
    patron = compilar_expresion(expresion)
    return patron.fullmatch(cadena) is not None
