from modelo.modelo import Invernadero


class Controlador:
    def __init__(self, modelo, vista):
        self.modelo = modelo
        self.vista = vista
        self.vista.set_controlador(self)

    def login(self, usuario, contrasena):
        if self.modelo.validar_usuario(usuario, contrasena):
            self.vista.mostrar_menu_principal()
        else:
            self.vista.mostrar_error_login()

    def agregar_invernadero(self, datos):
        inv = Invernadero(*datos)
        self.modelo.agregar_invernadero(inv)
        self.vista.actualizar_lista_invernaderos()

    def obtener_invernaderos(self):
        return self.modelo.obtener_invernaderos()

    def modificar_invernadero(self, index, datos):
        nuevo = Invernadero(*datos)
        self.modelo.modificar_invernadero(index, nuevo)
        self.vista.actualizar_lista_invernaderos()

    def eliminar_invernadero(self, index):
        self.modelo.eliminar_invernadero(index)
        self.vista.actualizar_lista_invernaderos()