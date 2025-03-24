import tkinter as tk
from tkinter import ttk
import pandas as pd

# Carregar os dados do Excel
df = pd.read_excel("Calculo supersaturacao RAM.xlsx", sheet_name="Sheet1")

# Limpar e organizar os dados
df = df.iloc[1:].drop(columns=["Unnamed: 0", "p/busca", "Unnamed: 6", "Unnamed: 7", 
                               "Buscando", "Escrever aqui os valores para busca", 
                               "Unnamed: 10", "Unnamed: 11"])
df.columns = ["temperatura", "brix", "pureza", "supersaturacao"]
df = df.dropna().astype(float)

# Função para encontrar a supersaturação exata no Excel
def calcular_supersaturacao():
    temp = temp_scale.get()
    brix = brix_scale.get()
    pureza = pureza_scale.get()

    # Filtrar a linha correspondente na tabela
    linha = df[(df["temperatura"] == temp) & (df["brix"] == brix) & (df["pureza"] == pureza)]
    
    if not linha.empty:
        resultado = linha["supersaturacao"].values[0]
        label_resultado.config(text=f"Supersaturação: {resultado:.3f}")
    else:
        label_resultado.config(text="Valores não encontrados!")

# Criar janela
root = tk.Tk()
root.title("Calculadora de Supersaturação")
root.geometry("500x500")

frame = ttk.Frame(root)
frame.pack(expand=True)

# Criar sliders para entrada de valores
def criar_slider(label_text, from_, to):
    ttk.Label(frame, text=label_text, font=("Arial", 12, "bold")).pack(pady=5)
    slider = tk.Scale(frame, from_=from_, to=to, orient="horizontal", length=300)
    slider.pack(pady=5)
    return slider

temp_scale = criar_slider("Temperatura (°C):", 60, 80)
brix_scale = criar_slider("Brix (°Brix):", 60, 90)
pureza_scale = criar_slider("Pureza (%):", 75, 90)

# Botão para calcular
btn_calcular = ttk.Button(frame, text="Calcular Supersaturação", command=calcular_supersaturacao)
btn_calcular.pack(pady=15)

# Rótulo para exibir o resultado
label_resultado = ttk.Label(frame, text="Supersaturação: ---", font=("Arial", 14, "bold"))
label_resultado.pack(pady=10)

# Rodar a interface
root.mainloop()
