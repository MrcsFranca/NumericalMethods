import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import linearEquations as le
import root as rt
import io
from contextlib import redirect_stdout
import numpy as np

class headquarterEntryWindow:
    def __init__(self, parentApp):
        self.parentApp = parentApp 
        
        self.window = tk.Toplevel(parentApp.root)
        self.window.title("Adicionar matriz manualmente")
        self.window.geometry("450x350")
        self.window.transient(parentApp.root)

        self.headquarterSize = 3 
        self.hqA = []
        self.hqB = []

        self.frameGrid = tk.Frame(self.window, padx=10, pady=10)
        self.frameGrid.pack(expand=True, fill='both')

        self.frameControls = tk.Frame(self.window, padx=10, pady=5)
        self.frameControls.pack(side='bottom', fill='x')

        self.createGrid()

        self.decreaseBtn = tk.Button(self.frameControls, text="-", command=self.decreaseHeadquarterSize, width=5)
        self.decreaseBtn.pack(side='left', padx=5)

        self.increaseBtn = tk.Button(self.frameControls, text="+", command=self.increaseHeadquarterSize, width=5)
        self.increaseBtn.pack(side='left', padx=5)
        
        self.saveBtn = tk.Button(self.frameControls, text="Salvar matriz", command=self.saveHeadquarter)
        self.saveBtn.pack(side='right', padx=5)

    def createGrid(self):
        for widget in self.frameGrid.winfo_children():
            widget.destroy()
            
        self.hqA = []
        self.hqB = []

        for i in range(self.headquarterSize):
            hqRow = []
            
            for j in range(self.headquarterSize):
                entry = tk.Entry(self.frameGrid, width=5)
                entry.grid(row=i, column=j, padx=2, pady=2, sticky='ew')
                hqRow.append(entry)
            
            self.hqA.append(hqRow)

            tk.Label(self.frameGrid, text=" = ").grid(row=i, column=self.headquarterSize, padx=5)
            
            hqResults = tk.Entry(self.frameGrid, width=5)
            hqResults.grid(row=i, column=self.headquarterSize + 1, padx=2, pady=2, sticky='ew')
            self.hqB.append(hqResults)
            
        for k in range(self.headquarterSize + 2):
            self.frameGrid.columnconfigure(k, weight=1)

    def increaseHeadquarterSize(self):
        if self.headquarterSize < 8:
            self.headquarterSize += 1
            self.createGrid()
            
    def decreaseHeadquarterSize(self):
        if self.headquarterSize > 2:
            self.headquarterSize -= 1
            self.createGrid()

    def saveHeadquarter(self):
        hqAList = []
        hqBList = []
        
        try:
            for i in range(self.headquarterSize):
                row = []
                for j in range(self.headquarterSize):
                    val = float(self.hqA[i][j].get())
                    row.append(val)
                hqAList.append(row)
            
            for i in range(self.headquarterSize):
                valB = float(self.hqB[i].get())
                hqBList.append(valB)
                
            finalA = np.array(hqAList, dtype=float)
            finalB = np.array(hqBList, dtype=float)
            
            self.parentApp.setManualHq(finalA, finalB)
            self.window.destroy()

        except ValueError:
            messagebox.showerror("Erro de Formato", "Todos os campos devem ser preenchidos com números válidos.", parent=self.window)
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}", parent=self.window)

class vectorEntryWindow:
    def __init__(self, parentApp, x0Size):
        self.parentApp = parentApp
        self.x0Size = x0Size
        
        self.window = tk.Toplevel(parentApp.root)
        self.window.title("Definir vector Inicial (x0)")
        self.window.geometry("250x400")
        self.window.transient(parentApp.root)

        self.entries = []
        
        mainFrame = tk.Frame(self.window)
        canvas = tk.Canvas(mainFrame)
        scrollbar = tk.Scrollbar(mainFrame, orient="vertical", command=canvas.yview)
        scrollLableFrame = tk.Frame(canvas)

        scrollLableFrame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollLableFrame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        mainFrame.pack(expand=True, fill='both', padx=10, pady=10)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.createGrid(scrollLableFrame)

        controlsFrame = tk.Frame(self.window, padx=10, pady=5)
        controlsFrame.pack(side='bottom', fill='x')

        saveBtn = tk.Button(controlsFrame, text="Salvar vetor", command=self.setX0Vector)
        saveBtn.pack(side='right', padx=5)

    def createGrid(self, container):
        for i in range(self.x0Size):
            tk.Label(container, text=f"x[{i}]:").grid(row=i, column=0, padx=5, pady=5)
            
            entry = tk.Entry(container, width=15)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky='ew')
            entry.insert(0, "0.0")
            self.entries.append(entry)
            
        container.columnconfigure(1, weight=1)

    def setX0Vector(self):
        vectorList = []
        try:
            for i in range(self.x0Size):
                val = float(self.entries[i].get())
                vectorList.append(val)
                
            x0Vector = np.array(vectorList, dtype=float)
            
            self.parentApp.setInitVector(x0Vector)
            self.window.destroy()

        except ValueError:
            messagebox.showerror("Erro de Formato", "Todos os campos devem ser preenchidos com números válidos.", parent=self.window)

class FunctionEntryWindow:
    def __init__(self, parentApp):
        self.parentApp = parentApp
        
        self.window = tk.Toplevel(parentApp.root)
        self.window.title("Definir funções manualmente")
        self.window.geometry("450x350")
        self.window.transient(parentApp.root)

        mainFrame = tk.Frame(self.window, padx=20, pady=20)
        mainFrame.pack(expand=True, fill='both')

        tk.Label(mainFrame, text="Função f(x):", font=("Arial", 12, "bold")).pack(anchor='w')
        tk.Label(mainFrame, text="(Ex: e^x - 5x)", font=("Arial", 10, "italic")).pack(anchor='w')
        self.entryFunction = tk.Entry(mainFrame, width=40)
        self.entryFunction.pack(fill='x', pady=(0, 10))

        tk.Label(mainFrame, text="Função Iterada g(x):", font=("Arial", 12, "bold")).pack(anchor='w')
        tk.Label(mainFrame, text="(Para Método Ponto Fixo. Ex: (e^x)/5)", font=("Arial", 10, "italic")).pack(anchor='w')
        self.entryItFunction = tk.Entry(mainFrame, width=40)
        self.entryItFunction.pack(fill='x', pady=(0, 10))

        tk.Label(mainFrame, text="Derivada f'(x):", font=("Arial", 12, "bold")).pack(anchor='w')
        tk.Label(mainFrame, text="(Para Método Newton. Ex: e^x - 5)", font=("Arial", 10, "italic")).pack(anchor='w')
        self.entryDxFunction = tk.Entry(mainFrame, width=40)
        self.entryDxFunction.pack(fill='x', pady=(0, 10))

        btnFrame = tk.Frame(self.window, pady=10)
        btnFrame.pack(side='bottom', fill='x')
        
        saveBtn = tk.Button(btnFrame, text="Salvar Funções", command=self.saveFunctions, height=2)
        saveBtn.pack(side='right', padx=20, pady=10)

    def saveFunctions(self):
        fx = self.entryFunction.get().strip()
        gx = self.entryItFunction.get().strip()
        dfx = self.entryDxFunction.get().strip()

        if not fx or not gx or not dfx:
            messagebox.showwarning("Aviso", "Por favor, preencha todos os campos.\nSe não tiver uma função específica, insira 'x' ou '0' apenas para não deixar vazio.", parent=self.window)
            return

        self.parentApp.setManualFunctions(fx, gx, dfx)
        self.window.destroy()

class InterfaceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de métodos muméricos")
        self.root.geometry("800x600")

        self.filePath = None
        self.insertAHeadquarter = None
        self.insertBHeadquarter = None
        self.x0Vector = None
        self.x0VectorSize = 0
        
        self.rootFilePath = None

        self.manualFx = None
        self.manualGx = None
        self.manualDfx = None

        style = ttk.Style(self.root)
        style.theme_use('clam') 

        self.notebook = ttk.Notebook(root)
        self.systemFrame = ttk.Frame(self.notebook, padding=10)
        self.rootFrame = ttk.Frame(self.notebook, padding=10)
        
        self.notebook.add(self.systemFrame, text="Sistemas lineares")
        self.notebook.add(self.rootFrame, text="Raízes")
        self.notebook.pack(expand=True, fill='both')

        self.createSystemFrame()
        self.createRootFrame()

    def createRootFrame(self):
        for widget in self.rootFrame.winfo_children():
            widget.destroy()

        mainFrame = ttk.Frame(self.rootFrame)
        mainFrame.pack(fill='x', expand=True, side='top')

        leftFrame = ttk.Frame(mainFrame)
        leftFrame.pack(side='left', fill='x', expand=True, padx=10)

        rightFrame = ttk.Frame(mainFrame)
        rightFrame.pack(side='right', fill='y', padx=10)

        ttk.Label(leftFrame, text="Solução de raízes de funções:", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, sticky='w', pady=10)

        ttk.Label(leftFrame, text="Escolher arquivo de funções:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        fileFrame = ttk.Frame(leftFrame)
        fileFrame.grid(row=1, column=1, sticky='we')
        
        self.rootFileBtn = ttk.Button(fileFrame, text="Carregar arquivo...", command=self.openRootFileWindow)
        self.rootFileBtn.pack(side='left')

        self.manualFuncBtn = ttk.Button(fileFrame, text="Adicionar funções", command=self.openFunctionEntryWindow)
        self.manualFuncBtn.pack(side='left', padx=10)
        
        self.infoRootBtn = ttk.Button(fileFrame, text="i", command=self.showRootInfo, width=2)
        self.infoRootBtn.pack(side='left', padx=5)

        self.selectedRootFileLabel = ttk.Label(leftFrame, text="Nenhum arquivo carregado", font=("Arial", 9, "italic"))
        self.selectedRootFileLabel.grid(row=2, column=0, columnspan=2, sticky='w', padx=5)

        ttk.Separator(leftFrame, orient='horizontal').grid(row=3, column=0, columnspan=2, sticky='we', pady=15)
        ttk.Label(leftFrame, text="Parâmetros:", font=("Arial", 12, "bold")).grid(row=4, column=0, columnspan=2, sticky='w', pady=5)

        ttk.Label(leftFrame, text="Intervalo [a] (ou x0):").grid(row=5, column=0, sticky='w', padx=5, pady=5)
        self.setRootA = ttk.Entry(leftFrame, state="normal")
        self.setRootA.grid(row=5, column=1, sticky='we')
        self.setRootA.insert(0, "1.0")

        ttk.Label(leftFrame, text="Intervalo [b] (ou x1):").grid(row=6, column=0, sticky='w', padx=5, pady=5)
        self.setRootB = ttk.Entry(leftFrame, state="normal")
        self.setRootB.grid(row=6, column=1, sticky='we')
        self.setRootB.insert(0, "2.0")
        
        ttk.Label(leftFrame, text="Precisão (tolerância):").grid(row=7, column=0, sticky='w', padx=5, pady=5)
        self.setRootPrecision = ttk.Entry(leftFrame, state="normal")
        self.setRootPrecision.grid(row=7, column=1, sticky='we')
        self.setRootPrecision.insert(0, "1e-5")

        ttk.Label(leftFrame, text="Nº Máximo de iterações:").grid(row=8, column=0, sticky='w', padx=5, pady=5)
        self.setRootMaxIt = ttk.Entry(leftFrame, state="normal")
        self.setRootMaxIt.grid(row=8, column=1, sticky='we')
        self.setRootMaxIt.insert(0, "50")
        
        leftFrame.columnconfigure(1, weight=1)

        self.calculateRootBtn = ttk.Button(rightFrame, text="Calcular raízes", command=self.calculateRoots)
        self.calculateRootBtn.pack(fill='x', expand=True, ipady=10, side='bottom', pady=20)

        ttk.Label(self.rootFrame, text="Resultados:", font=("Arial", 12, "bold")).pack(anchor='w', padx=10, pady=(20, 5))
        self.rootResultText = scrolledtext.ScrolledText(self.rootFrame, height=10, font=("Courier New", 10))
        self.rootResultText.pack(fill='both', expand=True, padx=10, pady=5)
        self.rootResultText.config(state="disabled")

    def createSystemFrame(self):
        mainFrame = ttk.Frame(self.systemFrame)
        mainFrame.pack(fill='x', expand=True, side='top')

        leftFrame = ttk.Frame(mainFrame)
        leftFrame.pack(side='left', fill='x', expand=True, padx=10)

        rightFrame = ttk.Frame(mainFrame)
        rightFrame.pack(side='right', fill='y', padx=10)

        ttk.Label(leftFrame, text="Solução de sistemas lineares:", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, sticky='w', pady=10)

        ttk.Label(leftFrame, text="Escolher matriz:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        
        fileFrame = ttk.Frame(leftFrame)
        fileFrame.grid(row=1, column=1, sticky='we')
        
        self.fileBtn = ttk.Button(fileFrame, text="Carregar Arquivo...", command=self.openFileWindow)
        self.fileBtn.pack(side='left')

        self.setHeadquarterBtn = ttk.Button(fileFrame, text="Adicionar matriz", command=self.setHeadquarterWindow)
        self.setHeadquarterBtn.pack(side='left', padx=10)
        
        self.infoBtn = ttk.Button(fileFrame, text="i", command=self.showInfo, width=2)
        self.infoBtn.pack(side='left', padx=5)

        self.selectedFileLabel = ttk.Label(leftFrame, text="Nenhuma matriz carregada", font=("Arial", 9, "italic"))
        self.selectedFileLabel.grid(row=2, column=0, columnspan=2, sticky='w', padx=5)

        ttk.Separator(leftFrame, orient='horizontal').grid(row=3, column=0, columnspan=2, sticky='we', pady=15)
        ttk.Label(leftFrame, text="Configurações de métodos iterativos:", font=("Arial", 12, "bold")).grid(row=4, column=0, columnspan=2, sticky='w', pady=5)

        ttk.Label(leftFrame, text="Selecione a tolerância:").grid(row=5, column=0, sticky='w', padx=5, pady=5)
        self.setTolerance = ttk.Entry(leftFrame, state="normal")
        self.setTolerance.grid(row=5, column=1, sticky='we')
        self.setTolerance.insert(0, "1e-5")

        ttk.Label(leftFrame, text="Selecione o nº máximo de iterações:").grid(row=6, column=0, sticky='w', padx=5, pady=5)
        self.setIterations = ttk.Entry(leftFrame, state="normal")
        self.setIterations.grid(row=6, column=1, sticky='we')
        self.setIterations.insert(0, "100")

        ttk.Label(leftFrame, text="Selecione o vetor inicial:").grid(row=7, column=0, sticky='w', padx=5, pady=5)

        vectorFrame = ttk.Frame(leftFrame)
        vectorFrame.grid(row=7, column=1, sticky='we')
        
        self.setVectorBtn = ttk.Button(vectorFrame, text="Definir vetor inicial", command=self.x0Window)
        self.setVectorBtn.pack(side='left')
        self.setVectorBtn.config(state="disabled")
        
        self.infoVectorBtn = ttk.Button(vectorFrame, text="i", command=self.infoX0, width=2)
        self.infoVectorBtn.pack(side='left', padx=5)

        leftFrame.columnconfigure(1, weight=1)

        ttk.Label(rightFrame, text="Método de solução:").pack(anchor='w')
        directMethods = ["Gauss (Simples)", "Gauss (Piv. Parcial)", "Gauss (Piv. Completo)", "Decomposição LU", "Fatoração de Cholesky", "Gauss-Jacobi", "Gauss-Seidel"]
        self.methodsComboBox = ttk.Combobox(rightFrame, values=directMethods, state="readonly")
        self.methodsComboBox.pack(fill='x', expand=True, pady=5)
        self.methodsComboBox.current(0)
        self.calculateBtn = ttk.Button(rightFrame, text="Calcular matriz", command=self.calculate)
        self.calculateBtn.pack(fill='x', expand=True, ipady=10, side='bottom', pady=20)

        ttk.Label(self.systemFrame, text="Resultados:", font=("Arial", 12, "bold")).pack(anchor='w', padx=10, pady=(20, 5))
        self.resultText = scrolledtext.ScrolledText(self.systemFrame, height=10, font=("Courier New", 10))
        self.resultText.pack(fill='both', expand=True, padx=10, pady=5)
        self.resultText.config(state="disabled")

    def openFileWindow(self):
        self.filePath = filedialog.askopenfilename(
            title="Selecionar arquivo",
            filetypes=(("Arquivos de Texto", "*.txt"), ("Todos os arquivos", "*.*"))
        )
        if self.filePath:
            try:
                fileToOpen = io.StringIO()
                with redirect_stdout(fileToOpen):
                    hqATemp, hqBTemp = le.openFile(self.filePath)
                
                if hqATemp is None:
                    self.selectedFileLabel.config(text="Erro ao ler o arquivo. Verifique o formato.")
                    self.filePath = None
                    return

                splitName = self.filePath.split('/')[-1]
                self.selectedFileLabel.config(text=f"Arquivo: {splitName}")
                
                self.x0SizeHq = hqATemp.shape[0]
                self.setVectorBtn.config(state="normal")
                self.initialVector = None
                self.insertAHeadquarter = None
                self.insertBHeadquarter = None

            except Exception as e:
                self.selectedFileLabel.config(text=f"Erro ao carregar: {e}")
                self.filePath = None
                self.setVectorBtn.config(state="disabled")
        else:
            self.selectedFileLabel.config(text="Nenhuma matriz carregada")
            self.setVectorBtn.config(state="disabled")

    def showInfo(self):
        messagebox.showinfo(
            "Formato do Arquivo",
            "O arquivo de texto deve conter a matriz aumentada [A|b].\n\n"
            "O vetor 'b' (resultados) deve ser a última coluna.\n\n"
            "Use '#' no início de uma linha para comentários."
        )

    def setHeadquarterWindow(self):
        self.headquarterPopup = headquarterEntryWindow(self)

    def setManualHq(self, A, b):
        self.insertAHeadquarter = A
        self.insertBHeadquarter = b
        
        self.filePath = None

        self.x0SizeHq = A.shape[0]
        self.setVectorBtn.config(state="normal")
        self.initialVector = None
        
        self.selectedFileLabel.config(text=f"Matriz manual {A.shape[0]}x{A.shape[1]} carregada.")
        print("Matriz manual recebida pela interface principal.")
        print("Matriz A:")
        print(self.insertAHeadquarter)
        print("\nvetor b:")
        print(self.insertBHeadquarter)

    def x0Window(self):
        if self.x0SizeHq > 0:
            self.x0Popup = vectorEntryWindow(self, self.x0SizeHq)
        else:
            messagebox.showerror("Erro", "Carregue uma matriz (arquivo ou manual) antes de definir o vetor inicial.")

    def infoX0(self):
        messagebox.showinfo(
            "vector Inicial (x0)",
            "Este é o 'chute' inicial para os métodos iterativos.\n\n"
            "Se não for definido, será usado um vetor nulo para os cálculos."
        )

    def setInitVector(self, x0):
        self.initialVector = x0
        vectorStatus = self.selectedFileLabel.cget("text")
        self.selectedFileLabel.config(text=vectorStatus + " | vector inicial (x0) definido.")
        print("vector inicial (x0) setado:")
        print(self.initialVector)

    def calculate(self):
        self.resultText.config(state="normal")
        self.resultText.delete(1.0, "end")

        chosenMethod = self.methodsComboBox.get()
        
        ACalc, BCalc = None, None
        
        if self.insertAHeadquarter is not None and self.insertBHeadquarter is not None:
            ACalc = self.insertAHeadquarter.copy()
            BCalc = self.insertBHeadquarter.copy()
            self.resultText.insert("end", "Iniciando cálculo...\n")
        
        elif self.filePath:
            self.resultText.insert("end", f"Carregando dados do arquivo: {self.filePath.split('/')[-1]}...\n")
            try:
                fileToOpen = io.StringIO()
                with redirect_stdout(fileToOpen):
                    ACalc, BCalc = le.openFile(self.filePath)
                
                output = fileToOpen.getvalue()
                self.resultText.insert("end", output)
                
                if ACalc is None:
                    self.resultText.insert("end", f"\nERRO: Não foi possível ler o arquivo.")
                    return
            except Exception as e:
                self.resultText.insert("end", f"ERRO ao processar o arquivo: {e}")
                return
        
        else:
            self.resultText.insert("end", "ERRO: Nenhum arquivo ou matriz manual foi carregado.")
            self.resultText.config(state="disabled")
            return
            
        f = io.StringIO()
        finalResult = None
        
        try:
            with redirect_stdout(f):
                if chosenMethod == "Gauss (Simples)":
                    finalResult = le.gaussElimination(ACalc.copy(), BCalc.copy())
                elif chosenMethod == "Gauss (Piv. Parcial)":
                    finalResult = le.partialPivoting(ACalc.copy(), BCalc.copy())
                elif chosenMethod == "Gauss (Piv. Completo)":
                    finalResult = le.completePivoting(ACalc.copy(), BCalc.copy())
                elif chosenMethod == "Decomposição LU":
                    finalResult = le.LUDecomposition(ACalc.copy(), BCalc.copy())
                elif chosenMethod == "Fatoração de Cholesky":
                    finalResult = le.choleskyFac(ACalc.copy(), BCalc.copy())
                elif chosenMethod == "Gauss-Jacobi":
                    try:
                        tolerance = float(self.setTolerance.get())
                        maxIter = int(self.setIterations.get())

                        finalResult = le.gaussJacobi(ACalc.copy(), BCalc.copy(), tolerance, maxIter, xk=self.initialVector)
                        
                    except ValueError:
                        finalResult = "ERRO: Verifique se a tolerância e o nº de iterações são números válidos."
                    except Exception as e:
                        finalResult = f"ERRO inesperado: {e}"
                elif chosenMethod == "Gauss-Seidel":
                    try:
                        tolerance = float(self.setTolerance.get())
                        maxIter = int(self.setIterations.get())

                        finalResult = le.gaussSeidel(ACalc.copy(), BCalc.copy(), tolerance, maxIter, xk=self.initialVector)
                        
                    except ValueError:
                        finalResult = "ERRO: Verifique se a tolerância e o nº de iterações são números válidos."
                    except Exception as e:
                        finalResult = f"ERRO inesperado: {e}"
            
            output = f.getvalue()
            
            if output:
                self.resultText.insert("end", "\n--- Saída do Console da Função ---\n")
                self.resultText.insert("end", output)
            
            if isinstance(finalResult, str):
                self.resultText.insert("end", f"\nERRO: {finalResult}")
            else:
                 self.resultText.insert("end", "\n--- Cálculo Concluído ---")
                 
        except Exception as e:
            self.resultText.insert("end", f"\n--- ERRO DURANTE O CÁLCULO ---\n{type(e).__name__}: {e}")

        self.resultText.config(state="disabled")

    def openRootFileWindow(self):
        self.rootFilePath = filedialog.askopenfilename(
            title="Selecionar arquivo de funções",
            filetypes=(("Arquivos de Texto", "*.txt"), ("Todos os arquivos", "*.*"))
        )
        if self.rootFilePath:
            splitName = self.rootFilePath.split('/')[-1]
            self.selectedRootFileLabel.config(text=f"Arquivo: {splitName}")
        else:
            self.selectedRootFileLabel.config(text="Nenhum arquivo carregado.")

    def openFunctionEntryWindow(self):
        self.functionPopup = FunctionEntryWindow(self)

    def setManualFunctions(self, fx, gx, dfx):
        self.manualFx = fx
        self.manualGx = gx
        self.manualDfx = dfx
        
        self.selectRootFilePath = None
        
        self.selectedRootFileLabel.config(text="Funções manuais carregadas.")
        print(f"Funções Manuais Recebidas:\nf(x)={fx}\ng(x)={gx}\nf'(x)={dfx}")

    def showRootInfo(self):
        messagebox.showinfo(
            "Formato do arquivo de funções",
            "O arquivo de texto deve conter pelo menos 3 linhas, sendo respectivamente:\n\n"
            "f(x), g(x) e f'(x)\n"
            "Cada função em uma linha\n"
            "Insira apenas a função (sem 'f(x) =' por exemplo)\n\n"
            "Use '#' para comentários. Linhas em branco são ignoradas."
        )

    def calculateRoots(self):
            self.rootResultText.config(state="normal")
            self.rootResultText.delete(1.0, "end")

            finalFormula = ""
            finalIt = ""
            finalDfx = ""
            origin = ""

            if self.manualFx and self.manualGx and self.manualDfx:
                try:
                    finalFormula = rt.padronizar(self.manualFx)
                    finalIt = rt.padronizar(self.manualGx)
                    finalDfx = rt.padronizar(self.manualDfx)
                    origin = "Entrada Manual"
                except Exception as e:
                    self.rootResultText.insert("end", f"ERRO ao processar funções manuais: {e}")
                    self.rootResultText.config(state="disabled")
                    return

            elif self.rootFilePath:
                fStdout = io.StringIO()
                try:
                    with redirect_stdout(fStdout):
                        finalFormula, finalIt, finalDfx = rt.openFile(self.rootFilePath)
                except Exception as e:
                    self.rootResultText.insert("end", f"Erro fatal ao ler arquivo: {e}")
                    return
                
                if finalFormula is None:
                    self.rootResultText.insert("end", fStdout.getvalue())
                    self.rootResultText.config(state="disabled")
                    return
                origin = f"Arquivo: {self.rootFilePath.split('/')[-1]}"
                
            else:
                self.rootResultText.insert("end", "ERRO: Nenhuma função carregada (Arquivo ou Manual).")
                self.rootResultText.config(state="disabled")
                return
            
            try:
                a = float(self.setRootA.get())
                b = float(self.setRootB.get())
                precision = float(self.setRootPrecision.get())
                maxIt = int(self.setRootMaxIt.get())
            except ValueError:
                self.rootResultText.insert("end", "ERRO: Verifique se 'a', 'b', 'precision' e 'maxIt' são números válidos.")
                self.rootResultText.config(state="disabled")
                return
            
            rootStdout = io.StringIO()
            self.rootResultText.insert("end", f"origem: {origin}\n")
            self.rootResultText.insert("end", f"Calculando com a={a}, b={b}, precision={precision}, maxIt={maxIt}\n")

            try:
                with redirect_stdout(rootStdout):
                    rt.allMethods(a, b, precision, maxIt, finalFormula, finalIt, finalDfx)
                
                output = rootStdout.getvalue()
                
                try:
                    with open("resultados.txt", 'w', encoding='utf-8') as f_out:
                        f_out.write(output)
                    self.rootResultText.insert("end", "\n--- Resultados salvos em 'resultados.txt' ---\n")
                except Exception as e:
                    self.rootResultText.insert("end", f"\n--- ERRO AO SALVAR ARQUIVO: {e} ---\n")

                self.rootResultText.insert("end", output)
                
            except Exception as e:
                self.rootResultText.insert("end", f"\n--- ERRO DURANTE O CÁLCULO ---\n{type(e).__name__}: {e}")

            self.rootResultText.config(state="disabled")

    def openFunctionEntryWindow(self):
        self.functionPopup = FunctionEntryWindow(self)

    def setManualFunctions(self, fx, gx, dfx):
        self.manualFx = fx
        self.manualGx = gx
        self.manualDfx = dfx
        
        # Limpa o arquivo para evitar conflito
        self.rootFilePath = None
        
        self.selectedRootFileLabel.config(text="Funções manuais carregadas.")
        print(f"Funções Manuais Recebidas:\n f(x)={fx}\n g(x)={gx}\n f'(x)={dfx}")

if __name__ == "__main__":
    root = tk.Tk()
    InterfaceApp(root)
    root.mainloop()
