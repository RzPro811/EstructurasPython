from src.Estructuras.Vector import Matriz

matriz:Matriz[int] = Matriz(int, 3,4)

for i in range(4):
    for j in range(3):
        matriz.setItem(j,i,j*4+i) 


print(matriz.getColumna(1))
