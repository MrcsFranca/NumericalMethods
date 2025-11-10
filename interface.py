import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import linearEquations as le  # Importa o arquivo com suas funções
import io
from contextlib import redirect_stdout
import numpy as np

class headquarterEntryWindow:
    def __init__(self, parentApp):
        self.parentApp = parentApp 
        
        # Toplevel é o mesmo
        self.window = tk.Toplevel(parentApp.root)
        self.window.title("Adicionar matriz manualmente")
        self.window.geometry("450x350")
        self.window.transient(parentApp.root)

        self.headquarterSize = 3 
        self.hqA = []
        self.hqB = []

        # MUDANÇA: Usando tk.Frame em vez de ttk.Frame
        self.frameGrid = tk.Frame(self.window, padx=10, pady=10)
        self.frameGrid.pack(expand=True, fill='both')

        # MUDANÇA: Usando tk.Frame em vez de ttk.Frame
        self.frameControls = tk.Frame(self.window, padx=10, pady=5)
        self.frameControls.pack(side='bottom', fill='x')

        self.createGrid()

        # --- Botões de Controle ---
        # MUDANÇA: Usando tk.Button em vez de ttk.Button
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
                # MUDANÇA: Usando tk.Entry em vez de ttk.Entry
                entry = tk.Entry(self.frameGrid, width=5)
                entry.grid(row=i, column=j, padx=2, pady=2, sticky='ew')
                hqRow.append(entry)
            
            self.hqA.append(hqRow)

            # MUDANÇA: Usando tk.Label em vez de ttk.Label
            tk.Label(self.frameGrid, text=" = ").grid(row=i, column=self.headquarterSize, padx=5)
            
            # MUDANÇA: Usando tk.Entry em vez de ttk.Entry
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
        self.window.geometry("250x400") # Janela mais fina
        self.window.transient(parentApp.root)

        self.entries = []
        
        # Frame principal com rolagem (caso a matriz seja muito grande)
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
        
        # Cria a grade de entradas
        self.createGrid(scrollLableFrame)

        # Frame para o botão de salvar
        controlsFrame = tk.Frame(self.window, padx=10, pady=5)
        controlsFrame.pack(side='bottom', fill='x')

        saveBtn = tk.Button(controlsFrame, text="Salvar vetor", command=self.setX0Vector)
        saveBtn.pack(side='right', padx=5)

    def createGrid(self, container):
        for i in range(self.x0Size):
            # Adiciona um label (x0, x1, x2...)
            tk.Label(container, text=f"x[{i}]:").grid(row=i, column=0, padx=5, pady=5)
            
            # Adiciona o campo de entrada
            entry = tk.Entry(container, width=15)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky='ew')
            entry.insert(0, "0.0") # Insere 0.0 como padrão
            self.entries.append(entry)
            
        container.columnconfigure(1, weight=1)

    def setX0Vector(self):
        vectorList = []
        try:
            # Lê os valores de todos os campos de entrada
            for i in range(self.x0Size):
                val = float(self.entries[i].get())
                vectorList.append(val)
                
            x0Vector = np.array(vectorList, dtype=float)
            
            # Envia o vetor de volta para a aplicação principal
            self.parentApp.setInitVector(x0Vector)
            self.window.destroy()

        except ValueError:
            messagebox.showerror("Erro de Formato", "Todos os campos devem ser preenchidos com números válidos.", parent=self.window)

class InterfaceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de métodos muméricos")
        self.root.geometry("800x600")

        # --- MUDANÇA: Variáveis para guardar a matriz ---
        self.filePath = None # Guarda o caminho do arquivo
        self.insertAHeadquarter = None # Guarda a Matriz A manual
        self.insertBHeadquarter = None # Guarda o vector B manual
        self.x0Vector = None
        self.x0VectorSize = 0

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
        label = ttk.Label(self.rootFrame, text="Conteúdo da aba 'Raízes' aqui.", font=("Arial", 14))
        label.pack(expand=True, anchor="center")

    def createSystemFrame(self):
        mainFrame = ttk.Frame(self.systemFrame)
        mainFrame.pack(fill='x', expand=True, side='top')

        leftFrame = ttk.Frame(mainFrame)
        leftFrame.pack(side='left', fill='x', expand=True, padx=10)

        rightFrame = ttk.Frame(mainFrame)
        rightFrame.pack(side='right', fill='y', padx=10)

        ttk.Label(leftFrame, text="Solução de sistemas lineares:", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, sticky='w', pady=10)

        # --- MUDANÇA: Frame de Arquivo modificado ---
        ttk.Label(leftFrame, text="Escolher matriz:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        
        fileFrame = ttk.Frame(leftFrame)
        fileFrame.grid(row=1, column=1, sticky='we')
        
        self.fileBtn = ttk.Button(fileFrame, text="Carregar Arquivo...", command=self.openFileWindow)
        self.fileBtn.pack(side='left')

        # --- NOVO BOTÃO ---
        self.setHeadquarterBtn = ttk.Button(fileFrame, text="Adicionar matriz", command=self.setHeadquarterWindow)
        self.setHeadquarterBtn.pack(side='left', padx=10)
        
        self.infoBtn = ttk.Button(fileFrame, text="i", command=self.showInfo, width=2)
        self.infoBtn.pack(side='left', padx=5)

        self.selectedFileLabel = ttk.Label(leftFrame, text="Nenhuma matriz carregada", font=("Arial", 9, "italic"))
        self.selectedFileLabel.grid(row=2, column=0, columnspan=2, sticky='w', padx=5)

        # (O resto da aba continua igual)
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
        self.setVectorBtn.config(state="disabled") # Começa desabilitado
        
        self.infoVectorBtn = ttk.Button(vectorFrame, text="i", command=self.infoX0, width=2)
        self.infoVectorBtn.pack(side='left', padx=5)

        leftFrame.columnconfigure(1, weight=1)

        # --- Frame Direita (Controles) ---
        ttk.Label(rightFrame, text="Método de solução:").pack(anchor='w')
        directMethods = ["Gauss (Simples)", "Gauss (Piv. Parcial)", "Gauss (Piv. Completo)", "Decomposição LU", "Fatoração de Cholesky", "Gauss-Jacobi", "Gauss-Seidel"]
        self.methodsComboBox = ttk.Combobox(rightFrame, values=directMethods, state="readonly")
        self.methodsComboBox.pack(fill='x', expand=True, pady=5)
        self.methodsComboBox.current(0)
        self.calculateBtn = ttk.Button(rightFrame, text="Calcular matriz", command=self.calculate)
        self.calculateBtn.pack(fill='x', expand=True, ipady=10, side='bottom', pady=20)

        # --- Área de Resultado ---
        ttk.Label(self.systemFrame, text="Resultados:", font=("Arial", 12, "bold")).pack(anchor='w', padx=10, pady=(20, 5))
        self.resultText = scrolledtext.ScrolledText(self.systemFrame, height=10, font=("Courier New", 10))
        self.resultText.pack(fill='both', expand=True, padx=10, pady=5)
        self.resultText.config(state="disabled")

#####################################################################################################
    def openFileWindow(self):
        self.filePath = filedialog.askopenfilename(
            title="Selecionar arquivo",
            filetypes=(("Arquivos de Texto", "*.txt"), ("Todos os arquivos", "*.*"))
        )
        if self.filePath:
            try:
                # Carrega em modo "silencioso"
                fileToOpen = io.StringIO()
                with redirect_stdout(fileToOpen):
                    hqATemp, hqBTemp = le.openFile(self.filePath)
                
                if hqATemp is None: # Se openFile falhou
                    self.selectedFileLabel.config(text="Erro ao ler o arquivo. Verifique o formato.")
                    self.filePath = None
                    return

                # Se deu certo, atualiza a interface
                splitName = self.filePath.split('/')[-1]
                self.selectedFileLabel.config(text=f"Arquivo: {splitName}")
                
                # --- ACRESCENTADO ---
                self.x0SizeHq = hqATemp.shape[0] # Salva o x0Size
                self.setVectorBtn.config(state="normal") # Habilita o botão do vetor
                self.initialVector = None # Reseta o vetor
                self.insertAHeadquarter = None # Reseta a matriz manual
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

##################################################################################################################################################################
    # --- NOVA FUNÇÃO ---
    def setHeadquarterWindow(self):
        # Cria a janela pop-up passando a si mesmo (self) como pai
        self.headquarterPopup = headquarterEntryWindow(self)

    # --- NOVA FUNÇÃO ---
    def setManualHq(self, A, b):
        self.insertAHeadquarter = A
        self.insertBHeadquarter = b
        
        # Limpa o caminho do arquivo para não haver conflito
        self.filePath = None

        self.x0SizeHq = A.shape[0] # Salva o x0Size
        self.setVectorBtn.config(state="normal") # Habilita o botão
        self.initialVector = None # Reseta o vetor
        
        # Atualiza o label para mostrar que a matriz foi carregada
        self.selectedFileLabel.config(text=f"Matriz manual {A.shape[0]}x{A.shape[1]} carregada.")
        print("Matriz manual recebida pela interface principal.")
        print("Matriz A:")
        print(self.insertAHeadquarter)
        print("\nvetor b:")
        print(self.insertBHeadquarter)

    def x0Window(self):
        # 'self.x0SizeHq' foi definido ao carregar a matriz
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
        
        # --- LÓGICA DE CÁLCULO ATUALIZADA ---
        ACalc, BCalc = None, None
        
        # 1. Verifica se existe uma matriz manual
        if self.insertAHeadquarter is not None and self.insertBHeadquarter is not None:
            ACalc = self.insertAHeadquarter.copy()
            BCalc = self.insertBHeadquarter.copy()
            self.resultText.insert("end", "Iniciando cálculo...\n")
        
        # 2. Se não, verifica se existe um caminho de arquivo
        elif self.filePath:
            self.resultText.insert("end", f"Carregando dados do arquivo: {self.filePath.split('/')[-1]}...\n")
            try:
                # Captura os prints da função openFile
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
        
        # 3. Se não houver nenhum dos dois
        else:
            self.resultText.insert("end", "ERRO: Nenhum arquivo ou matriz manual foi carregado.")
            self.resultText.config(state="disabled")
            return
            
        # 4. Captura o output (os prints) das suas funções de cálculo
        f = io.StringIO()
        finalResult = None
        
        try:
            with redirect_stdout(f):
                # colocar .copy nos parametros
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

                        le.gaussJacobiConvergence(ACalc.copy())
                        
                        finalResult = le.gaussJacobi(ACalc.copy(), BCalc.copy(), tolerance, maxIter, xk=self.initialVector)
                        
                    except ValueError:
                        finalResult = "ERRO: Verifique se a tolerância e o nº de iterações são números válidos."
                    except Exception as e:
                        finalResult = f"ERRO inesperado: {e}"
                elif chosenMethod == "Gauss-Seidel":
                    try:
                        tolerance = float(self.setTolerance.get())
                        maxIter = int(self.setIterations.get())

                        le.sassenfeld(ACalc.copy()) 
                        
                        finalResult = le.gaussSeidel(ACalc.copy(), BCalc.copy(), tolerance, maxIter, xk=self.initialVector)
                        
                    except ValueError:
                        finalResult = "ERRO: Verifique se a tolerância e o nº de iterações são números válidos."
                    except Exception as e:
                        finalResult = f"ERRO inesperado: {e}"
            
            output = f.getvalue()
            
            # 6. Exibe o resultado
            if output:
                self.resultText.insert("end", "\n--- Saída do Console da Função ---\n")
                self.resultText.insert("end", output)
            
            if isinstance(finalResult, str): # Se a função retornou uma string (erro)
                self.resultText.insert("end", f"\nERRO: {finalResult}")
            else:
                 self.resultText.insert("end", "\n--- Cálculo Concluído ---")
                 
        except Exception as e:
            # Captura erros que podem acontecer durante o cálculo (ex: divisão por 0)
            self.resultText.insert("end", f"\n--- ERRO DURANTE O CÁLCULO ---\n{type(e).__name__}: {e}")

        self.resultText.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    InterfaceApp(root)
    root.mainloop()