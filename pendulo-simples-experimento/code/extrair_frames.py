import cv2
import csv

# Caminho do vídeo (ajuste se necessário)
video = "C:/Users/Vinicius Antunes/Documents/pendulo-simples-experimento/video/WhatsApp Video 2025-06-23 at 16.32.36.mp4"

# Abre o vídeo
video_cv = cv2.VideoCapture(video)

# Verifica se conseguiu abrir
if not video_cv.isOpened():
    print("Erro ao abrir o vídeo")
    exit()

# Lê o FPS
fps = video_cv.get(cv2.CAP_PROP_FPS)
print(f"FPS do vídeo: {fps}")

# Prepara CSV para salvar posições
csv_file = open("posicoes.csv", mode='w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["frame", "tempo", "x", "y"])  # cabeçalho

frame_number = 0

while True:
    ret, frame = video_cv.read()
    if not ret:
        break

    frame_number += 1
    time = frame_number / fps

    # Converte o frame para HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Faixa de cor verde (ajuste se necessário)
    lower_green = (40, 40, 40)
    upper_green = (80, 255, 255)
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Encontra os contornos
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    x, y = None, None
    if contours:
        # Pega o maior contorno (provavelmente a bolinha)
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
        if M["m00"] != 0:
            x = int(M["m10"] / M["m00"])
            y = int(M["m01"] / M["m00"])
            # Desenha um ponto vermelho no centro da bolinha
            cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)

    # Salva no CSV
    csv_writer.writerow([frame_number, time, x, y])

    # Mostra o frame com a detecção (opcional)
    cv2.imshow("Frame", frame)

    # Sai do loop se apertar 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Fecha tudo
csv_file.close()
video_cv.release()
cv2.destroyAllWindows()


