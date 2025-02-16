import mediapipe as mp  # Importa la biblioteca MediaPipe para el procesamiento de imágenes.
import math  # Importa la biblioteca math para funciones matemáticas.
import cv2  # Importa OpenCV para la captura y procesamiento de video.
import pyautogui  # Importa pyautogui para controlar el mouse y el teclado.
import speech_recognition as sr  # Importa la biblioteca para el reconocimiento de voz.
import os  # Importa la biblioteca os para ejecutar comandos del sistema.
import time  # Importa la biblioteca time para manejar tiempos de espera.

# Inicializa la captura de video desde la cámara por defecto (índice 0).
cap = cv2.VideoCapture(0)

# Crea un objeto de reconocimiento de voz.
recognizer = sr.Recognizer()

def escribir():
    """Función para escuchar y reconocer comandos de voz."""
    with sr.Microphone() as source:  # Usa el micrófono como fuente de audio.
        audio = recognizer.listen(source)  # Escucha el audio.
        try:
            # Intenta reconocer el audio usando Google Speech Recognition en español (México).
            text = recognizer.recognize_google(audio, language="es-MX")
            return text  # Devuelve el texto reconocido.
        except sr.UnknownValueError:
            print("No se pudo entender el audio.")  # Maneja el error si no se entiende el audio.
        except sr.RequestError as e:
            print("Error de solicitud:", str(e))  # Maneja errores de solicitud.

# Verifica si la cámara se abrió correctamente.
if not cap.isOpened():
    print("Error: No se pudo abrir la cámara.")
    exit()  # Sale del programa si no se puede abrir la cámara.

# Inicializa MediaPipe Face Mesh para la detección de la malla facial.
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils  # Utilidades para dibujar en la imagen.

# Factor de conversión para ajustar la distancia medida a centímetros (ajustar según calibración).
factor_conversion = 100  # Por ejemplo, 100 píxeles = 1 cm

# Inicia el Face Mesh.
with mp_face_mesh.FaceMesh() as face_mesh:
    while True:  # Bucle principal para procesar cada cuadro de video.
        ret, frame = cap.read()  # Lee un cuadro de la cámara.
        if not ret:
            print("Error: No se pudo leer el marco.")
            break  # Sale del bucle si no se puede leer el cuadro.
        
        frame = cv2.flip(frame, 1)  # Voltea el cuadro horizontalmente para una vista espejo.
        
        height, width, _ = frame.shape  # Obtiene las dimensiones del cuadro.
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convierte el cuadro a RGB.
        results = face_mesh.process(frame_rgb)  # Procesa el cuadro para detectar la malla facial.
        
        referencia = height // 2  # Define una línea de referencia en el centro vertical del cuadro.
        
        if results.multi_face_landmarks:  # Verifica si se detectaron rostros.
            for face_landmarks in results.multi_face_landmarks:  # Itera sobre cada rostro detectado.
                # Extrae las coordenadas de los puntos de referencia de la malla facial.
                x_nariz = face_landmarks.landmark[1].x
                y_nariz = face_landmarks.landmark[1].y
                
                x_frente = face_landmarks.landmark[9].x
                y_frente = face_landmarks.landmark[9].y
                
                x_cachete = face_landmarks.landmark[13].x
                y_cachete = face_landmarks.landmark[13].y
                
                x_cachete1 = face_landmarks.landmark[14].x
                y_cachete1 = face_landmarks.landmark[14].y
                
                # Dibuja los puntos de referencia en el cuadro.
                cv2.circle(frame, (int(width // 2), int(referencia)), 1, (0, 0, 0), 2)  # Línea de referencia.
                cv2.circle(frame, (int(x_cachete * frame.shape[1]), int(y_cachete * frame.shape[0])), 1, (255, 0, 0), 2)  # Cachete izquierdo.
                cv2.circle(frame, (int(x_cachete1 * frame.shape[1]), int(y_cachete1 * frame.shape[0])), 1, (255, 0, 0), 2)  # Cachete derecho.
                cv2.circle(frame, (int(x_nariz * frame.shape[1]), int (y_nariz * frame.shape[0])), 1, (0, 255, 0), 2)  # Nariz.
                cv2.circle(frame, (int(x_frente * frame.shape[1]), int(y_frente * frame.shape[0])), 1, (0, 0, 255), 2)  # Frente.
                cv2.line(frame, (int(x_nariz * frame.shape[1]), int(y_nariz * frame.shape[0])), (int(x_frente * frame.shape[1]), int(y_frente * frame.shape[0])), (255, 0, 0), 2)  # Línea entre nariz y frente.
                
                # Calcula la inclinación de la cabeza.
                vector_x = x_nariz - x_frente  # Diferencia en la dirección x.
                vector_y = y_nariz - y_frente  # Diferencia en la dirección y.
                inclinacion = math.degrees(math.atan2(vector_y, vector_x))  # Convierte a grados.
                
                # Obtiene la posición actual del mouse.
                pocision_mouse = pyautogui.position()
                x_mouse = pocision_mouse[0]  # Coordenada x del mouse.
                y_mouse = pocision_mouse[1]  # Coordenada y del mouse.
                
                scroll = False  # Variable para controlar el desplazamiento.
                
                # Interpretación del ángulo de inclinación para mover el mouse.
                if inclinacion < 85:  # Si la inclinación es menor a 85 grados, mueve el mouse a la derecha.
                    x_mouse += 10
                elif inclinacion > 95:  # Si la inclinación es mayor a 95 grados, mueve el mouse a la izquierda.
                    x_mouse -= 10
                
                # Controla el movimiento vertical del mouse basado en la posición de la nariz.
                if y_nariz * frame.shape[0] > referencia + 10:  # Si la nariz está por debajo de la referencia, mueve el mouse hacia abajo.
                    y_mouse += 10
                elif y_nariz * frame.shape[0] < referencia - 10:  # Si la nariz está por encima de la referencia, mueve el mouse hacia arriba.
                    y_mouse -= 10
                
                # Mueve el mouse a la nueva posición calculada.
                pyautogui.moveTo(x_mouse, y_mouse, 0.1)  # Mueve el mouse suavemente a la nueva posición.
                
                # Verifica si la boca está abierta midiendo la distancia entre los cachetes.
                distancia_boca = math.sqrt((x_cachete1 - x_cachete) ** 2 + (y_cachete1 - y_cachete) ** 2)  # Calcula la distancia entre los cachetes.
                distancia_boca = distancia_boca * factor_conversion  # Convierte la distancia a centímetros.
                
                if distancia_boca > 2:  # Si la boca está abierta, simula un clic del mouse.
                    pyautogui.click()
                
                # Reconocimiento de comandos de voz si la boca está muy abierta.
                if distancia_boca > 4:  # Si la boca está muy abierta, escucha un comando de voz.
                    texto = str(escribir())  # Llama a la función para reconocer el comando de voz.
                    # Ejecuta acciones basadas en el comando de voz reconocido.
                    if texto.lower() == "apagar equipo":
                        os.system("shutdown -s")  # Apaga el equipo.
                    elif texto.lower() == "baja el volumen":
                        pyautogui.press("volumedown")  # Baja el volumen.
                    elif texto.lower() == "sube el volumen":
                        pyautogui.press("volumeup")  # Sube el volumen.
                    elif "abrir" in texto.lower():  # Si el comando es abrir un programa.
                        programa = texto.lower().replace("abrir", "").strip()  # Extrae el nombre del programa.
                        pyautogui.press("win")  # Abre el menú de inicio.
                        pyautogui.write(programa)  # Escribe el nombre del programa.
                        time.sleep(5)  # Espera un momento para que el programa se abra.
                        pyautogui.press("enter")  # Presiona Enter para abrir el programa.
                    elif texto.lower() == "cerrar":
                        pyautogui.hotkey("alt", "f4")  # Cierra la ventana activa.
                    elif texto.lower() == "minimizar":
                        pyautogui.hotkey("win", "m")  # Minimiza todas las ventanas.
                    elif texto.lower() == "bajar":
                        pyautogui .scroll(-1000)  # Desplaza hacia abajo.
                    elif texto.lower() == "subir":
                        pyautogui.scroll(1000)  # Desplaza hacia arriba.
                    else:  # Si el comando no es reconocido, escribe el texto.
                        for letra in texto:  # Itera sobre cada letra del texto.
                            pyautogui.press(letra)  # Presiona cada letra.
                        pyautogui.press("enter")  # Presiona Enter para enviar el texto.
                
        cv2.imshow('Face Mesh', frame)  # Muestra el cuadro procesado con la malla facial.

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Si se presiona la tecla 'q', sale del bucle.
            break

cap.release()  # Libera la captura de video.
cv2.destroyAllWindows()  # Cierra todas las ventanas de OpenCV.