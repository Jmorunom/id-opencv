import cv2
import numpy as np
import time

# Un método de callback requerido que se utiliza en la función del trackbar.
def nothing(x):
    pass

# Inicializando la captura de video de la cámara web.
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

# Crear una ventana llamada "Trackbars".
cv2.namedWindow("Trackbars")

# Ahora creamos 6 trackbars que controlarán el rango inferior y superior de
# los canales H, S y V. Los argumentos son así: Nombre del trackbar,
# nombre de la ventana, rango, función de callback. Para el canal de Hue el rango es 0-179 y
# para S y V es de 0-255.
cv2.createTrackbar("L - H", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("U - H", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)


while True:

    # Comienza a leer el video de la cámara fotograma a fotograma.
    ret, frame = cap.read()
    if not ret:
        break
    # Voltea el fotograma horizontalmente (No es necesario)
    frame = cv2.flip(frame, 1)

    # Convierte la imagen BGR a imagen HSV.
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Obtén los nuevos valores de los trackbars en tiempo real conforme el usuario los cambia.
    l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    l_v = cv2.getTrackbarPos("L - V", "Trackbars")
    u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    u_s = cv2.getTrackbarPos("U - S", "Trackbars")
    u_v = cv2.getTrackbarPos("U - V", "Trackbars")

    # Establece el rango inferior y superior de HSV según el valor seleccionado
    # por el trackbar.
    lower_range = np.array([l_h, l_s, l_v])
    upper_range = np.array([u_h, u_s, u_v])

    # Filtra la imagen y obtiene la máscara binaria, donde el color blanco representa
    # el color objetivo.
    mask = cv2.inRange(hsv, lower_range, upper_range)

    # También puedes visualizar la parte real del color objetivo (Opcional).
    res = cv2.bitwise_and(frame, frame, mask=mask)

    # Convierte la máscara binaria a una imagen de 3 canales, esto es solo para
    # poder apilarla con las otras.
    mask_3 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    # Apila la máscara, el fotograma original y el resultado filtrado.
    stacked = np.hstack((mask_3, frame, res))

    # Muestra este fotograma apilado al 40% del tamaño.
    cv2.imshow('Trackbars', cv2.resize(stacked, None, fx=0.4, fy=0.4))

    # Si el usuario presiona ESC, salir del programa.
    key = cv2.waitKey(1)
    if key == 27:
        break

    # Si el usuario presiona `s`, imprimir este arreglo.
    if key == ord('s'):

        thearray = [[l_h, l_s, l_v], [u_h, u_s, u_v]]
        print(thearray)

        # También guarda este arreglo como penval.npy.
        np.save('penval', thearray)
        break

# Liberar la cámara y destruir las ventanas.
cap.release()
cv2.destroyAllWindows()
