"""Utilidades iniciales para validar expresiones regulares y cadenas.

La implementación usa la sintaxis de expresiones regulares de Python (módulo re).
La validación de cadenas es completa: la cadena entera debe coincidir.
"""

import re


def compilar_expresion(expresion: str):
    """Compila una expresión regular o lanza ValueError con un mensaje claro."""
    if not isinstance(expresion, str):
        raise ValueError("La expresión regular debe ser texto.")
    if not expresion:
        raise ValueError("Ingresa una expresión regular.")

    try:
        return re.compile(expresion)
    except re.error as error:
        raise ValueError(f"La expresión regular no es válida: {error}") from error


def validar_cadena(expresion: str, cadena: str) -> bool:
    """Devuelve True si toda la cadena coincide con la expresión regular."""
    patron = compilar_expresion(expresion)
    return patron.fullmatch(cadena) is not None

def generar_afn_thompson(expresion: str):
    """Construye un AFN-ε mediante el algoritmo de Thompson.

    Subconjunto soportado: símbolos literales de un carácter, concatenación,
    unión (|), cerradura de Kleene (*) y paréntesis.
    """
    from modelos.afn import AFN

    if not isinstance(expresion, str) or not expresion.strip():
        raise ValueError("Ingresa una expresión regular.")
    expresion = expresion.replace(" ", "")
    if not expresion:
        raise ValueError("Ingresa una expresión regular.")

    operadores = {"|", "*", "(", ")"}
    tokens = []
    anterior = None
    for caracter in expresion:
        if caracter == "\\":
            raise ValueError("La generación de AFN no admite escapes con barra invertida.")
        tipo = "op" if caracter in operadores else "simbolo"
        if tipo == "simbolo" and caracter in {"+", "?", "[", "]", "{", "}", "."}:
            raise ValueError(f"El operador '{caracter}' no está soportado para generar AFN.")
        if anterior in {"simbolo", ")", "*"} and tipo in {"simbolo", "("}:
            tokens.append(".")
        tokens.append(caracter)
        anterior = tipo
        if caracter == ")":
            anterior = ")"
        elif caracter == "*":
            anterior = "*"
        elif caracter == "(":
            anterior = "("
        elif caracter == "|":
            anterior = "|"
        else:
            anterior = "simbolo"

    # Convertir infija a posfija con precedencia: * > concatenación > unión.
    salida, pila = [], []
    precedencia = {"|": 1, ".": 2}
    espera_operando = True
    balance = 0
    for token in tokens:
        if token not in operadores and token != ".":
            salida.append(token)
            espera_operando = False
        elif token == "(":
            pila.append(token)
            balance += 1
            espera_operando = True
        elif token == ")":
            if espera_operando:
                raise ValueError("La expresión tiene paréntesis vacíos o un operador incompleto.")
            while pila and pila[-1] != "(":
                salida.append(pila.pop())
            if not pila:
                raise ValueError("Hay un paréntesis de cierre sin apertura.")
            pila.pop()
            balance -= 1
            espera_operando = False
        elif token == "*":
            if espera_operando:
                raise ValueError("El operador * necesita una expresión a su izquierda.")
            salida.append(token)
            espera_operando = False
        else:
            if espera_operando:
                raise ValueError(f"Falta un operando antes de '{token}'.")
            while pila and pila[-1] != "(" and precedencia.get(pila[-1], 0) >= precedencia[token]:
                salida.append(pila.pop())
            pila.append(token)
            espera_operando = True
    if balance:
        raise ValueError("Hay un paréntesis de apertura sin cierre.")
    if espera_operando:
        raise ValueError("La expresión termina con un operador.")
    while pila:
        if pila[-1] == "(":
            raise ValueError("Hay un paréntesis de apertura sin cierre.")
        salida.append(pila.pop())

    estados, transiciones, alfabeto = set(), {}, set()
    contador = 0

    def nuevo_estado():
        nonlocal contador
        estado = f"q{contador}"
        contador += 1
        estados.add(estado)
        return estado

    def agregar(origen, simbolo, destino):
        transiciones.setdefault((origen, simbolo), set()).add(destino)

    fragmentos = []
    for token in salida:
        if token not in {".", "|", "*"}:
            inicio, fin = nuevo_estado(), nuevo_estado()
            alfabeto.add(token)
            agregar(inicio, token, fin)
            fragmentos.append((inicio, fin))
        elif token == ".":
            if len(fragmentos) < 2:
                raise ValueError("Concatenación incompleta.")
            b_inicio, b_fin = fragmentos.pop()
            a_inicio, a_fin = fragmentos.pop()
            agregar(a_fin, "ε", b_inicio)
            fragmentos.append((a_inicio, b_fin))
        elif token == "|":
            if len(fragmentos) < 2:
                raise ValueError("La unión necesita una expresión a cada lado.")
            b_inicio, b_fin = fragmentos.pop()
            a_inicio, a_fin = fragmentos.pop()
            inicio, fin = nuevo_estado(), nuevo_estado()
            agregar(inicio, "ε", a_inicio)
            agregar(inicio, "ε", b_inicio)
            agregar(a_fin, "ε", fin)
            agregar(b_fin, "ε", fin)
            fragmentos.append((inicio, fin))
        else:
            if not fragmentos:
                raise ValueError("La cerradura * necesita una expresión a su izquierda.")
            a_inicio, a_fin = fragmentos.pop()
            inicio, fin = nuevo_estado(), nuevo_estado()
            agregar(inicio, "ε", a_inicio)
            agregar(inicio, "ε", fin)
            agregar(a_fin, "ε", a_inicio)
            agregar(a_fin, "ε", fin)
            fragmentos.append((inicio, fin))

    if len(fragmentos) != 1:
        raise ValueError("La expresión regular no tiene una estructura válida.")
    inicial, final = fragmentos[0]
    return AFN(estados, alfabeto, inicial, {final}, transiciones)

