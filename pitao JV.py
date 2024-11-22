# Importação das bibliotecas necessárias
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.animation import FuncAnimation

# Definição dos parâmetros do problema
Sn0 = 47.8 # Taxa volumétrica de produção de calor no centro
a = 1   # Constante arbitrária para a relação com o tempo
b = 1   # Constante arbitrária para a relação com o raio
Rf = 10  # Raio do elemento físsil
Rc = 12  # Raio do cladding
kf = 40  # Condutividade térmica do elemento físsil
kc = 40  # Condutividade térmica do cladding

# Divisão da malha de raio
Nr = 100             # Número de pontos de raio a serem calculados
dr = Rf / (Nr-1)    # Delta(r)

# Definição da função fonte de calor
def Sn(raio,tempo):
    return  Sn0*(1 + b*(raio/Rf)**2) + a*np.exp(tempo)

# Criação das matrizes não populadas
A = np.zeros((Nr, Nr))
B = np.zeros(Nr)

# Adicionando coeficientes nas matrizes A e B
t = 0
def pop(t):
    for i in range(Nr-1):
        for j in range(Nr):
            if j == i-1:
                A[i,j] = i**2 - i
            if j == i:
                A[i,j] = - 2*i ** 2
            if j == i+1:
                A[i,j] = i**2 + i
    for i in range(Nr):
        r = i*dr
        B[i] = - Sn(r,t) * r**2 / kf
    A[0,0] = A[Nr-1,Nr-1] = 1   # Condições de contorno
    B[Nr-1] = 10    # Temperatura externa constante
pop(t)

# Resolvendo o sistema linear
T = np.linalg.solve(A,B)

# Configurando o gráfico
fig, ax = plt.subplots(subplot_kw= {'projection': 'polar'})
Nt = 36     # Número de pontos de ângulos
raios = np.linspace(0, Rf, Nr)      # Vetor com todos os raios
theta = np.linspace(0, 2 * np.pi, Nt)       # Vetor com todos os ângulos
Temperaturas = np.outer(T, np.ones(Nt))
Theta, Raios = np.meshgrid(theta, raios)
mapa = ax.contourf(Theta, Raios, Temperaturas, cmap= 'viridis', norm= Normalize(vmin = Temperaturas.min(), vmax = Temperaturas.max()))    # Geração do mapa de temperaturas
legenda = fig.colorbar(mapa, ax= ax, orientation = 'vertical', pad= 0.2)
legenda.set_label('Temperatura (°C)')
ax.set_title('Heat conduction with a nuclear heat source', pad= 50)

# Função de atualização
def update(tempo):
    pop(tempo)
    T = np.linalg.solve(A,B)
    Temperaturas = np.outer(T, np.ones(Nt))
    for coll in ax.collections:
        coll.remove()
    ax.contourf(Theta, Raios, Temperaturas, cmap='viridis')
    return ax.collections

# Criar a animação
ani = FuncAnimation(fig, update, frames=range(100), interval=1000)

# Mostrar o gráfico
plt.show()
