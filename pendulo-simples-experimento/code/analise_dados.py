import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Constantes do experimento
g = 9.8            # aceleração da gravidade (m/s^2)
L_cm = 40          # comprimento do fio em cm (medido)
L = L_cm / 100     # converter para metros

# Listas para armazenar dados
tempo = []
x = []
y = []

# Leitura do CSV
with open('data/posicoes.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        tempo.append(float(row['tempo']))
        try:
            x.append(float(row['x']))
        except:
            x.append(np.nan)
        try:
            y.append(float(row['y']))
        except:
            y.append(np.nan)

# Ponto de equilíbrio (média do x)
x_eq = np.nanmean(x)

# Comprimento do fio em pixels (meça no vídeo, ex: 300 pixels)
L_pixels = 300

# Calcular ângulo em radianos
dx = np.array(x) - x_eq
ratio = dx / L_pixels
ratio = np.clip(ratio, -1, 1)
theta = np.arcsin(ratio)

# Modelo do movimento harmônico amortecido
def modelo_oha(t, A, b, w, phi):
    return A * np.exp(-b * t) * np.cos(w * t + phi)

# Filtrar nan para ajuste
mask = ~np.isnan(theta)
tempo_fit = np.array(tempo)[mask]
theta_fit = theta[mask]

# Chute inicial para os parâmetros
param_inicial = [max(abs(theta_fit)), 0.1, 2*np.pi, 0]

# Ajuste do modelo aos dados
param_ajustado, cov = curve_fit(modelo_oha, tempo_fit, theta_fit, p0=param_inicial)

A, b, w, phi = param_ajustado

# Calcular frequência experimental (Hz)
f_exp = w / (2 * np.pi)

# Calcular frequência teórica do pêndulo simples (Hz)
f_teor = (1 / (2 * np.pi)) * np.sqrt(g / L)

# Calcular fator de qualidade Q
Q = w / (2 * b)

# Resultados
print(f"Ajuste concluído:")
print(f"Amplitude (rad): {A:.3f}")
print(f"Amortecimento (b): {b:.3f}")
print(f"Frequência angular (ω): {w:.3f} rad/s")
print(f"Frequência experimental (f): {f_exp:.3f} Hz")
print(f"Frequência teórica (f₀): {f_teor:.3f} Hz")
print(f"Fator de qualidade (Q): {Q:.3f}")
print(f"Fase (φ): {phi:.3f} rad")

# Plotar dados e ajuste
plt.figure(figsize=(10,6))
plt.plot(tempo_fit, theta_fit, 'b.', label='Dados (ângulo)')
plt.plot(tempo_fit, modelo_oha(tempo_fit, *param_ajustado), 'r-', label='Ajuste')
plt.xlabel('Tempo (s)')
plt.ylabel('Ângulo (rad)')
plt.title('Movimento Harmônico Amortecido do Pêndulo')
plt.legend()
plt.grid()
plt.show()
