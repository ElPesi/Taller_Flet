import flet as ft                      # Importa Flet, el framework de UI en Python usado para construir la app.
import mysql.connector                 # Importa el conector oficial de MySQL para Python.

# Importaciones de las "pantallas" (clases) que implementan cada módulo/CRUD.
# Estas clases reciben la Page de Flet y un callback para volver al menú principal.
from usuario import Herramienta_Usuario           # Pantalla de login/usuarios.
from cliente import Herramienta_Cliente           # Gestión de clientes.
from repuestos import Herramienta_Repuesto        # Gestión de repuestos.
from empleado import Herramienta_Empleado         # Gestión de empleados.
from proveedor import Herramienta_Proveedor       # Gestión de proveedores.
from ficha_tecnica import Herramienta_FichaTecnica# Gestión de fichas técnicas.
from presupuesto import Herramienta_Presupuesto   # Gestión de presupuestos.


def connect_to_db():
    """
    Abre una conexión a la base de datos MySQL y la devuelve.
    ¿Por qué aquí? Centraliza la configuración y permite verificar
    que el servidor/credenciales estén bien desde el arranque.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",         # Host del servidor MySQL.
            port=3306,                # Puerto por defecto de MySQL.
            user="root",              # Usuario de la BD.
            password="root",          # Contraseña del usuario.
            database="Taller_Mecanico", # Base de datos que usa la app.
            ssl_disabled=True         # Desactiva SSL (útil en entornos locales).
        )
        if connection.is_connected(): # Verificación de que realmente se conectó.
            print("Conexión exitosa")
            return connection         # Se retorna la conexión activa.
    except Exception as ex:
        # Cualquier problema (credenciales, servidor caído, etc.) cae acá.
        print("Conexión errónea")
        print(ex)
        return None                   # Devolvemos None para que el resto pueda manejarlo.


connection = connect_to_db()          # Ejecuta la conexión al iniciar el módulo. Útil para validar entorno.  :contentReference[oaicite:2]{index=2}


# ---------------------------
# Funciones de navegación
# ---------------------------
# Cada función solo instancia la herramienta correspondiente,
# pasándole la "page" actual y el callback "menu_principal" para volver atrás.
# Se usan como handlers de botones/menús (on_click).
def cliente(e, page: ft.Page):
    Herramienta_Cliente(page, menu_principal)     # Abre la pantalla de Clientes.  :contentReference[oaicite:3]{index=3}

def mostrar_cliente(e, page: ft.Page):
    Herramienta_Cliente(page, menu_principal)     # Alias usado por botones principales.  :contentReference[oaicite:4]{index=4}

def repuesto(e, page: ft.Page):
    Herramienta_Repuesto(page, menu_principal)    # Abre Repuestos.  :contentReference[oaicite:5]{index=5}

def mostrar_repuesto(e, page: ft.Page):
    Herramienta_Repuesto(page, menu_principal)    # Alias para botón principal.  :contentReference[oaicite:6]{index=6}

def proveedor(e, page: ft.Page):
    Herramienta_Proveedor(page, menu_principal)   # Abre Proveedores.  :contentReference[oaicite:7]{index=7}

def producto(e, page: ft.Page):
    pass                                          # Placeholder (no implementado).  :contentReference[oaicite:8]{index=8}

def empleado(e, page: ft.Page):
    Herramienta_Empleado(page, menu_principal)    # Abre Empleados.  :contentReference[oaicite:9]{index=9}

def usuario(e, page: ft.Page):
    Herramienta_Usuario(page, menu_principal)     # Abre Login/Usuarios.  :contentReference[oaicite:10]{index=10}

def ficha_tecnica(e, page: ft.Page):
    Herramienta_FichaTecnica(page, menu_principal)# Abre Fichas Técnicas.  :contentReference[oaicite:11]{index=11}

def presupuesto(e, page: ft.Page):
    Herramienta_Presupuesto(page, menu_principal) # Abre Presupuestos.  :contentReference[oaicite:12]{index=12}


# ---------------------------
# Menú principal (UI raíz)
# ---------------------------
def menu_principal(page: ft.Page):
    page.clean()                         # Limpia la vista actual antes de pintar el menú.
    page.window.maximized = True         # Maximiza la ventana (mejor uso del espacio en escritorio).
    page.title = "Administración de Taller Mecánico"  # Título de la ventana.

    # --- Ítems visuales reutilizables para los menús (con icono + texto) ---
    # Se usan dentro de PopupMenuItem para dar contexto visual a cada opción.
    cliente_icono = ft.Icon(ft.Icons.PERSON, size=28) # Icono de "Cliente".
    cliente_item = ft.Row(                           # Fila con icono + etiqueta "Cliente".
        controls=[cliente_icono, ft.Text("Cliente")],
        alignment=ft.MainAxisAlignment.START,        # Alinea a la izquierda dentro del menú.
        spacing=8,                                   # Espacio entre icono y texto.
    )

    proveedor_icono = ft.Icon(ft.Icons.BUSINESS, size=28) # Icono de "Proveedor".
    proveedor_item = ft.Row(
        controls=[proveedor_icono, ft.Text("Proveedor")],
        alignment=ft.MainAxisAlignment.START,
        spacing=8,
    )

    repuesto_icono = ft.Icon(ft.Icons.BUILD, size=28)     # Icono de "Repuesto".
    repuesto_item = ft.Row(
        controls=[repuesto_icono, ft.Text("Repuesto")],
        alignment=ft.MainAxisAlignment.START,
        spacing=8,
    )

    empleado_icono = ft.Icon(ft.Icons.PEOPLE, size=28)    # Icono de "Empleado".
    empleado_item = ft.Row(
        controls=[empleado_icono, ft.Text("Empleado")],
        alignment=ft.MainAxisAlignment.START,
        spacing=8,
    )

    usuario_icono = ft.Icon(ft.Icons.PERSON_OUTLINE, size=28) # Icono de "Usuario".
    usuario_item = ft.Row(
        controls=[usuario_icono, ft.Text("Usuario")],
        alignment=ft.MainAxisAlignment.START,
        spacing=8,
    )

    ficha_tecnica_icono = ft.Icon(ft.Icons.DIRECTIONS_CAR, size=28) # Icono de "Ficha Técnica".
    ficha_tecnica_item = ft.Row(
        controls=[ficha_tecnica_icono, ft.Text("Ficha Técnica")],
        alignment=ft.MainAxisAlignment.START,
        spacing=8,
    )

    presupuesto_icono = ft.Icon(ft.Icons.ATTACH_MONEY, size=28)    # Icono de "Presupuesto".
    presupuesto_icono_item = ft.Row(
        controls=[presupuesto_icono, ft.Text("Presupuesto")]
    )

    # --- Menú "Archivo": ejemplo de menú superior con acciones globales ---
    archivo_menu = ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(text="Copiar", icon=ft.Icons.COPY, tooltip="Copiar"), # Placeholder.
            ft.PopupMenuItem(text="Salir", icon=ft.Icons.EXIT_TO_APP, tooltip="Salir"), # Placeholder.
        ],
        content=ft.Text("Archivo"),         # Etiqueta visible del botón del menú.
        tooltip="Archivo",                  # Tooltip al pasar el mouse.
    )

    # --- Menú "Herramientas": entrada a las tablas maestras ---
    herramientas_menu = ft.PopupMenuButton(
        items=[
            # Cada ítem llama a su función de navegación correspondiente.
            ft.PopupMenuItem(content=cliente_item, on_click=lambda e: cliente(e, page)),
            ft.PopupMenuItem(content=proveedor_item, on_click=lambda e: proveedor(e, page)),
            ft.PopupMenuItem(content=repuesto_item, on_click=lambda e: repuesto(e, page)),
            ft.PopupMenuItem(content=empleado_item, on_click=lambda e: empleado(e, page)),
            ft.PopupMenuItem(content=usuario_item, on_click=lambda e: usuario(e, page)),
        ],
        content=ft.Text("Herramientas"),
        tooltip="Administrador de archivos maestros",   # Describe el propósito del menú.
    )

    # --- Menú "Administración": flujos operativos (ficha técnica y presupuesto) ---
    administracion = ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(
                content=ficha_tecnica_item,
                on_click=lambda e: ficha_tecnica(e, page)    # Abre ficha técnica.
            ),
            ft.PopupMenuItem(
                content=presupuesto_icono_item,
                on_click=lambda e: presupuesto(e, page)       # Abre presupuestos.
            ),
        ],
        content=ft.Text("Administración"),
        tooltip="Administración de presupuesto y ficha técnica",
    )

    # --- Botones "grandes" al centro: accesos directos frecuentes ---
    # ¿Por qué también estos accesos si ya están en los menús?
    # Porque mejoran la usabilidad para tareas comunes (menos clics).
    boton_cliente = ft.IconButton(
        icon=ft.Icons.PERSON,
        tooltip="Cliente",
        on_click=lambda e: mostrar_cliente(e, page),   # Reutiliza la misma navegación.
    )

    boton_usuario = ft.IconButton(
        icon=ft.Icons.PERSON_OUTLINE,
        tooltip="Usuario",
        on_click=lambda e: usuario(e, page),
    )

    boton_repuestos = ft.IconButton(
        icon=ft.Icons.BUILD,
        tooltip="Repuesto",
        on_click=lambda e: mostrar_repuesto(e, page),
    )

    boton_ficha_tecnica = ft.IconButton(
        icon=ft.Icons.DIRECTIONS_CAR,
        tooltip="Ficha Técnica",
        on_click=lambda e: ficha_tecnica(e, page),
    )

    boton_presupuesto = ft.IconButton(
        icon=ft.Icons.ATTACH_MONEY,
        tooltip="Presupuesto",
        on_click=lambda e: presupuesto(e, page),
    )

    # --- Composición final del layout del menú principal ---
    # Primera fila: los menús desplegables (archivo / administración / herramientas).
    # Segunda fila: los accesos directos con iconos grandes.
    page.add(
        ft.Row(
            controls=[archivo_menu, administracion, herramientas_menu], # Orden visible de menús.
            spacing=10,                                                 # Separación entre menús.
        ),
        ft.Row(
            controls=[
                boton_cliente,
                boton_repuestos,
                boton_ficha_tecnica,
                boton_presupuesto,
                boton_usuario,
            ]
        ),
    )


# ---------------------------
# Punto de entrada de Flet
# ---------------------------
def main(page: ft.Page):
    page.window.maximized = True   # Asegura pantalla grande desde el arranque de la app.
    menu_principal(page)           # Dibuja el menú principal al iniciar.  :contentReference[oaicite:13]{index=13}


ft.app(target=main)                # Lanza la app Flet, usando "main" como función objetivo.  :contentReference[oaicite:14]{index=14}
