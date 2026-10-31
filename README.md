# SimuladorAutomatas

## Requisitos del sistema

- **Sistema operativo:** Windows 10 o Windows 11.
- **Python:** versión 3.14.7.
- **RAM:** 4 GB como mínimo recomendado.
- **Dependencias:** ReportLab y pytest.
- **Conexión a Internet:** necesaria para descargar el proyecto desde GitHub.

## Pasos para probar el proyecto desde GitHub

### 1. Descargar el proyecto

Accede al repositorio:

https://github.com/Erickson-117/SimuladorAutomatas

Pulsa el botón **Code** y selecciona **Download ZIP**.

### 2. Extraer los archivos

Descomprime el archivo descargado en una carpeta de tu computadora.

### 3. Abrir una terminal

Entra en la carpeta `SimuladorAutomatas`, abre PowerShell y ejecuta los siguientes comandos.

### 4. Crear un entorno virtual

```powershell
python -m venv .venv
```

### 5. Activar el entorno virtual

```powershell
.\.venv\Scripts\Activate.ps1
```

### 6. Instalar las dependencias

```powershell
python -m pip install reportlab pytest
```

### 7. Ejecutar el simulador

```powershell
python main.py
```

Se abrirá la interfaz gráfica del programa, desde donde podrás probar sus diferentes módulos y funcionalidades.

### 8. Ejecutar las pruebas automatizadas (opcional)

Para comprobar el funcionamiento de las pruebas incluidas en el proyecto, ejecuta:

```powershell
python -m pytest -v
```

## Notas

- Si PowerShell no permite activar el entorno virtual, puedes ejecutar los comandos de instalación y ejecución usando directamente `.\.venv\Scripts\python.exe`.
- Para generar informes PDF, es necesario que ReportLab esté instalado correctamente.
- También puedes utilizar el instalador de Windows cuando esté disponible en la sección **Releases** del repositorio.
