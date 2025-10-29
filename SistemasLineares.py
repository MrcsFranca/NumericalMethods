from numpy import array, zeros, fabs
import numpy as np

def calcDeterminante():
    print("det")

# Metodos diretos
def gaussElimination(A, results):
    numVariables = len(results)
    x = []
    for _ in range(numVariables):
        x.append(0.0)
    
    for i in range(numVariables - 1): 
        for j in range(i + 1, numVariables):
            if A[j, i] == 0:
                continue

            multiplier = A[j, i] / A[i, i]

            for k in range(i, numVariables):
                A[j, k] = A[j, k] - A[i, k] * multiplier
            results[j] = results[j] - results[i] * multiplier

    x[numVariables - 1] = results[numVariables - 1] / A[numVariables - 1, numVariables - 1]
    for i in range(numVariables - 1, -1, -1):
        aux = 0
        for j in range(i + 1, numVariables):
            aux += A[i, j] * x[j]

        x[i] = (results[i] - aux) / A[i, i]
    
    print("O resultado é:")
    for result in range(len(x)):
        print(f'x[{result}] = {x[result]}')

def partialPivoting(A, results):
    numVariables = len(results)
    x = []
    for _ in range(numVariables):
        x.append(0.0)
    
    for i in range(numVariables - 1): 
        if fabs(A[i, i]) < 1.0e-12:
            for k in range(i + 1, numVariables):
                if fabs(A[k, i]) > fabs(A[i, i]):
                    A[[i, k]] = A[[k, i]]
                    results[[i, k]] = results[[k, i]]
                    break
        for j in range(i + 1, numVariables):
            if A[j, i] == 0:
                continue

            multiplier = A[j, i] / A[i, i]

            for k in range(i, numVariables):
                A[j, k] = A[j, k] - A[i, k] * multiplier
            results[j] = results[j] - results[i] * multiplier

    x[numVariables - 1] = results[numVariables - 1] / A[numVariables - 1, numVariables - 1]
    for i in range(numVariables - 1, -1, -1):
        aux = 0
        for j in range(i + 1, numVariables):
            aux += A[i, j] * x[j]

        x[i] = (results[i] - aux) / A[i, i]
    
    print("O resultado é:")
    for result in range(len(x)):
        print(f'x[{result}] = {x[result]}')


def pivoteamentoCompleto():
    print("pivoteamento completo")

def LUDecomposition(A, results):
    numVariables = len(results)
    x = np.zeros(numVariables)
    y = np.zeros(numVariables)
    U = A
    L = np.zeros([numVariables, numVariables])
    for i in range(0, numVariables):
        for j in range(0, numVariables):
            if i == j:
                L[i, j] = 1
            if i < j:
                multiplier = A[j, i] / A[i, i]
                L[j, i] = multiplier
                for k in range(0, numVariables):
                    U[j, k] = A[j, k] - A[i, k] * multiplier

    A = np.zeros([numVariables, numVariables])
    for i in range(0, numVariables):
        for j in range(0, numVariables):
            for k in range(0, numVariables):
                A[i, j] += L[i, k] * U[k, j]

    y = np.zeros(numVariables)
    for i in range(numVariables):
        aux = 0
        for j in range(i):
            aux += L[i, j] * y[j]
        
        y[i] = results[i] - aux

    x = np.zeros(numVariables)
    for i in range(numVariables - 1, -1, -1): 
        aux = 0
        for j in range(i + 1, numVariables):
            aux += U[i, j] * x[j]
        
        x[i] = (y[i] - aux) / U[i, i]

    print("O resultado é:")
    for result in range(len(x)):
        print(f'x[{result}] = {x[result]}')

def fatoracaoCholensky():
    print("Cholensky")

def criterioDeParada():
    print("criterio de parada")

# Metodos iterativos
def convergenciaGaussJacobi():
    print("convergencia gauss jacobi")

def convergenciaGaussSeidel():
    print("convergencia seidel")

def GaussJacobi():
    print("gauss jacobi")

def GaussSeidel():
    print("gauss seidel")

def testeDeParada():
    print("teste de parada")

# Execução

if __name__ == "__main__":
    A = array([[3, 1, 0, -1],
               [1, 3, 1, 1],
               [0, 1, 3, -1],
               [-1, 1, -1, 4]], dtype=float)

    results = array([10, 15, 10, 0], dtype=float)
    """

    A = np.array([[1, 1, 1, 1],
               [1, -1, 2, -1],
               [2, 1, -1, 1],
               [3, -1, -1, -2]], dtype=float)

    results = array([5, -6, 8, -4], dtype=float)

    A = np.array([[0, 7, -1, 3, 1],
               [0, 3, 4, 1, 7],
               [6, 2, 0, 2, -1],
               [2, 1, 2, 0, 2],
               [3, 4, 1, -2, 1]], dtype=float)

    results = np.array([5, 7, 2, 3, 4], dtype=float)

    A = np.array([[4, -2, 1],
                  [20, -7, 12],
                  [-8, 13, 17]], dtype=float)

    results = np.array([5, 7, 2], dtype=float)
    """

    LUDecomposition(A, results)