from algoritmos.analizador_logs import (
    analizar_registros,
    interpretar_registro,
    resumir_diagnosticos,
)


def registro(nivel, mensaje, modulo="interfaz.ventana_regex"):
    return {
        "fecha": "2026-10-29",
        "hora": "16:30:15",
        "nivel": nivel,
        "modulo": modulo,
        "mensaje": mensaje,
    }


def test_interpreta_parentesis_sin_cerrar():
    diagnostico = interpretar_registro(
        registro("WARNING", "No se pudo generar el AFN desde la expresión regular: Hay un paréntesis de apertura sin cierre.")
    )
    assert diagnostico["id_regla"] == "regex_parentesis_sin_cerrar"
    assert "paréntesis" in diagnostico["titulo"].lower()
    assert diagnostico["solucion"]


def test_interpreta_operador_no_admitido():
    diagnostico = interpretar_registro(
        registro("ERROR", "No se pudo convertir la expresión a AFD: El operador '[' no está soportado para generar AFN.")
    )
    assert diagnostico["id_regla"] == "regex_clase_caracteres_incompleta"
    assert "Thompson" in diagnostico["solucion"]


def test_interpreta_afd_sin_estados():
    diagnostico = interpretar_registro(
        registro("WARNING", "No se pudo crear el AFD: Debe ingresar al menos un estado.", "interfaz.ventana_afd")
    )
    assert diagnostico["id_regla"] == "afd_sin_estados"


def test_interpreta_operacion_sin_autómata():
    diagnostico = interpretar_registro(
        registro("WARNING", "No se pudo probar la cadena: primero debe crear el AFD.", "interfaz.ventana_afd")
    )
    assert diagnostico["id_regla"] == "automata_no_creado"


def test_omite_info():
    assert interpretar_registro(registro("INFO", "Acción iniciada: validar_expresion")) is None


def test_mensaje_desconocido_no_inventa_causa():
    diagnostico = interpretar_registro(registro("ERROR", "Error inesperado durante una operación nueva"))
    assert diagnostico["coincidencia"] == "regla_generica"
    assert "información suficiente" in diagnostico["causa_probable"]


def test_analizar_registros_y_resumen():
    diagnosticos = analizar_registros([
        registro("INFO", "Inicio"),
        registro("WARNING", "Debe ingresar al menos un estado.", "interfaz.ventana_afd"),
        registro("ERROR", "Error inesperado", "algoritmos.afd"),
    ])
    resumen = resumir_diagnosticos(diagnosticos)
    assert len(diagnosticos) == 2
    assert resumen["total"] == 2
    assert resumen["por_nivel"] == {"WARNING": 1, "ERROR": 1}
    assert resumen["sin_regla_especifica"] == 1
