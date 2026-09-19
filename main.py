from modelos.afn import AFN


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

print("Cadena 01:", afn.simular("01"))
print("Cadena 0:", afn.simular("0"))
print("Cadena 1:", afn.simular("1"))
print("Cadena 11:", afn.simular("11"))