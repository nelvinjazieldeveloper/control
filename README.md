## Mouse Control and Voice Commands with MediaPipe and Python  
## Control de Mouse y Comandos de Voz con MediaPipe y Python  

This project uses the **MediaPipe** library to detect facial landmarks and control mouse movement based on head tilt. It also incorporates voice recognition to execute specific commands such as opening programs, adjusting volume, shutting down the computer, and more.

Este proyecto utiliza la biblioteca **MediaPipe** para detectar la malla facial y controlar el movimiento del mouse en función de la inclinación de la cabeza. Además, incorpora reconocimiento de voz para ejecutar comandos específicos como abrir programas, ajustar el volumen, apagar el equipo, entre otros.  

## Requirements / Requisitos  

To run this project, you need to have the following Python libraries installed:
Para ejecutar este proyecto, necesitas tener instaladas las siguientes bibliotecas de Python:

- `mediapipe`  
- `opencv-python`  
- `pyautogui`  
- `speechrecognition`  
- `numpy`  

You can install them using pip:
Puedes instalarlas usando pip:

```bash
pip install -r requirements.txr
```
Setup / Configuración
Camera: Make sure you have a working webcam connected.
Cámara: Asegúrate de tener una cámara web conectada y funcionando correctamente.

Microphone: You need a microphone for voice recognition.
Micrófono: Necesitas un micrófono para usar el reconocimiento de voz.

Permissions: Ensure the program has permissions to access the camera and microphone.
Permisos: Asegúrate de que el programa tenga permisos para acceder a la cámara y el micrófono.

Usage / Uso
Run the script:
Ejecuta el script:

```bash
python english\main.py
```

or/o

```bash
python spanish\main.py
```

Mouse Control:
Control del Mouse:

Head tilt: Tilt your head left or right to move the mouse horizontally.
Inclinación de la cabeza: Mueve la cabeza hacia la izquierda o derecha para mover el mouse horizontalmente.

Vertical position: Move your head up or down to move the mouse vertically.
Posición vertical: Mueve la cabeza hacia arriba o abajo para mover el mouse verticalmente.

Click: Open your mouth to simulate a mouse click.
Clic: Abre la boca para simular un clic del mouse.

Voice Commands:
Comandos de Voz:

"Turn off computer": Shuts down the computer.
"Apagar equipo": Apaga el equipo.

"Lower the volume": Lowers the system volume.
"Baja el volumen": Reduce el volumen del sistema.

"Raise the volume": Increases the system volume.
"Sube el volumen": Aumenta el volumen del sistema.

"Open [program]": Opens the specified program (e.g., "Abrir Chrome").
"Abrir [programa]": Abre el programa especificado (por ejemplo, "Abrir Chrome").

"Close": Closes the active window.
"Cerrar": Cierra la ventana activa.

"Minimize": Minimizes all windows.
"Minimizar": Minimiza todas las ventanas.

"Down": Scrolls down on the current page.
"Bajar": Desplaza hacia abajo en la página actual.

"Up": Scrolls up on the current page.
"Subir": Desplaza hacia arriba en la página actual.

Free text: Any other recognized text will be typed in the active window.
Texto libre: Cualquier otro texto reconocido se escribirá en la ventana activa.

Exit: Press the q key in the camera window to close the program.
Salir: Presiona la tecla q en la ventana de la cámara para cerrar el programa.

## Code Structure / Estructura del Código
MediaPipe Face Mesh: Used to detect facial landmarks.
MediaPipe Face Mesh: Se utiliza para detectar los puntos de referencia faciales.

Voice Recognition: Used to interpret voice commands.
Reconocimiento de Voz: Se usa para interpretar comandos de voz.

Mouse Control: Controls mouse movement and clicks based on head position.
Control del Mouse: Se controla el movimiento del mouse y los clics en función de la posición de la cabeza.

Voice Commands: Executes specific actions based on recognized voice commands.
Comandos de Voz: Se ejecutan acciones específicas basadas en los comandos de voz reconocidos.

## Limitations / Limitaciones
Accuracy: The accuracy of mouse control and voice recognition may vary depending on the quality of the camera and microphone.
Precisión: La precisión del control del mouse y el reconocimiento de voz puede variar dependiendo de la calidad de la cámara y el micrófono.

Calibration: You may need to adjust the conversion factor (factor_conversion) for more precise mouse control.
Calibración: Es posible que necesites ajustar el factor de conversión (factor_conversion) para que el control del mouse sea más preciso.

## Contributions / Contribuciones
If you'd like to contribute to this project, feel free to fork it and submit a pull request! Any improvements or suggestions are welcome.
Si deseas contribuir a este proyecto, ¡siéntete libre de hacer un fork y enviar un pull request! Cualquier mejora o sugerencia es bienvenida.

## License / Licencia
This project is licensed under the MIT License. See the LICENSE file for details.
Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.