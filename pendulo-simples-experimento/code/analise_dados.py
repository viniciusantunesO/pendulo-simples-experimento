import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

tempo=[]
x=[]
y=[]

with open('posicoes.csv', 'r') as csvfile:
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

plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
plt.plot(tempo, x, 'b-', label='x (horizontal)')
plt.xlabel('Tempo (s)')
plt.ylabel('Posição x (unidade de pixel)')
plt.legend()
plt.grid()

plt.subplot(1, 2, 2)
plt.plot(tempo, y, 'r-', label='y (vertical)')
plt.xlabel('Tempo (s)')
plt.ylabel('Posição y (unidade de pixel)')
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()

def modelo_oha(t, A, b, w, phi):
    return A * np.exp(-b * t) * np.cos(w * t + phi)


# remover nan dos dados para ajuste
tempo_fit = np.array(tempo)
x_fit = np.array(x)
mask = ~np.isnan(x_fit)
tempo_fit = tempo_fit[mask]
x_fit = x_fit[mask]

# chute inicial
param_inicial = [max(x_fit), 0.1, 2*np.pi, 0]

param_ajustado, cov = curve_fit(modelo_oha, tempo_fit, x_fit, p0=param_inicial)

A, b, w, phi = param_ajustado

print(f"Ajuste concluído:")
print(f"A = {A:.3f}")
print(f"b = {b:.3f}")
print(f"ω = {w:.3f}")
print(f"φ = {phi:.3f}")


plt.plot(tempo_fit, x_fit, 'b.', label='Dados')
plt.plot(tempo_fit, modelo_oha(tempo_fit, *param_ajustado), 'r-', label='Ajuste')
plt.xlabel('Tempo (s)')
plt.ylabel('Posição x (pixel)')
plt.legend()
plt.grid()
plt.show()

    
