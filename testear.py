from src.Estructuras.Vector import Vector
from src.Estructuras.Validaciones import validarTipoObjeto

vector:Vector[int] = Vector(int, 10, True)

for i in range(20):
    vector.agregar(i)

for i in range(20):
    numero = vector.quitar()
    print(numero)

print(vector)
