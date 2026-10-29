import pytest

from algoritmos.banco_pruebas import generar_cadenas, ejecutar_banco_pruebas
from algoritmos.expresiones_regulares import generar_afn_thompson
from modelos.afn import AFN


def test_generar_cadenas_incluye_vacia_y_todas_hasta_longitud_dos():
    assert generar_cadenas({"0", "1"}, 2) == [
        "", "0", "1", "00", "01", "10", "11"
    ]


def test_generar_cadenas_puede_excluir_vacia():
    assert generar_cadenas({"a"}, 2, incluir_vacia=False) == ["a", "aa"]


@pytest.mark.parametrize("longitud", [-1, 1.5, True])
def test_longitud_invalida_genera_error(longitud):
    with pytest.raises(ValueError):
        generar_cadenas({"0"}, longitud)


def test_banco_compara_afn_afd_y_minimo_incluyendo_epsilon():
    afn = generar_afn_thompson("(0|1)*01")
    resultado = ejecutar_banco_pruebas(afn, longitud_maxima=4)

    assert resultado["resumen"]["total"] == 31
    assert resultado["resumen"]["equivalencia_observada"] is True
    assert resultado["resumen"]["discrepancias"] == 0
    assert all(fila["afn"] == fila["afd"] == fila["afd_minimo"] for fila in resultado["resultados"])
    assert resultado["resultados"][0]["cadena"] == ""


def test_banco_cadena_vacia_desactivada():
    afn = generar_afn_thompson("0*")
    resultado = ejecutar_banco_pruebas(afn, 2, incluir_vacia=False)
    assert resultado["resumen"]["total"] == 2
    assert all(fila["cadena"] != "" for fila in resultado["resultados"])


def test_banco_admite_afn_con_transicion_epsilon():
    afn = AFN(
        estados={"q0", "q1", "q2"},
        alfabeto={"a"},
        estado_inicial="q0",
        estados_finales={"q2"},
        transiciones={("q0", "ε"): {"q1"}, ("q1", "a"): {"q2"}},
    )
    resultado = ejecutar_banco_pruebas(afn, 2)
    assert resultado["resumen"]["equivalencia_observada"]
    assert resultado["resumen"]["total"] == 3
