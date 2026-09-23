class Producto:
    def __init__(self, codigo: str, nombre: str, categoria: str, precio: float, stock: int = 0) -> None:
        if not codigo or not codigo.strip():
            raise ValueError("El código del producto no puede estar vacío.")
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del producto no puede estar vacío.")
        if not categoria or not categoria.strip():
            raise ValueError("La categoría del producto no puede estar vacía.")
        if precio < 0:
            raise ValueError("El precio del producto no puede ser negativo.")
        if stock < 0:
            raise ValueError("El stock del producto no puede ser negativo.")

        self._codigo: str = codigo.strip()
        self._nombre: str = nombre.strip()
        self._categoria: str = categoria.strip()
        self._precio: float = precio
        self._stock: int = stock

    @property
    def codigo(self) -> str:
        return self._codigo

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self._nombre = valor.strip()

    @property
    def categoria(self) -> str:
        return self._categoria

    @categoria.setter
    def categoria(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("La categoría no puede estar vacía.")
        self._categoria = valor.strip()

    @property
    def precio(self) -> float:
        return self._precio

    @precio.setter
    def precio(self, valor: float) -> None:
        if valor < 0:
            raise ValueError("El precio no puede ser negativo.")
        self._precio = valor

    @property
    def stock(self) -> int:
        return self._stock

    @stock.setter
    def stock(self, valor: int) -> None:
        if valor < 0:
            raise ValueError("El stock no puede ser negativo.")
        self._stock = valor

    def disminuir_stock(self, cantidad: int) -> None:
        if cantidad <= 0:
            raise ValueError("La cantidad a disminuir debe ser mayor que cero.")
        if self._stock < cantidad:
            raise ValueError(f"Stock insuficiente ({self._stock} disponible) para descontar {cantidad}.")
        self._stock -= cantidad

    def to_dict(self) -> dict:
        return {
            "codigo": self._codigo,
            "nombre": self._nombre,
            "categoria": self._categoria,
            "precio": self._precio,
            "stock": self._stock
        }

    @classmethod
    def from_dict(cls, datos: dict) -> "Producto":
        try:
            return cls(
                codigo=datos["codigo"],
                nombre=datos["nombre"],
                categoria=datos["categoria"],
                precio=float(datos["precio"]),
                stock=int(datos.get("stock", 0))
            )
        except KeyError as e:
            raise KeyError(f"Falta el campo obligatorio {e} en los datos del producto.")
        except ValueError as e:
            raise ValueError(f"Formato de datos incorrecto en el diccionario del producto: {e}")

    def mostrar_informacion(self) -> str:
        return f"[{self._codigo}] {self._nombre} ({self._categoria}) - ${self._precio:.2f} | Stock: {self._stock}"