import numpy as np
import math

def openFile(file):
    matList = []
    try:
        with open(file, "r") as file:
            for line in file:
                blankLine = line.strip()

                if not blankLine or blankLine.startswith('#'):
                    continue

                numsStr = blankLine.split()
                numsFloat = [float(num) for num in numsStr]
                matList.append(numsFloat)

    except FileNotFoundError:
        print(f"O arquivo '{file}' não foi encontrado")
        return None, None
    except ValueError:
        print(f"O arquivo '{file}' contém caracteres inválidos")
        return None, None

    if not matList:
        print("Arquivo vazio ou não lido")
        return None, None

    matrix = np.array(matList, dtype=float)
    A = matrix[:, :-1]
    results = matrix[:, -1]
    print("matriz A")
    print(A)
    print("resultados")
    print(results)

    return A, results

def subDeterminant(A):
    n = len(A)
    subMatrixList = []
    for subSize in (0, n):
        subMatrix = A[0:subSize, 0:subSize]
        subMatrixList.append(np.linalg.det(subMatrix))
    return subMatrixList

# Metodos diretos
def gaussElimination(A, results):
    if np.linalg.det(A) == 0:
        return "A matriz tem determinante igual a 0, logo não tem solução por este método"

    numVariables = len(results)
    x = []
    x = np.zeros(numVariables)
    
    for i in range(numVariables - 1): 
        for j in range(i + 1, numVariables):
            if A[i, i] == 0:
                return "Foi encontrada um divisão por 0"
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
    if np.linalg.det(A) == 0:
        return "A matriz tem determinante igual a 0, logo não tem solução por este método"

    numVariables = len(results)
    x = np.zeros(numVariables)
    
    for i in range(numVariables):
        pivotLine = i
        maxValue = math.fabs(A[i, i])
        for j in range(i + 1, numVariables):
            if math.fabs(A[j, i]) > maxValue:
                pivotLine = j
                maxValue = math.fabs(A[j, i])
        if pivotLine != i:
            A[[i, pivotLine]] = A[[pivotLine, i]]
            results[[i, pivotLine]] = results[[pivotLine, i]]

        pivot = A[i, i]

        if pivot == 0:
            return "Foi encontrada um divisão por 0"

        for j in range(i + 1, numVariables):
            if A[j, i] == 0:
                continue
            
            multiplier = A[j, i] / pivot
            A[j] = A[j] - A[i] * multiplier
            results[j] = results[j] - results[i] * multiplier

    x[numVariables - 1] = results[numVariables - 1] / A[numVariables - 1, numVariables - 1]
    for i in range(numVariables - 2, -1, -1):
        aux = 0
        for j in range(i + 1, numVariables):
            aux += A[i, j] * x[j]

        x[i] = (results[i] - aux) / A[i, i]

    print("O resultado é:")
    for result in range(len(x)):
        print(f'x[{result}] = {x[result]}')
    
    return x

def completePivoting(A, results):
    if np.linalg.det(A) == 0:
        return "A matriz tem determinante igual a 0, logo não tem solução por este método"

    numVariables = len(results)
    x = np.zeros(numVariables)

    changeCol = np.arange(numVariables)

    for i in range(numVariables - 1):
        pivotLine = i
        pivotColumn = i
        maxValue = math.fabs(A[i, i])

        for j in range(i, numVariables):
            for k in range(i, numVariables):
                if math.fabs(A[j, k]) > maxValue:
                    pivotLine = j
                    pivotColumn = k
                    maxValue = math.fabs(A[j, k])
                
        if pivotLine != i:
            A[[i, pivotLine]] = A[[pivotLine, i]]
            results[[i, pivotLine]] = results[[pivotLine, i]]

        if pivotColumn != i:
            A[:, [i, pivotColumn]] = A[:, [pivotColumn, i]]
            changeCol[[i, pivotColumn]] = changeCol[[pivotColumn, i]]

        pivot = A[i, i]

        if pivot == 0:
            return "Foi encontrada um divisão por 0"

        for j in range(i + 1, numVariables):
            if A[j, i] == 0:
                continue
            
            multiplier = A[j, i] / pivot
            A[j] = A[j] - A[i] * multiplier
            results[j] = results[j] - results[i] * multiplier

    x[numVariables - 1] = results[numVariables - 1] / A[numVariables - 1, numVariables - 1]
    for i in range(numVariables - 1, -1, -1):
        aux = 0
        for j in range(i + 1, numVariables):
            aux += (A[i, j] * x[j])

        x[i] = (results[i] - aux) / A[i, i]

    
    xResult = np.zeros_like(x)
    for i in range(numVariables):
        xResult[changeCol[i]] = x[i]
    

    print("O resultado é:")
    for result in range(len(x)):
        print(f'x[{result}] = {xResult[result]}')

    return xResult

def LUDecomposition(A, results):
    subMatrixList = subDeterminant(A)
    for sub in subMatrixList:
        if sub == 0:
            return "A matriz tem determinante igual a 0, logo não tem solução por este método"

    numVariables = len(results)
    x = np.zeros(numVariables)
    y = np.zeros(numVariables)
    U = A
    L = np.zeros([numVariables, numVariables])
    for i in range(0, numVariables):
        if A[i, i] == 0:
            return "Foi encontrada um divisão por 0"
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

def choleskyFac(A, B):
    subMatrixList = subDeterminant(A)
    for sub in subMatrixList:
        if sub <= 0:
            return "A matriz tem determinante menor ou igual a 0, logo não tem solução por este método"

    numVariables = len(A)
    x = np.zeros(numVariables)

    for i in range(numVariables):
        for j in range(i + 1, numVariables):
            if A[i, j] != A[j, i]:
                return "A matriz não é simétrica, logo não pode ser resolvida por este método"

    auxMatrix = np.zeros((numVariables, numVariables), dtype = float)
    sumAux = 0
    for i in range(numVariables):
        sumAux = sum(auxMatrix[i, j] ** 2 for j in range(i))
        auxMatrix[i, i] = math.sqrt(A[i, i] - sumAux)

        for j in range(i + 1, numVariables):
            sumAux = sum(auxMatrix[i, k] * auxMatrix[j, k] for k in range(i))
            auxMatrix[j, i] = (A[j, i] - sumAux) / auxMatrix[i, i]

    transposeMatrix = auxMatrix.transpose()
    y = np.zeros(numVariables)

    for i in range(numVariables):
        sumAux = B[i]
        for j in range(i):
            sumAux -= auxMatrix[i, j] * y[j]
        y[i] = sumAux / auxMatrix[i, i]

    for i in range(numVariables - 1, -1, -1):
        aux = y[i]
        for j in range(i + 1, numVariables):
            aux -= transposeMatrix[i, j] * x[j]

        x[i] = aux / transposeMatrix[i, i]

    print("O resultado é:")
    for result in range(len(x)):
        print(f'x[{result}] = {x[result]}')

    return x

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
    matA, matResults = openFile("sistema.txt")
    if matA is not None and matResults is not None:
        print("matriz A")
        print(matA)
        print("resultados")
        print(matResults)

        print("gaus:")
        print(gaussElimination(matA.copy(), matResults.copy()))
        print("parcial:")
        print(partialPivoting(matA.copy(), matResults.copy()))
        print("completo:")
        print(completePivoting(matA.copy(), matResults.copy()))
        print("LU:")
        print(LUDecomposition(matA.copy(), matResults.copy()))
        print("cholesky:")
        print(choleskyFac(matA.copy(), matResults.copy()))