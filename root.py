import math
import re
import sys

def padronizar(linha):
    formula = re.sub(r'([0-9x])([a-zA-Z])', r'\1*\2', linha)
    formula = re.sub(r'(x)([a-zA-Z0-9])', r'\1*\2', formula)
    formula = re.sub(r'([0-9x])(\.)', r'\1*', formula)
    formula = re.sub(r'([0-9x])(\()', r'\1*\2', formula)
    formula = re.sub(r'(\be\b)', r'math.e', formula)
    formula = re.sub(r'(\bsqrt\b)', r'math.sqrt', formula)
    formula = formula.replace("^", "**")
    formula = formula.replace("log", "math.log10")
    formula = formula.replace("ln", "math.log")
    formula = formula.replace("sen", "math.sin")
    formula = formula.replace("cos", "math.cos")
    formula = formula.replace("tg", "math.tan")

    return formula

def openFile(filePath):
    formulas = []
    try:
        with open(filePath, "r") as file:
            for line in file:
                blankLine = line.strip()
                if not blankLine or blankLine.startswith('#'):
                    continue
                
                if len(formulas) < 3:
                    formulas.append(padronizar(blankLine))

    except FileNotFoundError:
        print(f"O arquivo '{filePath}' não foi encontrado")
        return None, None, None
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return None, None, None

    if len(formulas) < 3:
        print(f"ERRO: O arquivo deve conter 3 fórmulas (Função, Iterada, Derivada).")
        print(f"Encontradas: {len(formulas)}. Completando com strings vazias.")
        while len(formulas) < 3:
            formulas.append("")
            
    return formulas[0], formulas[1], formulas[2]

def funcExec(x, formula):
    try:
        bibliotecas = {'math': math}
        variaveis = {'x': x}
        return eval(formula, bibliotecas, variaveis)
    except Exception as e:
        print(f"Erro ao avaliar a formula: {formula} por conta do erro:\n{e}")
        return None

def bissec(a, b, precisao, maxIt, formula):
    k = 0
    aLimit = a
    bLimit = b
    print(f"{'Iter (k)':<10} {'a':<18} {'b':<18} {'Erro':<18}")

    if(math.fabs(b - a) < precisao):
        print(a + " | " + b)
    else:
        while((math.fabs(b - a) > precisao or math.fabs(funcExec(meio, formula)) > precisao) and k < maxIt):
            k += 1
            ini = funcExec(a, formula)
            if ini is None:
                return
            
            meio = (a + b)/2
            fim = funcExec(meio, formula)
            if fim is None:
                return
            
            if(ini * fim < 0):
                b = meio
            else:
                a = meio
            
            print(f"{k:<10} {a:<18.8f} {b:<18.8f} {math.fabs(meio):<18.8f}")
        
        if k >= maxIt:
            print("A função, provavelmente, e divergente")
        else:
            if aLimit < meio and meio < bLimit:
                print(f"=====A raiz {meio} foi encontrada em {k} iterações")
                return
            else:
                print(f"=====A função provavelmente é divergente")
                return

def mpf(x0, precisao, maxIt, formula, formulaIter):
    k = 0
    aLimit = x0
    bLimit = 100
    print(f"{'Iter (k)':<10} {'x0':<18} {'x1':<18} {'Erro':<18}")

    if math.fabs(funcExec(x0, formula)) < precisao:
        print(f"{k:<10} {x0:<18.8f} 0.00000000 {math.fabs(funcExec(x0, formula)):<18.8f}")
        print(f"=====A raiz {x0} foi encontrada em {k} iterações")
        return
    
    for k in range(1, maxIt + 1):
        x1 = funcExec(x0, formulaIter)

        if x1 is None: 
            print(f"Erro na iteração {k}: Cálculo de g(x) falhou (possível divisão por zero).")
            return

        print(f"{k:<10} {x0:<18.8f} {x1:<18.8f} {math.fabs(funcExec(x0, formula)):<18.8f}")

        if math.fabs(funcExec(x1, formula)) < precisao or math.fabs(x1 - x0) < precisao:
            if aLimit < x1 and x1 < bLimit:
                print(f"=====A raiz {x1} foi encontrada em {k} iterações")
                return
            else:
                print(f"=====A função provavelmente é divergente")
                return

        x0 = x1 

    if k >= maxIt:
        print("A função, provavelmente, e divergente")

def newton(x0, x1, precisao, maxIt, formula, formulaDer):
    k = 0
    x0 = (x0 + x1) /2
    aLimit = x0
    bLimit = x1
    print(f"{'Iter (k)':<10} {'x0':<18} {'x1':<18} {'Erro':<18}")

    if math.fabs(funcExec(x0, formula)) < precisao:
        print(f"{k:<10} {x0:<18.8f} 0.00000000 {math.fabs(funcExec(x0, formula)):<18.8f}")
        print(f"=====A raiz {x0} foi encontrada em {k} iterações")
        return

    for k in range(1, maxIt + 1):
        x1 = x0 - (funcExec(x0, formula) / funcExec(x0, formulaDer))
        
        print(f"{k:<10} {x0:<18.8f} {x1:<18.8f} {math.fabs(funcExec(x0, formula)):<18.8f}")

        if math.fabs(funcExec(x1, formula)) < precisao or math.fabs(x1 - x0) < precisao:
            if aLimit < x1 and x1 < bLimit:
                print(f"=====A raiz {x1} foi encontrada em {k} iterações")
                return
            else:
                print(f"=====A função provavelmente é divergente")
                return

        x0 = x1

    if k >= maxIt:
        print("A função, provavelmente, e divergente")

def secante(x0, x1, precisao, maxIt, formula):
    k = 0
    aLimit = x0
    bLimit = x1
    print(f"{'Iter (k)':<10} {'x0':<18} {'x1':<18} {'Erro':<18}")
    
    if math.fabs(funcExec(x0, formula)) < precisao:
        print(f"{k:<10} {x0:<18.8f} {x1:<18.8f} {math.fabs(funcExec(x0, formula)):<18.8f}")
        print(f"=====A raiz {x0} foi encontrada em {k} iterações")
        return

    if math.fabs(funcExec(x1, formula)) < precisao or math.fabs(x1 - x0) < precisao:
        print(f"{k:<10} {x0:<18.8f} {x1:<18.8f} {math.fabs(funcExec(x0, formula)):<18.8f}")
        print(f"=====A raiz {x0} foi encontrada em {k} iterações")
        return

    for k in range(1, maxIt + 1):
        x2 = x1 - ((funcExec(x1, formula) * (x1 - x0)) / (funcExec(x1, formula) - funcExec(x0, formula)))

        print(f"{k:<10} {x0:<18.8f} {x1:<18.8f} {math.fabs(funcExec(x0, formula)):<18.8f}")

        if math.fabs(funcExec(x2, formula)) < precisao or math.fabs(x2 - x1) < precisao:
            if aLimit < x2 and x2 < bLimit:
                print(f"=====A raiz {x2} foi encontrada em {k} iterações")
                return
            else:
                print(f"=====A função provavelmente é divergente")
                return

        x0 = x1
        x1 = x2

    if k >= maxIt:
        print("A função, provavelmente, e divergente")

def regulaFalsi(a, b, precisao, maxIt, formula):
    k = 0
    aLimit = a
    bLimit = b
    print(f"{'Iter (k)':<10} {'a':<18} {'b':<18} {'Erro':<18}")

    fa = funcExec(a, formula)
    fb = funcExec(b, formula)

    if fa * fb >= 0:
        print("Erro: a função não tem sinais opostos no intervalo inicial")
        return

    if math.fabs(b - a) < precisao or math.fabs(fa) < precisao or math.fabs(fb) < precisao:
        print(f"{k:<10} {a:<18.8f} {b:<18.8f} {math.fabs(funcExec(a, formula)):<18.8f}")
        print(f"=====A raiz {a} foi encontrada em {k} iterações")
        return

    x = 0
    for k in range(1, maxIt + 1):
        xAnt = x
        x = ((a * funcExec(b, formula)) - (b * funcExec(a, formula))) / (funcExec(b, formula) - funcExec(a, formula))
        fx = funcExec(x, formula)

        print(f"{k:<10} {a:<18.8f} {b:<18.8f} {math.fabs(funcExec(x, formula)):<18.8f}")

        if math.fabs(funcExec(x, formula)) < precisao or math.fabs(x - xAnt) < precisao:
            if aLimit < x and x < bLimit:
                print(f"=====A raiz {x} foi encontrada em {k} iterações")
                return
            else:
                print(f"=====A função provavelmente é divergente")
                return

        if fa * fx < 0:
            b = x
            fb = fx
        else:
            a = x
            fa = fx

    if k >= maxIt:
        print("A função, provavelmente, e divergente")

def allMethods(a, b, precisao, maxIt, formula, formulaIter, formulaDer):
    print("\n---[ Metodo da bisseccao ]------------------------------------------------")
    bissec(a, b, precisao, maxIt, formula)
    print("\n---[ Metodo iterativo linear ou metodo do ponto fixo ]--------------------")
    mpf(a, precisao, maxIt, formula, formulaIter)
    print("\n---[ Metodo de Newton ]---------------------------------------------------")
    newton(a, b, precisao, maxIt, formula, formulaDer)
    print("\n---[ Metodo da secante ]--------------------------------------------------")
    secante(a, b, precisao, maxIt, formula)
    print("\n---[ Metodo da regula-falsi ]--------------------------------------------------")
    regulaFalsi(a, b, precisao, maxIt, formula)
