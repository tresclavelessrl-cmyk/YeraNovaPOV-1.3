"""Pantalla de login para Android"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from loguru import logger


class LoginScreen(Screen):
    """Pantalla de autenticación de usuario"""

    def __init__(self, **kwargs):
        """Inicializar pantalla de login"""
        super().__init__(**kwargs)
        self.name = "login"
        
        # Layout principal
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        
        # Título
        titulo = Label(
            text="YeraPOV - Sistema POS",
            size_hint_y=0.2,
            font_size="24sp",
        )
        layout.add_widget(titulo)
        
        # Form layout
        form_layout = GridLayout(cols=2, spacing=10, size_hint_y=0.5)
        
        # Campo usuario
        form_layout.add_widget(Label(text="Usuario:", size_hint_x=0.3))
        self.txt_usuario = TextInput(multiline=False, size_hint_x=0.7)
        form_layout.add_widget(self.txt_usuario)
        
        # Campo contraseña
        form_layout.add_widget(Label(text="Contraseña:", size_hint_x=0.3))
        self.txt_password = TextInput(multiline=False, password=True, size_hint_x=0.7)
        form_layout.add_widget(self.txt_password)
        
        layout.add_widget(form_layout)
        
        # Botón de login
        btn_login = Button(text="Iniciar Sesión", size_hint_y=0.15)
        btn_login.bind(on_press=self.on_login)
        layout.add_widget(btn_login)
        
        self.add_widget(layout)
        logger.info("Pantalla de login creada")

    def on_login(self, instance):
        """Evento de login"""
        usuario = self.txt_usuario.text
        password = self.txt_password.text
        
        logger.info(f"Intento de login: {usuario}")
        # TODO: Validar credenciales
