import tkinter as tk
from tkinter import ttk, messagebox, font
import json
import os
from datetime import datetime
import uuid

# Paleta de colores mejorada
COLOR_PRIMARIO = "#6F4E37"  # Café principal
COLOR_SECUNDARIO = "#C4A484"  # Café claro
COLOR_TERCIARIO = "#8B5A2B"  # Café oscuro
COLOR_FONDO = "#F5F5DC"  # Beige claro
COLOR_TEXTO = "#FFFFFF"  # Blanco
COLOR_TEXTO_OSCURO = "#3E2723"  # Café muy oscuro
COLOR_BOTONES = "#A67C52"  # Café medio
COLOR_BOTONES_ACCION = "#5D4037"  # Café oscuro para acciones importantes
COLOR_BOTONES_PELIGRO = "#BF360C"  # Rojo café para acciones peligrosas
COLOR_CARRITO = "#D2B48C"  # Café claro para el carrito
COLOR_ENCABEZADO = "#5D4037"  # Café oscuro para encabezados
COLOR_ADMIN = "#3E2723"  # Café muy oscuro para admin
COLOR_DESTACADO = "#8D6E63"  # Café para elementos destacados

# Fuentes personalizadas
FUENTE_TITULO = ("Helvetica", 24, "bold")
FUENTE_SUBTITULO = ("Helvetica", 18, "bold")
FUENTE_TEXTO = ("Helvetica", 12)
FUENTE_BOTONES = ("Helvetica", 12, "bold")
FUENTE_PEQUENA = ("Helvetica", 10)

# Estilo global
def configurar_estilos():
    estilo = ttk.Style()
    
    # Configurar tema
    estilo.theme_use('clam')
    
    # Configurar colores de los frames
    estilo.configure('TFrame', background=COLOR_FONDO)
    estilo.configure('TNotebook', background=COLOR_FONDO)
    estilo.configure('TNotebook.Tab', background=COLOR_SECUNDARIO, foreground=COLOR_TEXTO_OSCURO, 
                    font=FUENTE_BOTONES, padding=[10, 5])
    estilo.map('TNotebook.Tab', background=[('selected', COLOR_PRIMARIO)], 
              foreground=[('selected', COLOR_TEXTO)])
    
    # Configurar Treeview
    estilo.configure("Treeview", background=COLOR_FONDO, fieldbackground=COLOR_FONDO, 
                    foreground=COLOR_TEXTO_OSCURO, font=FUENTE_TEXTO, rowheight=25)
    estilo.configure("Treeview.Heading", background=COLOR_PRIMARIO, foreground=COLOR_TEXTO, 
                    font=FUENTE_BOTONES)
    estilo.map("Treeview", background=[('selected', COLOR_SECUNDARIO)], 
              foreground=[('selected', COLOR_TEXTO_OSCURO)])
    
    # Configurar botones
    estilo.configure('TButton', font=FUENTE_BOTONES, background=COLOR_BOTONES, 
                   foreground=COLOR_TEXTO, borderwidth=1)
    estilo.map('TButton', background=[('active', COLOR_TERCIARIO)], 
              foreground=[('active', COLOR_TEXTO)])

class ProductoBase:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio
    
    def __str__(self):
        return f"{self.nombre} - ${self.precio:.2f}"

class Bebida(ProductoBase):
    def __init__(self, nombre, precio, tamano="Mediano", tipo="Caliente", opciones=None):
        super().__init__(nombre, precio)
        self.tamano = tamano
        self.tipo = tipo
        self.opciones = opciones if opciones else []
    
    def __str__(self):
        extras = ", ".join(self.opciones) if self.opciones else "sin extras"
        return f"{self.nombre} ({self.tamano}, {self.tipo}) - ${self.precio:.2f} [{extras}]"

class Postre(ProductoBase):
    def __init__(self, nombre, precio, es_vegano=False, sin_gluten=False):
        super().__init__(nombre, precio)
        self.es_vegano = es_vegano
        self.sin_gluten = sin_gluten
    
    def __str__(self):
        detalles = []
        if self.es_vegano:
            detalles.append("vegano")
        if self.sin_gluten:
            detalles.append("sin gluten")
        info = f"{self.nombre} - ${self.precio:.2f}"
        if detalles:
            info += f" [{', '.join(detalles)}]"
        return info

class Pedido:
    def __init__(self, cliente):
        self.cliente = cliente
        self.productos = []
        self.estado = "Nuevo"
        self.total = 0.0
        self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.id = str(uuid.uuid4())
    
    def agregar_producto(self, producto):
        self.productos.append(producto)
        self.total += producto.precio
        return self.productos
    
    def eliminar_producto(self, producto):
        if producto in self.productos:
            self.productos.remove(producto)
            self.total -= producto.precio
            return True
        return False
    
    def calcular_total(self):
        self.total = sum(producto.precio for producto in self.productos)
        return self.total
    
    def cambiar_estado(self, nuevo_estado):
        self.estado = nuevo_estado
        return self.estado
    
    def __str__(self):
        productos_str = "\n".join([f" - {p}" for p in self.productos])
        return f"""Pedido #{self.id[:8]}
Cliente: {self.cliente}
Fecha: {self.fecha}
Estado: {self.estado}
Productos:
{productos_str}
Total: ${self.total:.2f}"""

class Inventario:
    def __init__(self):
        self.ingredientes = {
            "café": 1000,  
            "leche": 1000,
            "azúcar": 1000,
            "chocolate": 500,
            "canela": 200,
            "vainilla": 200,
            "té negro": 500,
            "hielo": 1000,
            "agua": 2000
        }
    
    def agregar_ingrediente(self, nombre, cantidad):
        if nombre in self.ingredientes:
            self.ingredientes[nombre] += cantidad
        else:
            self.ingredientes[nombre] = cantidad
        return self.ingredientes[nombre]
    
    def eliminar_ingrediente(self, nombre):
        if nombre in self.ingredientes:
            del self.ingredientes[nombre]
            return True
        return False
    
    def verificar_disponibilidad(self, ingredientes_necesarios):
        return all(
            ingrediente in self.ingredientes and 
            self.ingredientes[ingrediente] >= cantidad 
            for ingrediente, cantidad in ingredientes_necesarios.items()
        )
    
    def usar_ingredientes(self, ingredientes_necesarios):
        if not self.verificar_disponibilidad(ingredientes_necesarios):
            return False
        
        for ingrediente, cantidad in ingredientes_necesarios.items():
            self.ingredientes[ingrediente] -= cantidad
        return True

class Empleado:
    def __init__(self, nombre, rol):
        self.nombre = nombre
        self.rol = rol
    
    def __str__(self):
        return f"{self.nombre} ({self.rol})"

class GestorDatos:
    def __init__(self, controller=None):
        self.directorio = "datos"
        self.archivo_inventario = os.path.join(self.directorio, "inventario.json")
        self.archivo_productos = os.path.join(self.directorio, "productos.json")
        self.archivo_pedidos = os.path.join(self.directorio, "pedidos.json")
        self.archivo_empleados = os.path.join(self.directorio, "empleados.json")
        self.controller = controller
        
        os.makedirs(self.directorio, exist_ok=True)
        self.cargar_datos()
    
    def cargar_datos(self):
        # Cargar inventario
        self.inventario = Inventario()
        if os.path.exists(self.archivo_inventario):
            with open(self.archivo_inventario, 'r') as f:
                self.inventario.ingredientes = json.load(f)
        
        # Cargar productos
        self.bebidas = []
        self.postres = []
        if os.path.exists(self.archivo_productos):
            with open(self.archivo_productos, 'r') as f:
                datos_productos = json.load(f)
                self.bebidas = [
                    Bebida(b['nombre'], b['precio'], b.get('tamano', 'Mediano'), 
                          b.get('tipo', 'Caliente'), b.get('opciones', []))
                    for b in datos_productos.get('bebidas', [])
                ]
                self.postres = [
                    Postre(p['nombre'], p['precio'], p.get('es_vegano', False), 
                          p.get('sin_gluten', False))
                    for p in datos_productos.get('postres', [])
                ]
        else:
            # Datos por defecto
            self.bebidas = [
                Bebida("Café Americano", 2.50),
                Bebida("Latte", 3.50, "Grande", "Caliente", ["Extra leche"]),
                Bebida("Té Chai", 3.00, "Mediano", "Caliente", ["Canela"])
            ]
            self.postres = [
                Postre("Croissant", 2.00),
                Postre("Galleta de Avena", 1.50, True, False),
                Postre("Brownie", 2.50)
            ]
            self.guardar_productos()
        
        # Cargar pedidos
        self.pedidos = []
        if os.path.exists(self.archivo_pedidos):
            with open(self.archivo_pedidos, 'r') as f:
                for pedido_data in json.load(f):
                    pedido = Pedido(pedido_data['cliente'])
                    pedido.estado = pedido_data['estado']
                    pedido.total = pedido_data['total']
                    pedido.fecha = pedido_data.get('fecha', datetime.now().strftime("%Y-%m-%d %H:%M"))
                    pedido.id = pedido_data.get('id', str(uuid.uuid4()))
                    
                    for producto_data in pedido_data['productos']:
                        if producto_data['tipo'] == 'bebida':
                            pedido.productos.append(Bebida(
                                producto_data['nombre'],
                                producto_data['precio'],
                                producto_data.get('tamano', 'Mediano'),
                                producto_data.get('tipo_bebida', 'Caliente'),
                                producto_data.get('opciones', [])
                            ))
                        elif producto_data['tipo'] == 'postre':
                            pedido.productos.append(Postre(
                                producto_data['nombre'],
                                producto_data['precio'],
                                producto_data.get('es_vegano', False),
                                producto_data.get('sin_gluten', False)
                            ))
                    
                    self.pedidos.append(pedido)
        
        # Cargar empleados
        self.empleados = []
        if os.path.exists(self.archivo_empleados):
            with open(self.archivo_empleados, 'r') as f:
                self.empleados = [
                    Empleado(e['nombre'], e['rol']) 
                    for e in json.load(f)
                ]
        else:
            self.empleados = [
                Empleado("Admin", "Administrador"),
                Empleado("Barista1", "Barista")
            ]
            self.guardar_empleados()
    
    def guardar_inventario(self):
        with open(self.archivo_inventario, 'w') as f:
            json.dump(self.inventario.ingredientes, f, indent=4)
    
    def guardar_productos(self):
        datos_productos = {
            'bebidas': [{
                'nombre': b.nombre,
                'precio': b.precio,
                'tamano': b.tamano,
                'tipo': b.tipo,
                'opciones': b.opciones
            } for b in self.bebidas],
            'postres': [{
                'nombre': p.nombre,
                'precio': p.precio,
                'es_vegano': p.es_vegano,
                'sin_gluten': p.sin_gluten
            } for p in self.postres]
        }
        with open(self.archivo_productos, 'w') as f:
            json.dump(datos_productos, f, indent=4)
    
    def guardar_pedidos(self):
        pedidos_data = []
        for pedido in self.pedidos:
            productos_data = []
            for producto in pedido.productos:
                if isinstance(producto, Bebida):
                    productos_data.append({
                        'tipo': 'bebida',
                        'nombre': producto.nombre,
                        'precio': producto.precio,
                        'tamano': producto.tamano,
                        'tipo_bebida': producto.tipo,
                        'opciones': producto.opciones
                    })
                elif isinstance(producto, Postre):
                    productos_data.append({
                        'tipo': 'postre',
                        'nombre': producto.nombre,
                        'precio': producto.precio,
                        'es_vegano': producto.es_vegano,
                        'sin_gluten': producto.sin_gluten
                    })
            
            pedidos_data.append({
                'id': pedido.id,
                'cliente': str(pedido.cliente),
                'estado': pedido.estado,
                'total': pedido.total,
                'productos': productos_data,
                'fecha': pedido.fecha
            })
        
        with open(self.archivo_pedidos, 'w') as f:
            json.dump(pedidos_data, f, indent=4)
    
    def guardar_empleados(self):
        empleados_data = [{
            'nombre': e.nombre,
            'rol': e.rol
        } for e in self.empleados]
        
        with open(self.archivo_empleados, 'w') as f:
            json.dump(empleados_data, f, indent=4)
    
    def guardar_todo(self):
        self.guardar_inventario()
        self.guardar_productos()
        self.guardar_pedidos()
        self.guardar_empleados()

class CafeteriaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión de Pedidos - Cafetería das Haus")
        self.geometry("1200x800")
        self.configure(bg=COLOR_FONDO)
        
        # Configurar estilos
        configurar_estilos()
        
        # Icono de la aplicación
        try:
            self.iconbitmap("cafe_icon.ico")  # Puedes reemplazar con tu propio icono
        except:
            pass
        
        self.gestor_datos = GestorDatos(self)
        self.cliente_actual = "Cliente"
        self.pedido_actual = None
        self.modo_admin = False
        
        # Contenedor principal
        self.container = tk.Frame(self, bg=COLOR_FONDO)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        # Pantallas
        self.frames = {}
        for F in (PantallaInicio, PantallaMenu, PantallaCarrito, PantallaAdmin):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.mostrar_pantalla(PantallaInicio)
    
    def mostrar_pantalla(self, pantalla):
        frame = self.frames[pantalla]
        frame.actualizar()
        frame.tkraise()
    
    def solicitar_nombre_cliente(self):
        ventana_nombre = tk.Toplevel(self)
        ventana_nombre.title("Nombre del Cliente")
        ventana_nombre.geometry("500x300")
        ventana_nombre.configure(bg=COLOR_FONDO)
        ventana_nombre.resizable(False, False)
        
        # Frame principal
        frame_principal = tk.Frame(ventana_nombre, bg=COLOR_FONDO, padx=20, pady=20)
        frame_principal.pack(fill="both", expand=True)
        
        # Título
        tk.Label(frame_principal, text="Ingrese su nombre:", font=FUENTE_SUBTITULO, 
                bg=COLOR_FONDO, fg=COLOR_TEXTO_OSCURO).pack(pady=(20, 10))
        
        # Entrada de texto
        entry_nombre = tk.Entry(frame_principal, font=FUENTE_TEXTO, bd=2, relief=tk.GROOVE)
        entry_nombre.pack(pady=10, ipady=5, ipadx=10, fill="x")
        entry_nombre.focus_set()
        
        # Frame de botones
        frame_botones = tk.Frame(frame_principal, bg=COLOR_FONDO)
        frame_botones.pack(pady=20)
        
        def confirmar():
            nombre = entry_nombre.get().strip()
            if nombre:
                self.cliente_actual = nombre
                self.iniciar_pedido()
                ventana_nombre.destroy()
            else:
                messagebox.showwarning("Error", "Debe ingresar un nombre")
        
        btn_confirmar = tk.Button(frame_botones, text="Confirmar", font=FUENTE_BOTONES,
                                command=confirmar, bg=COLOR_BOTONES_ACCION, fg=COLOR_TEXTO,
                                padx=20, pady=5)
        btn_confirmar.pack(side="left", padx=10)
        
        btn_cancelar = tk.Button(frame_botones, text="Cancelar", font=FUENTE_BOTONES,
                               command=ventana_nombre.destroy, bg=COLOR_BOTONES, fg=COLOR_TEXTO,
                               padx=20, pady=5)
        btn_cancelar.pack(side="right", padx=10)
    
    def iniciar_pedido(self):
        self.pedido_actual = Pedido(self.cliente_actual)
        self.mostrar_pantalla(PantallaMenu)
    
    def agregar_al_carrito(self, producto):
        if self.pedido_actual:
            self.pedido_actual.agregar_producto(producto)
            messagebox.showinfo("Producto Agregado", f"{producto.nombre} agregado al carrito")
    
    def ver_carrito(self):
        self.mostrar_pantalla(PantallaCarrito)
    
    def finalizar_pedido(self):
        if not (self.pedido_actual and self.pedido_actual.productos):
            messagebox.showwarning("Error", "El carrito está vacío")
            return
        
        # Verificar ingredientes
        for producto in self.pedido_actual.productos:
            if isinstance(producto, Bebida):
                ingredientes = self.obtener_ingredientes_bebida(producto)
                if not self.gestor_datos.inventario.verificar_disponibilidad(ingredientes):
                    messagebox.showwarning("Ingredientes Insuficientes", 
                                        f"No hay suficientes ingredientes para {producto.nombre}")
                    return
        
        confirmacion = messagebox.askyesno(
            "Confirmar Pedido",
            f"Total: ${self.pedido_actual.calcular_total():.2f}\n¿Confirmar pedido?"
        )
        
        if confirmacion:
            # Consumir ingredientes
            for producto in self.pedido_actual.productos:
                if isinstance(producto, Bebida):
                    self.gestor_datos.inventario.usar_ingredientes(
                        self.obtener_ingredientes_bebida(producto)
                    )
            
            # Guardar pedido
            self.gestor_datos.pedidos.append(self.pedido_actual)
            self.gestor_datos.guardar_pedidos()
            self.gestor_datos.guardar_inventario()
            
            messagebox.showinfo("Éxito", 
                f"Pedido #{self.pedido_actual.id[:8]} registrado correctamente\n"
                f"Total: ${self.pedido_actual.total:.2f}")
            
            self.pedido_actual = None
            self.mostrar_pantalla(PantallaInicio)
    
    def obtener_ingredientes_bebida(self, bebida):
        return {
            "café": 1,
            "leche": 1 if "Extra leche" in bebida.opciones else 0.5,
            "azúcar": 0 if "Sin azúcar" in bebida.opciones else 1
        }
    
    def entrar_modo_admin(self, usuario, contrasena):
        if usuario == "admin" and contrasena == "admin123":
            self.modo_admin = True
            self.mostrar_pantalla(PantallaAdmin)
            return True
        return False
    
    def salir_modo_admin(self):
        self.modo_admin = False
        self.mostrar_pantalla(PantallaInicio)
    
    def actualizar_inventario(self, ingrediente, cantidad):
        self.gestor_datos.inventario.agregar_ingrediente(ingrediente, cantidad)
        self.gestor_datos.guardar_inventario()
        messagebox.showinfo("Inventario Actualizado", f"{ingrediente} actualizado")
    
    def eliminar_ingrediente(self, ingrediente):
        if self.gestor_datos.inventario.eliminar_ingrediente(ingrediente):
            self.gestor_datos.guardar_inventario()
            messagebox.showinfo("Éxito", f"Ingrediente {ingrediente} eliminado")
            return True
        messagebox.showwarning("Error", f"Ingrediente {ingrediente} no encontrado")
        return False
    
    def agregar_bebida(self, nombre, precio, tamano, tipo):
        nueva_bebida = Bebida(nombre, precio, tamano, tipo)
        self.gestor_datos.bebidas.append(nueva_bebida)
        self.gestor_datos.guardar_productos()
        return nueva_bebida
    
    def eliminar_bebida(self, nombre):
        self.gestor_datos.bebidas = [b for b in self.gestor_datos.bebidas if b.nombre != nombre]
        self.gestor_datos.guardar_productos()
    
    def agregar_postre(self, nombre, precio, es_vegano, sin_gluten):
        nuevo_postre = Postre(nombre, precio, es_vegano, sin_gluten)
        self.gestor_datos.postres.append(nuevo_postre)
        self.gestor_datos.guardar_productos()
        return nuevo_postre
    
    def eliminar_postre(self, nombre):
        self.gestor_datos.postres = [p for p in self.gestor_datos.postres if p.nombre != nombre]
        self.gestor_datos.guardar_productos()
    
    def agregar_empleado(self, nombre, rol):
        nuevo_empleado = Empleado(nombre, rol)
        self.gestor_datos.empleados.append(nuevo_empleado)
        self.gestor_datos.guardar_empleados()
        return nuevo_empleado
    
    def eliminar_empleado(self, nombre):
        self.gestor_datos.empleados = [e for e in self.gestor_datos.empleados if e.nombre != nombre]
        self.gestor_datos.guardar_empleados()
    
    def cambiar_estado_pedido(self, pedido, nuevo_estado):
        pedido.cambiar_estado(nuevo_estado)
        self.gestor_datos.guardar_pedidos()
        messagebox.showinfo("Estado Actualizado", f"Pedido actualizado a: {nuevo_estado}")
    
    def eliminar_pedido(self, pedido):
        self.gestor_datos.pedidos = [p for p in self.gestor_datos.pedidos if p.id != pedido.id]
        self.gestor_datos.guardar_pedidos()
        messagebox.showinfo("Éxito", "Pedido eliminado correctamente")

class PantallaInicio(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_FONDO)
        self.controller = controller
        
        # Frame principal
        frame_principal = tk.Frame(self, bg=COLOR_FONDO)
        frame_principal.pack(fill="both", expand=True, padx=50, pady=50)
        
        # Logo y título
        frame_logo = tk.Frame(frame_principal, bg=COLOR_FONDO)
        frame_logo.pack(pady=(0, 30))
        
        # Logo (puedes reemplazar esto con una imagen real)
        canvas = tk.Canvas(frame_logo, width=200, height=200, bg=COLOR_ENCABEZADO, highlightthickness=0)
        canvas.create_text(100, 100, text="☕", font=("Arial", 80), fill=COLOR_TEXTO)
        canvas.pack(pady=10)
        
        # Título
        tk.Label(frame_logo, text="Cafetería das Haus", font=FUENTE_TITULO, 
                bg=COLOR_FONDO, fg=COLOR_TEXTO_OSCURO).pack(pady=10)
        
        # Subtítulo
        tk.Label(frame_logo, text="Sistema de Gestión de Pedidos", font=FUENTE_SUBTITULO,
               bg=COLOR_FONDO, fg=COLOR_DESTACADO).pack(pady=5)
        
        # Frame de botones
        frame_botones = tk.Frame(frame_principal, bg=COLOR_FONDO)
        frame_botones.pack(pady=20)
        
        # Botón Iniciar Pedido
        btn_iniciar = tk.Button(frame_botones, text="Iniciar Pedido", font=FUENTE_BOTONES, 
                              command=self.controller.solicitar_nombre_cliente, 
                              bg=COLOR_BOTONES_ACCION, fg=COLOR_TEXTO,
                              width=25, height=2, padx=20, pady=10,
                              activebackground=COLOR_TERCIARIO)
        btn_iniciar.pack(pady=15)
        
        # Botón Ver Pedidos
        btn_pedidos = tk.Button(frame_botones, text="Ver Pedidos Anteriores", font=FUENTE_BOTONES, 
                              command=self.ver_pedidos, 
                              bg=COLOR_BOTONES, fg=COLOR_TEXTO,
                              width=25, height=1, padx=20, pady=5,
                              activebackground=COLOR_TERCIARIO)
        btn_pedidos.pack(pady=10)
        
        # Botón Modo Administrador
        btn_admin = tk.Button(frame_botones, text="Modo Administrador", font=FUENTE_BOTONES, 
                            command=self.login_admin, 
                            bg=COLOR_ADMIN, fg=COLOR_TEXTO,
                            width=25, height=1, padx=20, pady=5,
                            activebackground=COLOR_TERCIARIO)
        btn_admin.pack(pady=10)
    
    def ver_pedidos(self):
        if not self.controller.gestor_datos.pedidos:
            messagebox.showinfo("Pedidos", "No hay pedidos registrados")
            return
        
        pedidos_window = tk.Toplevel(self)
        pedidos_window.title("Historial de Pedidos")
        pedidos_window.geometry("900x700")
        pedidos_window.configure(bg=COLOR_FONDO)
        
        # Frame principal
        frame_principal = tk.Frame(pedidos_window, bg=COLOR_FONDO)
        frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        tk.Label(frame_principal, text="Historial de Pedidos", font=FUENTE_SUBTITULO,
               bg=COLOR_FONDO, fg=COLOR_TEXTO_OSCURO).pack(pady=(0, 20))
        
        # Frame de contenido
        frame_contenido = tk.Frame(frame_principal, bg=COLOR_FONDO)
        frame_contenido.pack(fill="both", expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(frame_contenido)
        scrollbar.pack(side="right", fill="y")
        
        # Texto con los pedidos
        text_pedidos = tk.Text(frame_contenido, wrap="word", yscrollcommand=scrollbar.set,
                             font=FUENTE_TEXTO, bg=COLOR_FONDO, fg=COLOR_TEXTO_OSCURO,
                             padx=10, pady=10)
        text_pedidos.pack(fill="both", expand=True)
        
        for pedido in self.controller.gestor_datos.pedidos:
            text_pedidos.insert("end", f"{pedido}\n\n")
            text_pedidos.insert("end", "―"*50 + "\n\n")
        
        scrollbar.config(command=text_pedidos.yview)
        
        # Botón cerrar
        btn_cerrar = tk.Button(frame_principal, text="Cerrar", font=FUENTE_BOTONES,
                             command=pedidos_window.destroy,
                             bg=COLOR_BOTONES, fg=COLOR_TEXTO,
                             padx=20, pady=5)
        btn_cerrar.pack(pady=(20, 0))
    
    def login_admin(self):
        login_window = tk.Toplevel(self)
        login_window.title("Inicio de Sesión - Administrador")
        login_window.geometry("500x400")
        login_window.configure(bg=COLOR_FONDO)
        login_window.resizable(False, False)
        
        # Frame principal
        frame_principal = tk.Frame(login_window, bg=COLOR_FONDO, padx=30, pady=30)
        frame_principal.pack(fill="both", expand=True)
        
        # Título
        tk.Label(frame_principal, text="Acceso Administrador", font=FUENTE_SUBTITULO,
               bg=COLOR_FONDO, fg=COLOR_TEXTO_OSCURO).pack(pady=(0, 30))
        
        # Campos de entrada
        tk.Label(frame_principal, text="Usuario:", font=FUENTE_BOTONES, 
                bg=COLOR_FONDO, fg=COLOR_TEXTO_OSCURO).pack(anchor="w", pady=(10, 5))
        entry_usuario = tk.Entry(frame_principal, font=FUENTE_TEXTO, bd=2, relief=tk.GROOVE)
        entry_usuario.pack(fill="x", pady=(0, 20), ipady=5)
        
        tk.Label(frame_principal, text="Contraseña:", font=FUENTE_BOTONES, 
                bg=COLOR_FONDO, fg=COLOR_TEXTO_OSCURO).pack(anchor="w", pady=(10, 5))
        entry_contrasena = tk.Entry(frame_principal, font=FUENTE_TEXTO, bd=2, relief=tk.GROOVE, show="*")
        entry_contrasena.pack(fill="x", pady=(0, 30), ipady=5)
        
        # Frame de botones
        frame_botones = tk.Frame(frame_principal, bg=COLOR_FONDO)
        frame_botones.pack(fill="x", pady=(10, 0))
        
        def validar_login():
            usuario = entry_usuario.get().strip()
            contrasena = entry_contrasena.get().strip()
            if self.controller.entrar_modo_admin(usuario, contrasena):
                messagebox.showinfo("Éxito", "Inicio de sesión exitoso")
                login_window.destroy()
            else:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
        
        btn_login = tk.Button(frame_botones, text="Iniciar Sesión", font=FUENTE_BOTONES, 
                            command=validar_login, bg=COLOR_BOTONES_ACCION, fg=COLOR_TEXTO,
                            padx=20, pady=5)
        btn_login.pack(side="left", padx=10, expand=True)
        
        btn_cancelar = tk.Button(frame_botones, text="Cancelar", font=FUENTE_BOTONES, 
                               command=login_window.destroy, bg=COLOR_BOTONES, fg=COLOR_TEXTO,
                               padx=20, pady=5)
        btn_cancelar.pack(side="right", padx=10, expand=True)
    
    def actualizar(self):
        pass

class PantallaMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_FONDO)
        self.controller = controller
        
        # Frame principal
        frame_principal = tk.Frame(self, bg=COLOR_FONDO)
        frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        tk.Label(frame_principal, text="Menú de Productos", font=FUENTE_TITULO, 
               bg=COLOR_FONDO, fg=COLOR_TEXTO_OSCURO).pack(pady=(0, 20))
        
        # Pestañas
        notebook = ttk.Notebook(frame_principal)
        notebook.pack(fill="both", expand=True)
        
        # Pestaña de Bebidas
        tab_bebidas = ttk.Frame(notebook)
        notebook.add(tab_bebidas, text="Bebidas")
        self.crear_widgets_bebidas(tab_bebidas)
        
        # Pestaña de Postres
        tab_postres = ttk.Frame(notebook)
        notebook.add(tab_postres, text="Postres")
        self.crear_widgets_postres(tab_postres)
        
        # Frame de botones
        frame_botones = tk.Frame(frame_principal, bg=COLOR_FONDO)
        frame_botones.pack(fill="x", pady=(20, 0))
        
        btn_ver_carrito = tk.Button(frame_botones, text="Ver Carrito", font=FUENTE_BOTONES,
                                   command=self.controller.ver_carrito,
                                   bg=COLOR_BOTONES_ACCION, fg=COLOR_TEXTO,
                                   padx=20, pady=5)
        btn_ver_carrito.pack(side="left", padx=10)
        
        btn_volver = tk.Button(frame_botones, text="Volver al Inicio", font=FUENTE_BOTONES,
                              command=lambda: self.controller.mostrar_pantalla(PantallaInicio),
                              bg=COLOR_BOTONES, fg=COLOR_TEXTO,
                              padx=20, pady=5)
        btn_volver.pack(side="right", padx=10)
    
    def crear_widgets_bebidas(self, parent):
        # Frame para el scrollbar
        frame_scroll = tk.Frame(parent)
        frame_scroll.pack(fill="both", expand=True)
        
        # Canvas y scrollbar
        canvas = tk.Canvas(frame_scroll, bg=COLOR_FONDO, highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame_scroll, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Contenido de las bebidas
        for bebida in self.controller.gestor_datos.bebidas:
            frame_bebida = tk.Frame(scrollable_frame, bd=2, relief=tk.GROOVE, 
                                  bg=COLOR_CARRITO, padx=15, pady=15)
            frame_bebida.pack(fill="x", pady=10, ipadx=10, ipady=10)
            
            # Nombre y precio
            frame_superior = tk.Frame(frame_bebida, bg=COLOR_CARRITO)
            frame_superior.pack(fill="x")
            
            tk.Label(frame_superior, text=bebida.nombre, font=FUENTE_SUBTITULO, 
                    bg=COLOR_CARRITO, fg=COLOR_TEXTO_OSCURO).pack(side="left")
            
            tk.Label(frame_superior, text=f"${bebida.precio:.2f}", font=FUENTE_SUBTITULO,
                    bg=COLOR_CARRITO, fg=COLOR_DESTACADO).pack(side="right")
            
            # Personalización
            frame_personalizacion = tk.Frame(frame_bebida, bg=COLOR_CARRITO)
            frame_personalizacion.pack(fill="x", pady=(10, 0))
            
            # Tamaño
            tk.Label(frame_personalizacion, text="Tamaño:", font=FUENTE_TEXTO,
                   bg=COLOR_CARRITO, fg=COLOR_TEXTO_OSCURO).pack(anchor="w")
            
            frame_tamanos = tk.Frame(frame_personalizacion, bg=COLOR_CARRITO)
            frame_tamanos.pack(fill="x", pady=(5, 0))
            
            var_tamano = tk.StringVar(value=bebida.tamano)
            
            opciones_tamano = [
                ("Pequeño", "Pequeño"),
                ("Mediano", "Mediano"),
                ("Grande", "Grande")
            ]
            
            for texto, valor in opciones_tamano:
                tk.Radiobutton(frame_tamanos, text=texto, variable=var_tamano, 
                              value=valor, bg=COLOR_CARRITO, fg=COLOR_TEXTO_OSCURO,
                              selectcolor=COLOR_SECUNDARIO, font=FUENTE_TEXTO).pack(side="left", padx=10)
            
            # Opciones extras
            tk.Label(frame_personalizacion, text="Opciones:", font=FUENTE_TEXTO,
                   bg=COLOR_CARRITO, fg=COLOR_TEXTO_OSCURO).pack(anchor="w", pady=(10, 5))
            
            frame_opciones = tk.Frame(frame_personalizacion, bg=COLOR_CARRITO)
            frame_opciones.pack(fill="x")
            
            var_leche = tk.BooleanVar()
            tk.Checkbutton(frame_opciones, text="Extra leche", variable=var_leche,
                          bg=COLOR_CARRITO, fg=COLOR_TEXTO_OSCURO,
                          selectcolor=COLOR_SECUNDARIO, font=FUENTE_TEXTO).pack(side="left", padx=10)
            
            var_azucar = tk.BooleanVar()
            tk.Checkbutton(frame_opciones, text="Sin azúcar", variable=var_azucar,
                          bg=COLOR_CARRITO, fg=COLOR_TEXTO_OSCURO,
                          selectcolor=COLOR_SECUNDARIO, font=FUENTE_TEXTO).pack(side="left", padx=10)
            
            # Botón agregar
            btn_agregar = tk.Button(frame_bebida, text="Agregar al Carrito", 
                                   font=FUENTE_BOTONES,
                                   command=lambda b=bebida, vt=var_tamano, 
                                   vl=var_leche, va=var_azucar: 
                                   self.agregar_bebida(b, vt.get(), vl.get(), va.get()),
                                   bg=COLOR_BOTONES_ACCION, fg=COLOR_TEXTO,
                                   padx=15, pady=5)
            btn_agregar.pack(pady=(15, 5), fill="x")
    
    def agregar_bebida(self, bebida_base, tamano, extra_leche, sin_azucar):
        opciones = []
        if extra_leche:
            opciones.append("Extra leche")
        if sin_azucar:
            opciones.append("Sin azúcar")
        
        bebida_personalizada = Bebida(
            bebida_base.nombre,
            bebida_base.precio,
            tamano,
            bebida_base.tipo,
            opciones
        )
        self.controller.agregar_al_carrito(bebida_personalizada)
    
    def crear_widgets_postres(self, parent):
        # Frame para el scrollbar
        frame_scroll = tk.Frame(parent)
        frame_scroll.pack(fill="both", expand=True)
        
        # Canvas y scrollbar
        canvas = tk.Canvas(frame_scroll, bg=COLOR_FONDO, highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame_scroll, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Contenido de los postres
        for postre in self.controller.gestor_datos.postres:
            frame_postre = tk.Frame(scrollable_frame, bd=2, relief=tk.GROOVE, 
                                  bg=COLOR_CARRITO, padx=15, pady=15)
            frame_postre.pack(fill="x", pady=10, ipadx=10, ipady=10)
            
            # Nombre y precio
            frame_superior = tk.Frame(frame_postre, bg=COLOR_CARRITO)
            frame_superior.pack(fill="x")
            
            tk.Label(frame_superior, text=postre.nombre, font=FUENTE_SUBTITULO, 
                    bg=COLOR_CARRITO, fg=COLOR_TEXTO_OSCURO).pack(side="left")
            
            tk.Label(frame_superior, text=f"${postre.precio:.2f}", font=FUENTE_SUBTITULO,
                    bg=COLOR_CARRITO, fg=COLOR_DESTACADO).pack(side="right")
            
            # Detalles especiales
            detalles = []
            if postre.es_vegano:
                detalles.append("Vegano")
            if postre.sin_gluten:
                detalles.append("Sin gluten")
            
            if detalles:
                frame_detalles = tk.Frame(frame_postre, bg=COLOR_CARRITO)
                frame_detalles.pack(fill="x", pady=(10, 0))
                
                for detalle in detalles:
                    tk.Label(frame_detalles, text=detalle, font=FUENTE_TEXTO,
                            bg=COLOR_CARRITO, fg="green").pack(side="left", padx=10)
            
            # Botón agregar
            btn_agregar = tk.Button(frame_postre, text="Agregar al Carrito", 
                                   font=FUENTE_BOTONES,
                                   command=lambda p=postre: self.controller.agregar_al_carrito(p),
                                   bg=COLOR_BOTONES_ACCION, fg=COLOR_TEXTO,
                                   padx=15, pady=5)
            btn_agregar.pack(pady=(15, 5), fill="x")
    
    def actualizar(self):
        pass

class PantallaCarrito(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_FONDO)
        self.controller = controller
        
        # Frame principal
        frame_principal = tk.Frame(self, bg=COLOR_FONDO)
        frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        tk.Label(frame_principal, text="Tu Carrito de Compras", font=FUENTE_TITULO, 
               bg=COLOR_FONDO, fg=COLOR_TEXTO_OSCURO).pack(pady=(0, 20))
        
        # Frame de productos
        self.frame_productos = tk.Frame(frame_principal, bg=COLOR_FONDO)
        self.frame_productos.pack(fill="both", expand=True)
        
        # Total
        self.lbl_total = tk.Label(frame_principal, text="Total: $0.00", font=FUENTE_SUBTITULO,
                                 bg=COLOR_FONDO, fg=COLOR_DESTACADO)
        self.lbl_total.pack(pady=(20, 10))
        
        # Frame de botones
        frame_botones = tk.Frame(frame_principal, bg=COLOR_FONDO)
        frame_botones.pack(fill="x", pady=(10, 0))
        
        btn_seguir = tk.Button(frame_botones, text="Seguir Comprando", font=FUENTE_BOTONES,
                             command=lambda: self.controller.mostrar_pantalla(PantallaMenu),
                             bg=COLOR_BOTONES, fg=COLOR_TEXTO,
                             padx=20, pady=5)
        btn_seguir.pack(side="left", padx=10)
        
        btn_finalizar = tk.Button(frame_botones, text="Finalizar Pedido", font=FUENTE_BOTONES,
                                command=self.controller.finalizar_pedido,
                                bg=COLOR_BOTONES_ACCION, fg=COLOR_TEXTO,
                                padx=20, pady=5)
        btn_finalizar.pack(side="right", padx=10)
    
    def actualizar(self):
        # Limpiar frame
        for widget in self.frame_productos.winfo_children():
            widget.destroy()
        
        if not self.controller.pedido_actual or not self.controller.pedido_actual.productos:
            tk.Label(self.frame_productos, text="El carrito está vacío", 
                    font=FUENTE_SUBTITULO, bg=COLOR_FONDO, fg=COLOR_TEXTO_OSCURO).pack(pady=50)
            self.lbl_total.config(text="Total: $0.00")
            return
        
        # Frame para el scrollbar
        frame_scroll = tk.Frame(self.frame_productos)
        frame_scroll.pack(fill="both", expand=True)
        
        # Canvas y scrollbar
        canvas = tk.Canvas(frame_scroll, bg=COLOR_FONDO, highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame_scroll, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        total = 0
        for producto in self.controller.pedido_actual.productos:
            frame_producto = tk.Frame(scrollable_frame, bd=2, relief=tk.GROOVE,
                                    bg=COLOR_CARRITO, padx=15, pady=15)
            frame_producto.pack(fill="x", pady=5, ipadx=5, ipady=5)
            
            # Nombre y precio
            frame_superior = tk.Frame(frame_producto, bg=COLOR_CARRITO)
            frame_superior.pack(fill="x")
            
            tk.Label(frame_superior, text=producto.nombre, font=FUENTE_BOTONES,
                    bg=COLOR_CARRITO, fg=COLOR_TEXTO_OSCURO).pack(side="left")
            
            tk.Label(frame_superior, text=f"${producto.precio:.2f}", font=FUENTE_BOTONES,
                    bg=COLOR_CARRITO, fg=COLOR_DESTACADO).pack(side="right")
            
            # Detalles del producto
            frame_detalles = tk.Frame(frame_producto, bg=COLOR_CARRITO)
            frame_detalles.pack(fill="x", pady=(10, 0))
            
            detalles = []
            if isinstance(producto, Bebida):
                detalles.append(f"Tamaño: {producto.tamano}")
                detalles.append(f"Tipo: {producto.tipo}")
                if producto.opciones:
                    detalles.append(f"Extras: {', '.join(producto.opciones)}")
            elif isinstance(producto, Postre):
                if producto.es_vegano:
                    detalles.append("Vegano")
                if producto.sin_gluten:
                    detalles.append("Sin gluten")
            
            if detalles:
                tk.Label(frame_detalles, text=" | ".join(detalles), font=FUENTE_TEXTO,
                        bg=COLOR_CARRITO, fg=COLOR_TEXTO_OSCURO).pack(anchor="w")
            
            # Botón eliminar
            btn_eliminar = tk.Button(frame_producto, text="Eliminar", font=FUENTE_BOTONES,
                                   command=lambda p=producto: self.eliminar_producto(p),
                                   bg=COLOR_BOTONES_PELIGRO, fg=COLOR_TEXTO,
                                   padx=15, pady=3)
            btn_eliminar.pack(pady=(10, 0), fill="x")
            
            total += producto.precio
        
        self.lbl_total.config(text=f"Total: ${total:.2f}")
    
    def eliminar_producto(self, producto):
        if self.controller.pedido_actual:
            self.controller.pedido_actual.eliminar_producto(producto)
            self.actualizar()

class PantallaAdmin(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_FONDO)
        self.controller = controller
        
        # Frame principal
        frame_principal = tk.Frame(self, bg=COLOR_FONDO)
        frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        tk.Label(frame_principal, text="Panel de Administración", font=FUENTE_TITULO, 
               bg=COLOR_FONDO, fg=COLOR_TEXTO_OSCURO).pack(pady=(0, 20))
        
        # Pestañas
        notebook = ttk.Notebook(frame_principal)
        notebook.pack(fill="both", expand=True)
        
        # Pestaña de Productos
        tab_productos = ttk.Frame(notebook)
        notebook.add(tab_productos, text="Productos")
        self.crear_pestana_productos(tab_productos)
        
        # Pestaña de Inventario
        tab_inventario = ttk.Frame(notebook)
        notebook.add(tab_inventario, text="Inventario")
        self.crear_pestana_inventario(tab_inventario)
        
        # Pestaña de Pedidos
        tab_pedidos = ttk.Frame(notebook)
        notebook.add(tab_pedidos, text="Pedidos")
        self.crear_pestana_pedidos(tab_pedidos)
        
        # Pestaña de Empleados
        tab_empleados = ttk.Frame(notebook)
        notebook.add(tab_empleados, text="Empleados")
        self.crear_pestana_empleados(tab_empleados)
        
        # Botón salir
        btn_salir = tk.Button(frame_principal, text="Salir del Modo Administrador", font=FUENTE_BOTONES,
                            command=self.controller.salir_modo_admin,
                            bg=COLOR_ADMIN, fg=COLOR_TEXTO,
                            padx=20, pady=5)
        btn_salir.pack(pady=(20, 0))
    
    def crear_pestana_productos(self, parent):
        # Frame principal
        frame_principal = tk.Frame(parent)
        frame_principal.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Notebook para bebidas y postres
        notebook = ttk.Notebook(frame_principal)
        notebook.pack(fill="both", expand=True)
        
        # Pestaña Bebidas
        tab_bebidas = ttk.Frame(notebook)
        notebook.add(tab_bebidas, text="Bebidas")
        self.crear_seccion_bebidas(tab_bebidas)
        
        # Pestaña Postres
        tab_postres = ttk.Frame(notebook)
        notebook.add(tab_postres, text="Postres")
        self.crear_seccion_postres(tab_postres)
    
    def crear_seccion_bebidas(self, parent):
        # Frame para agregar nueva bebida
        frame_agregar = tk.Frame(parent)
        frame_agregar.pack(fill="x", padx=10, pady=10)
        
        tk.Label(frame_agregar, text="Nombre:", font=FUENTE_TEXTO).grid(row=0, column=0, padx=5, pady=5)
        self.entry_bebida_nombre = tk.Entry(frame_agregar, font=FUENTE_TEXTO, bd=2, relief=tk.GROOVE)
        self.entry_bebida_nombre.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        tk.Label(frame_agregar, text="Precio:", font=FUENTE_TEXTO).grid(row=0, column=2, padx=5, pady=5)
        self.entry_bebida_precio = tk.Entry(frame_agregar, font=FUENTE_TEXTO, bd=2, relief=tk.GROOVE)
        self.entry_bebida_precio.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        
        tk.Label(frame_agregar, text="Tamaño:", font=FUENTE_TEXTO).grid(row=1, column=0, padx=5, pady=5)
        self.combo_bebida_tamano = ttk.Combobox(frame_agregar, values=["Pequeño", "Mediano", "Grande"], font=FUENTE_TEXTO)
        self.combo_bebida_tamano.current(1)
        self.combo_bebida_tamano.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        tk.Label(frame_agregar, text="Tipo:", font=FUENTE_TEXTO).grid(row=1, column=2, padx=5, pady=5)
        self.combo_bebida_tipo = ttk.Combobox(frame_agregar, values=["Caliente", "Frío"], font=FUENTE_TEXTO)
        self.combo_bebida_tipo.current(0)
        self.combo_bebida_tipo.grid(row=1, column=3, padx=5, pady=5, sticky="ew")
        
        btn_agregar = tk.Button(frame_agregar, text="Agregar Bebida", font=FUENTE_BOTONES,
                              command=self.agregar_bebida,
                              bg=COLOR_BOTONES_ACCION, fg=COLOR_TEXTO,
                              padx=10, pady=5)
        btn_agregar.grid(row=2, column=0, columnspan=4, pady=10, sticky="ew")
        
        # Lista de bebidas
        frame_lista = tk.Frame(parent)
        frame_lista.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tree_bebidas = ttk.Treeview(frame_lista, columns=("Nombre", "Precio", "Tamaño", "Tipo"), show="headings")
        self.tree_bebidas.heading("Nombre", text="Nombre")
        self.tree_bebidas.heading("Precio", text="Precio")
        self.tree_bebidas.heading("Tamaño", text="Tamaño")
        self.tree_bebidas.heading("Tipo", text="Tipo")
        
        self.tree_bebidas.column("Nombre", width=150)
        self.tree_bebidas.column("Precio", width=80)
        self.tree_bebidas.column("Tamaño", width=80)
        self.tree_bebidas.column("Tipo", width=80)
        
        self.tree_bebidas.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(frame_lista, orient="vertical", command=self.tree_bebidas.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree_bebidas.configure(yscrollcommand=scrollbar.set)
        
        btn_eliminar = tk.Button(parent, text="Eliminar Bebida Seleccionada", font=FUENTE_BOTONES,
                               command=self.eliminar_bebida,
                               bg=COLOR_BOTONES_PELIGRO, fg=COLOR_TEXTO,
                               padx=10, pady=5)
        btn_eliminar.pack(pady=10, fill="x")
        
        self.actualizar_lista_bebidas()
    
    def agregar_bebida(self):
        nombre = self.entry_bebida_nombre.get().strip()
        precio = self.entry_bebida_precio.get().strip()
        tamano = self.combo_bebida_tamano.get()
        tipo = self.combo_bebida_tipo.get()
        
        if not nombre or not precio:
            messagebox.showwarning("Error", "Debe ingresar nombre y precio")
            return
        
        try:
            precio = float(precio)
        except ValueError:
            messagebox.showwarning("Error", "El precio debe ser un número")
            return
        
        self.controller.agregar_bebida(nombre, precio, tamano, tipo)
        self.actualizar_lista_bebidas()
        
        self.entry_bebida_nombre.delete(0, tk.END)
        self.entry_bebida_precio.delete(0, tk.END)
        messagebox.showinfo("Éxito", "Bebida agregada correctamente")
    
    def eliminar_bebida(self):
        seleccion = self.tree_bebidas.selection()
        if not seleccion:
            messagebox.showwarning("Error", "Debe seleccionar una bebida")
            return
        
        item = self.tree_bebidas.item(seleccion)
        nombre = item['values'][0]
        
        self.controller.eliminar_bebida(nombre)
        self.actualizar_lista_bebidas()
        messagebox.showinfo("Éxito", "Bebida eliminada correctamente")
    
    def actualizar_lista_bebidas(self):
        for item in self.tree_bebidas.get_children():
            self.tree_bebidas.delete(item)
        
        for bebida in self.controller.gestor_datos.bebidas:
            self.tree_bebidas.insert("", "end", values=(
                bebida.nombre, 
                f"${bebida.precio:.2f}", 
                bebida.tamano, 
                bebida.tipo
            ))
    
    def crear_seccion_postres(self, parent):
        # Frame para agregar nuevo postre
        frame_agregar = tk.Frame(parent)
        frame_agregar.pack(fill="x", padx=10, pady=10)
        
        tk.Label(frame_agregar, text="Nombre:", font=FUENTE_TEXTO).grid(row=0, column=0, padx=5, pady=5)
        self.entry_postre_nombre = tk.Entry(frame_agregar, font=FUENTE_TEXTO, bd=2, relief=tk.GROOVE)
        self.entry_postre_nombre.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        tk.Label(frame_agregar, text="Precio:", font=FUENTE_TEXTO).grid(row=0, column=2, padx=5, pady=5)
        self.entry_postre_precio = tk.Entry(frame_agregar, font=FUENTE_TEXTO, bd=2, relief=tk.GROOVE)
        self.entry_postre_precio.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        
        self.var_postre_vegano = tk.BooleanVar()
        tk.Checkbutton(frame_agregar, text="Vegano", variable=self.var_postre_vegano,
                      font=FUENTE_TEXTO, bg=COLOR_FONDO).grid(row=1, column=0, padx=5, pady=5)
        
        self.var_postre_sin_gluten = tk.BooleanVar()
        tk.Checkbutton(frame_agregar, text="Sin gluten", variable=self.var_postre_sin_gluten,
                      font=FUENTE_TEXTO, bg=COLOR_FONDO).grid(row=1, column=1, padx=5, pady=5)
        
        btn_agregar = tk.Button(frame_agregar, text="Agregar Postre", font=FUENTE_BOTONES,
                              command=self.agregar_postre,
                              bg=COLOR_BOTONES_ACCION, fg=COLOR_TEXTO,
                              padx=10, pady=5)
        btn_agregar.grid(row=2, column=0, columnspan=4, pady=10, sticky="ew")
        
        # Lista de postres
        frame_lista = tk.Frame(parent)
        frame_lista.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tree_postres = ttk.Treeview(frame_lista, columns=("Nombre", "Precio", "Vegano", "Sin gluten"), show="headings")
        self.tree_postres.heading("Nombre", text="Nombre")
        self.tree_postres.heading("Precio", text="Precio")
        self.tree_postres.heading("Vegano", text="Vegano")
        self.tree_postres.heading("Sin gluten", text="Sin gluten")
        
        self.tree_postres.column("Nombre", width=150)
        self.tree_postres.column("Precio", width=80)
        self.tree_postres.column("Vegano", width=80)
        self.tree_postres.column("Sin gluten", width=80)
        
        self.tree_postres.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(frame_lista, orient="vertical", command=self.tree_postres.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree_postres.configure(yscrollcommand=scrollbar.set)
        
        btn_eliminar = tk.Button(parent, text="Eliminar Postre Seleccionado", font=FUENTE_BOTONES,
                               command=self.eliminar_postre,
                               bg=COLOR_BOTONES_PELIGRO, fg=COLOR_TEXTO,
                               padx=10, pady=5)
        btn_eliminar.pack(pady=10, fill="x")
        
        self.actualizar_lista_postres()
    
    def agregar_postre(self):
        nombre = self.entry_postre_nombre.get().strip()
        precio = self.entry_postre_precio.get().strip()
        es_vegano = self.var_postre_vegano.get()
        sin_gluten = self.var_postre_sin_gluten.get()
        
        if not nombre or not precio:
            messagebox.showwarning("Error", "Debe ingresar nombre y precio")
            return
        
        try:
            precio = float(precio)
        except ValueError:
            messagebox.showwarning("Error", "El precio debe ser un número")
            return
        
        self.controller.agregar_postre(nombre, precio, es_vegano, sin_gluten)
        self.actualizar_lista_postres()
        
        self.entry_postre_nombre.delete(0, tk.END)
        self.entry_postre_precio.delete(0, tk.END)
        self.var_postre_vegano.set(False)
        self.var_postre_sin_gluten.set(False)
        messagebox.showinfo("Éxito", "Postre agregado correctamente")
    
    def eliminar_postre(self):
        seleccion = self.tree_postres.selection()
        if not seleccion:
            messagebox.showwarning("Error", "Debe seleccionar un postre")
            return
        
        item = self.tree_postres.item(seleccion)
        nombre = item['values'][0]
        
        self.controller.eliminar_postre(nombre)
        self.actualizar_lista_postres()
        messagebox.showinfo("Éxito", "Postre eliminado correctamente")
    
    def actualizar_lista_postres(self):
        for item in self.tree_postres.get_children():
            self.tree_postres.delete(item)
        
        for postre in self.controller.gestor_datos.postres:
            self.tree_postres.insert("", "end", values=(
                postre.nombre, 
                f"${postre.precio:.2f}", 
                "Sí" if postre.es_vegano else "No", 
                "Sí" if postre.sin_gluten else "No"
            ))
    
    def crear_pestana_inventario(self, parent):
        # Frame para agregar/actualizar inventario
        frame_agregar = tk.Frame(parent)
        frame_agregar.pack(fill="x", padx=10, pady=10)
        
        tk.Label(frame_agregar, text="Ingrediente:", font=FUENTE_TEXTO).grid(row=0, column=0, padx=5, pady=5)
        self.entry_ingrediente = tk.Entry(frame_agregar, font=FUENTE_TEXTO, bd=2, relief=tk.GROOVE)
        self.entry_ingrediente.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        tk.Label(frame_agregar, text="Cantidad:", font=FUENTE_TEXTO).grid(row=0, column=2, padx=5, pady=5)
        self.entry_cantidad = tk.Entry(frame_agregar, font=FUENTE_TEXTO, bd=2, relief=tk.GROOVE)
        self.entry_cantidad.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        
        btn_agregar = tk.Button(frame_agregar, text="Agregar/Actualizar", font=FUENTE_BOTONES,
                              command=self.actualizar_inventario,
                              bg=COLOR_BOTONES_ACCION, fg=COLOR_TEXTO,
                              padx=10, pady=5)
        btn_agregar.grid(row=1, column=0, columnspan=2, pady=5, sticky="ew")
        
        btn_eliminar = tk.Button(frame_agregar, text="Eliminar", font=FUENTE_BOTONES,
                               command=self.eliminar_ingrediente,
                               bg=COLOR_BOTONES_PELIGRO, fg=COLOR_TEXTO,
                               padx=10, pady=5)
        btn_eliminar.grid(row=1, column=2, columnspan=2, pady=5, sticky="ew")
        
        # Lista de inventario
        frame_lista = tk.Frame(parent)
        frame_lista.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tree_inventario = ttk.Treeview(frame_lista, columns=("Ingrediente", "Cantidad"), show="headings")
        self.tree_inventario.heading("Ingrediente", text="Ingrediente")
        self.tree_inventario.heading("Cantidad", text="Cantidad")
        
        self.tree_inventario.column("Ingrediente", width=150)
        self.tree_inventario.column("Cantidad", width=100)
        
        self.tree_inventario.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(frame_lista, orient="vertical", command=self.tree_inventario.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree_inventario.configure(yscrollcommand=scrollbar.set)
        
        self.actualizar_lista_inventario()
    
    def actualizar_inventario(self):
        ingrediente = self.entry_ingrediente.get().strip()
        cantidad = self.entry_cantidad.get().strip()
        
        if not ingrediente:
            messagebox.showwarning("Error", "Debe ingresar un ingrediente")
            return
        
        try:
            cantidad = int(cantidad) if cantidad else 0
        except ValueError:
            messagebox.showwarning("Error", "La cantidad debe ser un número entero")
            return
        
        self.controller.actualizar_inventario(ingrediente, cantidad)
        self.actualizar_lista_inventario()
        
        self.entry_ingrediente.delete(0, tk.END)
        self.entry_cantidad.delete(0, tk.END)
        messagebox.showinfo("Éxito", "Inventario actualizado correctamente")
    
    def eliminar_ingrediente(self):
        ingrediente = self.entry_ingrediente.get().strip()
        
        if not ingrediente:
            messagebox.showwarning("Error", "Debe ingresar un ingrediente")
            return
        
        if messagebox.askyesno("Confirmar", f"¿Está seguro que desea eliminar el ingrediente {ingrediente}?"):
            if self.controller.eliminar_ingrediente(ingrediente):
                self.actualizar_lista_inventario()
                self.entry_ingrediente.delete(0, tk.END)
                self.entry_cantidad.delete(0, tk.END)
    
    def actualizar_lista_inventario(self):
        for item in self.tree_inventario.get_children():
            self.tree_inventario.delete(item)
        
        for ingrediente, cantidad in self.controller.gestor_datos.inventario.ingredientes.items():
            self.tree_inventario.insert("", "end", values=(ingrediente, cantidad))
    
    def crear_pestana_pedidos(self, parent):
        # Frame principal
        frame_principal = tk.Frame(parent)
        frame_principal.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Lista de pedidos
        self.tree_pedidos = ttk.Treeview(frame_principal, 
                                       columns=("ID", "Cliente", "Estado", "Total", "Fecha"), 
                                       show="headings")
        self.tree_pedidos.heading("ID", text="ID")
        self.tree_pedidos.heading("Cliente", text="Cliente")
        self.tree_pedidos.heading("Estado", text="Estado")
        self.tree_pedidos.heading("Total", text="Total")
        self.tree_pedidos.heading("Fecha", text="Fecha")
        
        self.tree_pedidos.column("ID", width=80)
        self.tree_pedidos.column("Cliente", width=120)
        self.tree_pedidos.column("Estado", width=120)
        self.tree_pedidos.column("Total", width=80)
        self.tree_pedidos.column("Fecha", width=120)
        
        self.tree_pedidos.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(frame_principal, orient="vertical", command=self.tree_pedidos.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree_pedidos.configure(yscrollcommand=scrollbar.set)
        
        # Frame de botones
        frame_botones = tk.Frame(parent)
        frame_botones.pack(fill="x", padx=10, pady=10)
        
        btn_actualizar = tk.Button(frame_botones, text="Actualizar Lista", font=FUENTE_BOTONES,
                                 command=self.actualizar_lista_pedidos,
                                 bg=COLOR_BOTONES, fg=COLOR_TEXTO,
                                 padx=10, pady=5)
        btn_actualizar.pack(side="left", padx=5)
        
        btn_cambiar_estado = tk.Button(frame_botones, text="Cambiar Estado", font=FUENTE_BOTONES,
                                     command=self.cambiar_estado_pedido,
                                     bg=COLOR_BOTONES_ACCION, fg=COLOR_TEXTO,
                                     padx=10, pady=5)
        btn_cambiar_estado.pack(side="left", padx=5)
        
        btn_ver_detalles = tk.Button(frame_botones, text="Ver Detalles", font=FUENTE_BOTONES,
                                   command=self.ver_detalles_pedido,
                                   bg=COLOR_BOTONES, fg=COLOR_TEXTO,
                                   padx=10, pady=5)
        btn_ver_detalles.pack(side="left", padx=5)
        
        btn_eliminar = tk.Button(frame_botones, text="Eliminar Pedido", font=FUENTE_BOTONES,
                               command=self.eliminar_pedido,
                               bg=COLOR_BOTONES_PELIGRO, fg=COLOR_TEXTO,
                               padx=10, pady=5)
        btn_eliminar.pack(side="right", padx=5)
        
        self.actualizar_lista_pedidos()
    
    def actualizar_lista_pedidos(self):
        for item in self.tree_pedidos.get_children():
            self.tree_pedidos.delete(item)
        
        for pedido in self.controller.gestor_datos.pedidos:
            self.tree_pedidos.insert("", "end", values=(
                pedido.id[:8],
                pedido.cliente,
                pedido.estado,
                f"${pedido.total:.2f}",
                pedido.fecha
            ))
    
    def cambiar_estado_pedido(self):
        seleccion = self.tree_pedidos.selection()
        if not seleccion:
            messagebox.showwarning("Error", "Debe seleccionar un pedido")
            return
        
        item = self.tree_pedidos.item(seleccion)
        id_pedido = item['values'][0]
        
        pedido = next((p for p in self.controller.gestor_datos.pedidos if p.id[:8] == id_pedido), None)
        if not pedido:
            messagebox.showwarning("Error", "Pedido no encontrado")
            return
        
        # Ventana para cambiar estado
        ventana_estado = tk.Toplevel(self)
        ventana_estado.title("Cambiar Estado del Pedido")
        ventana_estado.geometry("400x300")
        ventana_estado.configure(bg=COLOR_FONDO)
        
        tk.Label(ventana_estado, text="Seleccione el nuevo estado:", font=FUENTE_BOTONES,
               bg=COLOR_FONDO, fg=COLOR_TEXTO_OSCURO).pack(pady=10)
        
        estados = ["Nuevo", "En preparación", "Listo", "Entregado", "Cancelado"]
        var_estado = tk.StringVar(value=pedido.estado)
        
        frame_estados = tk.Frame(ventana_estado, bg=COLOR_FONDO)
        frame_estados.pack(pady=10)
        
        for estado in estados:
            tk.Radiobutton(frame_estados, text=estado, variable=var_estado, value=estado,
                          bg=COLOR_FONDO, fg=COLOR_TEXTO_OSCURO, font=FUENTE_TEXTO,
                          selectcolor=COLOR_SECUNDARIO).pack(anchor="w", pady=5)
        
        def confirmar():
            nuevo_estado = var_estado.get()
            self.controller.cambiar_estado_pedido(pedido, nuevo_estado)
            self.actualizar_lista_pedidos()
            ventana_estado.destroy()
            messagebox.showinfo("Éxito", "Estado actualizado correctamente")
        
        tk.Button(ventana_estado, text="Confirmar", command=confirmar,
                bg=COLOR_BOTONES_ACCION, fg=COLOR_TEXTO, font=FUENTE_BOTONES,
                padx=15, pady=5).pack(pady=10)
    
    def ver_detalles_pedido(self):
        seleccion = self.tree_pedidos.selection()
        if not seleccion:
            messagebox.showwarning("Error", "Debe seleccionar un pedido")
            return
        
        item = self.tree_pedidos.item(seleccion)
        id_pedido = item['values'][0]
        
        pedido = next((p for p in self.controller.gestor_datos.pedidos if p.id[:8] == id_pedido), None)
        if not pedido:
            messagebox.showwarning("Error", "Pedido no encontrado")
            return
        
        # Ventana de detalles
        ventana_detalles = tk.Toplevel(self)
        ventana_detalles.title(f"Detalles del Pedido #{id_pedido}")
        ventana_detalles.geometry("600x500")
        ventana_detalles.configure(bg=COLOR_FONDO)
        
        # Frame principal
        frame_principal = tk.Frame(ventana_detalles, bg=COLOR_FONDO)
        frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        tk.Label(frame_principal, text=f"Detalles del Pedido #{id_pedido}", font=FUENTE_SUBTITULO,
               bg=COLOR_FONDO, fg=COLOR_TEXTO_OSCURO).pack(pady=(0, 10))
        
        # Frame de contenido
        frame_contenido = tk.Frame(frame_principal, bg=COLOR_FONDO)
        frame_contenido.pack(fill="both", expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(frame_contenido)
        scrollbar.pack(side="right", fill="y")
        
        # Texto con los detalles
        text_detalles = tk.Text(frame_contenido, wrap="word", yscrollcommand=scrollbar.set,
                              font=FUENTE_TEXTO, bg=COLOR_FONDO, fg=COLOR_TEXTO_OSCURO,
                              padx=10, pady=10)
        text_detalles.pack(fill="both", expand=True)
        
        text_detalles.insert("end", f"Pedido #{pedido.id[:8]}\n", "titulo")
        text_detalles.insert("end", f"Cliente: {pedido.cliente}\n")
        text_detalles.insert("end", f"Fecha: {pedido.fecha}\n")
        text_detalles.insert("end", f"Estado: {pedido.estado}\n")
        text_detalles.insert("end", f"Total: ${pedido.total:.2f}\n\n")
        text_detalles.insert("end", "Productos:\n", "subtitulo")
        
        for producto in pedido.productos:
            text_detalles.insert("end", f"- {producto}\n")
        
        text_detalles.tag_configure("titulo", font=("Helvetica", 14, "bold"))
        text_detalles.tag_configure("subtitulo", font=("Helvetica", 12, "bold"))
        text_detalles.config(state="disabled")
        scrollbar.config(command=text_detalles.yview)
        
        # Botón cerrar
        tk.Button(frame_principal, text="Cerrar", command=ventana_detalles.destroy,
                bg=COLOR_BOTONES, fg=COLOR_TEXTO, font=FUENTE_BOTONES,
                padx=20, pady=5).pack(pady=(20, 0))
    
    def eliminar_pedido(self):
        seleccion = self.tree_pedidos.selection()
        if not seleccion:
            messagebox.showwarning("Error", "Debe seleccionar un pedido")
            return
        
        item = self.tree_pedidos.item(seleccion)
        id_pedido = item['values'][0]
        
        pedido = next((p for p in self.controller.gestor_datos.pedidos if p.id[:8] == id_pedido), None)
        if not pedido:
            messagebox.showwarning("Error", "Pedido no encontrado")
            return
        
        confirmacion = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro que desea eliminar el pedido #{id_pedido}?"
        )
        
        if confirmacion:
            self.controller.eliminar_pedido(pedido)
            self.actualizar_lista_pedidos()
    
    def crear_pestana_empleados(self, parent):
        # Frame para agregar nuevo empleado
        frame_agregar = tk.Frame(parent)
        frame_agregar.pack(fill="x", padx=10, pady=10)
        
        tk.Label(frame_agregar, text="Nombre:", font=FUENTE_TEXTO).grid(row=0, column=0, padx=5, pady=5)
        self.entry_empleado_nombre = tk.Entry(frame_agregar, font=FUENTE_TEXTO, bd=2, relief=tk.GROOVE)
        self.entry_empleado_nombre.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        tk.Label(frame_agregar, text="Rol:", font=FUENTE_TEXTO).grid(row=0, column=2, padx=5, pady=5)
        self.combo_empleado_rol = ttk.Combobox(frame_agregar, values=["Administrador", "Barista", "Cajero", "Mesero"], 
                                             font=FUENTE_TEXTO)
        self.combo_empleado_rol.current(0)
        self.combo_empleado_rol.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        
        btn_agregar = tk.Button(frame_agregar, text="Agregar Empleado", font=FUENTE_BOTONES,
                              command=self.agregar_empleado,
                              bg=COLOR_BOTONES_ACCION, fg=COLOR_TEXTO,
                              padx=10, pady=5)
        btn_agregar.grid(row=1, column=0, columnspan=4, pady=10, sticky="ew")
        
        # Lista de empleados
        frame_lista = tk.Frame(parent)
        frame_lista.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tree_empleados = ttk.Treeview(frame_lista, columns=("Nombre", "Rol"), show="headings")
        self.tree_empleados.heading("Nombre", text="Nombre")
        self.tree_empleados.heading("Rol", text="Rol")
        
        self.tree_empleados.column("Nombre", width=150)
        self.tree_empleados.column("Rol", width=150)
        
        self.tree_empleados.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(frame_lista, orient="vertical", command=self.tree_empleados.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree_empleados.configure(yscrollcommand=scrollbar.set)
        
        btn_eliminar = tk.Button(parent, text="Eliminar Empleado Seleccionado", font=FUENTE_BOTONES,
                               command=self.eliminar_empleado,
                               bg=COLOR_BOTONES_PELIGRO, fg=COLOR_TEXTO,
                               padx=10, pady=5)
        btn_eliminar.pack(pady=10, fill="x")
        
        self.actualizar_lista_empleados()
    
    def agregar_empleado(self):
        nombre = self.entry_empleado_nombre.get().strip()
        rol = self.combo_empleado_rol.get()
        
        if not nombre or not rol:
            messagebox.showwarning("Error", "Debe ingresar nombre y rol")
            return
        
        self.controller.agregar_empleado(nombre, rol)
        self.actualizar_lista_empleados()
        
        self.entry_empleado_nombre.delete(0, tk.END)
        messagebox.showinfo("Éxito", "Empleado agregado correctamente")
    
    def eliminar_empleado(self):
        seleccion = self.tree_empleados.selection()
        if not seleccion:
            messagebox.showwarning("Error", "Debe seleccionar un empleado")
            return
        
        item = self.tree_empleados.item(seleccion)
        nombre = item['values'][0]
        
        self.controller.eliminar_empleado(nombre)
        self.actualizar_lista_empleados()
        messagebox.showinfo("Éxito", "Empleado eliminado correctamente")
    
    def actualizar_lista_empleados(self):
        for item in self.tree_empleados.get_children():
            self.tree_empleados.delete(item)
        
        for empleado in self.controller.gestor_datos.empleados:
            self.tree_empleados.insert("", "end", values=(empleado.nombre, empleado.rol))
    
    def actualizar(self):
        self.actualizar_lista_bebidas()
        self.actualizar_lista_postres()
        self.actualizar_lista_inventario()
        self.actualizar_lista_pedidos()
        self.actualizar_lista_empleados()

if __name__ == "__main__":
    app = CafeteriaApp()
    app.mainloop()