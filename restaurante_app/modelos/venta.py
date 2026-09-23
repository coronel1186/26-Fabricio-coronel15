from datetime import datetime

class Venta:
    def __init__(self, id_venta: str, identificacion_usuario: str, codigo_producto: str, 
                 cantidad: int, precio_unitario: float, total: float = 0.0, fecha: str = "") -> None:
        if not id_venta or not id_venta.strip():
            raise ValueError("El ID de venta no puede estar vacío.")
        if not identificacion_usuario or not identificacion_usuario.strip():
            raise ValueError("La identificación del usuario no puede estar vacía.")
        if not codigo_producto or not codigo_producto.strip():
            raise ValueError("El código de producto no puede estar vacío.")
        if cantidad <= 0:
            raise ValueError("La cantidad vendida debe ser mayor a cero.")
        if precio_unitario < 0:
            raise ValueError("El precio unitario no puede ser negativo.")

        self._id_venta: str = id_venta.strip()
        self._identificacion_usuario: str = identificacion_usuario.strip()
        self._codigo_producto: str = codigo_producto.strip()
        self._cantidad: int = cantidad
        self._precio_unitario: float = precio_unitario
        self._total: float = round(total if total > 0 else (cantidad * precio_unitario), 2)
        self._fecha: str = fecha.strip() if fecha else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @property
    def id_venta(self) -> str:
        return self._id_venta

    @property
    def identificacion_usuario(self) -> str:
        return self._identificacion_usuario

    @property
    def codigo_producto(self) -> str:
        return self._codigo_producto

    @property
    def cantidad(self) -> int:
        return self._cantidad

    @property
    def precio_unitario(self) -> float:
        return self._precio_unitario

    @property
    def total(self) -> float:
        return self._total

    @property
    def fecha(self) -> str:
        return self._fecha

    def to_dict(self) -> dict:
        return {
            "id_venta": self._id_venta,
            "identificacion_usuario": self._identificacion_usuario,
            "codigo_producto": self._codigo_producto,
            "cantidad": self._cantidad,
            "precio_unitario": self._precio_unitario,
            "total": self._total,
            "fecha": self._fecha
        }

    @classmethod
    def from_dict(cls, datos: dict) -> "Venta":
        try:
            return cls(
                id_venta=datos["id_venta"],
                identificacion_usuario=datos["identificacion_usuario"],
                codigo_producto=datos["codigo_producto"],
                cantidad=int(datos["cantidad"]),
                precio_unitario=float(datos["precio_unitario"]),
                total=float(datos.get("total", 0.0)),
                fecha=datos.get("fecha", "")
            )
        except KeyError as e:
            raise KeyError(f"Falta el campo obligatorio {e} en los datos de la venta.")
        except ValueError as e:
            raise ValueError(f"Formato numérico o de datos incorrecto en la venta: {e}")

    def mostrar_informacion(self) -> str:
        return f"Venta {self._id_venta} | Usuario: {self._identificacion_usuario} | Producto: {self._codigo_producto} x{self._cantidad} = ${self._total:.2f} ({self._fecha})"