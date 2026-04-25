import webbrowser
import requests
import time
import random

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, RoundedRectangle, Ellipse
from kivy.utils import get_color_from_hex
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.clock import Clock


# 🎨 CORES
DARK_PURPLE = get_color_from_hex('#1A0B3E')
ORANGE = (1, 0.45, 0, 1)
RED = get_color_from_hex('#FF3B30')
YELLOW = get_color_from_hex('#FFD60A')

Window.clearcolor = DARK_PURPLE


# 🔥 SUA IMAGEM SPLASH
SPLASH_IMG = "https://i.ibb.co/CprJXNN2/file-00000000c394720e90c297a08052e35a.png"


# 🖼️ LOGOS
LOGO_APP = "https://i.ibb.co/5hpvnHgN/image-e6ab577f.png"
LOGO_SHOPEE = "https://i.ibb.co/Xxd0Gxcz/Shopee-logo-svg.png"

ICON_SEARCH = "https://img.icons8.com/ios-filled/50/search.png"

URL_JSON = "https://raw.githubusercontent.com/Fabio257752/produtos-app/main/produtos.json"

LINK_PROMO = "https://s.shopee.com.br/1gEvlPfFPR?share_channel_code=1"


def carregar_produtos():
    try:
        r = requests.get(URL_JSON, timeout=5)
        return r.json()
    except:
        return []


# 🔥 SPLASH SCREEN PROFISSIONAL
class SplashScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(*DARK_PURPLE)
            self.bg = RoundedRectangle(size=self.size, pos=self.pos)

        self.bind(size=self.update_bg, pos=self.update_bg)

        self.img = AsyncImage(
            source=SPLASH_IMG,
            allow_stretch=True,
            keep_ratio=False
        )

        self.add_widget(self.img)

        # só continua quando carregar
        self.img.bind(on_load=self.imagem_carregada)

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def imagem_carregada(self, *args):
        # tempo extra depois de carregar
        Clock.schedule_once(self.ir_para_app, 3)

    def ir_para_app(self, dt):
        self.clear_widgets()
        self.add_widget(AppPromo().build())


# 💥 PREÇO ANIMADO
class PromoLabel(BoxLayout):
    def __init__(self, text, **kwargs):
        super().__init__(size_hint_y=None, height=30, padding=(6, 3), **kwargs)

        with self.canvas.before:
            Color(1, 0, 0, 1)
            self.bg = RoundedRectangle(radius=[6])

        self.bind(size=self.update_bg, pos=self.update_bg)

        self.label = Label(
            text=f"Só R$ {text}",
            color=(1, 1, 0, 1),
            bold=True,
            font_size='13sp'
        )

        self.add_widget(self.label)
        self.piscar()

    def piscar(self):
        anim = Animation(opacity=0.3, duration=0.5) + Animation(opacity=1, duration=0.5)
        anim.repeat = True
        anim.start(self.label)

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size


# 🧱 CARD PRODUTO
class ProductCard(BoxLayout):
    def __init__(self, produto, **kwargs):
        super().__init__(orientation='vertical', padding=6, spacing=4,
                         size_hint_y=None, height=420)

        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = RoundedRectangle(radius=[12])

        self.bind(pos=self.update_rect, size=self.update_rect)

        img_box = BoxLayout(size_hint_y=0.7, padding=5)

        with img_box.canvas.before:
            Color(1, 1, 1, 1)
            self.bg_img = RoundedRectangle(radius=[10])

        img_box.bind(pos=self.update_bg_img, size=self.update_bg_img)

        img = AsyncImage(
            source=produto.get("imagem", ""),
            allow_stretch=True,
            keep_ratio=True
        )

        img_box.add_widget(img)
        self.add_widget(img_box)

        self.add_widget(Label(
            text=produto.get("nome", "Sem nome"),
            color=(0, 0, 0, 1),
            font_size='13sp',
            size_hint_y=0.1,
            shorten=True
        ))

        if produto.get("preco"):
            valor = f"{float(produto['preco']):.2f}".replace(".", ",")
            box = BoxLayout(size_hint_y=0.1)
            box.add_widget(PromoLabel(valor))
            self.add_widget(box)

        self.view_label = Label(
            text=f"{random.randint(8, 47)} pessoas vendo agora",
            color=(0.2, 0.2, 0.2, 1),
            font_size='11sp',
            size_hint_y=0.08
        )
        self.add_widget(self.view_label)

        self.stock_label = Label(
            text=f"Últimas {random.randint(3, 12)} unidades",
            color=(1, 0, 0, 1),
            bold=True,
            font_size='11sp',
            size_hint_y=0.08
        )
        self.add_widget(self.stock_label)

        btn = Button(
            text=" PEGAR OFERTA AGORA",
            background_normal='',
            background_color=ORANGE,
            color=(1, 1, 1, 1),
            bold=True,
            font_size='14sp',
            size_hint_y=0.15
        )

        btn.bind(on_press=lambda x: webbrowser.open(produto.get("link", LINK_PROMO)))
        self.add_widget(btn)

        self.animar_botao(btn)

        Clock.schedule_interval(self.atualizar_prova_social, 3)

    def atualizar_prova_social(self, dt):
        self.view_label.text = f"{random.randint(5, 60)} pessoas vendo agora"
        self.stock_label.text = f"Últimas {random.randint(2, 10)} unidades"

    def animar_botao(self, btn):
        anim = Animation(size_hint_y=0.17, duration=0.6) + Animation(size_hint_y=0.15, duration=0.6)
        anim.repeat = True
        anim.start(btn)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def update_bg_img(self, instance, value):
        self.bg_img.pos = instance.pos
        self.bg_img.size = instance.size


# 🔥 BOTÃO ESPECIAL
class BotaoOfertaEspecial(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(size_hint_y=None, height=200, padding=10, **kwargs)

        with self.canvas.before:
            Color(1, 0.2, 0, 1)
            self.bg = RoundedRectangle(radius=[20])

        self.bind(pos=self.update_bg, size=self.update_bg)

        self.btn = Button(
            text="🔥 NÃO ENCONTROU?\nVEJA OFERTAS DO DIA!",
            markup=True,
            background_normal='',
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 1),
            bold=True,
            font_size='18sp'
        )

        self.btn.bind(on_press=lambda x: webbrowser.open(LINK_PROMO))
        self.add_widget(self.btn)

        self.animar()

    def animar(self):
        anim = Animation(opacity=0.6, duration=0.6) + Animation(opacity=1, duration=0.6)
        anim.repeat = True
        anim.start(self)

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size


# ⏳ BOTÃO RELÂMPAGO
class BotaoOfertas(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(size_hint_y=None, height=70, **kwargs)

        self.end_time = time.time() + 3600
        self.show_plus = True

        self.btn = Button(
            text="",
            markup=True,
            background_normal='',
            background_color=RED,
            color=(1, 1, 0, 1),
            bold=True,
            font_size='15sp'
        )

        self.btn.bind(on_press=lambda x: webbrowser.open(LINK_PROMO))
        self.add_widget(self.btn)

        Clock.schedule_interval(self.piscar, 0.2)
        Clock.schedule_interval(self.atualizar_tempo, 1)

    def piscar(self, dt):
        self.show_plus = not self.show_plus

    def atualizar_tempo(self, dt):
        restante = int(self.end_time - time.time())

        if restante <= 0:
            self.btn.text = "OFERTAS ENCERRADAS"
            return

        minutos = restante // 60
        segundos = restante % 60

        simbolo = "[size=60][b]+[/b][/size]" if self.show_plus else ""

        self.btn.text = f"{simbolo} OFERTAS RELÂMPAGO ({minutos:02d}:{segundos:02d})"


# 📱 APP PRINCIPAL
class AppPromo(App):
    def build(self):
        main = BoxLayout(orientation='vertical', padding=15, spacing=10)

        header = BoxLayout(size_hint_y=None, height=150)
        container = BoxLayout(size_hint=(1, 1))

        logos_row = BoxLayout(size_hint=(None, None), size=(420, 120), spacing=15,
                              pos_hint={'center_x': 0.5, 'top': 1})

        logo_box = BoxLayout(size_hint=(0.7, 1))
        logo_box.add_widget(AsyncImage(source=LOGO_APP))

        shopee_box = BoxLayout(size_hint=(0.1, 1))
        circle_box = BoxLayout(size_hint=(None, None), size=(130, 130))

        with circle_box.canvas.before:
            Color(1, 1, 1, 1)
            self.circle = Ellipse(pos=circle_box.pos, size=circle_box.size)

        def update_circle(instance, value):
            self.circle.pos = instance.pos
            self.circle.size = instance.size

        circle_box.bind(pos=update_circle, size=update_circle)

        circle_box.add_widget(AsyncImage(source=LOGO_SHOPEE))
        shopee_box.add_widget(circle_box)

        logos_row.add_widget(logo_box)
        logos_row.add_widget(shopee_box)

        container.add_widget(logos_row)
        header.add_widget(container)
        main.add_widget(header)

        search = BoxLayout(size_hint_y=None, height=140, orientation='vertical', spacing=8)

        top_bar = BoxLayout(size_hint_y=None, height=50)
        top_bar.add_widget(Label())

        toggle_sair = ToggleButton(text="Sair", size_hint=(None, None), size=(70, 40),
                                   color=(1, 1, 1, 1), background_normal='', background_color=(0, 0, 0, 0))

        with toggle_sair.canvas.before:
            Color(0, 0, 0, 1)
            toggle_sair.bg = RoundedRectangle(radius=[10])

        def update_btn(*args):
            toggle_sair.bg.pos = toggle_sair.pos
            toggle_sair.bg.size = toggle_sair.size

        toggle_sair.bind(pos=update_btn, size=update_btn)

        toggle_sair.bind(on_press=lambda x: App.get_running_app().stop() if x.state == "down" else None)

        top_bar.add_widget(toggle_sair)

        search_box = BoxLayout(size_hint_y=None, height=80, spacing=10, padding=(10, 5))

        with search_box.canvas.before:
            Color(1, 1, 1, 1)
            self.search_bg = RoundedRectangle(radius=[12])

        search_box.bind(pos=self.update_search_bg, size=self.update_search_bg)

        search_box.add_widget(AsyncImage(source=ICON_SEARCH, size_hint_x=None, width=30))

        self.input_busca = TextInput(hint_text='Buscar produtos...', multiline=False,
                                    font_size='18sp', background_color=(0, 0, 0, 0),
                                    foreground_color=(0, 0, 0, 1))

        self.input_busca.bind(text=self.filtrar_produtos)
        search_box.add_widget(self.input_busca)

        search.add_widget(top_bar)
        search.add_widget(search_box)
        search.add_widget(BotaoOfertas())

        main.add_widget(search)

        self.produtos = carregar_produtos()

        scroll = ScrollView()
        self.grid = GridLayout(cols=2, spacing=12, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))

        scroll.add_widget(self.grid)
        main.add_widget(scroll)

        self.atualizar_lista(self.produtos)

        return main

    def update_search_bg(self, instance, value):
        self.search_bg.pos = instance.pos
        self.search_bg.size = instance.size

    def filtrar_produtos(self, instance, value):
        termo = value.lower()
        filtrados = [p for p in self.produtos if termo in p.get("nome", "").lower()]
        self.atualizar_lista(filtrados)

    def atualizar_lista(self, lista):
        self.grid.clear_widgets()

        if not lista:
            self.grid.add_widget(BotaoOfertaEspecial())
            return

        for p in lista:
            self.grid.add_widget(ProductCard(p))


# 🚀 APP COM SPLASH
class MainApp(App):
    def build(self):
        root = BoxLayout()
        root.add_widget(SplashScreen())
        return root


if __name__ == "__main__":
    MainApp().run()
