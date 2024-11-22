import numpy as np
import matplotlib.pyplot as plt

# Parâmetros
Rf = 1 # Raio final
Tf = 1 # Tempo final
a, b = 0, Rf # Intervalo em r
c, d = 0, Tf # Intervalo em t
Nr, Nt = 10, 10 # Número de pontos em r e t
hr = (b - a) / (Nr - 1) # Passo em r
ht = (d - c) / (Nt - 1) # Passo em t

# Constantes
Sn0 = 1
b = 1
kf = 1

r = np.linspace(a, b, Nr)
t = np.linspace(c, d, Nt)

# Função f(r, t)
def f(r, t):
    return Sn0*(1+np.exp(-t)+b*(r/Rf)**2)*r**2

# Matriz A e vetor B
A = np.zeros((Nr * Nt, Nr * Nt))
B = np.zeros(Nr * Nt)

# Preencher A e B
for j in range(1, Nt-1):
    for i in range(1, Nr-1):
        k = i + j * Nr
        A[k, k] = 2*i**2*kf
        A[k, k-1] = -i*kf*(i+1)
        A[k, k+1] = -i*kf*(i+1)
        B[k] = f(r[i], t[j])

# Condições de contorno (T = 0 nas bordas)
for i in range(Nr):
    A[i, i] = 1
    A[i + (Nt-1) * Nr, i + (Nt-1) * Nr] = 1
    B[i] = 0
    B[i + (Nt-1) * Nr] = 0

for j in range(Nt):
    A[j * Nr, j * Nr] = 1
    A[(j+1) * Nr - 1, (j+1) * Nr - 1] = 1
    B[j * Nr] = 0
    B[(j+1) * Nr - 1] = 0

# Resolver o sistema
Temp = np.linalg.solve(A, B)
Temp = Temp.reshape((Nt, Nr))

# Plotar a solução
R, T = np.meshgrid(r, t)
plt.contourf(R, T, Temp, 20, cmap='viridis')
plt.colorbar()
plt.title('Heat conduction with a nuclear heat source')
plt.xlabel('r')
plt.ylabel('t')
plt.show()