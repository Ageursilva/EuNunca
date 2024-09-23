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


from kivymd.uix.button import MDRaisedButton
from kivymd.app import MDApp

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
        self.separator_height = 0

        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))

        creditos_label = Label(
            text="Desenvolvedor: [ref=Ageu]Ageu Silva[/ref]\n"
                 "UX/UI: [ref=Vitor]Vitor Alvim[/ref]\n"
                 "GitHub: [ref=github]https://github.com/Ageursilva/EuNunca[/ref]\n"
                 "PIX: sua_chave_pix@exemplo.com",
            font_size='16sp',
            color=(0.96, 0.93, 0.99, 1),
            markup=True, 
        )
        creditos_label.bind(on_ref_press=self.abrir_link) 
        layout.add_widget(creditos_label)

        fechar_botao = MDRaisedButton(
            text="Fechar",
            md_bg_color=App.get_running_app().theme_cls.primary_color,
            on_press=self.dismiss,
        )
        layout.add_widget(fechar_botao)

        self.content = layout

    def abrir_link(self, instance, ref):
        if ref == 'github':
            webbrowser.open('https://github.com/Ageursilva/EuNunca') 
        if ref == 'Ageu':
            webbrowser.open('https://github.com/Ageursilva') 
        if ref == 'Vitor':
            webbrowser.open('https://www.linkedin.com/in/vitor-alvim-604080319/') 

class EuNuncaApp(MDApp):
    def build(self):
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
            size_hint=(1, 0.1)
        )
        layout.add_widget(titulo_label)

        card = RoundedCard()
        self.frase_label = Label(
            text=self.proxima_frase(),
            font_size='20sp',
            halign='center',
            valign='middle',
            text_size=(dp(200), None), 
            color=(0.96, 0.93, 0.99, 1) 
        )
        card.add_widget(self.frase_label)
        layout.add_widget(card)

        pergunta_label = Label(
            text="Eae, já fez?",
            font_size='18sp',
            color=(1, 1, 1, 1), 
            size_hint=(1, 0.1)
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

        botoes_layout = BoxLayout(size_hint=(1, 0.2), spacing=dp(10))
        botao_nunca = MDRaisedButton(
            text="Eu nunca!",
            md_bg_color=self.theme_cls.primary_color,
            size_hint=(0.4, 0.8),
            on_press=self.clicou_esquerda,
            elevation=5,
        )
        botao_ja = MDRaisedButton(
            text="Eu já!",
            md_bg_color=self.theme_cls.primary_color,
            size_hint=(0.4, 0.8),
            on_press=self.clicou_direita,
            elevation=5,
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
            halign='center'
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