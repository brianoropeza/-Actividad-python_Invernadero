from modelo.modelo import Invernadero
import datetime

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

    def _procesar_datos_invernadero(self, datos_vista):
        try:
            nombre = datos_vista[0]
            
            try:
                capacidad = int(datos_vista[1])
            except ValueError:
                self.vista.mostrar_error_generico("Error de Datos", f"La capacidad '{datos_vista[1]}' debe ser un número entero.")
                return None

            superficie = float(datos_vista[2]) 
            tipo_cultivo = datos_vista[3]
            fecha_str = datos_vista[4]
            
            try:
                fecha_obj = datetime.datetime.strptime(fecha_str, "%Y-%m-%d").date()
            except ValueError:
                self.vista.mostrar_error_generico("Error de Datos", f"Formato de fecha incorrecto: '{fecha_str}'. Use YYYY-MM-DD.")
                return None
            
            responsable = datos_vista[5]
            sistema_riego = datos_vista[6]

            return Invernadero(nombre, capacidad, superficie, tipo_cultivo, fecha_obj, responsable, sistema_riego)

        except ValueError as e: 
            self.vista.mostrar_error_generico("Error de Datos", f"Error al procesar los datos: {e}. Verifique los números.")
            return None
        except IndexError:
            self.vista.mostrar_error_generico("Error de Datos", "Faltan datos para el invernadero.")
            return None

    def agregar_invernadero(self, datos_vista):
        invernadero_obj = self._procesar_datos_invernadero(datos_vista)
        if invernadero_obj:
            self.modelo.agregar_invernadero(invernadero_obj)
            return True
        return False

    def obtener_invernaderos(self):
        return self.modelo.obtener_invernaderos()

    def modificar_invernadero(self, index, datos_vista):
        invernadero_actualizado_obj = self._procesar_datos_invernadero(datos_vista)
        if invernadero_actualizado_obj:
            if self.modelo.modificar_invernadero(index, invernadero_actualizado_obj):
                return True
            else:
                self.vista.mostrar_error_generico("Error de Modificación", "No se pudo modificar el invernadero en el modelo (ej. índice inválido).")
                return False
        return False

    def eliminar_invernadero(self, index):
        if self.modelo.eliminar_invernadero(index):
            return True
        else:
            self.vista.mostrar_error_generico("Error de Eliminación", "No se pudo eliminar el invernadero del modelo (ej. índice inválido).")
            return False