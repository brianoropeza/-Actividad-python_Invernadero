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
        ejemplo = Invernadero(
            "Invernadero A", 1000, 500.0, "Hortalizas",
            datetime.date(2023, 5, 10), "Juan Pérez", "Goteo"
        )
        self.agregar_invernadero(ejemplo)

    def agregar_invernadero(self, inv):
        self.invernaderos.append(inv)

    def obtener_invernaderos(self):
        return self.invernaderos

    def validar_usuario(self, usuario, contrasena):
        return self.usuarios.get(usuario) == contrasena