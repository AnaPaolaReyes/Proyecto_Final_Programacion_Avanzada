from datetime import datetime

class Paciente:
    lista_pacientes = []

    def __init__(self, nombre, telefono, edad, sexo, localidad):
        self.nombre = nombre
        self.telefono = telefono
        self.edad = edad
        self.sexo = sexo
        self.localidad = localidad
        Paciente.lista_pacientes.append(self)

    def __str__(self):
        return f"{self.nombre} - Tel: {self.telefono} - Edad: {self.edad} - Sexo: {self.sexo} - Localidad: {self.localidad}"


class Cita:
    lista_citas = []

    def __init__(self, paciente, fecha, hora, motivo):
        self.paciente = paciente
        self.fecha = datetime.strptime(fecha, "%Y-%m-%d").date()
        self.hora = hora  
        self.motivo = motivo
        Cita.lista_citas.append(self)

    def __str__(self):
        return f"Cita - {self.paciente.nombre} el {self.fecha} a las {self.hora}"


class HistoriaClinica:
    lista_historias = []

    def __init__(self, paciente):
        self.paciente = paciente
        self.registros = []  
        HistoriaClinica.lista_historias.append(self)

    def agregar_registro(self, observacion):
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.registros.append((fecha_actual, observacion))

    def __str__(self):
        registros_texto = "\n".join([f"{f} - {o}" for f, o in self.registros])
        return f"Historia clínica de {self.paciente.nombre}:\n{registros_texto}"


class Dentista:
    def __init__(self, nombre, contraseña):
        self.nombre = nombre
        self.__contraseña = contraseña

    def verificar_credenciales(self, nombre, contraseña):
        return self.nombre == nombre and self.__contraseña == contraseña