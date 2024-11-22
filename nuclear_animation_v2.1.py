# Importação das bibliotecas necessárias
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle

# Definição dos parâmetros do problema
Sn0 = 50 # Taxa volumétrica de produção de calor no centro
a = 20   # Constante arbitrária para a relação com o tempo
b = 5   # Constante arbitrária para a relação com o raio
Rf = 100  # Raio do elemento físsil
Rc = 120  # Raio do cladding
kf = 2  # Condutividade térmica do elemento físsil
kc = 235  # Condutividade térmica do cladding

# Divisão da malha de raio
Nr = 1000             # Número de pontos de raio a serem calculados
dr = Rc / (Nr-1)    # Delta(r)

# Definição da função fonte de calor
def Sn(raio,tempo):
    return  Sn0*(1 + b*(raio/Rf)**2) + a*(np.tanh(tempo - np.e) + 1)

# Criação das matrizes não populadas
A = np.zeros((Nr, Nr))
B = np.zeros(Nr)

# Populando a matriz A (constante no tempo para nossa aproximação)
t = 0
for i in range(Nr-1):
    for j in range(Nr):
        if j == i-1:
            A[i,j] = i**2 - i
        if j == i:
            A[i,j] = - 2*i ** 2
        if j == i+1:
            A[i,j] = i**2 + i
A[0,0] = A[Nr-1,Nr-1] = 1   # Condições de contorno

# Populando a matriz B (variante no tempo)
def popB(t):
    for i in range(Nr):
        r = i*dr
        if r <= Rf:
            B[i] = - Sn(r,t) * r**2 / kf
B[Nr-1] = 20    # Temperatura externa
popB(t)

# Resolvendo o sistema linear
T = np.linalg.solve(A,B)
T[0] = T[1]

# Definir limites de cores
temperatura_min = T.min()
temperatura_max = T.max()

# Configurando o gráfico
color_map = 'coolwarm'
fig, ax = plt.subplots(subplot_kw= {'projection': 'polar'})
Nt = 36     # Número de pontos de ângulos
raios = np.linspace(0, Rc, Nr)      # Vetor com todos os raios
theta = np.linspace(0, 2 * np.pi, Nt)       # Vetor com todos os ângulos
Temperaturas = np.outer(T, np.ones(Nt))
Theta, Raios = np.meshgrid(theta, raios)
mapa = ax.contourf(Theta, Raios, Temperaturas, levels= 50, cmap= color_map, vmin=temperatura_min, vmax=temperatura_max)    # Geração do mapa de temperaturas
legenda = fig.colorbar(mapa, ax= ax, orientation = 'vertical', pad= 0.05)
legenda.set_label('Temperatura (°C)', labelpad=30 , fontsize=15)
ax.set_title('Heat conduction with a nuclear heat source' , pad= 50, fontsize=20)

# Marcando a camada de isolamento
def marcar():
    circle1 = Circle((0, 0), Rf, transform=ax.transData._b, fill=False, linewidth=1)
    circle2 = Circle((0,0), Rc, transform=ax.transData._b, fill=False, linewidth=1)
    ax.add_patch(circle1)
    ax.add_patch(circle2)
marcar()

# Função de atualização
def update(tempo):
    popB(tempo/10)
    T = np.linalg.solve(A,B)
    T[0] = T[1]
    Temperaturas = np.outer(T, np.ones(Nt))
    for coll in ax.collections:
        coll.remove()
    ax.contourf(Theta, Raios, Temperaturas, levels=100 , cmap= color_map, vmin=temperatura_min, vmax=temperatura_max)
    marcar()
    return ax.collections

# Criar a animação
ani = FuncAnimation(fig, update, frames=range(60), interval= 60)

# Mostrar o gráfico
ax.spines['polar'].set_visible(False)
ax.set_xticks([])
ax.set_yticks([])
plt.show()
