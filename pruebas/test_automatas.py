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