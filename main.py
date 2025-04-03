import kivy
import os
import numpy as np
from kivy.app import App
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
import pandas as pd
from kivy.lang import Builder
from kivy.core.window import Window

# Obter o caminho do arquivo na raiz do projeto
file_path = os.path.join(os.path.dirname(__file__), "Calculo supersaturacao RAM.xlsx")

# Carregar os dados do Excel
df = pd.read_excel(file_path, sheet_name="Sheet1")

# Limpar e organizar os dados
df = df.iloc[1:].drop(columns=["Unnamed: 0", "p/busca", "Unnamed: 6", "Unnamed: 7", 
                               "Buscando", "Escrever aqui os valores para busca", 
                               "Unnamed: 10", "Unnamed: 11"])
df.columns = ["temperatura", "brix", "pureza", "supersaturacao"]
df = df.dropna().astype(float)

# Criar um arquivo kv para estilização customizada
kv = '''
<CustomSlider>:
    background_color: 1, 0.5, 0, 1      # Cor laranja para o track
    background_width: '5dp'             # Aumentando a espessura para 5dp
    cursor_color: 1, 1, 1, 1            # Cursor branco
    cursor_size: '20dp', '20dp'         # Tamanho do cursor
    value_track: True                   # Habilita o track de valor
    value_track_color: 1, 0.5, 0, 1     # Cor laranja para o track de valor
    value_track_width: 5                # Espessura do track de valor
'''

Builder.load_string(kv)

# Classe de slider personalizada
class CustomSlider(Slider):
    pass

class SupersaturacaoApp(App):
    def build(self):
        # Definir o fundo da janela como preto
        Window.clearcolor = (0, 0, 0, 1)
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Adicionar sliders para Temperatura, Brix e Pureza usando a classe personalizada
        self.temp_slider = CustomSlider(min=60, max=80, value=70, step=1)
        self.temp_slider.bind(value=self.atualizar_resultado)
        self.temp_label = Label(text=f"Temperatura (°C): {int(self.temp_slider.value)}")
        layout.add_widget(self.temp_label)
        layout.add_widget(self.temp_slider)

        self.brix_slider = CustomSlider(min=60, max=90, value=75, step=1)
        self.brix_slider.bind(value=self.atualizar_resultado)
        self.brix_label = Label(text=f"Brix (°Brix): {int(self.brix_slider.value)}")
        layout.add_widget(self.brix_label)
        layout.add_widget(self.brix_slider)

        self.pureza_slider = CustomSlider(min=75, max=90, value=80, step=1)
        self.pureza_slider.bind(value=self.atualizar_resultado)
        self.pureza_label = Label(text=f"Pureza (%): {int(self.pureza_slider.value)}")
        layout.add_widget(self.pureza_label)
        layout.add_widget(self.pureza_slider)

        # Rótulo para exibir o resultado
        self.label_resultado = Label(text="Supersaturação: ---")
        layout.add_widget(self.label_resultado)

        return layout

    def atualizar_resultado(self, instance, value):
        # Obter os valores dos sliders
        temp = int(self.temp_slider.value)
        brix = int(self.brix_slider.value)
        pureza = int(self.pureza_slider.value)

        # Atualizar os labels com os valores dos sliders
        self.temp_label.text = f"Temperatura (°C): {temp}"
        self.brix_label.text = f"Brix (°Brix): {brix}"
        self.pureza_label.text = f"Pureza (%): {pureza}"

        # Imprimir os valores para depuração
        print(f"Temperatura: {temp}, Brix: {brix}, Pureza: {pureza}")

        # Filtrar a linha correspondente na tabela, permitindo uma comparação aproximada
        tolerancia = 0.1  # Defina uma tolerância de comparação
        linha = df[
            (np.isclose(df["temperatura"], temp, atol=tolerancia)) & 
            (np.isclose(df["brix"], brix, atol=tolerancia)) & 
            (np.isclose(df["pureza"], pureza, atol=tolerancia))
        ]

        # Imprimir a linha filtrada para depuração
        print(f"Linha filtrada:\n{linha}")

        # Atualizar o rótulo com o resultado ou mensagem de erro
        if not linha.empty:
            resultado = linha["supersaturacao"].values[0]
            self.label_resultado.text = f"Supersaturação: {resultado:.3f}"
        else:
            self.label_resultado.text = "Valores não encontrados!"

if __name__ == "__main__":
    SupersaturacaoApp().run()