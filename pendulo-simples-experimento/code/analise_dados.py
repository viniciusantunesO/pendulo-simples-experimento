import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Parâmetros que você deve ajustar conforme seu vídeo
L = 300  # comprimento do fio em pixels (meça no vídeo)

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

# Calcular ponto de equilíbrio x (posição média)
x_eq = np.nanmean(x)

# Calcular deslocamento horizontal e ângulo em radianos
dx = np.array(x) - x_eq
ratio = dx / L
ratio = np.clip(ratio, -1, 1)  # Evitar valores inválidos
theta = np.arcsin(ratio)

# Função do modelo movimento harmônico amortecido
def modelo_oha(t, A, b, w, phi):
    return A * np.exp(-b * t) * np.cos(w * t + phi)

# Remover nan para ajuste
mask = ~np.isnan(theta)
tempo_fit = np.array(tempo)[mask]
theta_fit = theta[mask]

# Chute inicial dos parâmetros: amplitude, amortecimento, frequência angular, fase
param_inicial = [max(abs(theta_fit)), 0.1, 2*np.pi, 0]

# Ajuste dos parâmetros
param_ajustado, cov = curve_fit(modelo_oha, tempo_fit, theta_fit, p0=param_inicial)

A, b, w, phi = param_ajustado

print(f"Ajuste concluído:")
print(f"Amplitude (rad): {A:.3f}")
print(f"Amortecimento (b): {b:.3f}")
print(f"Frequência angular (ω): {w:.3f} rad/s")
print(f"Frequência (f): {w/(2*np.pi):.3f} Hz")
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
    
