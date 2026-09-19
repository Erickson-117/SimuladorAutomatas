import tkinter as tk
from tkinter import ttk
from interfaz.ventana_afd import VentanaAFD
from interfaz.ventana_afn import VentanaAFN


class Aplicacion:

    def __init__(self, ventana):
        self.ventana = ventana

        self.ventana.title("Simulador de Autómatas")
        self.ventana.geometry("900x600")
        self.ventana.minsize(800, 500)

        self.crear_interfaz()

    def crear_interfaz(self):

        titulo = ttk.Label(
            self.ventana,
            text="SIMULADOR DE AUTÓMATAS",
            font=("Arial", 20, "bold")
        )

        titulo.pack(pady=30)

        subtitulo = ttk.Label(
            self.ventana,
            text="Autómatas Finitos Deterministas y No Deterministas",
            font=("Arial", 12)
        )

        subtitulo.pack(pady=10)

        marco = ttk.Frame(self.ventana)
        marco.pack(pady=40)

        boton_afd = ttk.Button(
            marco,
            text="Crear AFD",
            width=25,
            command=lambda: VentanaAFD(self.ventana)
        )

        boton_afd.grid(row=0, column=0, padx=20, pady=10)

        boton_afn = ttk.Button(
            marco,
            text="Crear AFN",
            width=25,
            command=lambda: VentanaAFN(self.ventana)
        )

        boton_afn.grid(row=0, column=1, padx=20, pady=10)