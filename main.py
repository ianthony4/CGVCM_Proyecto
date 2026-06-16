import cv2
import math

def overlay_image_alpha(img, img_overlay, x, y):
    """
    Superpone img_overlay sobre img en la posición (x, y) 
    respetando el canal de transparencia (alpha).
    """
    if img_overlay.shape[2] < 4:
        return img
    
    h, w, _ = img_overlay.shape
    
    y1, y2 = max(0, y), min(img.shape[0], y + h)
    x1, x2 = max(0, x), min(img.shape[1], x + w)

    y1o, y2o = max(0, -y), min(h, img.shape[0] - y)
    x1o, x2o = max(0, -x), min(w, img.shape[1] - x)

    if y1 >= y2 or x1 >= x2 or y1o >= y2o or x1o >= x2o:
        return img

    img_crop = img[y1:y2, x1:x2]
    img_overlay_crop = img_overlay[y1o:y2o, x1o:x2o]

    alpha = img_overlay_crop[:, :, 3] / 255.0
    alpha_inv = 1.0 - alpha

    for c in range(3):
        img_crop[:, :, c] = (alpha * img_overlay_crop[:, :, c] +
                             alpha_inv * img_crop[:, :, c])
                             
    return img

def main():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    # Cargar lente de sol
    lentes_img = cv2.imread('assets/lente_sol.png', cv2.IMREAD_UNCHANGED)
    if lentes_img is None:
        print("Error: No se encontró 'assets/lente_sol.png'.")
        return

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: No se pudo acceder a la camara.")
        return

    print("camara iniciada, presiona 'q' para salir")

    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Deteccion de rostro
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))
        
        for (x, y, w, h) in faces:
            # anchura para que se ajusten al rostro
            glasses_width = int(w * 1.05)
            
            # proporción de las lentes para mantener la relación de aspecto
            gh, gw, _ = lentes_img.shape
            ratio = glasses_width / gw
            glasses_height = int(gh * ratio)
            
            # Redimensionar
            resized_glasses = cv2.resize(lentes_img, (glasses_width, glasses_height))
            
            # Buscar ojos dentro del rostro para ajustar la altura y rotación 
            roi_gray = gray[y:y+int(h/2), x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=5)
            
            angle = 0
            # Si detecta 2 ojos rotaremos los lentes
            if len(eyes) >= 2:
                # Ordenar por coordenada X los ojos
                eyes = sorted(eyes, key=lambda e: e[0])
                ex1, ey1, ew1, eh1 = eyes[0]
                ex2, ey2, ew2, eh2 = eyes[1]
                
                # Centro de los ojos
                eye1_center = (ex1 + ew1//2, ey1 + eh1//2)
                eye2_center = (ex2 + ew2//2, ey2 + eh2//2)
                
                # Calcular ángulo
                dy = eye2_center[1] - eye1_center[1]
                dx = eye2_center[0] - eye1_center[0]
                angle = math.degrees(math.atan2(dy, dx))
            
            # Rotar los lentes
            center_glasses = (glasses_width // 2, glasses_height // 2)
            M = cv2.getRotationMatrix2D(center_glasses, angle, 1.0)
            rotated_glasses = cv2.warpAffine(
                resized_glasses, M, (glasses_width, glasses_height), 
                flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0,0)
            )
            
            # Posicionar los lentes (aproximadamente en la altura de los ojos)
            pos_x = x - int(w * 0.025) 
            pos_y = y + int(h * 0.2)   
            
            # Superponer
            frame = overlay_image_alpha(frame, rotated_glasses, pos_x, pos_y)
                
        cv2.imshow('Probador Virtual AR - OpenCV', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
