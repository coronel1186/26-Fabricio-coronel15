import os
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable

try:
    from PIL import Image, ImageTk
except ModuleNotFoundError:
    Image = None
    ImageTk = None

from restaurante_app.modelos.producto import Producto

class MainView(tk.Frame):
    def __init__(self, parent: tk.Widget, restaurante_servicio, usuario_actual, on_logout: Callable, assets_path: str = "") -> None:
        super().__init__(parent)
        self.restaurante_servicio = restaurante_servicio
        self.usuario_actual = usuario_actual
        self.on_logout = on_logout
        self.assets_path = assets_path
        self.logo_small = None

        self._crear_componentes()

    def _crear_componentes(self) -> None:
        top_bar = ttk.Frame(self, padding="8")
        top_bar.pack(fill="x", side="top")

        logo_file = os.path.join(self.assets_path, "logo.png") if self.assets_path else ""
        if os.path.exists(logo_file) and Image is not None and ImageTk is not None:
            try:
                pil_img = Image.open(logo_file).resize((36, 36))
                self.logo_small = ImageTk.PhotoImage(pil_img)
                lbl_logo = ttk.Label(top_bar, image=self.logo_small)
                lbl_logo.pack(side="left", padx=(0, 10))
            except Exception as e:
                print(f"No se pudo cargar el logo reducido: {e}")

        lbl_bienvenida = ttk.Label(
            top_bar, 
            text=f"Bienvenido/a, {self.usuario_actual.nombre} | Sistema del Restaurante", 
            font=("Helvetica", 11, "bold")
        )
        lbl_bienvenida.pack(side="left")

        btn_logout = ttk.Button(
            top_bar, 
            text="Cerrar Sesión", 
            command=self.on_logout
        )
        btn_logout.pack(side="right")

        ttk.Separator(self, orient="horizontal").pack(fill="x")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        tab_productos = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab_productos, text="📦 Gestión de Productos")

        tab_usuarios = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab_usuarios, text="👥 Usuarios Registrados")

        tab_ventas = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab_ventas, text="🛒 Registro de Ventas (Semana 15)")

        self._configurar_tab_productos(tab_productos)
        self._configurar_tab_usuarios(tab_usuarios)
        self._configurar_tab_ventas(tab_ventas)

    # --- PESTAÑA 1: PRODUCTOS ---
    def _configurar_tab_productos(self, parent: ttk.Frame) -> None:
        frm_datos = ttk.LabelFrame(parent, text=" Formulario de Producto ", padding="10")
        frm_datos.pack(fill="x", side="top", pady=(0, 10))

        ttk.Label(frm_datos, text="Código:", font=("Helvetica", 9, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=4)
        self.entry_codigo = ttk.Entry(frm_datos, width=15)
        self.entry_codigo.grid(row=0, column=1, sticky="w", padx=5, pady=4)

        ttk.Label(frm_datos, text="Nombre del Plato:", font=("Helvetica", 9, "bold")).grid(row=0, column=2, sticky="w", padx=5, pady=4)
        self.entry_nombre = ttk.Entry(frm_datos, width=30)
        self.entry_nombre.grid(row=0, column=3, sticky="w", padx=5, pady=4)

        ttk.Label(frm_datos, text="Categoría:", font=("Helvetica", 9, "bold")).grid(row=1, column=0, sticky="w", padx=5, pady=4)
        self.combo_categoria = ttk.Combobox(
            frm_datos, 
            values=self.restaurante_servicio.obtener_categorias(), 
            width=18, 
            state="normal"
        )
        self.combo_categoria.grid(row=1, column=1, sticky="w", padx=5, pady=4)

        ttk.Label(frm_datos, text="Precio ($):", font=("Helvetica", 9, "bold")).grid(row=1, column=2, sticky="w", padx=5, pady=4)
        self.entry_precio = ttk.Entry(frm_datos, width=12)
        self.entry_precio.grid(row=1, column=3, sticky="w", padx=5, pady=4)

        ttk.Label(frm_datos, text="Stock Inicial:", font=("Helvetica", 9, "bold")).grid(row=2, column=0, sticky="w", padx=5, pady=4)
        self.entry_stock = ttk.Entry(frm_datos, width=15)
        self.entry_stock.grid(row=2, column=1, sticky="w", padx=5, pady=4)

        frm_acciones = ttk.Frame(parent, padding="5")
        frm_acciones.pack(fill="x", side="top", pady=(0, 10))

        btn_registrar = ttk.Button(frm_acciones, text="➕ Registrar Producto", command=self._registrar_producto)
        btn_registrar.pack(side="left", padx=5)

        btn_actualizar = ttk.Button(frm_acciones, text="✏️ Actualizar Producto", command=self._actualizar_producto)
        btn_actualizar.pack(side="left", padx=5)

        btn_eliminar = ttk.Button(frm_acciones, text="🗑️ Eliminar Producto", command=self._eliminar_producto)
        btn_eliminar.pack(side="left", padx=5)

        btn_limpiar = ttk.Button(frm_acciones, text="🧹 Limpiar Campos", command=self._limpiar_formulario_producto)
        btn_limpiar.pack(side="right", padx=5)

        frm_tabla = ttk.LabelFrame(parent, text=" Menú de Productos y Stock ", padding="10")
        frm_tabla.pack(fill="both", expand=True, side="bottom")

        columnas = ("codigo", "nombre", "categoria", "precio", "stock")
        self.tree_productos = ttk.Treeview(frm_tabla, columns=columnas, show="headings", selectmode="browse")

        self.tree_productos.heading("codigo", text="Código")
        self.tree_productos.heading("nombre", text="Nombre Comercial")
        self.tree_productos.heading("categoria", text="Categoría")
        self.tree_productos.heading("precio", text="Precio Unitario ($)")
        self.tree_productos.heading("stock", text="Stock Disponible")

        self.tree_productos.column("codigo", width=80, anchor="center")
        self.tree_productos.column("nombre", width=220, anchor="w")
        self.tree_productos.column("categoria", width=140, anchor="center")
        self.tree_productos.column("precio", width=100, anchor="e")
        self.tree_productos.column("stock", width=110, anchor="center")

        scrollbar = ttk.Scrollbar(frm_tabla, orient="vertical", command=self.tree_productos.yview)
        self.tree_productos.configure(yscrollcommand=scrollbar.set)

        self.tree_productos.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree_productos.bind("<<TreeviewSelect>>", self._cargar_producto_seleccionado)

        self._refrescar_tabla_productos()

    def _refrescar_tabla_productos(self) -> None:
        for row in self.tree_productos.get_children():
            self.tree_productos.delete(row)
        productos = self.restaurante_servicio.listar_productos()
        for p in productos:
            self.tree_productos.insert("", "end", values=(p.codigo, p.nombre, p.categoria, f"${p.precio:.2f}", p.stock))

        self.combo_categoria["values"] = self.restaurante_servicio.obtener_categorias()

    def _cargar_producto_seleccionado(self, event: tk.Event) -> None:
        seleccion = self.tree_productos.selection()
        if not seleccion:
            return
        item_data = self.tree_productos.item(seleccion[0], "values")
        if not item_data:
            return

        codigo, nombre, categoria, precio_str, stock_str = item_data

        self.entry_codigo.delete(0, tk.END)
        self.entry_codigo.insert(0, codigo)

        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.insert(0, nombre)

        self.combo_categoria.set(categoria)

        precio_clean = str(precio_str).replace("$", "").replace(",", "").strip()
        self.entry_precio.delete(0, tk.END)
        self.entry_precio.insert(0, precio_clean)

        self.entry_stock.delete(0, tk.END)
        self.entry_stock.insert(0, str(stock_str))

    def _limpiar_formulario_producto(self) -> None:
        self.entry_codigo.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)
        self.combo_categoria.set("")
        self.entry_precio.delete(0, tk.END)
        self.entry_stock.delete(0, tk.END)

    def _registrar_producto(self) -> None:
        codigo = self.entry_codigo.get().strip()
        nombre = self.entry_nombre.get().strip()
        categoria = self.combo_categoria.get().strip()
        precio_str = self.entry_precio.get().strip()
        stock_str = self.entry_stock.get().strip()

        if not codigo or not nombre or not categoria or not precio_str or not stock_str:
            messagebox.showwarning("Campos Incompletos", "Por favor, complete todos los campos del producto.")
            return

        try:
            precio = float(precio_str)
            stock = int(stock_str)
            nuevo_producto = Producto(codigo, nombre, categoria, precio, stock)
        except ValueError as e:
            messagebox.showerror("Error de Formato", f"Datos numéricos inválidos: {e}")
            return

        if self.restaurante_servicio.registrar_producto(nuevo_producto):
            messagebox.showinfo("Registro Exitoso", f"Producto [{codigo}] '{nombre}' registrado correctamente.")
            self._refrescar_tabla_productos()
            self._refrescar_combos_ventas()
            self._limpiar_formulario_producto()
        else:
            messagebox.showerror("Código Duplicado", f"Ya existe un producto con el código '{codigo}'.")

    def _actualizar_producto(self) -> None:
        codigo = self.entry_codigo.get().strip()
        nombre = self.entry_nombre.get().strip()
        categoria = self.combo_categoria.get().strip()
        precio_str = self.entry_precio.get().strip()
        stock_str = self.entry_stock.get().strip()

        if not codigo or not nombre or not categoria or not precio_str or not stock_str:
            messagebox.showwarning("Campos Incompletos", "Seleccione un producto de la tabla o ingrese todos los datos.")
            return

        try:
            precio = float(precio_str)
            stock = int(stock_str)
        except ValueError:
            messagebox.showerror("Error de Formato", "El precio debe ser decimal y el stock un entero.")
            return

        if self.restaurante_servicio.actualizar_producto(codigo, nombre, categoria, precio, stock):
            messagebox.showinfo("Actualización Exitosa", f"Producto [{codigo}] actualizado correctamente.")
            self._refrescar_tabla_productos()
            self._refrescar_combos_ventas()
            self._limpiar_formulario_producto()
        else:
            messagebox.showerror("No Encontrado", f"No se encontró ningún producto con el código '{codigo}'.")

    def _eliminar_producto(self) -> None:
        codigo = self.entry_codigo.get().strip()
        if not codigo:
            messagebox.showwarning("Selección Requerida", "Seleccione un producto de la tabla para eliminar.")
            return

        confirmar = messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de eliminar el producto [{codigo}]?")
        if confirmar:
            if self.restaurante_servicio.eliminar_producto(codigo):
                messagebox.showinfo("Eliminación Exitosa", f"Producto [{codigo}] eliminado correctamente.")
                self._refrescar_tabla_productos()
                self._refrescar_combos_ventas()
                self._limpiar_formulario_producto()
            else:
                messagebox.showerror("Error", f"No se pudo eliminar: el código [{codigo}] no existe.")

    # --- PESTAÑA 2: USUARIOS ---
    def _configurar_tab_usuarios(self, parent: ttk.Frame) -> None:
        lbl = ttk.Label(parent, text="Clientes / Usuarios Registrados en el Sistema", font=("Helvetica", 11, "bold"))
        lbl.pack(anchor="w", pady=(0, 10))

        columnas = ("identificacion", "nombre", "correo")
        tree = ttk.Treeview(parent, columns=columnas, show="headings", height=10)

        tree.heading("identificacion", text="ID / Usuario")
        tree.heading("nombre", text="Nombre Completo")
        tree.heading("correo", text="Correo Electrónico")

        tree.column("identificacion", width=120, anchor="center")
        tree.column("nombre", width=240, anchor="w")
        tree.column("correo", width=240, anchor="w")

        tree.pack(fill="both", expand=True, pady=(0, 10))

        usuarios = self.restaurante_servicio.listar_usuarios()
        for u in usuarios:
            tree.insert("", "end", values=(u.identificacion, u.nombre, u.correo))

    # --- PESTAÑA 3: VENTAS (SEMANA 15 - EVENTOS & CALLBACKS) ---
    def _configurar_tab_ventas(self, parent: ttk.Frame) -> None:
        lbl_info = ttk.Label(
            parent,
            text="Flujo de Evento: Acción del Usuario ➔ command= ➔ Callback (_callback_registrar_venta) ➔ Servicio ➔ JSON ➔ Respuesta Visual",
            font=("Helvetica", 9, "italic"),
            foreground="#006666"
        )
        lbl_info.pack(anchor="w", pady=(0, 8))

        frm_venta = ttk.LabelFrame(parent, text=" Nueva Venta (Manejo de Eventos mediante command=) ", padding="12")
        frm_venta.pack(fill="x", side="top", pady=(0, 10))

        ttk.Label(frm_venta, text="Cliente / Usuario:", font=("Helvetica", 9, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=6)
        self.combo_venta_cliente = ttk.Combobox(frm_venta, width=32, state="readonly")
        self.combo_venta_cliente.grid(row=0, column=1, sticky="w", padx=5, pady=6)

        ttk.Label(frm_venta, text="Producto:", font=("Helvetica", 9, "bold")).grid(row=0, column=2, sticky="w", padx=5, pady=6)
        self.combo_venta_producto = ttk.Combobox(frm_venta, width=38, state="readonly")
        self.combo_venta_producto.grid(row=0, column=3, sticky="w", padx=5, pady=6)

        ttk.Label(frm_venta, text="Cantidad:", font=("Helvetica", 9, "bold")).grid(row=1, column=0, sticky="w", padx=5, pady=6)
        self.spin_cantidad = ttk.Spinbox(frm_venta, from_=1, to=100, width=10)
        self.spin_cantidad.grid(row=1, column=1, sticky="w", padx=5, pady=6)
        self.spin_cantidad.set(1)

        self.lbl_precio_unitario = ttk.Label(frm_venta, text="Precio Unitario: $0.00", font=("Helvetica", 9))
        self.lbl_precio_unitario.grid(row=1, column=2, sticky="w", padx=5, pady=6)

        self.lbl_total_estimado = ttk.Label(frm_venta, text="Total Estimado: $0.00", font=("Helvetica", 10, "bold"), foreground="#008000")
        self.lbl_total_estimado.grid(row=1, column=3, sticky="w", padx=5, pady=6)

        # BOTÓN CON command= VINCULADO AL CALLBACK
        btn_registrar_venta = ttk.Button(
            frm_venta, 
            text="🛒 Registrar Venta (Ejecutar Callback)", 
            command=self._callback_registrar_venta
        )
        btn_registrar_venta.grid(row=2, column=0, columnspan=4, sticky="ew", padx=5, pady=(10, 2))

        # Eventos para cálculo dinámico
        self.combo_venta_producto.bind("<<ComboboxSelected>>", lambda e: self._actualizar_calculo_venta())
        self.spin_cantidad.bind("<KeyRelease>", lambda e: self._actualizar_calculo_venta())
        self.spin_cantidad.bind("<<Increment>>", lambda e: self._actualizar_calculo_venta())
        self.spin_cantidad.bind("<<Decrement>>", lambda e: self._actualizar_calculo_venta())

        frm_tabla_ventas = ttk.LabelFrame(parent, text=" Historial de Ventas Registradas (Persistencia en ventas.json) ", padding="10")
        frm_tabla_ventas.pack(fill="both", expand=True, side="bottom")

        columnas = ("id_venta", "cliente", "producto", "cantidad", "precio_unitario", "total", "fecha")
        self.tree_ventas = ttk.Treeview(frm_tabla_ventas, columns=columnas, show="headings", selectmode="browse")

        self.tree_ventas.heading("id_venta", text="ID Venta")
        self.tree_ventas.heading("cliente", text="Cliente (ID)")
        self.tree_ventas.heading("producto", text="Producto (Código)")
        self.tree_ventas.heading("cantidad", text="Cant.")
        self.tree_ventas.heading("precio_unitario", text="P. Unit ($)")
        self.tree_ventas.heading("total", text="Total ($)")
        self.tree_ventas.heading("fecha", text="Fecha / Hora")

        self.tree_ventas.column("id_venta", width=75, anchor="center")
        self.tree_ventas.column("cliente", width=160, anchor="w")
        self.tree_ventas.column("producto", width=180, anchor="w")
        self.tree_ventas.column("cantidad", width=60, anchor="center")
        self.tree_ventas.column("precio_unitario", width=85, anchor="e")
        self.tree_ventas.column("total", width=95, anchor="e")
        self.tree_ventas.column("fecha", width=140, anchor="center")

        scrollbar = ttk.Scrollbar(frm_tabla_ventas, orient="vertical", command=self.tree_ventas.yview)
        self.tree_ventas.configure(yscrollcommand=scrollbar.set)

        self.tree_ventas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self._refrescar_combos_ventas()
        self._refrescar_tabla_ventas()

    def _refrescar_combos_ventas(self) -> None:
        usuarios = self.restaurante_servicio.listar_usuarios()
        opciones_usuarios = [f"{u.nombre} ({u.identificacion})" for u in usuarios]
        self.combo_venta_cliente["values"] = opciones_usuarios
        if opciones_usuarios:
            if not self.combo_venta_cliente.get() or self.combo_venta_cliente.get() not in opciones_usuarios:
                self.combo_venta_cliente.set(opciones_usuarios[0])

        productos = self.restaurante_servicio.listar_productos()
        opciones_productos = [f"{p.codigo} - {p.nombre} [Stock: {p.stock}] [${p.precio:.2f}]" for p in productos]
        self.combo_venta_producto["values"] = opciones_productos
        if opciones_productos:
            if not self.combo_venta_producto.get() or self.combo_venta_producto.get() not in opciones_productos:
                self.combo_venta_producto.set(opciones_productos[0])
            self._actualizar_calculo_venta()

    def _obtener_codigo_producto_seleccionado(self) -> str:
        prod_str = self.combo_venta_producto.get().strip()
        if not prod_str:
            return ""
        return prod_str.split(" - ", 1)[0].strip()

    def _obtener_id_usuario_seleccionado(self) -> str:
        usr_str = self.combo_venta_cliente.get().strip()
        if not usr_str or "(" not in usr_str:
            return ""
        return usr_str.rsplit("(", 1)[-1].replace(")", "").strip()

    def _actualizar_calculo_venta(self) -> None:
        cod_prod = self._obtener_codigo_producto_seleccionado()
        producto = self.restaurante_servicio.buscar_producto(cod_prod)
        if producto:
            self.lbl_precio_unitario.config(text=f"Precio Unitario: ${producto.precio:.2f}")
            try:
                cant = int(self.spin_cantidad.get())
                if cant <= 0:
                    cant = 1
            except ValueError:
                cant = 1
            total = cant * producto.precio
            self.lbl_total_estimado.config(text=f"Total Estimado: ${total:.2f}")
        else:
            self.lbl_precio_unitario.config(text="Precio Unitario: $0.00")
            self.lbl_total_estimado.config(text="Total Estimado: $0.00")

    def _refrescar_tabla_ventas(self) -> None:
        for row in self.tree_ventas.get_children():
            self.tree_ventas.delete(row)
        ventas = self.restaurante_servicio.listar_ventas()
        for v in ventas:
            u = self.restaurante_servicio.buscar_usuario(v.identificacion_usuario)
            p = self.restaurante_servicio.buscar_producto(v.codigo_producto)
            nombre_cliente = f"{u.nombre} ({v.identificacion_usuario})" if u else v.identificacion_usuario
            nombre_producto = f"{p.nombre} ({v.codigo_producto})" if p else v.codigo_producto

            self.tree_ventas.insert(
                "", "end", 
                values=(v.id_venta, nombre_cliente, nombre_producto, v.cantidad, f"${v.precio_unitario:.2f}", f"${v.total:.2f}", v.fecha)
            )

    # --- CALLBACK QUE RESPONDE AL EVENTO DEL BOTÓN ---
    def _callback_registrar_venta(self) -> None:
        id_usuario = self._obtener_id_usuario_seleccionado()
        cod_producto = self._obtener_codigo_producto_seleccionado()

        try:
            cantidad = int(self.spin_cantidad.get())
        except ValueError:
            messagebox.showerror("Cantidad Inválida", "La cantidad debe ser un entero mayor a 0.")
            return

        if not id_usuario or not cod_producto:
            messagebox.showwarning("Selección Requerida", "Por favor, seleccione un cliente y un producto válidos.")
            return

        # Delegar la operación al servicio
        exito, mensaje = self.restaurante_servicio.registrar_venta(id_usuario, cod_producto, cantidad)

        if exito:
            messagebox.showinfo("Venta Exitosa", mensaje)
            self._refrescar_tabla_ventas()
            self._refrescar_tabla_productos()
            self._refrescar_combos_ventas()
            self.spin_cantidad.set(1)
        else:
            messagebox.showerror("Error al Registrar Venta", mensaje)