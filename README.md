# Probador Virtual de Accesorios (AR)

Proyecto final para el curso de **Computación Gráfica, Visión Computacional y Multimedia**.

## Descripción
Este proyecto consiste en una aplicación de Realidad Aumentada (AR) que permite a los usuarios probarse virtualmente accesorios (como lentes y sombreros) utilizando la cámara web. 

Se empleará **OpenCV** para el procesamiento de imágenes en tiempo real y **MediaPipe** para la detección precisa de los puntos clave del rostro (Face Mesh).

## Estructura del Proyecto (Avance Inicial)
- `main.py`: Script principal. Actualmente abre la cámara web y muestra el video en espejo.
- `requirements.txt`: Dependencias necesarias para ejecutar el proyecto.
- `assets/`: Carpeta donde se guardarán las imágenes PNG con transparencia de los lentes y sombreros.

## Requisitos de Instalación
1. Instalar Python 3.x
2. Instalar las dependencias usando pip:
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución
Para probar el avance actual, simplemente ejecuta:
```bash
python main.py
```
Presiona la tecla **'q'** con la ventana seleccionada para salir.
