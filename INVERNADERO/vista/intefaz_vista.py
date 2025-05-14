import tkinter as tk
from tkinter import ttk, messagebox

class Vista:
    def __init__(self, root):
        self.root = root
        self.root.title("Vivero vital")
        self.root.geometry("800x500")
        self.root.configure(bg="white")

        self.controlador = None
        self.marco_login = None
        self.marco_menu = None
        self.marco_formulario = None

        self.crear_interfaz_login()

    def set_controlador(self, controlador):
        self.controlador = controlador

    def crear_interfaz_login(self):
        self.marco_login = tk.Frame(self.root, bg="white")
        self.marco_login.pack(fill='both', expand=True)

        tk.Label(self.marco_login, text="Iniciar Sesión", font=("Helvetica", 18), bg="#FFFACD", fg="#FFA500", width=20).pack(pady=40)

        self.usuario_entry = tk.Entry(self.marco_login, bg="#f0f7da")
        self.usuario_entry.insert(0, "Admin")
        self.usuario_entry.pack(pady=5)

        self.contrasena_entry = tk.Entry(self.marco_login, show="●", bg="#f0f7da")
        self.contrasena_entry.insert(0, "12345678")
        self.contrasena_entry.pack(pady=5)

        tk.Button(self.marco_login, text="Confirmar", bg="#4CAF50", fg="white", command=self.verificar_login).pack(pady=10)

    def verificar_login(self):
        usuario = self.usuario_entry.get()
        contrasena = self.contrasena_entry.get()
        self.controlador.login(usuario, contrasena)

    def mostrar_error_login(self):
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def mostrar_menu_principal(self):
        if self.marco_login:
            self.marco_login.destroy()

        self.marco_menu = tk.Frame(self.root, bg="white")
        self.marco_menu.pack(fill='both', expand=True)

        boton_agregar = tk.Button(self.marco_menu, text="Registrar invernadero", bg="#4CAF50", fg="white", command=self.mostrar_formulario)
        boton_agregar.pack(pady=10)

        self.lista_frame = tk.Frame(self.marco_menu, bg="white")
        self.lista_frame.pack(fill='both', expand=True)

        self.tree = ttk.Treeview(self.lista_frame, columns=("Nombre", "Capacidad", "Superficie", "Cultivo", "Fecha", "Responsable", "Riego"), show="headings")
        columnas = ["Nombre", "Capacidad", "Superficie", "Cultivo", "Fecha", "Responsable", "Riego"]
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(fill="both", expand=True)

        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_item)

        boton_modificar = tk.Button(self.marco_menu, text="Modificar seleccionado", bg="orange", fg="white", command=self.mostrar_formulario_modificacion)
        boton_modificar.pack(pady=5)

        boton_eliminar = tk.Button(self.marco_menu, text="Eliminar seleccionado", bg="red", fg="white", command=self.eliminar_invernadero)
        boton_eliminar.pack(pady=5)

        self.actualizar_lista_invernaderos()

    def mostrar_formulario(self, datos=None, index=None):
        if self.marco_formulario:
            self.marco_formulario.destroy()

        self.marco_formulario = tk.Toplevel(self.root)
        self.marco_formulario.title("Formulario Invernadero")
        self.marco_formulario.configure(bg="white")

        campos = [
            ("Nombre del invernadero", "nombre"),
            ("Capacidad de producción", "capacidad"),
            ("Superficie (m²)", "superficie"),
            ("Tipo de cultivo", "cultivo"),
            ("Fecha de creación (YYYY-MM-DD)", "fecha"),
            ("Responsable del invernadero", "responsable")
        ]

        self.entradas = {}
        for i, (texto, clave) in enumerate(campos):
            tk.Label(self.marco_formulario, text=texto, bg="white").grid(row=i, column=0, sticky="e", padx=10, pady=5)
            entrada = tk.Entry(self.marco_formulario, bg="#f0f7da")
            entrada.grid(row=i, column=1, padx=10, pady=5)
            if datos:
                entrada.insert(0, datos[i])
            self.entradas[clave] = entrada

        tk.Label(self.marco_formulario, text="Sistema de riego", bg="white").grid(row=len(campos), column=0, sticky="e", padx=10, pady=5)
        self.sistema_riego_var = tk.StringVar(value=datos[6] if datos else "Manual")
        opciones = ["Manual", "Automatizado", "Por goteo"]
        riego_menu = ttk.Combobox(self.marco_formulario, textvariable=self.sistema_riego_var, values=opciones, state="readonly")
        riego_menu.grid(row=len(campos), column=1, padx=10, pady=5)

        if index is not None:
            comando = lambda: self.guardar_modificacion(index)
            texto_boton = "Modificar"
        else:
            comando = self.enviar_datos
            texto_boton = "Guardar"

        tk.Button(self.marco_formulario, text=texto_boton, bg="green", fg="white", command=comando).grid(row=7, column=0, pady=15)
        tk.Button(self.marco_formulario, text="Cancelar", bg="red", fg="white", command=self.marco_formulario.destroy).grid(row=7, column=1, pady=15)

    def enviar_datos(self):
        try:
            datos = [
                self.entradas["nombre"].get(),
                self.entradas["capacidad"].get(),
                self.entradas["superficie"].get(),
                self.entradas["cultivo"].get(),
                self.entradas["fecha"].get(),
                self.entradas["responsable"].get(),
                self.sistema_riego_var.get()
            ]
            self.controlador.agregar_invernadero(datos)
            self.marco_formulario.destroy()
            self.actualizar_lista_invernaderos()
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {e}")

    def actualizar_lista_invernaderos(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        invernaderos = self.controlador.obtener_invernaderos()
        for inv in invernaderos:
            self.tree.insert("", "end", values=(inv.nombre, inv.capacidad, inv.superficie, inv.tipo_cultivo, inv.fecha_creacion, inv.responsable, inv.sistema_riego))

    def seleccionar_item(self, event):
        selected = self.tree.selection()
        if selected:
            self.item_index = self.tree.index(selected[0])
        else:
            self.item_index = None

    def mostrar_formulario_modificacion(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Info", "Seleccione un invernadero para modificar.")
            return

        index = self.tree.index(selected[0])
        inv = self.controlador.obtener_invernaderos()[index]
        datos = [inv.nombre, inv.capacidad, inv.superficie, inv.tipo_cultivo, inv.fecha_creacion, inv.responsable, inv.sistema_riego]
        self.mostrar_formulario(datos, index)

    def guardar_modificacion(self, index):
        datos = [
            self.entradas["nombre"].get(),
            self.entradas["capacidad"].get(),
            self.entradas["superficie"].get(),
            self.entradas["cultivo"].get(),
            self.entradas["fecha"].get(),
            self.entradas["responsable"].get(),
            self.sistema_riego_var.get()
        ]
        self.controlador.modificar_invernadero(index, datos)
        self.marco_formulario.destroy()
        self.actualizar_lista_invernaderos()

    def eliminar_invernadero(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Info", "Seleccione un invernadero para eliminar.")
            return

        index = self.tree.index(selected[0])
        confirmar = messagebox.askyesno("Confirmar", "¿Desea eliminar este invernadero?")
        if confirmar:
            self.controlador.eliminar_invernadero(index)
            self.actualizar_lista_invernaderos()