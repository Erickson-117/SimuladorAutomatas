import logging
import os
from pathlib import Path


FORMATO_LOG = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
FORMATO_FECHA = "%Y-%m-%d %H:%M:%S"


def configurar_logging():
    """Configura el registro en logs.txt y en la consola."""
    ruta_log = Path(__file__).resolve().parent.parent / "logs.txt"
    logger_raiz = logging.getLogger()
    logger_raiz.setLevel(logging.INFO)

    # Evita agregar handlers duplicados si se inicializa más de una vez.
    if not any(getattr(handler, "_simulador_logs", False)
               for handler in logger_raiz.handlers):
        archivo = logging.FileHandler(ruta_log, encoding="utf-8")
        archivo.setFormatter(logging.Formatter(FORMATO_LOG, datefmt=FORMATO_FECHA))
        archivo._simulador_logs = True
        logger_raiz.addHandler(archivo)

        consola = logging.StreamHandler()
        consola.setFormatter(logging.Formatter(FORMATO_LOG, datefmt=FORMATO_FECHA))
        consola._simulador_logs = True
        logger_raiz.addHandler(consola)

    return ruta_log
