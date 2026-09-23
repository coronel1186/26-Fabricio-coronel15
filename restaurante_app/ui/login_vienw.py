import os
import tkinter as tk
from tkinter import ttk
from typing import Callable

try:
    from PIL import Image, ImageTk
except ModuleNotFoundError:
    Image = None
    ImageTk = None


class LoginView(tk.Frame):
    def __init__(self, parent: tk.Widget, restaurante_servicio, on_login_success: Callable, assets_path: str = "") -> None:
        super().__init__(parent)
        self.restaurante_servicio = restaurante_servicio
        self.on_login_success = on_login_success
        self.assets_path = assets_path
        self.logo_image = None

        self._crear_componentes()

    def _crear_componentes(self) -> None:
        card = ttk.Frame(self, padding="25")
        card.place(relx=0.5, rely=0.5, anchor="center")

        logo_file = os.path.join(self.assets_path, "logo", "logo.png.png") if self.assets_path else ""
        if os.path.exists(logo_file) and Image is not None and ImageTk is not None:
            try:
                pil_img = Image.open(logo_file).resize((80, 80))
                self.logo_image = ImageTk.PhotoImage(pil_img)
                lbl_logo = ttk.Label(card, image=self.logo_image)
                lbl_logo.pack(pady=(0, 10))
            except Exception as e:
                print(f"No se pudo cargar el logo: {e}")

        lbl_titulo = ttk.Label(
            card,
            text="RESTAURANTE APP",
            font=("Helvetica", 16, "bold")
        )
        lbl_titulo.pack(pady=(0, 5))

        lbl_subtitulo = ttk.Label(
            card,
            text="Acceso al Sistema (Semana 15 - Eventos)",
            font=("Helvetica", 10)
        )
        lbl_subtitulo.pack(pady=(0, 15))

        lbl_usuario = ttk.Label(card, text="Usuario o ID:", font=("Helvetica", 10))
        lbl_usuario.pack(anchor="w", pady=(5, 2))

        self.usuario_entry = ttk.Entry(card, width=30, font=("Helvetica", 10))
        self.usuario_entry.pack(pady=(0, 10))
        self.usuario_entry.focus()

        lbl_clave = ttk.Label(card, text="Contraseña:", font=("Helvetica", 10))
        lbl_clave.pack(anchor="w", pady=(5, 2))

        self.clave_entry = ttk.Entry(card, width=30, font=("Helvetica", 10), show="*")
        self.clave_entry.pack(pady=(0, 15))

        self.lbl_error = ttk.Label(
            card,
            text="",
            foreground="red",
            font=("Helvetica", 9)
        )
        self.lbl_error.pack(pady=(0, 10))

        btn_ingresar = ttk.Button(
            card,
            text="Iniciar Sesión",
            command=self._iniciar_sesion
        )
        btn_ingresar.pack(fill="x", ipady=4)

        lbl_nota = ttk.Label(
            card,
            text="* Credenciales de prueba: U001 / 1234  o  U002 / admin",
            font=("Helvetica", 8, "italic")
        )
        lbl_nota.pack(pady=(15, 0))

        self.clave_entry.bind("<Return>", lambda event: self._iniciar_sesion())
        self.usuario_entry.bind("<Return>", lambda event: self._iniciar_sesion())

    def _iniciar_sesion(self) -> None:
        usuario_txt = self.usuario_entry.get().strip()
        clave_txt = self.clave_entry.get().strip()

        if not usuario_txt or not clave_txt:
            self.lbl_error.config(text="Por favor, ingrese usuario y contraseña.")
            return

        usuario_validado = self.restaurante_servicio.validar_acceso(usuario_txt, clave_txt)

        if usuario_validado:
            self.lbl_error.config(text="")
            self.usuario_entry.delete(0, tk.END)
            self.clave_entry.delete(0, tk.END)
            self.on_login_success(usuario_validado)
        else:
            self.lbl_error.config(text="Credenciales incorrectas. Intente nuevamente.")