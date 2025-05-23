import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from backdentista import Dentista, Paciente, Cita, HistoriaClinica
from backconguardadodentista import (
    cargar_pacientes, cargar_citas, cargar_historias,
    guardar_pacientes, guardar_citas, guardar_historias
)

# Dentista fijo
dentista = Dentista("dentista", "1234")
IMAGEN_FONDO = "C://Users//ana_p//OneDrive//Escritorio//proyecto programacion//pagina principal.jpg"

def fondo_ventana(ventana, ancho, alto):
    imagen = Image.open(IMAGEN_FONDO)
    imagen = imagen.resize((ancho, alto))
    fondo = ImageTk.PhotoImage(imagen)
    canvas = tk.Canvas(ventana, width=ancho, height=alto)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, anchor="nw", image=fondo)
    canvas.image = fondo
    return canvas

def ventana_login():
    cargar_pacientes()
    cargar_citas()
    cargar_historias()

    root = tk.Tk()
    root.title("Consultorio Dental - Login")
    root.geometry("600x400")
    canvas = fondo_ventana(root, 600, 400)

    texto = tk.Label(root, text="Bienvenido Dentista\nIngrese la contraseña para que podamos empezar a trabajar",
                     font=("Arial", 14, "bold"), bg="#ffdce8")
    canvas.create_window(300, 80, window=texto)

    entry_password = tk.Entry(root, show="*", font=("Arial", 12))
    canvas.create_window(300, 150, window=entry_password)

    def iniciar_sesion():
        password = entry_password.get()
        if dentista.verificar_credenciales("dentista", password):
            messagebox.showinfo("Acceso permitido", "¡Bienvenido al sistema!")
            root.destroy()
            ventana_principal()
        else:
            messagebox.showerror("Error", "Contraseña incorrecta")

    btn_login = tk.Button(root, text="Iniciar sesión", command=iniciar_sesion, font=("Arial", 12, "bold"))
    canvas.create_window(300, 200, window=btn_login)
    root.mainloop()

def ventana_principal():
    ventana = tk.Tk()
    ventana.title("Consultorio Dental - Panel")
    ventana.geometry("600x400")
    canvas = fondo_ventana(ventana, 600, 400)

    titulo = tk.Label(ventana, text="Panel del Dentista", font=("Arial", 16, "bold"), bg="#ffdce8")
    canvas.create_window(300, 60, window=titulo)

    b1 = tk.Button(ventana, text="Agendar Cita", font=("Arial", 12), width=20, command=ventana_agendar)
    b2 = tk.Button(ventana, text="Historias Clínicas", font=("Arial", 12), width=20, command=ventana_historial)

    canvas.create_window(300, 150, window=b1)
    canvas.create_window(300, 200, window=b2)
    ventana.mainloop()

def ventana_agendar():
    ventana = tk.Toplevel()
    ventana.title("Agendar Cita")
    ventana.geometry("500x500")
    canvas = fondo_ventana(ventana, 500, 500)

    y = 60
    campos = {}

    for etiqueta in ["Nombre", "Edad", "Motivo", "Hora", "Tel"]:
        lbl = tk.Label(ventana, text=f"{etiqueta}:", bg="#ffdce8")
        entry = tk.Entry(ventana)
        canvas.create_window(120, y, window=lbl)
        canvas.create_window(300, y, window=entry)
        campos[etiqueta.lower()] = entry
        y += 40

    lbl_fecha = tk.Label(ventana, text="Fecha:", bg="#ffdce8")
    calendario = DateEntry(ventana, width=12, background="#ffdce8", foreground="white")
    canvas.create_window(120, y, window=lbl_fecha)
    canvas.create_window(300, y, window=calendario)

    def confirmar():
        nombre = campos["nombre"].get()
        edad = campos["edad"].get()
        motivo = campos["motivo"].get()
        hora = campos["hora"].get()
        fecha = calendario.get_date().strftime("%Y-%m-%d")

        if not all([nombre, edad, motivo, hora]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        paciente = next((p for p in Paciente.lista_pacientes if p.nombre == nombre), None)
        if not paciente:
            paciente = Paciente(nombre, "Desconocido", edad, "Desconocido", "Desconocida")

        Cita(len(Cita.lista_citas) + 1, paciente, fecha, hora, motivo)
        guardar_pacientes()
        guardar_citas()
        messagebox.showinfo("Éxito", f"Cita agendada para {nombre}")
        ventana.destroy()

    canvas.create_window(250, y + 60, window=tk.Button(ventana, text="Confirmar Cita", command=confirmar))

def ventana_historial():
    ventana = tk.Toplevel()
    ventana.title("Historias Clínicas")
    ventana.geometry("600x600")
    canvas = fondo_ventana(ventana, 600, 600)

    tk.Label(ventana, text="Seleccione paciente:", bg="#ffdce8").place(x=50, y=30)
    seleccion = tk.StringVar()
    opciones = tk.OptionMenu(ventana, seleccion, *[p.nombre for p in Paciente.lista_pacientes])
    opciones.place(x=200, y=25)

    def mostrar():
        nombre = seleccion.get()
        if not nombre:
            return

        paciente = next((p for p in Paciente.lista_pacientes if p.nombre == nombre), None)
        historia = next((h for h in HistoriaClinica.lista_historias if h.paciente == paciente), None)
        if not historia:
            historia = HistoriaClinica(paciente)

        frame = tk.Frame(ventana, bg="#ffdce8")
        frame.place(x=50, y=80)

        tk.Label(frame, text=f"Nombre: {paciente.nombre}", bg="#ffdce8").pack()
        tk.Label(frame, text="Sexo:").pack()
        entry_sexo = tk.Entry(frame)
        entry_sexo.insert(0, paciente.sexo)
        entry_sexo.pack()

        tk.Label(frame, text="Localidad:").pack()
        entry_localidad = tk.Entry(frame)
        entry_localidad.insert(0, paciente.localidad)
        entry_localidad.pack()

        tk.Label(frame, text="Nueva Observación:").pack()
        entry_obs = tk.Entry(frame, width=40)
        entry_obs.pack()

        tk.Label(frame, text=f"Visitas registradas: {len(historia.registros)}", bg="#ffdce8").pack()

        def guardar():
            paciente.sexo = entry_sexo.get()
            paciente.localidad = entry_localidad.get()
            obs = entry_obs.get()
            if obs:
                historia.agregar_registro(obs)
            guardar_pacientes()
            guardar_historias()
            messagebox.showinfo("Guardado", "Información actualizada.")

        tk.Button(frame, text="Guardar Cambios", command=guardar).pack(pady=5)

        tk.Label(frame, text="Historial:", bg="#ffdce8").pack()
        for fecha, obs in historia.registros:
            tk.Label(frame, text=f"{fecha} - {obs}", bg="#ffdce8").pack()

    tk.Button(ventana, text="Ver Historia", command=mostrar).place(x=400, y=25)

ventana_login()
