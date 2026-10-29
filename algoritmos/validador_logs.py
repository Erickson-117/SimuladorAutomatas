import re
from datetime import datetime

# Formato: fecha hora | NIVEL | modulo | mensaje
PATRON_LOG = re.compile(
    r"^(?P<fecha>\d{4}-\d{2}-\d{2}) "
    r"(?P<hora>(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d) "
    r"\| (?P<nivel>INFO|WARNING|ERROR|CRITICAL) "
    r"\| (?P<modulo>[^|\r\n]+) "
    r"\| (?P<mensaje>.*)$"
)

NIVELES_LOG = ("INFO", "WARNING", "ERROR", "CRITICAL")

# Patrones para reconocer el nivel en su campo del registro, no en el mensaje.
# Se ancla la búsqueda al comienzo de la línea y al separador posterior al nivel.
PATRONES_NIVELES_LOG = {
    nivel: re.compile(
        rf"^\d{{4}}-\d{{2}}-\d{{2}} "
        rf"(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d "
        rf"\|\s*{nivel}\s*\|"
    )
    for nivel in NIVELES_LOG
}


def clasificar_nivel_log(linea):
    """Clasifica una línea mediante regex según el nivel de su campo.

    Devuelve INFO, WARNING, ERROR o CRITICAL. Devuelve None si ningún
    patrón reconoce un nivel en la posición esperada del registro.
    La línea debería validarse primero con analizar_linea_log().
    """
    texto = linea.rstrip("\r\n")
    for nivel, patron in PATRONES_NIVELES_LOG.items():
        if patron.search(texto):
            return nivel
    return None


def analizar_linea_log(linea):
    """Valida una línea de log con regex y valida además la fecha real."""
    texto = linea.rstrip("\r\n")
    coincidencia = PATRON_LOG.fullmatch(texto)
    if not coincidencia:
        return None, "La línea no cumple el formato esperado."

    datos = coincidencia.groupdict()
    try:
        datetime.strptime(datos["fecha"], "%Y-%m-%d")
    except ValueError:
        return None, "La fecha no es válida."

    return datos, None


def validar_archivo_logs(ruta):
    """Devuelve registros válidos y líneas inválidas con su número."""
    validos = []
    invalidos = []
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            for numero, linea in enumerate(archivo, start=1):
                if not linea.strip():
                    continue
                datos, error = analizar_linea_log(linea)
                if error:
                    invalidos.append((numero, linea.rstrip("\r\n"), error))
                else:
                    datos["linea"] = linea.rstrip("\r\n")
                    validos.append(datos)
    except FileNotFoundError:
        return [], []
    return validos, invalidos
