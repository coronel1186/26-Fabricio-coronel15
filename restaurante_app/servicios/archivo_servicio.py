import json
import os
from typing import List

from restaurante_app.modelos.producto import Producto
from restaurante_app.modelos.usuario import Usuario
from restaurante_app.modelos.venta import Venta

class ArchivoServicio:
    def __init__(self, carpeta_datos: str = "datos") -> None:
        self._carpeta: str = carpeta_datos
        self._ruta_productos: str = os.path.join(carpeta_datos, "productos.json")
        self._ruta_usuarios: str = os.path.join(carpeta_datos, "usuarios.json")
        self._ruta_ventas: str = os.path.join(carpeta_datos, "ventas.json")

    def _guardar(self, ruta: str, datos_serializados: list) -> None:
        try:
            directorio = os.path.dirname(ruta)
            if directorio and not os.path.exists(directorio):
                os.makedirs(directorio, exist_ok=True)
            with open(ruta, "w", encoding="utf-8") as f:
                json.dump(datos_serializados, f, indent=4, ensure_ascii=False)
        except PermissionError:
            print(f"\n[Error de Permisos] No se poseen permisos de escritura para: {ruta}")
        except Exception as e:
            print(f"\n[Error Inesperado] No se pudo guardar en '{ruta}': {e}")

    def _cargar(self, ruta: str) -> list:
        if not os.path.exists(ruta):
            return []
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                datos = json.load(f)
                if isinstance(datos, list):
                    return datos
                return []
        except json.JSONDecodeError:
            print(f"\n[Error Crítico] El archivo '{ruta}' no posee un formato JSON válido.")
            return []
        except PermissionError:
            print(f"\n[Error de Permisos] No se poseen permisos de lectura para: {ruta}")
            return []
        except Exception as e:
            print(f"\n[Error Inesperado] No se pudo cargar '{ruta}': {e}")
            return []

    def guardar_productos(self, productos: List[Producto]) -> None:
        self._guardar(self._ruta_productos, [p.to_dict() for p in productos])

    def guardar_usuarios(self, usuarios: List[Usuario]) -> None:
        self._guardar(self._ruta_usuarios, [u.to_dict() for u in usuarios])

    def guardar_ventas(self, ventas: List[Venta]) -> None:
        self._guardar(self._ruta_ventas, [v.to_dict() for v in ventas])

    def cargar_productos(self) -> List[Producto]:
        datos = self._cargar(self._ruta_productos)
        productos: List[Producto] = []
        for indice, item in enumerate(datos):
            try:
                productos.append(Producto.from_dict(item))
            except (KeyError, ValueError) as ke:
                print(f"\n[Inconsistencia] Producto #{indice+1} omitido: {ke}")
        return productos

    def cargar_usuarios(self) -> List[Usuario]:
        datos = self._cargar(self._ruta_usuarios)
        usuarios: List[Usuario] = []
        for indice, item in enumerate(datos):
            try:
                usuarios.append(Usuario.from_dict(item))
            except (KeyError, ValueError) as ke:
                print(f"\n[Inconsistencia] Usuario #{indice+1} omitido: {ke}")
        return usuarios

    def cargar_ventas(self) -> List[Venta]:
        datos = self._cargar(self._ruta_ventas)
        ventas: List[Venta] = []
        for indice, item in enumerate(datos):
            try:
                ventas.append(Venta.from_dict(item))
            except (KeyError, ValueError) as ke:
                print(f"\n[Inconsistencia] Venta #{indice+1} omitida: {ke}")
        return ventas
    