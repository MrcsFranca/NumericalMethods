import numpy as np
import math
import time

def openFile(file):
    hQList = []
    try:
        with open(file, "r") as file:
            for line in file:
                blankLine = line.strip()

                if not blankLine or blankLine.startswith('#'):
                    continue

                numsStr = blankLine.split()
                numsFloat = [float(num) for num in numsStr]
                hQList.append(numsFloat)

    except FileNotFoundError:
        print(f"O arquivo '{file}' não foi encontrado")
        return None, None
    except ValueError:
        print(f"O arquivo '{file}' contém caracteres inválidos")
        return None, None

    if not hQList:
        print("Arquivo vazio ou não lido")
        return None, None

    Headquarters = np.array(hQList, dtype=float)
    A = Headquarters[:, :-1]
    results = Headquarters[:, -1]
    print("matriz A")
    print(A)
    print("resultados")
    print(results)

    return A, results

def subDeterminant(A):
    n = len(A)
    subHeadQuartersList = []
    for subSize in (0, n):
        subHeadQuarters = A[0:subSize, 0:subSize]
        subHeadQuartersList.append(np.linalg.det(subHeadQuarters))
    return subHeadQuartersList

# Metodos diretos
def gaussElimination(A, results):
    begin = time.time()
    print("Eliminação de gauss")
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

    end = time.time()
    print(f"---O programa levou {end - begin} segundos para gerar o resultado:")
    for result in range(len(x)):
        print(f'x[{result}] = {x[result]}')

def partialPivoting(A, results):
    begin = time.time()
    print("Eliminação de gauss parcial")
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

    end = time.time()
    print(f"---O programa levou {end - begin} segundos para gerar o resultado:")
    for result in range(len(x)):
        print(f'x[{result}] = {x[result]}')
    
def completePivoting(A, results):
    begin = time.time()
    print("Eliminação de gauss completa")
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
    

    end = time.time()
    print(f"---O programa levou {end - begin} segundos para gerar o resultado:")
    for result in range(len(x)):
        print(f'x[{result}] = {xResult[result]}')

def LUDecomposition(A, results):
    begin = time.time()
    print("Eliminação LU")
    subHeadQuartersList = subDeterminant(A)
    for sub in subHeadQuartersList:
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

    end = time.time()
    print(f"---O programa levou {end - begin} segundos para gerar o resultado:")
    for result in range(len(x)):
        print(f'x[{result}] = {x[result]}')

def choleskyFac(A, B):
    begin = time.time()
    print("Eliminação cholesky")
    subHeadQuartersList = subDeterminant(A)
    for sub in subHeadQuartersList:
        if sub <= 0:
            return "A matriz tem determinante menor ou igual a 0, logo não tem solução por este método"

    numVariables = len(A)
    x = np.zeros(numVariables)

    for i in range(numVariables):
        for j in range(i + 1, numVariables):
            if A[i, j] != A[j, i]:
                return "A matriz não é simétrica, logo não pode ser resolvida por este método"

    auxHeadQuarters = np.zeros((numVariables, numVariables), dtype = float)
    sumAux = 0
    for i in range(numVariables):
        sumAux = sum(auxHeadQuarters[i, j] ** 2 for j in range(i))
        auxHeadQuarters[i, i] = math.sqrt(A[i, i] - sumAux)

        for j in range(i + 1, numVariables):
            sumAux = sum(auxHeadQuarters[i, k] * auxHeadQuarters[j, k] for k in range(i))
            auxHeadQuarters[j, i] = (A[j, i] - sumAux) / auxHeadQuarters[i, i]

    transposeHeadQuarters = auxHeadQuarters.transpose()
    y = np.zeros(numVariables)

    for i in range(numVariables):
        sumAux = B[i]
        for j in range(i):
            sumAux -= auxHeadQuarters[i, j] * y[j]
        y[i] = sumAux / auxHeadQuarters[i, i]

    for i in range(numVariables - 1, -1, -1):
        aux = y[i]
        for j in range(i + 1, numVariables):
            aux -= transposeHeadQuarters[i, j] * x[j]

        x[i] = aux / transposeHeadQuarters[i, i]

    end = time.time()
    print(f"---O programa levou {end - begin} segundos para gerar o resultado:")
    for result in range(len(x)):
        print(f'x[{result}] = {x[result]}')

# Metodos iterativos
def gaussJacobi(A, results, tolerance, maxIt, xk = None):
    begin = time.time()

    numVariables = len(A)
    if xk is None:
        xk = np.zeros(numVariables, dtype=float)

    it = 0
    newXk = np.array(np.zeros(numVariables))
    while it < maxIt:
        for i in range(numVariables):
            x = results[i]
            for j in range(numVariables):
                if j != i:
                    x -= A[i, j] * xk[j]

            x /= A[i, i]
            newXk[i] = x

        if stopCondition(xk.copy(), newXk.copy(), numVariables) < tolerance:
            end = time.time()
            print(f"---O programa levou {end - begin} segundos para gerar o resultado com {it + 1} iterações:")
            for result in range(len(newXk)):
                print(f'x[{result}] = {newXk[result]}')
            return
        else:
            it += 1
            xk = np.copy(newXk)

    end = time.time()
    print(f"---O programa levou {end - begin} segundos para gerar o resultado com {it + 1} iterações, porém não convergiu:")
    for result in range(len(newXk)):
        print(f'x[{result}] = {newXk[result]}')
    return
        
def gaussJacobiConvergence(A):
    numVariables = len(A)
    maxSum = np.zeros(numVariables)

    for i in range(numVariables):
        sumLine = 0
        for j in range(numVariables):
            if i != j:
                sumLine += math.fabs(A[i, j])

        pivot = math.fabs(A[i, i])
        maxSum[i] = sumLine / pivot

    if maxVector(maxSum) < 1:
        print("A matriz tem a diagonal dominante, portanto ela irá convergir")
    else:
        print("A matriz não é dominante, logo não da para afirmar que irá convergir")

def gaussSeidel(A, results, tolerance, maxIt, xk = None):
    begin = time.time()
    numVariables = len(A)
    if xk is None:
        xk = np.zeros(numVariables, dtype = float)
    
    it = 0
    while it < maxIt:
        oldXk = xk.copy()

        for i in range(numVariables):
            x = results[i]

            for j in range(numVariables):
                if i != j:
                    x -= A[i, j] * xk[j]

            xk[i] = x / A[i, i]

        if stopCondition(oldXk.copy(), xk.copy(), numVariables) < tolerance:
            end = time.time()
            print(f"---O programa levou {end - begin} segundos para gerar o resultado com {it + 1} iterações:")
            for result in range(len(xk)):
                print(f'x[{result}] = {xk[result]}')
            return
        else:
            it += 1

    end = time.time()
    print(f"---O programa levou {end - begin} segundos para gerar o resultado com {it + 1} iterações, porém não convergiu:")
    for result in range(len(xk)):
        print(f'x[{result}] = {xk[result]}')
    return

def sassenfeld(A):
    numVariables = len(A)
    beta = np.zeros(numVariables, dtype=float)

    for i in range(numVariables):
        pivot = math.fabs(A[i, i])
        if pivot == 0:
            print("O pivot é 0, a convergência falhará")
            return

        betaSum = 0
        for j in range(i):
            betaSum += math.fabs(A[i, j]) * beta[j]

        commonSum = 0
        for j in range(i + 1, numVariables):
            commonSum += math.fabs(A[i, j])

        beta[i] = (betaSum + commonSum) / pivot

        print(f"Linha {i}: beta[{i}] = {beta[i]}")
    
    maxVal = maxVector(beta)
    if maxVal < 1:
        print(f"Beta máximo: {maxVal} -> a convergência é garantida\n")
    else:
        print(f"Beta máximo: {maxVal} -> a convergência não é garantida\n")
    
    return

def stopCondition(xk, newXk, numVariables):
    tempHq = newXk - xk
    if maxVector(newXk) == 0:
        return 0.0
    stopValue = maxVector(tempHq) / maxVector(newXk)
    return stopValue

def maxVector(vector):
    maxValue = 0
    for i in range(len(vector)):
        if math.fabs(vector[i]) > maxValue:
            maxValue = math.fabs(vector[i])
    
    return maxValue

"""
if "__main__" == __name__:
    hQA, hQResults = openFile("sistema.txt")
    if hQA is not None and hQResults is not None:
        print("matriz A")
        print(hQA)
        print("resultados")
        print(hQResults)
    
    x0 = np.zeros(len(hQA))
    gaussJacobi(hQA.copy(), hQResults.copy(), 0.01, 100, x0.copy())
"""