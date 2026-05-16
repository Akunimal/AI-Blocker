# -*- coding: utf-8 -*-
import os
import sys
import ctypes
import subprocess
import tkinter as tk
from tkinter import messagebox

# =====================================================================
# CONFIGURACIÓN DE DOMINIOS A BLOQUEAR
# =====================================================================
# Lista de dominios asociados a proveedores de IA organizados por categorías.
BLOCKLIST = {
    "OpenAI": [
        "api.openai.com", "chatgpt.com", "chat.openai.com", 
        "platform.openai.com", "openai.com", "auth.openai.com", 
        "oaistatic.com", "oaiusercontent.com"
    ],
    "Anthropic": [
        "api.anthropic.com", "claude.ai", "anthropic.com", 
        "claudeusercontent.com"
    ],
    "GitHub Copilot": [
        "api.githubcopilot.com", "copilot.microsoft.com", 
        "copilot.github.com", "githubcopilot.com", 
        "api.individual.githubcopilot.com"
    ],
    "Google AI": [
        "generativelanguage.googleapis.com", "aistudio.google.com", 
        "gemini.google.com", "ai.google.dev"
    ],
    "Meta AI": [
        "meta.ai", "ai.meta.com"
    ],
    "Mistral AI": [
        "api.mistral.ai", "mistral.ai"
    ],
    "Microsoft Copilot": [
        "copilot.microsoft.com", "bing.com", "edgeservices.bing.com"
    ],
    "Otros": [
        "api.perplexity.ai", "perplexity.ai", "labs.openai.com", 
        "app.wordware.ai", "deepseek.com", "api.deepseek.com"
    ]
}

# Lista de ejecutables de editores de código que integran IA a forzar su cierre.
PROCESS_LIST = [
    "Code.exe", "Cursor.exe", "Windsurf.exe", "Claude.exe", 
    "Trae.exe", "Cline.exe", "Roo.exe", "Augment.exe"
]

# Comentario único para identificar las líneas agregadas por esta aplicación.
COMMENT_TAG = "# AI-Block"

# Ruta dinámica del archivo hosts de Windows
HOSTS_PATH = os.path.join(
    os.environ.get('SystemRoot', 'C:\\Windows'), 
    'System32\\drivers\\etc\\hosts'
)

# =====================================================================
# COMPROBACIONES DE SISTEMA Y UTILIDADES
# =====================================================================
def is_admin():
    """
    Comprueba si el script se está ejecutando con privilegios de administrador.
    Requerido para poder modificar el archivo hosts del sistema.
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def check_block_status():
    """
    Lee el archivo hosts para determinar si el bloqueo está activo actualmente.
    Retorna True si encuentra al menos una línea con la marca de comentario # AI-Block.
    """
    if not os.path.exists(HOSTS_PATH):
        return False
    try:
        with open(HOSTS_PATH, 'r', encoding='utf-8') as file:
            for line in file:
                if COMMENT_TAG in line:
                    return True
    except Exception as e:
        print(f"Error al leer el archivo hosts: {e}")
    return False

# =====================================================================
# ACCIONES DE BLOQUEO Y DESBLOQUEO
# =====================================================================
def force_close_processes():
    """
    Intenta cerrar de forma forzada los procesos en PROCESS_LIST.
    Retorna una lista con los nombres de los procesos que fueron cerrados exitosamente.
    """
    closed_processes = []
    # Ocultar la ventana de consola al invocar taskkill
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE

    for process in PROCESS_LIST:
        try:
            # Ejecuta 'taskkill /F /IM nombre_proceso' de forma silenciosa
            result = subprocess.run(
                ["taskkill", "/F", "/IM", process],
                capture_output=True,
                text=True,
                startupinfo=startupinfo
            )
            # Si el código de salida es 0, significa que se encontró y cerró el proceso
            if result.returncode == 0:
                closed_processes.append(process)
        except Exception as e:
            print(f"Error al intentar cerrar {process}: {e}")
    return closed_processes

def activate_block():
    """
    Aplica el bloqueo de red para las IAs.
    1. Cierra los procesos de editores de IA.
    2. Modifica el archivo hosts agregando las entradas de BLOCKLIST redirigiendo a 127.0.0.1.
    """
    # 1. Cerrar procesos activos
    closed_list = force_close_processes()
    
    # 2. Agregar dominios al archivo hosts
    try:
        # Leer líneas existentes del hosts
        existing_lines = []
        if os.path.exists(HOSTS_PATH):
            with open(HOSTS_PATH, 'r', encoding='utf-8') as file:
                existing_lines = file.readlines()

        # Determinar qué dominios de nuestra blocklist ya están presentes
        # para evitar duplicados
        hosts_content_str = "".join(existing_lines)
        new_entries = []

        for category, domains in BLOCKLIST.items():
            for domain in domains:
                entry = f"127.0.0.1 {domain} {COMMENT_TAG}\n"
                # Solo agregamos si no existe el dominio en el hosts actual
                if domain not in hosts_content_str:
                    new_entries.append(entry)

        # Si hay nuevas entradas, las añadimos
        if new_entries:
            # Aseguramos un salto de línea al final del archivo antes de escribir
            if existing_lines and not existing_lines[-1].endswith('\n'):
                existing_lines[-1] += '\n'
            
            with open(HOSTS_PATH, 'w', encoding='utf-8') as file:
                file.writelines(existing_lines + new_entries)
        
        # Mensaje de éxito informando los procesos cerrados
        if closed_list:
            processes_msg = ", ".join(closed_list)
            info_msg = f"¡Bloqueo activado con éxito!\n\nSe cerraron los siguientes procesos activos:\n{processes_msg}"
        else:
            info_msg = "¡Bloqueo activado con éxito!\n\nNo se detectaron editores de IA abiertos en ejecución."
            
        messagebox.showinfo("Bloqueo de IA Activo", info_msg)
        return True
        
    except PermissionError:
        messagebox.showerror(
            "Error de Permisos", 
            "No se pudo escribir en el archivo hosts.\nPor favor, ejecuta la aplicación como Administrador."
        )
    except Exception as e:
        messagebox.showerror(
            "Error Inesperado", 
            f"Ocurrió un error al intentar aplicar el bloqueo:\n{str(e)}"
        )
    return False

def deactivate_block():
    """
    Desactiva el bloqueo de red para las IAs.
    Elimina del archivo hosts todas las líneas que contengan la marca '# AI-Block'.
    """
    try:
        if not os.path.exists(HOSTS_PATH):
            messagebox.showinfo("Información", "El archivo hosts no existe. El bloqueo ya está inactivo.")
            return True

        # Leer archivo actual
        with open(HOSTS_PATH, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Filtrar conservando únicamente las líneas que NO contienen la etiqueta de bloqueo
        cleaned_lines = [line for line in lines if COMMENT_TAG not in line]

        # Escribir de vuelta al hosts
        with open(HOSTS_PATH, 'w', encoding='utf-8') as file:
            file.writelines(cleaned_lines)

        messagebox.showinfo("Bloqueo Desactivado", "¡El bloqueo de IA ha sido desactivado!\n\nTodos los dominios y herramientas de IA vuelven a estar accesibles.")
        return True

    except PermissionError:
        messagebox.showerror(
            "Error de Permisos", 
            "No se pudo escribir en el archivo hosts.\nPor favor, ejecuta la aplicación como Administrador."
        )
    except Exception as e:
        messagebox.showerror(
            "Error Inesperado", 
            f"Ocurrió un error al desactivar el bloqueo:\n{str(e)}"
        )
    return False

# =====================================================================
# INTERFAZ GRÁFICA (GUI) CON TKINTER
# =====================================================================
class AIBlockerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Network Blocker")
        self.root.geometry("450x320")
        self.root.resizable(False, False)
        
        # Configurar colores generales para lograr una interfaz moderna y premium
        self.root.configure(bg="#1E1E2E")  # Fondo oscuro elegante
        
        # Comprobar el estado inicial del archivo hosts
        self.is_blocked = check_block_status()

        # Frame contenedor principal para centrar el botón y dar espaciado
        self.main_frame = tk.Frame(self.root, bg="#1E1E2E")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Botón Toggle Principal
        self.toggle_btn = tk.Button(
            self.main_frame,
            text="",
            font=("Segoe UI", 16, "bold"),
            bd=0,
            cursor="hand2",
            activeforeground="#FFFFFF",
            relief="flat",
            command=self.handle_toggle
        )
        self.toggle_btn.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Etiqueta de estado en la parte inferior
        self.status_label = tk.Label(
            self.main_frame,
            text="",
            font=("Segoe UI", 9, "italic"),
            bg="#1E1E2E",
            fg="#A5ADCB"
        )
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

        # Actualizar visualizaciones del botón basadas en el estado inicial
        self.update_visuals()

    def handle_toggle(self):
        """
        Manejador del evento de clic del botón. Alterna entre bloquear y desbloquear.
        """
        if self.is_blocked:
            # Si estaba bloqueado, procedemos a desbloquear
            if deactivate_block():
                self.is_blocked = False
                self.update_visuals()
        else:
            # Si estaba desbloqueado, procedemos a bloquear
            if activate_block():
                self.is_blocked = True
                self.update_visuals()

    def update_visuals(self):
        """
        Actualiza el color, el texto y las propiedades del botón e indicador
        basándose en si el bloqueo está activo o inactivo.
        """
        if self.is_blocked:
            # El bloqueo ESTÁ activo -> El botón debe permitir DESBLOQUEAR
            # Color verde premium indicando estado seguro y opción de liberar
            self.toggle_btn.configure(
                text="DESBLOQUEAR IA",
                bg="#10B981",         # Verde esmeralda moderno
                fg="#FFFFFF",
                activebackground="#059669"
            )
            self.status_label.configure(
                text="ESTADO: Bloqueo activo. Editores de IA incomunicados offline."
            )
        else:
            # El bloqueo NO está activo -> El botón debe permitir BLOQUEAR
            # Color rojo/rosa moderno invitando a bloquear
            self.toggle_btn.configure(
                text="BLOQUEAR IA",
                bg="#EF4444",         # Rojo moderno brillante
                fg="#FFFFFF",
                activebackground="#DC2626"
            )
            self.status_label.configure(
                text="ESTADO: Bloqueo inactivo. Tu tráfico de red de IA está expuesto."
            )

# =====================================================================
# PUNTO DE ENTRADA PRINCIPAL
# =====================================================================
if __name__ == "__main__":
    # Comprobar privilegios de administrador antes de lanzar la GUI
    if not is_admin():
        # Crear una ventana raíz oculta temporalmente para mostrar el cuadro de diálogo
        root_temp = tk.Tk()
        root_temp.withdraw()
        messagebox.showerror(
            "Acceso Denegado",
            "Error: Se requieren privilegios de Administrador para ejecutar esta herramienta.\n\n"
            "Por favor, haz clic derecho sobre el ejecutable o script y selecciona 'Ejecutar como administrador'."
        )
        root_temp.destroy()
        sys.exit(1)

    # Iniciar la aplicación
    root = tk.Tk()
    app = AIBlockerApp(root)
    root.mainloop()
