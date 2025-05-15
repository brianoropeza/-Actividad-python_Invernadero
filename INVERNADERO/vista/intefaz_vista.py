import tkinter as tk
from tkinter import ttk, messagebox

class Vista:
    def __init__(self, root):
        self.root = root
        self.root.title("Onda Vital")
        self.root.geometry("800x600")
        self.root.configure(bg="white")

        self.controlador = None
        self.nombre_usuario_actual = None
        self.marco_login = None
        self.marco_menu = None
        self.marco_formulario = None
        self.item_index = None
        self.selected_item_id = None

        self.crear_interfaz_login()

    def set_controlador(self, controlador):
        self.controlador = controlador

    def crear_interfaz_login(self):
        self.nombre_usuario_actual = None
        if hasattr(self, 'marco_formulario') and self.marco_formulario and self.marco_formulario.winfo_exists():
            self.marco_formulario.destroy()
        self.marco_formulario = None
        
        if self.marco_menu and self.marco_menu.winfo_exists():
            self.marco_menu.destroy()
        self.marco_menu = None

        self.marco_login = tk.Frame(self.root, bg="white")
        self.marco_login.pack(fill='both', expand=True, padx=20, pady=20)

        tk.Label(self.marco_login, text="Iniciar Sesión", font=("Helvetica", 22, "bold"), bg="white", fg="#C5CAE9").pack(pady=(20, 30))

        tk.Label(self.marco_login, text="Usuario:", font=("Helvetica", 12), bg="white", fg="#333").pack(pady=(10,0))
        self.usuario_entry = tk.Entry(self.marco_login, bg="#f0f7da", font=("Helvetica", 12), width=30)
        self.usuario_entry.insert(0, "Admin")
        self.usuario_entry.pack(pady=(5,10), ipady=4)

        tk.Label(self.marco_login, text="Contraseña:", font=("Helvetica", 12), bg="white", fg="#333").pack(pady=(10,0))
        self.contrasena_entry = tk.Entry(self.marco_login, show="●", bg="#f0f7da", font=("Helvetica", 12), width=30)
        self.contrasena_entry.insert(0, "12345678")
        self.contrasena_entry.pack(pady=(5,20), ipady=4)

        tk.Button(self.marco_login, text="Confirmar", bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"), command=self.verificar_login, width=15, height=2, relief=tk.FLAT).pack(pady=20)

    def verificar_login(self):
        usuario = self.usuario_entry.get()
        contrasena = self.contrasena_entry.get()
        if self.controlador:
            self.controlador.login(usuario, contrasena)
        else:
            self.mostrar_error_generico("Error de Configuración", "El controlador no ha sido asignado a la vista.")

    def mostrar_error_login(self):
        messagebox.showerror("Error de Acceso", "Usuario o contraseña incorrectos. Por favor, intente de nuevo.", parent=self.root)

    def mostrar_error_generico(self, titulo, mensaje):
        parent_window = self.root
        if hasattr(self, 'marco_formulario') and self.marco_formulario and self.marco_formulario.winfo_exists():
            parent_window = self.marco_formulario
        elif hasattr(self, 'marco_menu') and self.marco_menu and self.marco_menu.winfo_exists():
             parent_window = self.marco_menu 
        messagebox.showerror(titulo, mensaje, parent=parent_window)

    def cerrar_sesion(self):
        if self.marco_menu and self.marco_menu.winfo_exists():
            self.marco_menu.destroy()
        self.marco_menu = None

        if hasattr(self, 'marco_formulario') and self.marco_formulario and self.marco_formulario.winfo_exists():
            self.marco_formulario.destroy()
        self.marco_formulario = None
        
        self.item_index = None
        self.selected_item_id = None
        self.nombre_usuario_actual = None
        
        self.crear_interfaz_login()

    def mostrar_menu_principal(self, nombre_usuario="Usuario"):
        self.nombre_usuario_actual = nombre_usuario
        if self.marco_login and self.marco_login.winfo_exists():
            self.marco_login.destroy()
            self.marco_login = None

        if self.marco_menu and self.marco_menu.winfo_exists():
            for widget in self.marco_menu.winfo_children(): 
                if isinstance(widget, tk.Frame) and hasattr(widget, "_user_info_frame"):
                    widget.destroy() 
            
            if hasattr(self, 'label_usuario_actual') and self.label_usuario_actual.winfo_exists():
                 self.label_usuario_actual.config(text=f"Usuario: {self.nombre_usuario_actual}")
            self.actualizar_lista_invernaderos()
            return

        self.marco_menu = tk.Frame(self.root, bg="white")
        self.marco_menu.pack(fill='both', expand=True, padx=20, pady=20)

        top_bar_frame = tk.Frame(self.marco_menu, bg="white")
        top_bar_frame.pack(fill='x', pady=(0,10))
        top_bar_frame._user_info_frame = True 

        tk.Label(top_bar_frame, text="Gestión de Invernaderos", font=("Helvetica", 18, "bold"), bg="white", fg="#C5CAE9").pack(side=tk.LEFT, padx=(0,20))

        user_actions_frame = tk.Frame(top_bar_frame, bg="white")
        user_actions_frame.pack(side=tk.RIGHT)

        self.label_usuario_actual = tk.Label(user_actions_frame, text=f"Usuario: {self.nombre_usuario_actual}", font=("Helvetica", 10), bg="white", fg="#333")
        self.label_usuario_actual.pack(side=tk.LEFT, padx=(0,10), pady=5)

        boton_cerrar_sesion = tk.Button(user_actions_frame, text="Cerrar Sesión", bg="#D32F2F", fg="white", font=("Helvetica", 9, "bold"), command=self.cerrar_sesion, relief=tk.FLAT, padx=8, pady=4)
        boton_cerrar_sesion.pack(side=tk.LEFT, padx=(0,10))
        
        boton_agregar = tk.Button(user_actions_frame, text="Registrar Invernadero", bg="#4CAF50", fg="white", font=("Helvetica", 9, "bold"), command=self.mostrar_formulario_nuevo, relief=tk.FLAT, padx=8, pady=4)
        boton_agregar.pack(side=tk.LEFT)


        self.lista_frame = tk.Frame(self.marco_menu, bg="white")
        self.lista_frame.pack(fill='both', expand=True, pady=(10,0))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"), background="#E8F5E9", foreground="#004D40")
        style.configure("Treeview", font=("Helvetica", 9), rowheight=25, fieldbackground="white")
        style.map("Treeview", background=[('selected', '#AED581')])

        self.tree = ttk.Treeview(self.lista_frame, columns=("Nombre", "Capacidad", "Superficie", "Cultivo", "Fecha", "Responsable", "Riego"), show="headings")
        columnas_config = [
            ("Nombre", 120), ("Capacidad", 100), ("Superficie", 80),
            ("Cultivo", 100), ("Fecha", 90), ("Responsable", 120), ("Riego", 90)
        ]
        for col, width in columnas_config:
            self.tree.heading(col, text=col, anchor=tk.W)
            self.tree.column(col, width=width, anchor=tk.W, minwidth=60)
        self.tree.pack(fill="both", expand=True, side=tk.LEFT)

        scrollbar = ttk.Scrollbar(self.lista_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_item)

        botones_acciones_frame = tk.Frame(self.marco_menu, bg="white")
        botones_acciones_frame.pack(fill='x', pady=(15, 0))

        boton_modificar = tk.Button(botones_acciones_frame, text="Modificar Seleccionado", bg="#FFA726", fg="white", font=("Helvetica", 10, "bold"), command=self.mostrar_formulario_modificacion, relief=tk.FLAT, padx=10, pady=5)
        boton_modificar.pack(side=tk.LEFT, padx=(0, 10))

        boton_eliminar = tk.Button(botones_acciones_frame, text="Eliminar Seleccionado", bg="#EF5350", fg="white", font=("Helvetica", 10, "bold"), command=self.eliminar_invernadero, relief=tk.FLAT, padx=10, pady=5)
        boton_eliminar.pack(side=tk.LEFT)

        self.actualizar_lista_invernaderos()

    def mostrar_formulario_nuevo(self):
        self.mostrar_formulario(datos_invernadero=None, index=None)

    def mostrar_formulario(self, datos_invernadero=None, index=None):
        if hasattr(self, 'marco_formulario') and self.marco_formulario and self.marco_formulario.winfo_exists():
            self.marco_formulario.destroy()

        self.marco_formulario = tk.Toplevel(self.root)
        self.marco_formulario.title("Formulario Invernadero")
        self.marco_formulario.geometry("450x480")
        self.marco_formulario.configure(bg="white")
        self.marco_formulario.resizable(False, False)
        self.marco_formulario.transient(self.root)
        self.marco_formulario.grab_set()

        form_frame = tk.Frame(self.marco_formulario, bg="white", padx=20, pady=20)
        form_frame.pack(expand=True, fill="both")

        titulo_formulario = "Registrar Invernadero" if index is None else "Modificar Invernadero"
        tk.Label(form_frame, text=titulo_formulario, font=("Helvetica", 14, "bold"), bg="white", fg="#005A31").grid(row=0, column=0, columnspan=2, pady=(0,20), sticky="ew")

        campos = [
            ("Nombre del invernadero:", "nombre"), ("Capacidad de producción:", "capacidad"),
            ("Superficie (m²):", "superficie"), ("Tipo de cultivo:", "cultivo"),
            ("Fecha de creación (YYYY-MM-DD):", "fecha"), ("Responsable del invernadero:", "responsable")
        ]
        self.entradas = {}
        for i, (texto, clave) in enumerate(campos):
            tk.Label(form_frame, text=texto, font=("Helvetica", 10), bg="white", fg="#333").grid(row=i+1, column=0, sticky="w", padx=5, pady=8)
            entrada = tk.Entry(form_frame, bg="#f0f7da", font=("Helvetica", 10), width=30)
            entrada.grid(row=i+1, column=1, padx=5, pady=8, ipady=3)
            if datos_invernadero and len(datos_invernadero) > i:
                entrada.insert(0, datos_invernadero[i])
            self.entradas[clave] = entrada

        tk.Label(form_frame, text="Sistema de riego:", font=("Helvetica", 10), bg="white", fg="#333").grid(row=len(campos)+1, column=0, sticky="w", padx=5, pady=8)
        riego_inicial = datos_invernadero[6] if datos_invernadero and len(datos_invernadero) > 6 else "Manual"
        self.sistema_riego_var = tk.StringVar(value=riego_inicial)
        opciones_riego = ["Manual", "Automatizado", "Por goteo", "Aspersión", "Hidropónico"]
        riego_menu = ttk.Combobox(form_frame, textvariable=self.sistema_riego_var, values=opciones_riego, state="readonly", font=("Helvetica", 10), width=28)
        riego_menu.grid(row=len(campos)+1, column=1, padx=5, pady=8, ipady=1)

        form_botones_frame = tk.Frame(form_frame, bg="white")
        form_botones_frame.grid(row=len(campos)+2, column=0, columnspan=2, pady=(25,0))

        if index is not None:
            comando_principal = lambda: self.guardar_modificacion(index)
            texto_boton_principal = "Modificar"
            color_boton_principal = "#FFA726"
        else:
            comando_principal = self.enviar_datos
            texto_boton_principal = "Guardar"
            color_boton_principal = "#4CAF50"

        tk.Button(form_botones_frame, text=texto_boton_principal, bg=color_boton_principal, fg="white", font=("Helvetica", 10, "bold"), command=comando_principal, relief=tk.FLAT, padx=10, pady=5).pack(side=tk.LEFT, padx=10)
        tk.Button(form_botones_frame, text="Cancelar", bg="#757575", fg="white", font=("Helvetica", 10, "bold"), command=self.marco_formulario.destroy, relief=tk.FLAT, padx=10, pady=5).pack(side=tk.LEFT, padx=10)

    def _validar_campos(self):
        campos_info = {
            "nombre": "Nombre del invernadero", "capacidad": "Capacidad de producción",
            "superficie": "Superficie", "cultivo": "Tipo de cultivo",
            "fecha": "Fecha de creación", "responsable": "Responsable"
        }
        parent_win = self.marco_formulario if hasattr(self, 'marco_formulario') and self.marco_formulario and self.marco_formulario.winfo_exists() else self.root
        for clave, nombre_amigable in campos_info.items():
            if not self.entradas[clave].get().strip():
                messagebox.showwarning("Campo Vacío", f"El campo '{nombre_amigable}' no puede estar vacío.", parent=parent_win)
                self.entradas[clave].focus_set()
                return False
        return True

    def enviar_datos(self):
        if not self._validar_campos():
            return
        
        try:
            datos = [
                self.entradas["nombre"].get(), self.entradas["capacidad"].get(),
                self.entradas["superficie"].get(), self.entradas["cultivo"].get(),
                self.entradas["fecha"].get(), self.entradas["responsable"].get(),
                self.sistema_riego_var.get()
            ]
            if self.controlador:
                if self.controlador.agregar_invernadero(datos):
                    if hasattr(self, 'marco_formulario') and self.marco_formulario.winfo_exists():
                        self.marco_formulario.destroy()
                    self.actualizar_lista_invernaderos()
                    messagebox.showinfo("Éxito", "Invernadero registrado correctamente.", parent=self.root)
            else:
                self.mostrar_error_generico("Error de Configuración", "El controlador no ha sido asignado.")
        
        except Exception as e:
            self.mostrar_error_generico("Error al Guardar", f"Ocurrió un error inesperado: {e}")

    def actualizar_lista_invernaderos(self):
        if not hasattr(self, 'tree') or not self.tree or not self.tree.winfo_exists():
            return
        for row in self.tree.get_children():
            self.tree.delete(row)

        if self.controlador:
            invernaderos = self.controlador.obtener_invernaderos()
            if invernaderos:
                for inv_obj in invernaderos:
                    if inv_obj:
                        values = (
                            getattr(inv_obj, 'nombre', ''),
                            getattr(inv_obj, 'capacidad', ''),
                            getattr(inv_obj, 'superficie', ''),
                            getattr(inv_obj, 'tipo_cultivo', ''),
                            getattr(inv_obj, 'fecha_creacion', ''),
                            getattr(inv_obj, 'responsable', ''),
                            getattr(inv_obj, 'sistema_riego', '')
                        )
                        self.tree.insert("", "end", values=values)
        self.item_index = None
        self.selected_item_id = None

    def seleccionar_item(self, event):
        selected_items = self.tree.selection()
        if selected_items:
            self.selected_item_id = selected_items[0]
            self.item_index = self.tree.index(self.selected_item_id)
        else:
            self.selected_item_id = None
            self.item_index = None

    def mostrar_formulario_modificacion(self):
        if self.item_index is None or self.selected_item_id is None:
            messagebox.showinfo("Información", "Por favor, seleccione un invernadero de la lista para modificar.", parent=self.root)
            return

        if self.controlador:
            invernaderos = self.controlador.obtener_invernaderos()
            if 0 <= self.item_index < len(invernaderos):
                inv_obj = invernaderos[self.item_index]
                if inv_obj:
                    datos_invernadero_lista = [
                        str(getattr(inv_obj, 'nombre', '')),
                        str(getattr(inv_obj, 'capacidad', '')),
                        str(getattr(inv_obj, 'superficie', '')),
                        str(getattr(inv_obj, 'tipo_cultivo', '')),
                        str(getattr(inv_obj, 'fecha_creacion', '')),
                        str(getattr(inv_obj, 'responsable', '')),
                        str(getattr(inv_obj, 'sistema_riego', ''))
                    ]
                    self.mostrar_formulario(datos_invernadero_lista, self.item_index)
                else:
                    self.mostrar_error_generico("Error", "El objeto invernadero seleccionado es inválido (None).")
                    self.actualizar_lista_invernaderos()
            else:
                self.mostrar_error_generico("Error", "El invernadero seleccionado ya no es válido o el índice es incorrecto.")
                self.actualizar_lista_invernaderos()
        else:
            self.mostrar_error_generico("Error de Configuración", "El controlador no ha sido asignado.")

    def guardar_modificacion(self, index):
        if not self._validar_campos():
            return
        
        try:
            datos_modificados = [
                self.entradas["nombre"].get(), self.entradas["capacidad"].get(),
                self.entradas["superficie"].get(), self.entradas["cultivo"].get(),
                self.entradas["fecha"].get(), self.entradas["responsable"].get(),
                self.sistema_riego_var.get()
            ]
            if self.controlador:
                if self.controlador.modificar_invernadero(index, datos_modificados):
                    if hasattr(self, 'marco_formulario') and self.marco_formulario.winfo_exists():
                        self.marco_formulario.destroy()
                    self.actualizar_lista_invernaderos()
                    messagebox.showinfo("Éxito", "Invernadero modificado correctamente.", parent=self.root)
            else:
                self.mostrar_error_generico("Error de Configuración", "El controlador no ha sido asignado.")
        
        except Exception as e:
            self.mostrar_error_generico("Error al Modificar", f"Ocurrió un error inesperado: {e}")

    def eliminar_invernadero(self):
        if self.item_index is None or self.selected_item_id is None:
            messagebox.showinfo("Información", "Por favor, seleccione un invernadero de la lista para eliminar.", parent=self.root)
            return

        confirmar = messagebox.askyesno("Confirmar Eliminación", "¿Está seguro de que desea eliminar este invernadero de la lista?", parent=self.root)
        if confirmar:
            if self.controlador:
                if self.controlador.eliminar_invernadero(self.item_index):
                    self.actualizar_lista_invernaderos()
                    messagebox.showinfo("Éxito", "Invernadero eliminado correctamente.", parent=self.root)
            else:
                self.mostrar_error_generico("Error de Configuración", "El controlador no ha sido asignado.")