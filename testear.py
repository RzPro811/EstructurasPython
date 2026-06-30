from src.Estructuras.Vector import Matriz

matriz:Matriz[int] = Matriz(int, 3,4)

for i in range(3):
    for j in range(4):
        matriz.setItem(i,j,j*3+i)


print(matriz)

matriz.remover(2,3)

print(matriz)