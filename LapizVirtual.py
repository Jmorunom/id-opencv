import cv2  # Importa la librería OpenCV para el procesamiento de imágenes y video
import numpy as np  # Importa la librería numpy para el manejo de matrices

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Abre la cámara web (índice 0), usando el controlador DirectShow para Windows

# Definición de los rangos de colores en el espacio HSV para detectar el color del lapiz virtual
colorBajo = np.array([60, 40, 27], np.uint8)  # Límite inferior del color 
colorAlto = np.array([109, 156, 112], np.uint8)  # Límite superior del color 

# Definición de los colores en formato BGR (usados para dibujar)
colorCeleste = (255, 113, 82)  # Celeste (en BGR)
colorAmarillo = (89, 222, 255)  # Amarillo (en BGR)
colorRosa = (128, 0, 255)  # Rosa (en BGR)
colorVerde = (0, 255, 36)  # Verde (en BGR)
colorLimpiarPantalla = (29, 112, 246)  # Color para el botón de limpiar pantalla (en BGR)

# Definición del grosor de las líneas para los cuadros superiores (representan los colores a dibujar)
grosorCeleste = 6
grosorAmarillo = 2
grosorRosa = 2
grosorVerde = 2

# Grosor de los rectángulos en la parte superior derecha (grosor del marcador)
grosorPeque = 6
grosorMedio = 1
grosorGrande = 1

# Variables para el marcador o lápiz virtual (color y grosor del marcador)
color = colorCeleste  # El color inicial del marcador es el celeste
grosor = 3  # El grosor inicial del marcador es 3

# Variables para almacenar la posición anterior del marcador y una imagen auxiliar
x1 = None
y1 = None
imAux = None  # Imagen auxiliar para dibujar las líneas

# Bucle principal para procesar cada fotograma del video
while True:
    ret, frame = cap.read()  # Lee un fotograma de la cámara
    if ret == False: break  # Si no se puede leer el fotograma, termina el bucle

    frame = cv2.flip(frame, 1)  # Voltea el fotograma horizontalmente para crear un espejo

    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # Convierte el fotograma de BGR a HSV
    if imAux is None: imAux = np.zeros(frame.shape, dtype=np.uint8)  # Inicializa la imagen auxiliar si aún no está definida

    # ------------------ Sección para dibujar los cuadros de selección de color y grosor en la parte superior ------------------

    # Cuadrados en la parte superior izquierda que permiten elegir el color del marcador
    cv2.rectangle(frame, (0, 0), (50, 50), colorAmarillo, grosorAmarillo)  # Cuadro amarillo
    cv2.rectangle(frame, (50, 0), (100, 50), colorRosa, grosorRosa)  # Cuadro rosa
    cv2.rectangle(frame, (100, 0), (150, 50), colorVerde, grosorVerde)  # Cuadro verde
    cv2.rectangle(frame, (150, 0), (200, 50), colorCeleste, grosorCeleste)  # Cuadro celeste

    # Rectángulo para la opción de limpiar la pantalla
    cv2.rectangle(frame, (300, 0), (400, 50), colorLimpiarPantalla, 1)
    cv2.putText(frame, 'Limpiar', (320, 20), 6, 0.6, colorLimpiarPantalla, 1, cv2.LINE_AA)
    cv2.putText(frame, 'pantalla', (320, 40), 6, 0.6, colorLimpiarPantalla, 1, cv2.LINE_AA)

    # Cuadrados en la parte superior derecha para seleccionar el grosor del marcador
    cv2.rectangle(frame, (490, 0), (540, 50), (0, 0, 0), grosorPeque)
    cv2.circle(frame, (515, 25), 3, (0, 0, 0), -1)
    cv2.rectangle(frame, (540, 0), (590, 50), (0, 0, 0), grosorMedio)
    cv2.circle(frame, (565, 25), 7, (0, 0, 0), -1)
    cv2.rectangle(frame, (590, 0), (640, 50), (0, 0, 0), grosorGrande)
    cv2.circle(frame, (615, 25), 11, (0, 0, 0), -1)

    # ------------------------ Fin de la sección de selección de color y grosor --------------------------

    # Detección del color (el color del marcador)
    maskColor = cv2.inRange(frameHSV, colorBajo, colorAlto)  # Crea una máscara con el rango de color celeste
    maskColor = cv2.erode(maskColor, None, iterations=1)  # Erosiona la máscara para reducir el ruido
    maskColor = cv2.dilate(maskColor, None, iterations=2)  # Dila la máscara para aumentar el área
    maskColor = cv2.medianBlur(maskColor, 13)  # Aplica un desenfoque mediano para suavizar la máscara
    cnts, _ = cv2.findContours(maskColor, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # Encuentra los contornos en la máscara
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:1]  # Ordena los contornos por área y toma el más grande

    # Recorre los contornos encontrados
    for c in cnts:
        area = cv2.contourArea(c)  # Calcula el área del contorno
        if area > 1000:  # Si el área es suficientemente grande
            x, y2, w, h = cv2.boundingRect(c)  # Obtiene el rectángulo delimitador del contorno
            x2 = x + w // 2  # Calcula el centro del contorno en el eje x

            # Cambia el color y grosor según la posición del centro (x2, y2)
            if x1 is not None:
                if 0 < x2 < 50 and 0 < y2 < 50:  # Si está en el área del color amarillo
                    color = colorAmarillo  # Cambia el color a amarillo
                    grosorAmarillo = 6
                    grosorRosa = 2
                    grosorVerde = 2
                    grosorCeleste = 2
                if 50 < x2 < 100 and 0 < y2 < 50:  # Si está en el área del color rosa
                    color = colorRosa  # Cambia el color a rosa
                    grosorAmarillo = 2
                    grosorRosa = 6
                    grosorVerde = 2
                    grosorCeleste = 2
                if 100 < x2 < 150 and 0 < y2 < 50:  # Si está en el área del color verde
                    color = colorVerde  # Cambia el color a verde
                    grosorAmarillo = 2
                    grosorRosa = 2
                    grosorVerde = 6
                    grosorCeleste = 2
                if 150 < x2 < 200 and 0 < y2 < 50:  # Si está en el área del color celeste
                    color = colorCeleste  # Cambia el color a celeste
                    grosorAmarillo = 2
                    grosorRosa = 2
                    grosorVerde = 2
                    grosorCeleste = 6
                if 490 < x2 < 540 and 0 < y2 < 50:  # Si está en el área del grosor pequeño
                    grosor = 3  # Cambia el grosor del lápiz a pequeño
                    grosorPeque = 6
                    grosorMedio = 1
                    grosorGrande = 1
                if 540 < x2 < 590 and 0 < y2 < 50:  # Si está en el área del grosor medio
                    grosor = 7  # Cambia el grosor del lápiz a medio
                    grosorPeque = 1
                    grosorMedio = 6
                    grosorGrande = 1
                if 590 < x2 < 640 and 0 < y2 < 50:  # Si está en el área del grosor grande
                    grosor = 11  # Cambia el grosor del lápiz a grande
                    grosorPeque = 1
                    grosorMedio = 1
                    grosorGrande = 6
                if 300 < x2 < 400 and 0 < y2 < 50:  # Si está en el área de limpiar pantalla
                    cv2.rectangle(frame, (300, 0), (400, 50), colorLimpiarPantalla, 2)
                    cv2.putText(frame, 'Limpiar', (320, 20), 6, 0.6, colorLimpiarPantalla, 2, cv2.LINE_AA)
                    cv2.putText(frame, 'pantalla', (320, 40), 6, 0.6, colorLimpiarPantalla, 2, cv2.LINE_AA)
                    imAux = np.zeros(frame.shape, dtype=np.uint8)  # Limpia la pantalla

                # Dibuja la línea del marcador
                if 0 < y2 < 60 or 0 < y1 < 60:
                    imAux = imAux  # No dibuja la línea si está dentro del área superior (eligiendo colores y grosor)
                else:
                    imAux = cv2.line(imAux, (x1, y1), (x2, y2), color, grosor)  # Dibuja la línea del marcador

            cv2.circle(frame, (x2, y2), grosor, color, 3)  # Dibuja un círculo en la posición actual
            x1 = x2  # Actualiza las coordenadas del marcador
            y1 = y2
        else:
            x1, y1 = None, None  # Si el área es demasiado pequeña, no se hace nada

    # Procesamiento de la imagen auxiliar para superponerla en el fotograma
    imAuxGray = cv2.cvtColor(imAux, cv2.COLOR_BGR2GRAY)  # Convierte la imagen auxiliar a escala de grises
    _, th = cv2.threshold(imAuxGray, 10, 255, cv2.THRESH_BINARY)  # Aplica un umbral binario
    thInv = cv2.bitwise_not(th)  # Invierte la máscara binaria
    frame = cv2.bitwise_and(frame, frame, mask=thInv)  # Aplica la máscara invertida al fotograma
    frame = cv2.add(frame, imAux)  # Suma la imagen auxiliar al fotograma para dibujar las líneas

    # Muestra el fotograma final con las líneas dibujadas y la imagen auxiliar
    cv2.imshow('maskColor', maskColor)  # (Opcional) Muestra la máscara del color
    cv2.imshow('imAux', imAux)  # Muestra la imagen auxiliar
    cv2.imshow('frame', frame)  # Muestra el fotograma final

    k = cv2.waitKey(1)  # Espera por una tecla
    if k == 27:  # Si se presiona la tecla Esc (código 27), termina el bucle
        break

cap.release()  # Libera la cámara
cv2.destroyAllWindows()  # Cierra todas las ventanas abiertas
