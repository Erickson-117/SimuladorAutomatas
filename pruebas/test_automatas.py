from modelos.afd import AFD
from modelos.afn import AFN
from algoritmos.conversion import convertir_afn_a_afd


def test_afd_acepta_cadena_correcta():
    estados = {"q0", "q1"}
    alfabeto = {"0", "1"}
    estado_inicial = "q0"
    estados_finales = {"q1"}

    transiciones = {
        ("q0", "0"): "q1",
        ("q0", "1"): "q0",
        ("q1", "0"): "q1",
        ("q1", "1"): "q0"
    }

    afd = AFD(
        estados,
        alfabeto,
        estado_inicial,
        estados_finales,
        transiciones
    )

    assert afd.simular("0") is True


def test_afd_rechaza_cadena_incorrecta():
    estados = {"q0", "q1"}
    alfabeto = {"0", "1"}
    estado_inicial = "q0"
    estados_finales = {"q1"}

    transiciones = {
        ("q0", "0"): "q1",
        ("q0", "1"): "q0",
        ("q1", "0"): "q1",
        ("q1", "1"): "q0"
    }

    afd = AFD(
        estados,
        alfabeto,
        estado_inicial,
        estados_finales,
        transiciones
    )

    assert afd.simular("1") is False


def test_afn_con_epsilon():
    estados = {"q0", "q1", "q2", "q3"}
    alfabeto = {"0", "1"}
    estado_inicial = "q0"
    estados_finales = {"q3"}

    transiciones = {
        ("q0", "ε"): {"q1"},
        ("q1", "0"): {"q2"},
        ("q2", "1"): {"q3"}
    }

    afn = AFN(
        estados,
        alfabeto,
        estado_inicial,
        estados_finales,
        transiciones
    )

    assert afn.simular("01") is True
    assert afn.simular("0") is False


def test_conversion_afn_a_afd():

    estados = {
        "q0",
        "q1",
        "q2",
        "q3"
    }

    alfabeto = {
        "0",
        "1"
    }

    estado_inicial = "q0"

    estados_finales = {
        "q3"
    }

    transiciones = {

        ("q0", "ε"): {
            "q1"
        },

        ("q1", "0"): {
            "q2"
        },

        ("q2", "1"): {
            "q3"
        }
    }

    afn = AFN(
        estados,
        alfabeto,
        estado_inicial,
        estados_finales,
        transiciones
    )

    afd = convertir_afn_a_afd(afn)

    assert afd.simular("01")

    assert not afd.simular("0")

def test_minimizacion_fusiona_estados_equivalentes_y_preserva_lenguaje():
    from algoritmos.minimizacion import minimizar_afd

    # q0 y q1 son equivalentes; qx es inaccesible.
    estados = {"q0", "q1", "q2", "qx"}
    alfabeto = {"0", "1"}
    transiciones = {
        ("q0", "0"): "q1", ("q0", "1"): "q2",
        ("q1", "0"): "q0", ("q1", "1"): "q2",
        ("q2", "0"): "q2", ("q2", "1"): "q2",
        ("qx", "0"): "qx", ("qx", "1"): "qx",
    }
    original = AFD(estados, alfabeto, "q0", {"q2"}, transiciones)

    minimo, pasos = minimizar_afd(original)

    assert len(minimo.estados) == 2
    assert all("qx" not in estado for estado in minimo.estados)
    assert pasos[-1]["titulo"] == "5. AFD mínimo"
    for longitud in range(5):
        for numero in range(2 ** longitud):
            cadena = format(numero, f"0{longitud}b") if longitud else ""
            assert original.simular(cadena) == minimo.simular(cadena)


def test_minimizacion_no_modifica_afd_original():
    from algoritmos.minimizacion import minimizar_afd

    original = AFD(
        {"a", "b"}, {"0"}, "a", {"b"},
        {("a", "0"): "b", ("b", "0"): "b"},
    )
    estados_antes = set(original.estados)
    minimo, _ = minimizar_afd(original)
    assert original.estados == estados_antes
    assert len(minimo.estados) == 2


def test_regex_acepta_coincidencia_completa():
    from algoritmos.expresiones_regulares import validar_cadena

    assert validar_cadena(r"(0|1)*01", "1101") is True
    assert validar_cadena(r"(0|1)*01", "01") is True


def test_regex_rechaza_coincidencia_parcial():
    from algoritmos.expresiones_regulares import validar_cadena

    assert validar_cadena(r"(0|1)*01", "010") is False
    assert validar_cadena(r"(0|1)*01", "110") is False


def test_regex_detecta_sintaxis_invalida():
    import pytest
    from algoritmos.expresiones_regulares import validar_cadena

    with pytest.raises(ValueError, match="no es válida"):
        validar_cadena("(01", "01")
