import datetime

class Invernadero:
    def __init__(self, nombre, capacidad, superficie, tipo_cultivo, fecha_creacion, responsable, sistema_riego):
        self.nombre = nombre
        self.capacidad = capacidad
        self.superficie = superficie
        self.tipo_cultivo = tipo_cultivo
        self.fecha_creacion = fecha_creacion
        self.responsable = responsable
        self.sistema_riego = sistema_riego

class Modelo:
    def __init__(self):
        self.invernaderos = []
        self.usuarios = {'Admin': '12345678'}
        self._datos_ejemplo()

    def _datos_ejemplo(self):
        ejemplo_nuevo = Invernadero(
            "El Sol Radiante", 
            2500, 
            850.75, 
            "Tomates Cherry",
            datetime.date(2022, 11, 15), 
            "Luisa Fernanda Gómez",      
            "Hidropónico"                
        )
        self.agregar_invernadero(ejemplo_nuevo) 


    def agregar_invernadero(self, invernadero_obj): 
        self.invernaderos.append(invernadero_obj)

    def obtener_invernaderos(self):
        return self.invernaderos

    def validar_usuario(self, usuario, contrasena):
        return self.usuarios.get(usuario) == contrasena

   
    def modificar_invernadero(self, index, invernadero_actualizado_obj):
        if 0 <= index < len(self.invernaderos):
            self.invernaderos[index] = invernadero_actualizado_obj
            return True
        else:
           
            return False

    def eliminar_invernadero(self, index):
        if 0 <= index < len(self.invernaderos):
            self.invernaderos.pop(index)
            return True
        else:
           
            return False