import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Configurar os dados iniciais
theta = np.linspace(0, 2 * np.pi, 100)
raio_inicial = 1

# Criar a figura e o eixo polar
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
linha, = ax.plot(theta, np.full_like(theta, raio_inicial))

# Configurar os limites do gráfico
ax.set_ylim(0, 2)  # Ajustar o limite do raio para ver a animação

# Função de inicialização
def init():
    linha.set_ydata(np.full_like(theta, raio_inicial))  # Inicializar com o raio inicial
    return linha,
init()

# Função de atualização
def update(frame):
    raio = 1 + 0.5 * np.sin(frame / 10.0)  # Varia o raio para expandir e contrair
    linha.set_ydata(np.full_like(theta, raio))  # Atualiza os dados de y
    return linha,

# Criar a animação
ani = FuncAnimation(fig, update, frames=range(200), init_func=init, blit=True, interval=50)

# Mostrar o gráfico
plt.show()
