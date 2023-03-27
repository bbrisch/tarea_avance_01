#!/usr/bin/env python
# Autor: Benjamín Brito
# Propósito: Scripy con la implementación de funciones útiles

import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ============================ Funciones del enunciado ============================================

# Parte b): Implemente una interfaz de difusión
def interfaz_difusion(input: float, conjunto: list) -> float:
    """
    Función que retorna el grado de pertenencia de un número al conjuto trapezoidal
    descrito por los puntos del arreglo que definen al conjuto.

    - input: numero a partir del cual se obtiene la pertenecia
    - conjunto: lista con los 'vertices' del trapecio que actua como función de pertenencia
    """

    # Generamos el trapecio con if-else
    if input < conjunto[0]:  # caso en el que no entramos al trepecio
        return 0

    elif input < conjunto[1]:  # caso cuando el número entra a la primera pendiente
        return (input - conjunto[0]) / (conjunto[1] - conjunto[0])

    elif input < conjunto[2]:  # caso en el que el numero está en el punto máximo
        return 1

    elif input < conjunto[3]:  # caso cuando el número entra a la segunda pendiente
        return (input - conjunto[3]) / (conjunto[2] - conjunto[3])
    else:
        return 0


# Parte c): Implemente una función para el operador de_a
def de_a(conjunto1: list, conjunto2: list) -> list:
    """
    El operador “de_a” es la unión del intervalo entre los valores difusos definidos.
    Se considera la versión generalizada del operador.

    - conjunto1/2: listas que representan los conjuntos
    """

    # Iteramos por los conjuntos. Debemos quedarnos con los bordes inferiores para los dos primeros
    # números, pero con los bordes superiores para los dos últimos

    output = []  # lista donde se guardarán los vertices del nuevo conjunto

    for i, (n1, n2) in enumerate(
        zip(conjunto1, conjunto2)
    ):  # iteramos para obtener el ínidice, el elemnto de c1 y el elemento de c2

        if i < 3:  # caso para las dos primeras iteraciones (inicio del trapecio)
            output.append(min(n1, n2))

        else:
            output.append(
                max(n1, n2)
            )  # Caso para las útimas interaciones (final del trapecio)

    return output


# Parte d): Se genera una función que permite visualizar el grado de pertenencia a cada regla dadas dos entradas
def base_reglas(input1: float, input2: float, reglas: list):
    """
    Función que computa manualmente el grado de activación de cada regla y sus entradas.

    - input1/2: Numeros de entrada a la base de reglas
    - reglas: lista con diccionarios con reglas a operar

    Estructura del diccionairio:
        entrada1:
            - conjunto
            - conjunto

        entrada2:
            - conjunto
            - conjunto

        salida: conjunto de la salida
    """

    # Listas para las pertenencias a los conjuntos de entrada y salida
    E1 = []
    E2 = []
    Salida = []
    S_conj = []

    # Iteramos por las reglas
    for regla in reglas:
        # print(regla)
        # Computamos las pertenencias
        e1 = interfaz_difusion(input1, de_a(*regla["entrada1"]))
        e2 = interfaz_difusion(input2, de_a(*regla["entrada2"]))
        # print(e1, e2, min(e1, e2), "\n")
        # s = interfaz_difusion(min(e1, e2), regla["salida"])

        # Truncamos las reglas para obtener el conjunto de salida
        # S_conj.append([regla["salida"][0], s, s, regla["salida"][-1]])

        # Guardamos los resultados
        E1.append(e1)
        E2.append(e2)
        Salida.append(min(e1, e2))

    return (
        E1,
        E2,
        Salida,
    )  # S_conj


# Parte e): Implemente una máquina de inferencia que ocupe una base de conocimientos con reglas difusas
def maquina_de_inferencia(input1: float, input2: float, reglas: list, n: int = 41):

    # Aplicamos las reglas y obtenemos su activación
    _, _, activaciones = base_reglas(input1, input2, reglas)

    # Sampleamos las activaciones
    cdm_ = 0
    acum = 0

    # Iteramos cada punto
    for i in np.linspace(-1, 1, n):
        aux = []
        # Verificamos la activación el el punto de cada regla
        for regla, activacion in zip(reglas, activaciones):
            # print(regla, activacion,)

            pertenencia = interfaz_difusion(i, regla["salida"])
            # print(
            #     "i",
            #     i,
            #     "\tregla",
            #     regla["salida"],
            #     "\tactivación",
            #     activacion,
            #     "\tpertenencia",
            #     pertenencia,
            #     "\tactivación de regla",
            #     pertenencia if pertenencia < activacion else activacion,
            # )
            aux.append(pertenencia if pertenencia < activacion else activacion)
        # print("\n")

        cdm_ += i * max(aux)  # Consideramos solo la máxima activación
        acum += max(aux)
        # print(max(aux), i * max(aux))
        # print(acum, cdm_)
        # break
    print(cdm_, acum)
    # Retornamos el centro de masa
    return cdm_ / acum if acum != 0 else 0


# ============================ Funciones extra ============================================

# Fución para graficar conjuntos difusos
def graficar_conjunto_difuso(mu, conjunto, n=43):
    """
    Función que grafica los conjuntos difusos definidos por una función de pertenencia
    """
    eje = np.linspace(-1, 1, n)
    pertenencia = [mu(x, conjunto) for x in eje]

    # return px.scatter(x=eje, y=pertenencia)
    # return eje, pertenencia

    return go.Scatter(x=eje, y=pertenencia)
