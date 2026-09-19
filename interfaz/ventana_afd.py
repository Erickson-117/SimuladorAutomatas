import tkinter as tk
from tkinter import ttk, messagebox

from modelos.afd import AFD


class VentanaAFD:

    def __init__(self, ventana_padre):

        self.ventana = tk.Toplevel(ventana_padre)

        self.ventana.title("Crear AFD")
        self.ventana.geometry("850x700")
        self.ventana.minsize(750, 600)

        self.afd = None

        self.crear_interfaz()

    def crear_interfaz(self):

        titulo = ttk.Label(
            self.ventana,
            text="CREAR AUTÓMATA FINITO DETERMINISTA",
            font=("Arial", 16, "bold")
        )

        titulo.pack(pady=20)

        formulario = ttk.Frame(self.ventana)
        formulario.pack(pady=10)

        # Estados
        ttk.Label(
            formulario,
            text="Estados:"
        ).grid(row=0, column=0, padx=10, pady=8, sticky="e")

        self.entrada_estados = ttk.Entry(
            formulario,
            width=45
        )

        self.entrada_estados.grid(
            row=0,
            column=1,
            padx=10,
            pady=8
        )

        # Alfabeto
        ttk.Label(
            formulario,
            text="Alfabeto:"
        ).grid(row=1, column=0, padx=10, pady=8, sticky="e")

        self.entrada_alfabeto = ttk.Entry(
            formulario,
            width=45
        )

        self.entrada_alfabeto.grid(
            row=1,
            column=1,
            padx=10,
            pady=8
        )

        # Estado inicial
        ttk.Label(
            formulario,
            text="Estado inicial:"
        ).grid(row=2, column=0, padx=10, pady=8, sticky="e")

        self.entrada_inicial = ttk.Entry(
            formulario,
            width=45
        )

        self.entrada_inicial.grid(
            row=2,
            column=1,
            padx=10,
            pady=8
        )

        # Estados finales
        ttk.Label(
            formulario,
            text="Estados finales:"
        ).grid(row=3, column=0, padx=10, pady=8, sticky="e")

        self.entrada_finales = ttk.Entry(
            formulario,
            width=45
        )

        self.entrada_finales.grid(
            row=3,
            column=1,
            padx=10,
            pady=8
        )

        # Transiciones
        ttk.Label(
            formulario,
            text="Transiciones:"
        ).grid(row=4, column=0, padx=10, pady=8, sticky="ne")

        self.entrada_transiciones = tk.Text(
            formulario,
            width=45,
            height=8
        )

        self.entrada_transiciones.grid(
            row=4,
            column=1,
            padx=10,
            pady=8
        )

        ayuda = ttk.Label(
            formulario,
            text="Formato: estado,símbolo,destino\n"
                 "Ejemplo: q0,0,q1"
        )

        ayuda.grid(
            row=5,
            column=1,
            sticky="w",
            padx=10
        )

        # Botón crear
        boton_crear = ttk.Button(
            formulario,
            text="Crear AFD",
            command=self.crear_afd
        )

        boton_crear.grid(
            row=6,
            column=0,
            columnspan=2,
            pady=20
        )

        # Resultado de creación
        self.resultado = ttk.Label(
            self.ventana,
            text=""
        )

        self.resultado.pack(pady=5)

        # Separador
        ttk.Separator(
            self.ventana,
            orient="horizontal"
        ).pack(fill="x", padx=30, pady=15)

        # ==========================
        # SIMULACIÓN
        # ==========================

        ttk.Label(
            self.ventana,
            text="SIMULAR CADENA",
            font=("Arial", 13, "bold")
        ).pack(pady=5)

        self.entrada_cadena = ttk.Entry(
            self.ventana,
            width=40
        )

        self.entrada_cadena.pack(pady=5)

        boton_simular = ttk.Button(
            self.ventana,
            text="Simular",
            command=self.simular
        )

        boton_simular.pack(pady=5)

        self.resultado_simulacion = ttk.Label(
            self.ventana,
            text=""
        )

        self.resultado_simulacion.pack(pady=10)

        # Recorrido
        ttk.Label(
            self.ventana,
            text="RECORRIDO DE LA SIMULACIÓN",
            font=("Arial", 11, "bold")
        ).pack(pady=(10, 5))

        self.ventana_recorrido = tk.Text(
            self.ventana,
            width=70,
            height=8
        )

        self.ventana_recorrido.pack(
            padx=30,
            pady=5
        )

    def crear_afd(self):

        try:

            estados = {
                estado.strip()
                for estado in self.entrada_estados.get().split(",")
                if estado.strip()
            }

            alfabeto = {
                simbolo.strip()
                for simbolo in self.entrada_alfabeto.get().split(",")
                if simbolo.strip()
            }

            estado_inicial = self.entrada_inicial.get().strip()

            estados_finales = {
                estado.strip()
                for estado in self.entrada_finales.get().split(",")
                if estado.strip()
            }

            texto_transiciones = self.entrada_transiciones.get(
                "1.0",
                tk.END
            ).strip()

            transiciones = {}

            if texto_transiciones:

                for linea in texto_transiciones.splitlines():

                    partes = [
                        parte.strip()
                        for parte in linea.split(",")
                    ]

                    if len(partes) != 3:
                        raise ValueError(
                            f"Transición inválida: {linea}\n"
                            "Use el formato estado,símbolo,destino."
                        )

                    origen, simbolo, destino = partes

                    clave = (origen, simbolo)

                    if clave in transiciones:
                        raise ValueError(
                            f"El AFD ya tiene una transición "
                            f"para ({origen}, {simbolo})."
                        )

                    transiciones[clave] = destino

            self.afd = AFD(
                estados,
                alfabeto,
                estado_inicial,
                estados_finales,
                transiciones
            )

            self.resultado.config(
                text="✓ AFD creado correctamente."
            )

            self.resultado_simulacion.config(
                text=""
            )

            self.ventana_recorrido.delete(
                "1.0",
                tk.END
            )

        except ValueError as error:

            self.afd = None

            messagebox.showerror(
                "Error",
                str(error)
            )

    def simular(self):

        if self.afd is None:

            messagebox.showwarning(
                "Advertencia",
                "Primero debe crear el AFD."
            )

            return

        cadena = self.entrada_cadena.get()

        recorrido, aceptada = self.afd.obtener_recorrido(
            cadena
        )

        if aceptada:

            resultado = "✓ CADENA ACEPTADA"

        else:

            resultado = "✗ CADENA RECHAZADA"

        texto_recorrido = "\n".join(recorrido)

        self.resultado_simulacion.config(
            text=resultado
        )

        self.ventana_recorrido.delete(
            "1.0",
            tk.END
        )

        self.ventana_recorrido.insert(
            tk.END,
            texto_recorrido
        )