import logging
import tkinter as tk

from servicios.configuracion_logs import configurar_logging
from interfaz.principal import Aplicacion


ruta_logs = configurar_logging()
logging_logger = logging.getLogger(__name__)
logging_logger.info("Inicio del Simulador de Autómatas")

ventana = tk.Tk()

app = Aplicacion(ventana)

ventana.mainloop()