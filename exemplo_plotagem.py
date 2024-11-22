import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

# TESTE DO CÓDIGO
Nr = 10
Nt = 36

# Exemplo de dados de temperatura (Nr pontos de raio, Nt pontos de ângulo)
raios = np.linspace(0, 1, Nr)
theta = np.linspace(0, 2 * np.pi, Nt)
temperaturas = np.outer(np.linspace(100, 10, Nr), np.ones(Nt))

# Criar o grid em coordenadas polares
Theta, Raios = np.meshgrid(theta, raios)

# Criar o mapa de calor
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
c = ax.contourf(Theta, Raios, temperaturas, cmap='viridis', norm=Normalize(vmin=temperaturas.min(), vmax=temperaturas.max()))

# Adicionar a barra de cores (legenda)
cb = fig.colorbar(c, ax=ax, orientation='vertical', pad=0.1)
cb.set_label('Temperatura (°C)')

# Configurações do gráfico
ax.set_title('Distribuição de Temperatura em Coordenadas Polares')
plt.show()