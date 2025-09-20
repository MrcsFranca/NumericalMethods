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

def openFile():
    arquivo = open("formula.txt", "r")

    linha = arquivo.readline()
    formula = padronizar(linha)

    linha = arquivo.readline()
    formulaIter = padronizar(linha)

    linha = arquivo.readline()
    formulaDer   = padronizar(linha)

    arquivo.close()
    return formula, formulaIter, formulaDer

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
        print(f"=====A raiz {meio} foi encontrada em {k} iterações")

def mpf(x0, precisao, maxIt, formula, formulaIter):
    k = 0
    print(f"{'Iter (k)':<10} {'x0':<18} {'x1':<18} {'Erro':<18}")

    if math.fabs(funcExec(x0, formula)) < precisao:
        print(f"{k:<10} {x0:<18.8f} {x1:<18.8f} {math.fabs(funcExec(x0, formula)):<18.8f}")
        print(f"=====A raiz {x0} foi encontrada em {k} iterações")
        return
    
    for k in range(1, maxIt + 1):
        x1 = funcExec(x0, formulaIter)

        print(f"{k:<10} {x0:<18.8f} {x1:<18.8f} {math.fabs(funcExec(x0, formula)):<18.8f}")

        if math.fabs(funcExec(x1, formula)) < precisao or math.fabs(x1 - x0) < precisao:
            print(f"=====A raiz {x1} foi encontrada em {k} iterações")
            return

        x0 = x1 

    print("A funcao chegou ao seu limite de iterações")
    print(f"=====A raiz {x1} foi encontrada em {k} iterações")

def newton(x0, precisao, maxIt, formula, formulaDer):
    k = 0
    print(f"{'Iter (k)':<10} {'x0':<18} {'x1':<18} {'Erro':<18}")

    if math.fabs(funcExec(x0, formula)) < precisao:
        print(f"{k:<10} {x0:<18.8f} {x1:<18.8f} {math.fabs(funcExec(x0, formula)):<18.8f}")
        print(f"=====A raiz {x0} foi encontrada em {k} iterações")
        return

    for k in range(1, maxIt + 1):
        x1 = x0 - (funcExec(x0, formula) / funcExec(x0, formulaDer))
        
        print(f"{k:<10} {x0:<18.8f} {x1:<18.8f} {math.fabs(funcExec(x0, formula)):<18.8f}")

        if math.fabs(funcExec(x1, formula)) < precisao or math.fabs(x1 - x0) < precisao:
            print(f"=====A raiz {x1} foi encontrada em {k} iterações")
            return

        x0 = x1

    print("A funcao chegou ao seu limite de iterações")
    print(f"=====A raiz {x1} foi encontrada em {k} iterações")

def secante(x0, x1, precisao, maxIt, formula):
    k = 0
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
            print(f"=====A raiz {x2} foi encontrada em {k} iterações")
            return

        x0 = x1
        x1 = x2

    print("A funcao chegou ao seu limite de iterações")
    print(f"=====A raiz {x2} foi encontrada em {k} iterações")

def regulaFalsi(a, b, precisao, maxIt, formula):
    k = 0
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
            print(f"=====A raiz {x} foi encontrada em {k} iterações")
            return

        if fa * fx < 0:
            b = x
            fb = fx
        else:
            a = x
            fa = fx

    print("A funcao chegou ao seu limite de iterações")
    print(f"=====A raiz {x} foi encontrada em {k} iterações")

if __name__ == "__main__":
    a = float(input("Insira o limite menor: "))
    b = float(input("Insira o limete maior: "))
    precisao = float(input("Insira a precisao: "))
    maxIt = int(input("Insira o número de interações máxima: "))

    stdout = sys.stdout

    formula, formulaIter, formulaDer = openFile()

    with open("resultados.txt", 'w') as resultados:

        sys.stdout = resultados

        print("\n---[ Metodo da bisseccao ]------------------------------------------------")
        bissec(a, b, precisao, maxIt, formula)
        print("\n---[ Metodo iterativo linear ou metodo do ponto fixo ]--------------------")
        mpf(a, precisao, maxIt, formula, formulaIter)
        print("\n---[ Metodo de Newton ]---------------------------------------------------")
        newton(a, precisao, maxIt, formula, formulaDer)
        print("\n---[ Metodo da secante ]--------------------------------------------------")
        secante(a, b, precisao, maxIt, formula)
        print("\n---[ Metodo da regula-falsi ]--------------------------------------------------")
        regulaFalsi(a, b, precisao, maxIt, formula)

    sys.stdout = stdout
    print("Resultados salvos no arquivo \"Resultados.txt\"")
