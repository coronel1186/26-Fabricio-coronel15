import tkinter as tk
from pathlib import Path
from tkinter import ttk

from restaurante_app.modelos.usuario import Usuario
from restaurante_app.servicios.archivo_servicio import ArchivoServicio
from restaurante_app.servicios.restaurante_servicio import RestauranteServicio
from restaurante_app.ui.login_vienw import LoginView
from restaurante_app.ui.main_vienw import MainView

class AplicacionRestaurante:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Restaurante App - Interfaz Gráfica & Eventos (Semana 15)")
        self.root.geometry("760x600")
        self.root.minsize(680, 520)

        ruta_base = Path(__file__).resolve().parent / "restaurante_app"
        self._configurar_icono_ventana(ruta_base)
        carpeta_datos = ruta_base / "datos"
        self.assets_path = str(ruta_base / "assets")

        self.archivo_servicio = ArchivoServicio(str(carpeta_datos))
        self.restaurante_servicio = RestauranteServicio(self.archivo_servicio)

        self.vista_actual = None
        self.usuario_autenticado = None

        self._configurar_estilos()
        self.mostrar_login()

    def _configurar_icono_ventana(self, ruta_base):
        ruta_icono = ruta_base / "assets" / "logo.png"
        if not ruta_icono.exists():
            print(f"no existe: {ruta_icono}")
            return

        try:
            self.icono = tk.PhotoImage(file=str(ruta_icono))
            self.root.iconphoto(True, self.icono)
            print("icono de ventana cargado")
        except tk.TclError as e:
            print(f"no se pudo cargar el icono: {e}")

    def cambiar_vista(self, nueva_vista: tk.Frame) -> None:
        if self.vista_actual is not None:
            self.vista_actual.destroy()
        self.vista_actual = nueva_vista
        self.vista_actual.pack(fill="both", expand=True)

    def mostrar_login(self) -> None:
        self.usuario_autenticado = None
        login_view = LoginView(
            parent=self.root,
            restaurante_servicio=self.restaurante_servicio,
            on_login_success=self.on_login_exitoso,
            assets_path=self.assets_path
        )
        self.cambiar_vista(login_view)

    def on_login_exitoso(self, usuario: Usuario) -> None:
        self.usuario_autenticado = usuario
        self.mostrar_main_view()

    def mostrar_main_view(self) -> None:
        main_view = MainView(
            parent=self.root,
            restaurante_servicio=self.restaurante_servicio,
            usuario_actual=self.usuario_autenticado,
            on_logout=self.mostrar_login,
            assets_path=self.assets_path
        )
        self.cambiar_vista(main_view)

    def iniciar(self) -> None:
        self.root.mainloop()

def main() -> None:
    app = AplicacionRestaurante()
    app.iniciar()

if __name__ == "__main__":
    main()
