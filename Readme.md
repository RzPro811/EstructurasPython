# ESTRUCTURAS PYTHON

hecho por **RzPro811**

version 1.0

Hecho por mero aburrimiento, para pasar el rato.

## INDICE

0. TypeStruct/DataStruct
1. Vector
2. Matriz
3. Lista
4. Cola/Pila
5. Heap
6. Ordenador/Visualizador
7. Grafo/Digrafo
8. Vector Algebraico
9. Matriz Algebraica
10. Validaciones y Excepciones


## Estructuras

### 0. Type/Data Struct
    

Estas estructuras son heredables, diseñados para crear estructuras de datos de un solo tipo, especificamente.

-   **TypeStruct**:
    
    Este TDA recibe un tipo de dato (type). Luego, incluye un metodo "privado" (totalmente publico) el cual recibe datos que filtran los que no sean del tipo ingresado por constructor.

    De este Objeto, heredan:
    -   DataStruct
    -   Vector
    -   Matriz
    -   Lista
    -   Cola
    -   Pila
    -   Heap

    **Constructor**
    -   
    ```python

    tipo = int #Ingresa un tipo de dato, por ejemeplo int

    ts = TypeStruct(tipo)
    
    ```

    **Metodos**
    -   
    - ```getType()```: 
        -   Obtiene el tipo de dato que filtra el TypeStruct
    - ```getTypeName()```: 
        -   Obtiene un string con el nombre del tipo de dato
    - ```__validarEntrada__(entrada, permitirNone)```:  
        -   Recibe una entrada y valida que sea del tipo que se ingreso, sino, saltará un ```TypeError```
        -   permitirNone por defecto está en False. Si se activa, no saltará error al ingresar un None
        -   Se recomienda usar dentro de las estructuras que hereden TypeStruct
    - ```__validarEntradas__(*entradas, permitirNone)```:
        -   Es exactamente lo mismo que validarEntrada, pero recibe más de un elemento para validar
        -   Tambien es para uso interno de las estructuras que usan TypeStruct 

-   **DataStruct**
    
    Este TDA fue creado para, que de él, herenden metodos y un funcionamiento interno las estructuras que estén diseñadas para almacenar un solo elemento. Por ejemplo, los nodos de una lista o las semillas de un arbol. Tambien Hereda de TypeStruct, así cuenta con los mismos metodos

    **Constructor**
    -   
    ```python
    tipo = int #Tipo de dato que se almacena
    dato = 1 #El dato que se almacena

    ds = DataStruct(tipo, dato, permitirNone)
    #Permitir None es False, por defecto
    ```

    **Metodos**
    -   
    -   ```getDato()```
        -   Obtiene el dato almacenado
    -   ```setDato(dato)```
        -   Almacena el dato ingresado
        -   Si permitirNone se configuro como True, entonces se puede introducir un None.
        -   Este metodo se puede usar en cualquier momento para alterar el dato almacenado en el dataStruct
    -   **MetodosHeredados**
        -   ```getType()```
        -   ```getTypeName()```
        -   ```__validarEntrada__()```
        -   ```__validarEntradas__()```

    #

### 1. Vector

Tipo de estructura lineal. Una terna de datos de principio a fin, almacenados en fila desde una poscicion hasta la ultima en algun lugar de la memoria.