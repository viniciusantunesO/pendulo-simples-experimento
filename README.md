# 🧪 Projeto Experimental: Pêndulo Simples com Análise de Movimento via OpenCV

Este projeto tem como objetivo analisar o movimento de um **pêndulo simples** através da extração de dados de um vídeo utilizando **OpenCV** e ajuste com um modelo de **movimento harmônico amortecido (OHA)** em Python.

---

## 🎯 Objetivos

1. Montar um pêndulo simples e registrar seu movimento em vídeo.
2. Extrair dados de posição da massa usando processamento de imagem.
3. Analisar o comportamento oscilatório e ajustar a equação do OHA.
4. Calcular parâmetros físicos como frequência angular, amortecimento e fator de qualidade.

---

## 📹 Etapas do Experimento

1. **Construção** do pêndulo com um fio de 40 cm e uma massa de 70 g.
2. **Filmagem** do pêndulo oscilando, com plano fixo e iluminação constante.
3. **Extração de dados** usando OpenCV para detectar a posição da massa frame a frame.
4. **Análise dos dados** com Python, convertendo as posições em ângulo e ajustando o modelo físico.
5. **Geração de gráficos** e cálculo de parâmetros como frequência experimental e teórica.

---

## 🧠 Análise Física

O movimento angular do pêndulo foi descrito pelo modelo de **movimento harmônico amortecido**:

\[
\theta(t) = A \cdot e^{-bt} \cdot \cos(\omega t + \phi)
\]

Onde:
- \(A\): Amplitude angular inicial
- \(b\): Coeficiente de amortecimento
- \(\omega\): Frequência angular
- \(\phi\): Fase inicial

Além disso, foi calculado:
- A frequência teórica: \(f_0 = \frac{1}{2\pi} \sqrt{\frac{g}{L}}\)
- O fator de qualidade: \(Q = \frac{\omega}{2b}\)

---