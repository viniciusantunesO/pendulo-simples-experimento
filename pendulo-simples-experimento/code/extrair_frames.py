import cv2
import csv
import numpy as np
import os

# Garante que a pasta 'data/' exista
os.makedirs('data', exist_ok=True)


# Caminho do vídeo (ajuste se necessário)
video = 'C:/Users/Vinicius Antunes/Documents/pendulo-simples-experimento/video/WhatsApp Video 2025-06-25 at 16.00.48.mp4'

# Abre o vídeo
video_cv = cv2.VideoCapture(video)

if not video_cv.isOpened():
    print("Erro ao abrir o vídeo.")
    exit()

# FPS do vídeo
fps = video_cv.get(cv2.CAP_PROP_FPS)
print(f"FPS do vídeo: {fps}")

# Criar arquivo CSV para salvar dados
csv_file = open("data/posicoes.csv", mode='w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["frame", "tempo", "x", "y"])

frame_number = 0

while True:
    ret, frame = video_cv.read()
    if not ret:
        break

    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

    frame_number += 1
    time = frame_number / fps

    # Converter para HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Intervalo de cor verde (ajustável)
    lower_green = np.array([25, 40, 40])   # mais aberto para tons mais claros e amarelados
    upper_green = np.array([95, 255, 255]) # pega até verdes mais vibrantes e claros




    # Criar máscara para partes verdes
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Encontrar contornos
    contornos, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    x, y = None, None
    if contornos:
        maior = max(contornos, key=cv2.contourArea)
        (x_, y_), raio = cv2.minEnclosingCircle(maior)
        if raio > 5:  # Ignorar contornos muito pequenos
            x, y = int(x_), int(y_)
            cv2.circle(frame, (x, y), int(raio), (0, 0, 255), 2)  # desenha o círculo vermelho

    # Mostrar as janelas
    cv2.imshow("Máscara Verde", mask)
    cv2.imshow("Frame com Detecção", frame)

    # Tecla 'q' para sair
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

    # Salvar no CSV
    csv_writer.writerow([frame_number, time, x, y])

# Encerrar
csv_file.close()
video_cv.release()
cv2.destroyAllWindows()

