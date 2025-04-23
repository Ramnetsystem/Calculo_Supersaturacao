import kivy
import os
import numpy as np
import pandas as pd
from kivy.app import App
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.uix.widget import Widget
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stencilview import StencilView
from kivy.graphics import RoundedRectangle, Color, Rectangle
from kivy.core.window import Window
from kivy.lang import Builder

# Caminho do Excel
file_path = os.path.join(os.path.dirname(__file__), "Calculo supersaturacao RAM.xlsx")

# Carregar dados
df = pd.read_excel(file_path, sheet_name="Sheet1")
df = df.iloc[1:].drop(columns=["Unnamed: 0", "p/busca", "Unnamed: 6", "Unnamed: 7",
                               "Buscando", "Escrever aqui os valores para busca",
                               "Unnamed: 10", "Unnamed: 11"])
df.columns = ["temperatura", "brix", "pureza", "supersaturacao"]
df = df.dropna().astype(float)

# Estilo do slider
kv = '''
<CustomSlider>:
    background_color: 1, 0.5, 0, 1
    background_width: '5dp'
    cursor_color: 0.2, 0.7, 1, 1
    cursor_size: '20dp', '20dp'
    value_track: True
    value_track_color: 1, 0.5, 0, 1
    value_track_width: 5
'''
Builder.load_string(kv)

class CustomSlider(Slider):
    pass

# Imagem com cantos arredondados sem fundo branco
class RoundedImageNoBackground(StencilView):
    def __init__(self, source="imglogo.png", **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            # Usando o mesmo preto do fundo para o StencilView
            self.rect_color = Color(0, 0, 0, 1)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[20])
        self.bind(pos=self.update_rect, size=self.update_rect)

        self.img = AsyncImage(source=source, allow_stretch=True, keep_ratio=True)
        self.add_widget(self.img)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.img.pos = self.pos
        self.img.size = self.size

class SupersaturacaoApp(App):
    def build(self):
        Window.clearcolor = (0, 0, 0, 1)

        root = AnchorLayout(anchor_x='center', anchor_y='center')
        layout = BoxLayout(orientation='vertical', size_hint=(0.8, None), spacing=30)
        layout.bind(minimum_height=layout.setter('height'))

        # Logo com cantos arredondados sem fundo branco
        logo = RoundedImageNoBackground(size_hint=(1, None), height=120)
        layout.add_widget(logo)

        # Widget espaçador
        spacer = Widget(size_hint=(1, None), height=20)
        layout.add_widget(spacer)

        # Sliders e labels - garantindo que funcionem corretamente
        temp_box = BoxLayout(orientation='vertical', size_hint=(1, None), height=70, spacing=5)
        self.temp_label = Label(text="Temperatura (°C): 70", color=(1, 1, 1, 1), size_hint=(1, None), height=20)
        self.temp_slider = CustomSlider(min=60, max=80, value=70, step=1, size_hint=(1, None), height=30)
        self.temp_slider.bind(value=self.atualizar_resultado)
        temp_box.add_widget(self.temp_label)
        temp_box.add_widget(self.temp_slider)
        layout.add_widget(temp_box)

        # Segundo slider
        brix_box = BoxLayout(orientation='vertical', size_hint=(1, None), height=70, spacing=5)
        self.brix_label = Label(text="Brix (°Brix): 75", color=(1, 1, 1, 1), size_hint=(1, None), height=20)
        self.brix_slider = CustomSlider(min=60, max=90, value=75, step=1, size_hint=(1, None), height=30)
        self.brix_slider.bind(value=self.atualizar_resultado)
        brix_box.add_widget(self.brix_label)
        brix_box.add_widget(self.brix_slider)
        layout.add_widget(brix_box)

        # Terceiro slider
        pureza_box = BoxLayout(orientation='vertical', size_hint=(1, None), height=70, spacing=5)
        self.pureza_label = Label(text="Pureza (%): 80", color=(1, 1, 1, 1), size_hint=(1, None), height=20)
        self.pureza_slider = CustomSlider(min=75, max=90, value=80, step=1, size_hint=(1, None), height=30)
        self.pureza_slider.bind(value=self.atualizar_resultado)
        pureza_box.add_widget(self.pureza_label)
        pureza_box.add_widget(self.pureza_slider)
        layout.add_widget(pureza_box)

        # Resultado
        self.label_resultado = Label(text="Supersaturação: ---", color=(1, 1, 1, 1), size_hint=(1, None), height=30)
        layout.add_widget(self.label_resultado)

        # Atualizar resultado inicial
        self.atualizar_resultado(None, None)
        
        root.add_widget(layout)
        return root

    def atualizar_resultado(self, instance, value):
        temp = int(self.temp_slider.value)
        brix = int(self.brix_slider.value)
        pureza = int(self.pureza_slider.value)

        self.temp_label.text = f"Temperatura (°C): {temp}"
        self.brix_label.text = f"Brix (°Brix): {brix}"
        self.pureza_label.text = f"Pureza (%): {pureza}"

        tolerancia = 0.1
        linha = df[
            (np.isclose(df["temperatura"], temp, atol=tolerancia)) &
            (np.isclose(df["brix"], brix, atol=tolerancia)) &
            (np.isclose(df["pureza"], pureza, atol=tolerancia))
        ]

        if not linha.empty:
            resultado = linha["supersaturacao"].values[0]
            self.label_resultado.text = f"Supersaturação: {resultado:.3f}"
        else:
            self.label_resultado.text = "Valores não encontrados!"

if __name__ == "__main__":
    SupersaturacaoApp().run()