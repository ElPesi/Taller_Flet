import flet as ft                  # Importamos Flet para construir la interfaz gráfica.
import mysql.connector             # Importamos el conector oficial para conectarnos a MySQL.


# ---------- Conexión a la base de datos ----------
def connect_to_db():
    """
    Abre una conexión con la base de datos MySQL.
    Centraliza la configuración de conexión.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",      # Servidor local.
            port=3306,             # Puerto por defecto de MySQL.
            user="root",           # Usuario con permisos.
            password="root",       # Contraseña.
            database="Taller_Mecanico",  # Nombre de la base usada.
            ssl_disabled=True      # Deshabilitamos SSL (no necesario en local).
        )
        if connection.is_connected():   # Si la conexión se estableció correctamente:
            print("Conexión exitosa")
            return connection
    except Exception as ex:
        print("Conexión errónea")       # Si algo falla, mostramos error.
        print(ex)
        return None


# ---------- Clase principal para la gestión de clientes ----------
class Herramienta_Cliente:
    """
    Esta clase maneja todo lo relacionado con la gestión de clientes:
    - Alta (crear)
    - Consulta (listar)
    - Actualización (editar)
    - Eliminación (borrar)
    Incluye también búsqueda con filtros y actualización en vivo de la tabla.
    """

    def __init__(self, page: ft.Page, main_menu_callback):
        # Recibe la "page" de Flet (donde se dibuja la UI)
        # y el callback al menú principal para poder volver atrás.
        self.page = page
        self.main_menu_callback = main_menu_callback

        # Conexión a la base de datos
        self.connection = connect_to_db()
        self.cursor = self.connection.cursor() if self.connection else None

        # Campo de búsqueda (texto que el usuario escribe para filtrar)
        self.search_field = ft.TextField(label="Buscar", width=300, on_change=self.search)

        # Menú desplegable para elegir la columna sobre la cual buscar.
        self.search_column = ft.Dropdown(
            options=[
                ft.dropdown.Option("cod_cliente"),
                ft.dropdown.Option("apellido"),
                ft.dropdown.Option("nombre"),
                ft.dropdown.Option("dni"),
                ft.dropdown.Option("direccion"),
                ft.dropdown.Option("telefono"),
            ],
            value="apellido",   # Columna por defecto: apellido
            width=200,
            on_change=self.search,
        )

        # Mostramos la pantalla inicial de clientes
        self.mostrar_cliente()


    # ---------- Pantalla principal de clientes ----------
    def mostrar_cliente(self):
        self.page.clean()   # Limpia la pantalla

        # Cabecera con botones de navegación
        header = ft.Row(
            controls=[
                ft.Text("Herramienta de Gestión de Clientes", size=20, weight="bold"),
                ft.ElevatedButton(text="Alta", on_click=self.alta_cliente),
                ft.ElevatedButton(text="Consulta", on_click=self.consulta_cliente),
                ft.ElevatedButton(text="Imprimir", on_click=self.imprimir_clientes),
                ft.ElevatedButton(text="Volver al Menú", on_click=self.volver_al_menu),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        # Fila de búsqueda (dropdown + campo texto)
        search_row = ft.Row(
            [self.search_column, self.search_field],
            alignment=ft.MainAxisAlignment.START,
        )

        # Tabla con los clientes de la BD
        self.data_table = self.create_client_table()

        # Agregamos todo a la UI
        self.page.add(
            ft.Container(
                content=ft.Column(
                    controls=[header, search_row, self.data_table],
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=20,
            )
        )


    # ---------- Alta de cliente ----------
    def alta_cliente(self, e):
        """
        Limpia la pantalla y muestra el formulario para crear un cliente nuevo.
        """
        self.page.clean()
        # Campos del formulario
        self.dni = ft.TextField(label="DNI", width=300)
        self.apellido = ft.TextField(label="Apellido", width=300)
        self.nombre = ft.TextField(label="Nombre", width=300)
        self.direccion = ft.TextField(label="Dirección", width=300)
        self.telefono = ft.TextField(label="Teléfono", width=300)
        self.cod_cliente = ft.TextField(label="Código Cliente", width=300)

        # Botones de acción
        guardar_btn = ft.ElevatedButton("Guardar", icon=ft.Icons.SAVE, on_click=self.guardar_cliente)
        volver_btn = ft.ElevatedButton("Volver", icon=ft.Icons.ARROW_BACK, on_click=self.mostrar_cliente)

        # Renderizar en pantalla
        self.page.add(
            ft.Column(
                [
                    ft.Text("Alta de Cliente", size=24, weight="bold"),
                    self.dni, self.apellido, self.nombre, self.direccion, self.telefono, self.cod_cliente,
                    ft.Row([guardar_btn, volver_btn], spacing=10),
                ],
                spacing=10,
            )
        )
        self.page.update()


    # ---------- Guardar cliente en la BD ----------
    def guardar_cliente(self, e):
        try:
            # Insertamos primero en "persona"
            self.cursor.execute(
                "INSERT INTO persona (dni, apellido, nombre, direccion, tele_contac) VALUES (%s, %s, %s, %s, %s)",
                (self.dni.value, self.apellido.value, self.nombre.value, self.direccion.value, self.telefono.value),
            )
            # Luego relacionamos con la tabla "cliente"
            self.cursor.execute(
                "INSERT INTO cliente (cod_cliente, dni) VALUES (%s, %s)",
                (self.cod_cliente.value, self.dni.value),
            )
            self.connection.commit()   # Guardamos cambios

            # Notificación visual
            self.page.snack_bar = ft.SnackBar(ft.Text("Cliente guardado correctamente"))
            self.page.snack_bar.open = True

            # Volvemos a la lista
            self.mostrar_cliente()
        except Exception as ex:
            # Si algo falla, mostramos el error
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error al guardar: {ex}"))
            self.page.snack_bar.open = True
            self.page.update()


    # ---------- Consultar clientes ----------
    def consulta_cliente(self, e):
        """
        Muestra solo la tabla de clientes, sin los botones de alta/imprimir.
        """
        self.page.clean()
        self.page.add(ft.Text("Consulta de Clientes", size=24, weight="bold"))
        self.page.add(self.create_client_table())
        self.page.add(ft.ElevatedButton("Volver", on_click=self.mostrar_cliente))
        self.page.update()


    # ---------- Imprimir clientes (placeholder) ----------
    def imprimir_clientes(self, e):
        self.page.snack_bar = ft.SnackBar(ft.Text("Función de impresión no implementada"))
        self.page.snack_bar.open = True
        self.page.update()


    # ---------- Volver al menú principal ----------
    def volver_al_menu(self, e):
        self.page.clean()
        self.main_menu_callback(self.page)


    # ---------- Crear la tabla de clientes ----------
    def create_client_table(self):
        if not self.cursor:   # Si no hay conexión
            return ft.Text("No hay conexión a la base de datos")

        # Consulta SQL para traer todos los clientes
        listado_todos_clientes = """
            SELECT per.apellido, per.nombre, per.dni,
                   per.direccion, per.tele_contac, c.cod_cliente
            FROM persona per INNER JOIN cliente c ON per.dni = c.dni
            ORDER BY per.apellido
        """
        self.cursor.execute(listado_todos_clientes)
        datos_clientes = self.cursor.fetchall()   # Lista de tuplas con resultados
        self.all_data = datos_clientes            # Guardamos todo para búsquedas

        rows = self.get_rows(datos_clientes)      # Convertimos a filas de DataTable

        # Creamos la tabla
        data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Apellido")),
                ft.DataColumn(ft.Text("Nombres")),
                ft.DataColumn(ft.Text("DNI")),
                ft.DataColumn(ft.Text("Direccion")),
                ft.DataColumn(ft.Text("Teléfono")),
                ft.DataColumn(ft.Text("Código de Cliente")),
                ft.DataColumn(ft.Text("Acciones")), # Editar / Eliminar
            ],
            rows=rows,
        )
        return data_table


    # ---------- Generar filas de la tabla ----------
    def get_rows(self, clientes):
        rows = []
        for cliente in clientes:
            # Botón para eliminar cliente
            eliminar_button = ft.IconButton(
                icon=ft.Icons.DELETE,
                tooltip="Borrar",
                on_click=lambda e, c=cliente: self.eliminar_cliente(e, c),
            )
            # Botón para editar cliente
            actualizar_button = ft.IconButton(
                icon=ft.Icons.EDIT,
                tooltip="Modificar",
                on_click=lambda e, c=cliente: self.actualizar_cliente(e, c),
            )
            # Cada fila contiene las celdas de datos + botones de acción
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(cliente[0])), # Apellido
                        ft.DataCell(ft.Text(cliente[1])), # Nombre
                        ft.DataCell(ft.Text(str(cliente[2]))), # DNI
                        ft.DataCell(ft.Text(cliente[3])), # Dirección
                        ft.DataCell(ft.Text(cliente[4])), # Teléfono
                        ft.DataCell(ft.Text(str(cliente[5]))), # Código Cliente
                        ft.DataCell(ft.Row(controls=[eliminar_button, actualizar_button])),
                    ],
                ),
            )
        return rows


    # ---------- Buscar clientes ----------
    def search(self, e):
        search_term = self.search_field.value.lower()   # Texto a buscar
        search_column = self.search_column.value        # Columna seleccionada
        filtered_data = []

        # Filtrado según la columna elegida
        for row in self.all_data:
            if search_column == "cod_cliente" and str(row[5]).lower().__contains__(search_term):
                filtered_data.append(row)
            elif search_column == "apellido" and row[0].lower().__contains__(search_term):
                filtered_data.append(row)
            elif search_column == "nombre" and row[1].lower().__contains__(search_term):
                filtered_data.append(row)
            elif search_column == "dni" and str(row[2]).lower().__contains__(search_term):
                filtered_data.append(row)
            elif search_column == "direccion" and row[3].lower().__contains__(search_term):
                filtered_data.append(row)
            elif search_column == "telefono" and row[4].lower().__contains__(search_term):
                filtered_data.append(row)

        # Actualizamos la tabla con los resultados filtrados
        self.data_table.rows = self.get_rows(filtered_data)
        self.page.update()


    # ---------- Eliminar cliente ----------
    def eliminar_cliente(self, e, cliente):
        try:
            dni = cliente[2]
            cod_cliente = cliente[5]
            # Primero borramos en cliente
            self.cursor.execute("DELETE FROM cliente WHERE cod_cliente = %s", (cod_cliente,))
            # Luego en persona (para no romper la FK)
            self.cursor.execute("DELETE FROM persona WHERE dni = %s", (dni,))
            self.connection.commit()
            self.page.snack_bar = ft.SnackBar(ft.Text("Cliente eliminado correctamente"))
            self.page.snack_bar.open = True
            self.mostrar_cliente()   # Refrescamos la tabla
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error al eliminar: {ex}"))
            self.page.snack_bar.open = True
            self.page.update()


    # ---------- Editar cliente ----------
    def actualizar_cliente(self, e, cliente):
        self.page.clean()
        # Campos precargados con valores actuales
        self.dni = ft.TextField(label="DNI", value=str(cliente[2]), width=300, disabled=True)
        self.apellido = ft.TextField(label="Apellido", value=cliente[0], width=300)
        self.nombre = ft.TextField(label="Nombre", value=cliente[1], width=300)
        self.direccion = ft.TextField(label="Dirección", value=cliente[3], width=300)
        self.telefono = ft.TextField(label="Teléfono", value=cliente[4], width=300)
        self.cod_cliente = ft.TextField(label="Código Cliente", value=str(cliente[5]), width=300, disabled=True)

        guardar_btn = ft.ElevatedButton(
            "Guardar Cambios", icon=ft.Icons.SAVE, on_click=lambda e: self.guardar_cambios_cliente(e, cliente)
        )
        volver_btn = ft.ElevatedButton("Volver", icon=ft.Icons.ARROW_BACK, on_click=self.mostrar_cliente)

        # Renderizamos formulario de edición
        self.page.add(
            ft.Column(
                [
                    ft.Text("Editar Cliente", size=24, weight="bold"),
                    self.dni, self.apellido, self.nombre, self.direccion, self.telefono, self.cod_cliente,
                    ft.Row([guardar_btn, volver_btn], spacing=10),
                ],
                spacing=10,
            )
        )
        self.page.update()


    # ---------- Guardar cambios en cliente ----------
    def guardar_cambios_cliente(self, e, cliente):
        try:
            self.cursor.execute(
                "UPDATE persona SET apellido=%s, nombre=%s, direccion=%s, tele_contac=%s WHERE dni=%s",
                (self.apellido.value, self.nombre.value, self.direccion.value, self.telefono.value, self.dni.value),
            )
            self.connection.commit()
            self.page.snack_bar = ft.SnackBar(ft.Text("Cliente actualizado correctamente"))
            self.page.snack_bar.open = True
            self.mostrar_cliente()
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error al actualizar: {ex}"))
            self.page.snack_bar.open = True
            self.page.update()


# ---------- Callback dummy para menú principal ----------
def main_menu_callback(page: ft.Page):
    page.clean()
    page.add(ft.Text("Menú Principal"))


# ---------- Punto de entrada de este módulo ----------
def main(page: ft.Page):
    app = Herramienta_Cliente(page, main_menu_callback)
