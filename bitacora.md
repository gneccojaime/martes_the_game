# Bitácora de Desarrollo - Sandbox Zombies 3D

## Fecha de Inicio: 24 de noviembre de 2026
**Desarrollador:** Estudiante de Ingeniería Energética (1er ingreso)  
**Proyecto:** Juego Sandbox 3D - Campaña Zombies con AK-47  
**Tecnología evaluada:** Python (Ursina Engine vs. Streamlit)

---

### Registro de Comandos y Consultas

#### Sesión 1: Planteamiento y Arquitectura
- **Consulta inicial:** 
  - Saludo y presentación del perfil del desarrollador.
  - Objetivo: Desarrollar un juego 3D tipo sandbox con modo campaña de disparar a zombies con un AK-47 en un plano.
  - Pregunta: *¿Puedo usar Streamlit y Python para crear mi juego?*
- **Análisis Técnico:**
  - *Streamlit:* Diseñado para aplicaciones web de datos y dashboards, no soporta bucles de juego a 60 FPS en tiempo real ni controles nativos de mouse/teclado en primera persona en 3D.
  - *Recomendación:* **Ursina Engine** (Python) o **Godot Engine** (con GDScript similar a Python). Ursina permite crear juegos 3D en Python puro con controlador de primera persona y físicas en muy pocas líneas de código.
- **Acciones Realizadas:**
  - Creación del archivo de registro `bitacora.md`.

#### Sesión 2: Fase 1 - Escenario y Controlador en 1ª Persona
- **Comando del usuario:** "vamos con la fase 1"
- **Objetivo de la fase:** 
  - Generar el plano (terreno) de 64x64 unidades con textura y colisiones.
  - Configurar cielo e iluminación del sandbox.
  - Implementar el `FirstPersonController` para soporte de cámara con ratón y desplazamiento con teclas `WASD` y salto con `Espacio`.
  - Agregar bloques de referencia en el plano.
- **Archivos creados/modificados:**
  - `main.py`: Código completo y comentado de la Fase 1.
- **Comandos necesarios en terminal:**
  ```powershell
  # 1. Instalar la librería Ursina
  pip install ursina

  # 2. Ejecutar el juego
  python main.py
  ```
- **Controles configurados:**
  - `W, A, S, D`: Movimiento del personaje.
  - `Ratón`: Girar vista (Pitch y Yaw).
  - `Espacio`: Saltar.
  - `Escape`: Salir de la ventana de juego.

#### Incidencia Técnica: Incompatibilidad de versión de Python (Python 3.15)
- **Problema:** El usuario intentó instalar `ursina` con `pip` y obtuvo el error `ERROR: ResolutionImpossible`.
- **Causa:** La máquina tiene instalada la versión **Python 3.15.2**. `ursina` y su motor gráfico `panda3d` dependen de binarios compilados en C++ que actualmente son compatibles hasta Python 3.11/3.12. No existen *wheels* de Panda3D para Python 3.15 en PyPI.
- **Diagnóstico:** Se identificó la presencia de la herramienta `uv` (`C:\Users\ESTUDIANTES\.local\bin\uv.exe`).
- **Solución recomendada:**
  Utilizar `uv` para crear un entorno virtual con Python 3.11 o ejecutar el juego directamente con la versión adecuada:
  ```powershell
  # Opción directa y recomendada:
  uv run --python 3.11 --with ursina python main.py
  
  # O creando el entorno virtual:
  uv venv --python 3.11
  .\.venv\Scripts\Activate.ps1
  uv pip install ursina
  python main.py
  ```

#### Incidencia Técnica: Política de ejecución de PowerShell (PSSecurityException)
- **Problema:** El script de activación `.\.venv\Scripts\Activate.ps1` falló debido a la directiva de seguridad por defecto de Windows (`ExecutionPolicy Restricted`).
- **Consecuencia:** `uv pip install ursina` instaló exitosamente Ursina en `.venv`, pero al ejecutar `python main.py` se invocó el Python global (3.15) en lugar del Python del entorno virtual (3.11), arrojando `ModuleNotFoundError: No module named 'ursina'`.
- **Solución directa:**
  1. Ejecutar directamente con `uv run`:
     ```powershell
     uv run python main.py
     ```
  2. O usar la ruta explícita del ejecutable de `.venv`:
     ```powershell
     .\.venv\Scripts\python.exe main.py
     ```
  3. O desbloquear la política para la sesión actual:
     ```powershell
     Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
     .\.venv\Scripts\Activate.ps1
     python main.py
     ```
