# Restaurante App - Manejo de Eventos y Registro de Ventas (Semana 15)

Este proyecto representa la evolución modular del sistema **`restaurante_app`** para la **Semana 15** de la asignatura **Programación Orientada a Objetos**. En esta entrega se abordan los **conceptos fundamentales del manejo de eventos** en Tkinter/ttk, utilizando la operación de **Venta de Productos** como contexto práctico para demostrar cómo una acción del usuario en la interfaz gráfica desencadena una respuesta coordinada a través de todas las capas del sistema.

---

## 📌 1. Propósito y Fundamento de Eventos (Semana 15)

El objetivo central es comprender la arquitectura dirigida por eventos (*event-driven programming*) y garantizar la separación estricta de responsabilidades entre la interfaz gráfica (UI), los servicios de dominio y la capa de persistencia en disco.

### Flujo Reactivo de Ejecución:

```text
       USUARIO
          │
          ▼  (Selecciona cliente, producto y cantidad)
  BOTÓN / COMPONENTE
          │
          ▼  (Atributo command=self._callback_registrar_venta)
       CALLBACK
          │
          ▼  (Captura selecciones y solicita la operación)
  RestauranteServicio
          │
          ▼  (Valida existencia, reglas de negocio y descuenta stock)
     PERSISTENCIA
          │
          ▼  (ArchivoServicio escribe en ventas.json y productos.json)
 RESPUESTA EN LA INTERFAZ
             (Muestra messagebox de confirmación y refresca Treeview)
Principios Clave Demostrados:
Vinculación Limpia: El botón de la interfaz utiliza la referencia directa al callback command=self._callback_registrar_venta (sin paréntesis ()), evitando ejecuciones prematuras al instanciar el componente.
Delegación Estricta al Servicio: El callback en ui/main_view.py no contiene reglas de negocio ni manipula directamente archivos JSON; únicamente extrae los valores seleccionados y solicita la operación a RestauranteServicio.
Persistencia Sincronizada: Al registrar cada venta, el servicio actualiza el stock del producto en memoria y escribe simultáneamente los cambios en datos/ventas.json y datos/productos.json.

Estructura Modular del Repositorio
restaurante_app/
├── assets/
│   └── logo.png                  # Recurso visual obligatorio (Logotipo del restaurante)
├── datos/
│   ├── productos.json            # Base de datos física de inventario
│   ├── usuarios.json             # Base de datos física de clientes y accesos
│   └── ventas.json               # Base de datos física de historial transaccional
├── modelos/
│   ├── __init__.py
│   ├── producto.py               # Entidad Producto con getters/setters y control de stock
│   ├── usuario.py                # Entidad Usuario con validación de credenciales
│   └── venta.py                  # Entidad Venta (ID, usuario_id, producto_codigo, cantidad, total, fecha)
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py       # Lectura/Escritura de archivos JSON con control de excepciones
│   └── restaurante_servicio.py   # Lógica de negocio, CRUD e índice O(1) de ventas
├── ui/
│   ├── __init__.py
│   ├── login_view.py             # Pantalla de inicio de sesión con logotipo de marca
│   └── main_view.py              # Vista principal (Productos, Usuarios y Registro de Ventas)
├── main.py                       # Orquestador principal Tkinter (Ventana única y mainloop)
└── README.md                     # Documentación técnica del proyecto

Descripción de Componentes por CapaCapa de Modelo (modelos/):Producto: Encapsula atributos como codigo, nombre, categoria, precio y stock. Posee setters validados y el método disminuir_stock(cantidad).Usuario: Modela al cliente/usuario del sistema con su método validar_clave().Venta: Modela la transacción asociando un usuario y un producto con su cantidad, precio_unitario, total y fecha.Capa de Servicio (servicios/):ArchivoServicio: Gestiona el I/O seguro con archivos JSON (productos.json, usuarios.json, ventas.json) con captura de excepciones.RestauranteServicio: Contiene toda la lógica de negocio. Mantiene índices en RAM ($O(1)$) y coordina el método registrar_venta().Capa de Interfaz Gráfica (ui/):LoginView: Pantalla de autenticación que despliega el logotipo assets/logo.png.MainView: Contenedor por pestañas (ttk.Notebook) que incluye la gestión de productos, consulta de usuarios y el formulario de ventas reactivo.

Credenciales de Prueba
Usuario / ID
Contraseña
Nombre Completo
Rol
U001
1234
Carlos Gómez
Cliente Registrado
U002
admin
Ana López
Administrador / Cliente

Instrucciones de Instalación y Ejecución
Requisitos Previos:
Python 3.10+
Librerías estándar: tkinter, json, os, pathlib
Librería externa: Pillow (para el procesamiento de imágenes .png)
pip install Pillow
Pasos para Ejecutar:
Sitúese en la carpeta del proyecto:
cd restaurante_app
Ejecute el archivo principal:
python main.py
