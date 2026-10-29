"""Interpretación basada en reglas para errores y advertencias del simulador.

Este módulo no modifica los registros originales. Recibe los diccionarios
producidos por ``analizar_linea_log`` / ``validar_archivo_logs`` y devuelve
un diagnóstico estructurado para presentar en la interfaz.
"""

from __future__ import annotations

import re
from collections import Counter


# Cada regla contiene patrones del mensaje y una explicación accionable.
# Se priorizan los mensajes concretos que ya aparecen en logs.txt.
REGLAS_DIAGNOSTICO = [
    {
        "id": "regex_parentesis_sin_cerrar",
        "patrones": (r"paréntesis de apertura sin cierre", r"missing \)", r"unterminated subpattern"),
        "titulo": "Paréntesis sin cerrar en la expresión regular",
        "interpretacion": "La expresión contiene un grupo que se abrió con '(' y no se cerró correctamente.",
        "causa_probable": "Falta un paréntesis de cierre ')' o la expresión está agrupada incorrectamente.",
        "solucion": "Revisa los paréntesis de la expresión y asegúrate de que cada '(' tenga su correspondiente ')'.",
        "impacto": "No se puede validar o convertir correctamente la expresión mientras el error persista.",
    },
    {
        "id": "regex_clase_caracteres_incompleta",
        "patrones": (r"unterminated character set", r"conjunto de caracteres", r"operador '\['"),
        "titulo": "Clase de caracteres no admitida o incompleta",
        "interpretacion": "La expresión usa una clase de caracteres entre corchetes que está incompleta o no es compatible con el generador de AFN.",
        "causa_probable": "Puede faltar ']' o se está usando una sintaxis que el algoritmo de Thompson actual no implementa.",
        "solucion": "Comprueba que los corchetes estén cerrados. Si la expresión es válida en Python pero el generador la rechaza, usa por ahora los operadores compatibles con Thompson: concatenación, '|', '*', y paréntesis.",
        "impacto": "La validación con Python y la generación del autómata pueden dar resultados diferentes porque admiten gramáticas distintas.",
    },
    {
        "id": "regex_escape_no_admitido",
        "patrones": (r"no admite escapes con barra invertida", r"escape.*no soport", r"barra invertida"),
        "titulo": "Secuencia de escape no compatible con el generador",
        "interpretacion": "La expresión contiene una barra invertida que el generador de AFN no admite actualmente.",
        "causa_probable": "El generador de Thompson implementa un subconjunto de la sintaxis de expresiones regulares.",
        "solucion": "Retira o simplifica la secuencia de escape, o adapta la expresión a los operadores admitidos por el generador.",
        "impacto": "No se puede construir el AFN a partir de esa expresión con la implementación actual.",
    },
    {
        "id": "afd_sin_estados",
        "patrones": (r"debe ingresar al menos un estado", r"sin estados", r"no se han definido estados"),
        "titulo": "No se han definido estados para el AFD",
        "interpretacion": "Se solicitó crear un autómata determinista sin proporcionar estados.",
        "causa_probable": "El campo de estados está vacío o los valores introducidos no se interpretaron como estados válidos.",
        "solucion": "Introduce al menos un estado y comprueba que los campos del autómata estén completos antes de crearlo.",
        "impacto": "El AFD no puede construirse ni utilizarse para simular cadenas.",
    },
    {
        "id": "automata_no_creado",
        "patrones": (r"primero debe crear el afd", r"primero debe crear el afn", r"no se ha creado el autómata", r"no existe un afd"),
        "titulo": "Se intentó operar sin crear el autómata",
        "interpretacion": "Se intentó probar o ejecutar una operación antes de tener disponible el autómata requerido.",
        "causa_probable": "El autómata todavía no se ha creado o la creación anterior falló.",
        "solucion": "Completa la configuración y crea el autómata antes de probar cadenas, convertirlo o minimizarlo.",
        "impacto": "La operación solicitada no puede continuar porque falta el autómata de entrada.",
    },
    {
        "id": "regex_invalida_python",
        "patrones": (r"la expresión regular no es válida", r"bad character in group name", r"nothing to repeat", r"unterminated"),
        "titulo": "Expresión regular inválida",
        "interpretacion": "El motor de expresiones regulares de Python no pudo interpretar la expresión introducida.",
        "causa_probable": "Hay un operador, grupo, corchete o secuencia con una sintaxis incompleta o incorrecta.",
        "solucion": "Lee el detalle del error, corrige la parte indicada de la expresión y vuelve a validarla antes de generar el autómata.",
        "impacto": "No se puede validar cadenas con esa expresión hasta corregir su sintaxis.",
    },
]


def _texto_registro(registro: dict) -> str:
    """Combina módulo y mensaje para permitir reglas contextuales."""
    modulo = str(registro.get("modulo", ""))
    mensaje = str(registro.get("mensaje", ""))
    return f"{modulo} {mensaje}".casefold()


def interpretar_registro(registro: dict) -> dict | None:
    """Devuelve un diagnóstico para WARNING/ERROR/CRITICAL, si aplica.

    El registro debe ser un diccionario válido devuelto por el validador.
    Los INFO se omiten intencionalmente en esta primera versión.
    """
    nivel = str(registro.get("nivel", "")).upper()
    if nivel not in {"WARNING", "ERROR", "CRITICAL"}:
        return None

    texto = _texto_registro(registro)
    for regla in REGLAS_DIAGNOSTICO:
        if any(re.search(patron, texto, re.IGNORECASE) for patron in regla["patrones"]):
            return {
                "nivel": nivel,
                "fecha": registro.get("fecha", ""),
                "hora": registro.get("hora", ""),
                "modulo": registro.get("modulo", ""),
                "mensaje_original": registro.get("mensaje", ""),
                "id_regla": regla["id"],
                "titulo": regla["titulo"],
                "interpretacion": regla["interpretacion"],
                "causa_probable": regla["causa_probable"],
                "solucion": regla["solucion"],
                "impacto": regla["impacto"],
                "coincidencia": "regla_conocida",
            }

    # No inventamos una causa específica si no conocemos el patrón.
    return {
        "nivel": nivel,
        "fecha": registro.get("fecha", ""),
        "hora": registro.get("hora", ""),
        "modulo": registro.get("modulo", ""),
        "mensaje_original": registro.get("mensaje", ""),
        "id_regla": "sin_regla_especifica",
        "titulo": "Incidencia que requiere revisión",
        "interpretacion": "El registro indica una advertencia o error, pero no coincide con una regla de interpretación conocida.",
        "causa_probable": "No hay información suficiente para determinar una causa concreta a partir del mensaje registrado.",
        "solucion": "Revisa el contexto de la operación y el código del módulo indicado. Si es posible, registra el detalle de la excepción.",
        "impacto": "El impacto exacto depende de la operación que falló.",
        "coincidencia": "regla_generica",
    }


def analizar_registros(registros: list[dict]) -> list[dict]:
    """Interpreta únicamente los registros WARNING, ERROR y CRITICAL."""
    diagnosticos = []
    for registro in registros:
        diagnostico = interpretar_registro(registro)
        if diagnostico is not None:
            diagnosticos.append(diagnostico)
    return diagnosticos


def resumir_diagnosticos(diagnosticos: list[dict]) -> dict:
    """Genera un resumen simple para mostrarlo en la futura ventana gráfica."""
    niveles = Counter(item.get("nivel", "DESCONOCIDO") for item in diagnosticos)
    modulos = Counter(item.get("modulo", "Sin módulo") for item in diagnosticos)
    reglas = Counter(item.get("id_regla", "sin_regla_especifica") for item in diagnosticos)
    return {
        "total": len(diagnosticos),
        "por_nivel": dict(niveles),
        "por_modulo": dict(modulos),
        "por_tipo": dict(reglas),
        "sin_regla_especifica": sum(
            item.get("coincidencia") == "regla_generica" for item in diagnosticos
        ),
    }
