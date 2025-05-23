import json
import os
from datetime import datetime
from backdentista import Paciente, Cita, HistoriaClinica

PACIENTES_JSON = "pacientes.json"
CITAS_JSON = "citas.json"
HISTORIAS_JSON = "historias.json"

def guardar_pacientes():
    data = []
    for p in Paciente.lista_pacientes:
        data.append({
            "nombre": p.nombre,
            "telefono": p.telefono,
            "edad": p.edad,
            "sexo": p.sexo,
            "localidad": p.localidad
        })
    with open(PACIENTES_JSON, "w") as f:
        json.dump(data, f, indent=4)

def cargar_pacientes():
    Paciente.lista_pacientes.clear()
    if os.path.exists(PACIENTES_JSON):
        with open(PACIENTES_JSON, "r") as f:
            data = json.load(f)
            for d in data:
                Paciente(
                    d["nombre"],
                    d["telefono"],
                    d["edad"],
                    d["sexo"],
                    d["localidad"]
                )

def guardar_citas():
    data = []
    for c in Cita.lista_citas:
        data.append({
            "paciente": c.paciente.nombre,
            "fecha": c.fecha.strftime("%Y-%m-%d"),
            "hora": c.hora,
            "motivo": c.motivo
        })
    with open(CITAS_JSON, "w") as f:
        json.dump(data, f, indent=4)

def cargar_citas():
    Cita.lista_citas.clear()
    if os.path.exists(CITAS_JSON):
        with open(CITAS_JSON, "r") as f:
            data = json.load(f)
            for d in data:
                paciente = next((p for p in Paciente.lista_pacientes if p.nombre == d["paciente"]), None)
                if paciente:
                    Cita(
                        paciente,
                        d["fecha"],
                        d["hora"],
                        d["motivo"]
                    )

def guardar_historias():
    data = []
    for h in HistoriaClinica.lista_historias:
        data.append({
            "paciente": h.paciente.nombre,
            "registros": h.registros
        })
    with open(HISTORIAS_JSON, "w") as f:
        json.dump(data, f, indent=4)

def cargar_historias():
    HistoriaClinica.lista_historias.clear()
    if os.path.exists(HISTORIAS_JSON):
        with open(HISTORIAS_JSON, "r") as f:
            data = json.load(f)
            for d in data:
                paciente = next((p for p in Paciente.lista_pacientes if p.nombre == d["paciente"]), None)
                if paciente:
                    historia = HistoriaClinica(paciente)
                    historia.registros = d["registros"]