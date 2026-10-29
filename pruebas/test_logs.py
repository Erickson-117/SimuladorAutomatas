from algoritmos.validador_logs import analizar_linea_log, validar_archivo_logs


def test_analizar_linea_log_valida():
    datos, error = analizar_linea_log(
        "2026-10-28 21:15:32 | INFO | ventana_regex | Expresión validada"
    )
    assert error is None
    assert datos["nivel"] == "INFO"
    assert datos["modulo"] == "ventana_regex"
    assert datos["mensaje"] == "Expresión validada"


def test_analizar_linea_log_rechaza_nivel_desconocido():
    datos, error = analizar_linea_log(
        "2026-10-28 21:15:32 | DEBUG | ventana_regex | Mensaje"
    )
    assert datos is None
    assert error is not None


def test_analizar_linea_log_rechaza_fecha_imposible():
    datos, error = analizar_linea_log(
        "2026-15-40 21:15:32 | ERROR | conversion | Falló"
    )
    assert datos is None
    assert "fecha" in error.lower()


def test_validar_archivo_logs_separa_validos_e_invalidos(tmp_path):
    archivo = tmp_path / "logs.txt"
    archivo.write_text(
        "2026-10-28 21:15:32 | INFO | principal | Inicio\n"
        "línea mal formada\n",
        encoding="utf-8",
    )
    validos, invalidos = validar_archivo_logs(archivo)
    assert len(validos) == 1
    assert len(invalidos) == 1
    assert invalidos[0][0] == 2
