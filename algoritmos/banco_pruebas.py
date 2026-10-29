"""Pruebas sistemáticas de equivalencia observada entre AFN, AFD y AFD mínimo."""
from itertools import product

from algoritmos.conversion import convertir_afn_a_afd
from algoritmos.minimizacion import minimizar_afd


def generar_cadenas(alfabeto, longitud_maxima, incluir_vacia=True):
    """Genera todas las cadenas sobre el alfabeto hasta la longitud indicada.

    El resultado incluye primero la cadena vacía (si se solicita), seguida por
    las cadenas ordenadas por longitud y por el orden lexicográfico del alfabeto.
    """
    if not isinstance(longitud_maxima, int) or isinstance(longitud_maxima, bool):
        raise ValueError("La longitud máxima debe ser un número entero.")
    if longitud_maxima < 0:
        raise ValueError("La longitud máxima no puede ser negativa.")

    simbolos = sorted(alfabeto)
    if not simbolos:
        raise ValueError("El alfabeto no puede estar vacío.")
    if any(not isinstance(simbolo, str) or len(simbolo) != 1 for simbolo in simbolos):
        raise ValueError("El banco de pruebas requiere símbolos de un carácter.")

    cadenas = [""] if incluir_vacia else []
    for longitud in range(1, longitud_maxima + 1):
        cadenas.extend("".join(elementos) for elementos in product(simbolos, repeat=longitud))
    return cadenas


def ejecutar_banco_pruebas(afn, longitud_maxima=3, incluir_vacia=True):
    """Prueba cadenas y compara los resultados del AFN, AFD y AFD mínimo.

    Devuelve un diccionario con los autómatas usados, los resultados por cadena,
    las discrepancias y un resumen. Es una verificación acotada a las cadenas
    generadas; no es por sí sola una demostración formal de equivalencia.
    """
    cadenas = generar_cadenas(afn.alfabeto, longitud_maxima, incluir_vacia)
    afd = convertir_afn_a_afd(afn)
    afd_minimo, _pasos = minimizar_afd(afd)

    resultados = []
    discrepancias = []
    for cadena in cadenas:
        aceptada_afn = afn.simular(cadena)
        aceptada_afd = afd.simular(cadena)
        aceptada_minimo = afd_minimo.simular(cadena)
        coincide = aceptada_afn == aceptada_afd == aceptada_minimo
        fila = {
            "cadena": cadena,
            "afn": aceptada_afn,
            "afd": aceptada_afd,
            "afd_minimo": aceptada_minimo,
            "coincide": coincide,
        }
        resultados.append(fila)
        if not coincide:
            discrepancias.append(fila)

    total = len(resultados)
    return {
        "afd": afd,
        "afd_minimo": afd_minimo,
        "resultados": resultados,
        "discrepancias": discrepancias,
        "resumen": {
            "total": total,
            "coincidentes": total - len(discrepancias),
            "discrepancias": len(discrepancias),
            "equivalencia_observada": not discrepancias,
            "longitud_maxima": longitud_maxima,
            "incluye_vacia": incluir_vacia,
        },
    }
