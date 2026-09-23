from typing import Dict, List, Optional, Set, Tuple

from restaurante_app.modelos.producto import Producto
from restaurante_app.modelos.usuario import Usuario
from restaurante_app.modelos.venta import Venta
from restaurante_app.servicios.archivo_servicio import ArchivoServicio


class RestauranteServicio:
    def __init__(self, archivo_servicio: ArchivoServicio) -> None:
        self._archivo_servicio: ArchivoServicio = archivo_servicio
        self._productos: List[Producto] = []
        self._usuarios: List[Usuario] = []
        self._ventas: List[Venta] = []
        self._productos_por_codigo: Dict[str, Producto] = {}
        self._usuarios_por_identificacion: Dict[str, Usuario] = {}
        self._ventas_por_id: Dict[str, Venta] = {}

        self.cargar_datos()

    def cargar_datos(self) -> None:
        self._productos = self._archivo_servicio.cargar_productos()
        self._usuarios = self._archivo_servicio.cargar_usuarios()
        self._ventas = self._archivo_servicio.cargar_ventas()
        self._reconstruir_indices()

    def _reconstruir_indices(self) -> None:
        self._productos_por_codigo.clear()
        self._usuarios_por_identificacion.clear()
        self._ventas_por_id.clear()

        for p in self._productos:
            self._productos_por_codigo[p.codigo] = p

        for u in self._usuarios:
            self._usuarios_por_identificacion[u.identificacion] = u

        for v in self._ventas:
            self._ventas_por_id[v.id_venta] = v

    def validar_acceso(self, identificacion_o_usuario: str, contrasena: str) -> Optional[Usuario]:
        if not identificacion_o_usuario or not contrasena:
            return None
        identificacion_o_usuario = identificacion_o_usuario.strip()
        contrasena = contrasena.strip()

        usuario = self.buscar_usuario(identificacion_o_usuario)
        if usuario is None:
            for u in self._usuarios:
                if u.nombre.lower() == identificacion_o_usuario.lower():
                    usuario = u
                    break

        if usuario and usuario.validar_clave(contrasena):
            return usuario
        return None

    def buscar_producto(self, codigo: str) -> Optional[Producto]:
        return self._productos_por_codigo.get(codigo.strip())

    def buscar_usuario(self, identificacion: str) -> Optional[Usuario]:
        return self._usuarios_por_identificacion.get(identificacion.strip())

    def registrar_producto(self, producto: Producto) -> bool:
        if producto.codigo in self._productos_por_codigo:
            return False
        self._productos.append(producto)
        self._productos_por_codigo[producto.codigo] = producto
        self._archivo_servicio.guardar_productos(self._productos)
        return True

    def actualizar_producto(self, codigo: str, nombre: str, categoria: str, precio: float, stock: int) -> bool:
        producto = self.buscar_producto(codigo)
        if producto is None:
            return False
        producto.nombre = nombre
        producto.categoria = categoria
        producto.precio = precio
        producto.stock = stock
        self._archivo_servicio.guardar_productos(self._productos)
        return True

    def eliminar_producto(self, codigo: str) -> bool:
        producto = self.buscar_producto(codigo)
        if producto is None:
            return False
        self._productos.remove(producto)
        if codigo in self._productos_por_codigo:
            del self._productos_por_codigo[codigo]
        self._archivo_servicio.guardar_productos(self._productos)
        return True

    def obtener_categorias(self) -> List[str]:
        categorias: Set[str] = {p.categoria for p in self._productos}
        categorias_base = {"Comida Rápida", "Pizzas", "Bebidas", "Ensaladas", "Postres"}
        return sorted(list(categorias.union(categorias_base)))

    def listar_productos(self) -> List[Producto]:
        return self._productos.copy()

    def listar_usuarios(self) -> List[Usuario]:
        return self._usuarios.copy()

    def listar_ventas(self) -> List[Venta]:
        return self._ventas.copy()

    def registrar_venta(self, identificacion_usuario: str, codigo_producto: str, cantidad: int) -> Tuple[bool, str]:
        usuario = self.buscar_usuario(identificacion_usuario)
        if usuario is None:
            return False, f"El usuario/cliente con ID '{identificacion_usuario}' no existe."

        producto = self.buscar_producto(codigo_producto)
        if producto is None:
            return False, f"El producto con código '{codigo_producto}' no existe."

        if cantidad <= 0:
            return False, "La cantidad a vender debe ser mayor a 0."

        if producto.stock < cantidad:
            return False, f"Stock insuficiente para '{producto.nombre}'. Stock disponible: {producto.stock}, solicitado: {cantidad}."

        producto.disminuir_stock(cantidad)

        siguiente_num = len(self._ventas) + 1
        id_venta = f"V{siguiente_num:03d}"
        while id_venta in self._ventas_por_id:
            siguiente_num += 1
            id_venta = f"V{siguiente_num:03d}"

        nueva_venta = Venta(
            id_venta=id_venta,
            identificacion_usuario=usuario.identificacion,
            codigo_producto=producto.codigo,
            cantidad=cantidad,
            precio_unitario=producto.precio
        )

        self._ventas.append(nueva_venta)
        self._ventas_por_id[id_venta] = nueva_venta

        self._archivo_servicio.guardar_ventas(self._ventas)
        self._archivo_servicio.guardar_productos(self._productos)

        return True, f"¡Venta {id_venta} registrada con éxito!\nCliente: {usuario.nombre}\nProducto: {producto.nombre} (x{cantidad})\nTotal: ${nueva_venta.total:.2f}"
