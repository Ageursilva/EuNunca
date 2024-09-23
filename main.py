from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window 
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.popup import Popup
import json
import random
import webbrowser 
from kivy.core.text import LabelBase
from kivymd.uix.button import MDRaisedButton
from kivymd.app import MDApp
from kivymd.uix.button import MDFloatingActionButton
from kivy.uix.scrollview import ScrollView
import os
import sys
from kivy.resources import resource_add_path, resource_find

if hasattr(sys, '_MEIPASS'):
    resource_add_path(os.path.join(sys._MEIPASS, 'fonts'))
else:
    
    resource_add_path(os.path.join(os.path.dirname(__file__), 'fonts'))

title_font_path = resource_find('Montserrat.ttf') 
body_font_path = resource_find('OpenSan.ttf') 

if title_font_path:
    LabelBase.register(name='TitleFont', fn_regular=title_font_path)
else:
    print("Erro: Arquivo de fonte 'Montserrat.ttf' não encontrado.")

if body_font_path:
    LabelBase.register(name='BodyFont', fn_regular=body_font_path)
else:
    print("Erro: Arquivo de fonte 'OpenSan.ttf' não encontrado.")
class RoundedCard(BoxLayout):
    def __init__(self, **kwargs):
        super(RoundedCard, self).__init__(**kwargs)
        self.padding = dp(20)
        self.size_hint = (1, 0.6)
        with self.canvas.before:
            Color(0.61, 0.02, 1, 1) 
            self.rect = RoundedRectangle(
                pos=self.pos, size=self.size, radius=[20]
            )
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class CreditosPopup(Popup):
    def __init__(self, **kwargs):
        super(CreditosPopup, self).__init__(**kwargs)
        self.title = "Créditos"
        self.size_hint = (0.8, 0.6)

        scroll_view = ScrollView()
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10), size_hint_y=None)

       
        linha1 = BoxLayout(orientation='horizontal', spacing=dp(5))
        linha1.add_widget(Label(text="Dev:", font_size='14sp', color=(0.96, 0.93, 0.99, 1), bold=True))  # Aplicando negrito diretamente
        dev_label = Label(text="[ref=Ageu]Ageu Silva[/ref]", font_size='14sp', color=(0.96, 0.93, 0.99, 1), markup=True)
        dev_label.bind(on_ref_press=self.abrir_link)
        linha1.add_widget(dev_label)
        layout.add_widget(linha1)

        
        linha2 = BoxLayout(orientation='horizontal', spacing=dp(5))
        linha2.add_widget(Label(text="UX/UI:", font_size='14sp', color=(0.96, 0.93, 0.99, 1), bold=True))  # Aplicando negrito diretamente
        ui_label = Label(text="[ref=Vitor]Vitor Alvim[/ref]", font_size='14sp', color=(0.96, 0.93, 0.99, 1), markup=True)
        ui_label.bind(on_ref_press=self.abrir_link)
        linha2.add_widget(ui_label)
        layout.add_widget(linha2)

       
        linha3 = BoxLayout(orientation='horizontal') 
        linha3.add_widget(Label(text="GitHub:", font_size='14sp', color=(0.96, 0.93, 0.99, 1), bold=True))  # Aplicando negrito diretamente
        github_label = Label(text="[ref=github]Repostitório[/ref]", font_size='14sp', color=(0.96, 0.93, 0.99, 1), markup=True)
        github_label.bind(on_ref_press=self.abrir_link)
        linha3.add_widget(github_label)
        layout.add_widget(linha3)


        fechar_botao = MDRaisedButton(
            text="Fechar",
            md_bg_color=App.get_running_app().theme_cls.primary_color,
            on_press=self.dismiss,
            font_name='BodyFont'
        )
        layout.add_widget(fechar_botao)

        
        layout.height = sum(c.height for c in layout.children) + layout.spacing * (len(layout.children) - 1) + layout.padding[1] + layout.padding[3]

        scroll_view.add_widget(layout)
        self.content = scroll_view

    def _update_label_height(self, instance, texture_size):
        
        instance.height = texture_size[1]
        
        self.content.children[0].height = sum(c.height for c in self.content.children[0].children) + self.content.children[0].spacing * (len(self.content.children[0].children) - 1) + self.content.children[0].padding[1] + self.content.children[0].padding[3]

    def abrir_link(self, instance, ref):
        if ref == 'github':
            webbrowser.open('https://github.com/Ageursilva/EuNunca') 
        if ref == 'Ageu':
            webbrowser.open('https://github.com/Ageursilva') 
        if ref == 'Vitor':
            webbrowser.open('https://www.linkedin.com/in/vitor-alvim-604080319/')
class EuNuncaApp(MDApp):
    def build(self):
        if hasattr(sys, '_MEIPASS'):
            os.chdir(sys._MEIPASS)
        with open('frases.json', encoding='utf-8') as f:
            self.frases = json.load(f)
        self.frases_usadas = set()

        self.theme_cls.theme_style = "Dark" 
        self.theme_cls.primary_palette = "Purple" 

        Window.clearcolor = (0.61, 0.02, 1, 1) 

        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))

        titulo_label = Label(
            text="EU NUNCA...",
            font_size='32sp',
            color=(0.96, 0.93, 0.99, 1), 
            size_hint=(1, 0.1),
            font_name='TitleFont' 
        )
        layout.add_widget(titulo_label)

        card = RoundedCard()
        self.frase_label = Label(
            text=self.proxima_frase(),
            font_size='20sp',
            halign='center',
            valign='middle',
            text_size=(dp(200), None), 
            color=(0.96, 0.93, 0.99, 1),
            font_name='BodyFont' 
        )
        card.add_widget(self.frase_label)
        layout.add_widget(card)

        pergunta_label = Label(
            text="Eae, já fez?",
            font_size='18sp',
            color=(1, 1, 1, 1), 
            size_hint=(1, 0.1),
            font_name='BodyFont'
        )
        layout.add_widget(pergunta_label)

        self.mensagem_label = Label(
            text='',
            font_size='18sp',
            halign='center',
            valign='middle',
            color=(0.96, 0.93, 0.99, 1),
            size_hint=(1, 0.2),
            text_size=(Window.width - dp(40), None)
        )
        layout.add_widget(self.mensagem_label)

        botoes_layout = BoxLayout(
            size_hint=(1, 0.3), 
            padding=[dp(20), dp(0)], 
            spacing=dp(10),
            pos_hint={'center_x': 0.5}, 
            orientation='horizontal' 
        )

        botao_nunca = MDFloatingActionButton(
            icon="thumb-down",
            md_bg_color=self.theme_cls.primary_color,
            size_hint=(0.4, 0.8),
            size=(dp(56), dp(56)),
            on_press=self.clicou_esquerda,
        
        )

        botao_ja = MDFloatingActionButton(
            icon="thumb-up",
            md_bg_color=self.theme_cls.primary_color,
            size_hint=(0.4, 0.8),
            size=(dp(56), dp(56)), 
            on_press=self.clicou_direita,
            theme_icon_color="Custom",
            icon_color="white",
          
        )

        botoes_layout.add_widget(botao_nunca)
        botoes_layout.add_widget(botao_ja)

        layout.add_widget(botoes_layout) 

        creditos_label = Label(
            text="[ref=creditos]Créditos[/ref]",
            font_size='16sp',
            color=self.theme_cls.primary_color, 
            markup=True, 
            size_hint=(1, 0.1), 
            halign='center',
            font_name='BodyFont'
        )
        creditos_label.bind(on_ref_press=self.mostrar_creditos)
        layout.add_widget(creditos_label)

        return layout 

    def proxima_frase(self):
        frases_disponiveis = [f for f in self.frases if f not in self.frases_usadas]
        if frases_disponiveis:
            frase = random.choice(frases_disponiveis)
            self.frases_usadas.add(frase)
            return frase
        else:
            self.frases_usadas.clear()
            return self.proxima_frase()

    def clicou_esquerda(self, instance):
        self.mensagem_label.text = "Se safou!"
        self.frase_label.text = self.proxima_frase()

    def clicou_direita(self, instance):
        self.mensagem_label.text = "Beba um drink!"
        self.frase_label.text = self.proxima_frase()

    def mostrar_creditos(self, instance, value): 
        popup = CreditosPopup()
        popup.open()

if __name__ == '__main__':
    EuNuncaApp().run()