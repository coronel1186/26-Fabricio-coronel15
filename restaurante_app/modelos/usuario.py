class Usuario:
    def __init__(self, identificacion: str, nombre: str, correo: str, clave: str = "1234") -> None:
        if not identificacion or not identificacion.strip():
            raise ValueError("La identificación del usuario no puede estar vacía.")
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del usuario no puede estar vacío.")
        if not correo or not correo.strip():
            raise ValueError("El correo del usuario no puede estar vacío.")

        self._identificacion: str = identificacion.strip()
        self._nombre: str = nombre.strip()
        self._correo: str = correo.strip()
        self._clave: str = clave.strip() if clave else "1234"

    @property
    def identificacion(self) -> str:
        return self._identificacion

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def correo(self) -> str:
        return self._correo

    @property
    def clave(self) -> str:
        return self._clave

    def validar_clave(self, contrasena: str) -> bool:
        return self._clave == contrasena.strip() or self._identificacion == contrasena.strip()

    def to_dict(self) -> dict:
        return {
            "identificacion": self._identificacion,
            "nombre": self._nombre,
            "correo": self._correo,
            "clave": self._clave
        }

    @classmethod
    def from_dict(cls, datos: dict) -> "Usuario":
        try:
            return cls(
                identificacion=datos["identificacion"],
                nombre=datos["nombre"],
                correo=datos["correo"],
                clave=datos.get("clave", "1234")
            )
        except KeyError as e:
            raise KeyError(f"Falta el campo obligatorio {e} en los datos del usuario.")
        except ValueError as e:
            raise ValueError(f"Formato de datos incorrecto en el diccionario del usuario: {e}")
        