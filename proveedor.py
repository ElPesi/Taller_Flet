import flet as ft
import mysql.connector

# ---------- Conexión a la base de datos ----------
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="root",
            database="Taller_Mecanico",
            ssl_disabled=True
        )
        if connection.is_connected():
            print("Conexión exitosa")
            return connection
    except Exception as ex:
        print("Conexión errónea")
        print(ex)
        return None


# ---------- Clase principal ----------
class Herramienta_Proveedor:
    def __init__(self, page: ft.Page, main_menu_callback):
        self.page = page
        self.main_menu_callback = main_menu_callback
        self.connection = connect_to_db()
        self.cursor = self.connection.cursor() if self.connection else None

        # Campos de búsqueda
        self.search_field = ft.TextField(label="Buscar", width=300, on_change=self.search)
        self.search_column = ft.Dropdown(
            options=[
                ft.dropdown.Option("cod_proveedor"),
                ft.dropdown.Option("nombre"),
                ft.dropdown.Option("direccion"),
                ft.dropdown.Option("telefono"),
                ft.dropdown.Option("email"),
            ],
            value="nombre",
            width=200,
            on_change=self.search,
        )

        self.mostrar_proveedor()

    # ---------- Vista principal ----------
    def mostrar_proveedor(self):
        self.page.clean()
        header = ft.Row(
            controls=[
                ft.Text("Gestión de Proveedores", size=20, weight="bold"),
                ft.ElevatedButton(text="Alta", on_click=self.alta_proveedor),
                ft.ElevatedButton(text="Consulta", on_click=self.consulta_proveedor),
                ft.ElevatedButton(text="Imprimir", on_click=self.imprimir_proveedores),
                ft.ElevatedButton(text="Volver al Menú", on_click=self.volver_al_menu),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        search_row = ft.Row([self.search_column, self.search_field])
        self.data_table = self.create_proveedor_table()

        self.page.add(
            ft.Container(
                content=ft.Column([header, search_row, self.data_table]),
                padding=20,
            )
        )

    # ---------- Alta ----------
    def alta_proveedor(self, e):
        self.page.clean()
        self.cod_proveedor = ft.TextField(label="Código Proveedor", width=300)
        self.nombre = ft.TextField(label="Nombre", width=300)
        self.direccion = ft.TextField(label="Dirección", width=300)
        self.telefono = ft.TextField(label="Teléfono", width=300)
        self.email = ft.TextField(label="Email", width=300)

        guardar_btn = ft.ElevatedButton("Guardar", icon=ft.Icons.SAVE, on_click=self.guardar_proveedor)
        volver_btn = ft.ElevatedButton("Volver", icon=ft.Icons.ARROW_BACK, on_click=self.mostrar_proveedor)

        self.page.add(
            ft.Column(
                [
                    ft.Text("Alta de Proveedor", size=24, weight="bold"),
                    self.cod_proveedor, self.nombre, self.direccion, self.telefono, self.email,
                    ft.Row([guardar_btn, volver_btn], spacing=10),
                ],
                spacing=10,
            )
        )
        self.page.update()

    def guardar_proveedor(self, e):
        try:
            self.cursor.execute(
                "INSERT INTO proveedor (cod_proveedor, nombre, direccion, telefono, email) VALUES (%s, %s, %s, %s, %s)",
                (
                    self.cod_proveedor.value, self.nombre.value,
                    self.direccion.value, self.telefono.value, self.email.value,
                ),
            )
            self.connection.commit()
            self.page.snack_bar = ft.SnackBar(ft.Text("Proveedor guardado correctamente"), open=True)
            self.mostrar_proveedor()
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error al guardar: {ex}"), open=True)
            self.page.update()

    # ---------- Consulta ----------
    def consulta_proveedor(self, e):
        self.page.clean()
        self.page.add(ft.Text("Consulta de Proveedores", size=24, weight="bold"))
        self.data_table = self.create_proveedor_table()
        self.page.add(self.data_table)
        self.page.add(ft.ElevatedButton("Volver", on_click=self.mostrar_proveedor))
        self.page.update()

    def imprimir_proveedores(self, e):
        self.page.snack_bar = ft.SnackBar(ft.Text("Función de impresión no implementada"), open=True)
        self.page.update()

    def volver_al_menu(self, e):
        self.page.clean()
        self.main_menu_callback(self.page)

    # ---------- Tabla ----------
    def create_proveedor_table(self):
        if not self.cursor:
            return ft.Text("No hay conexión a la base de datos")

        self.cursor.execute(
            "SELECT cod_proveedor, nombre, direccion, telefono, email FROM proveedor ORDER BY nombre"
        )
        datos_proveedores = self.cursor.fetchall()
        self.all_data = datos_proveedores

        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Código Proveedor")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Dirección")),
                ft.DataColumn(ft.Text("Teléfono")),
                ft.DataColumn(ft.Text("Email")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=self.get_rows(datos_proveedores),
        )

    def get_rows(self, proveedores):
        rows = []
        for proveedor in proveedores:
            eliminar_button = ft.IconButton(
                icon=ft.Icons.DELETE,
                tooltip="Borrar",
                on_click=lambda e, p=proveedor: self.eliminar_proveedor(e, p),
            )
            actualizar_button = ft.IconButton(
                icon=ft.Icons.EDIT,
                tooltip="Modificar",
                on_click=lambda e, p=proveedor: self.actualizar_proveedor(e, p),
            )
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(proveedor[0]))),
                        ft.DataCell(ft.Text(proveedor[1])),
                        ft.DataCell(ft.Text(proveedor[2])),
                        ft.DataCell(ft.Text(proveedor[3])),
                        ft.DataCell(ft.Text(proveedor[4])),
                        ft.DataCell(ft.Row(controls=[eliminar_button, actualizar_button])),
                    ],
                )
            )
        return rows

    # ---------- Buscar ----------
    def search(self, e):
        search_term = self.search_field.value.lower()
        search_column = self.search_column.value
        column_map = {"cod_proveedor": 0, "nombre": 1, "direccion": 2, "telefono": 3, "email": 4}
        idx = column_map[search_column]

        filtered_data = [row for row in self.all_data if search_term in str(row[idx]).lower()]
        self.data_table.rows = self.get_rows(filtered_data)
        self.page.update()

    # ---------- Eliminar ----------
    def eliminar_proveedor(self, e, proveedor):
        try:
            cod_proveedor = proveedor[0]
            self.cursor.execute("DELETE FROM proveedor WHERE cod_proveedor = %s", (cod_proveedor,))
            self.connection.commit()
            self.page.snack_bar = ft.SnackBar(ft.Text("Proveedor eliminado correctamente"), open=True)
            self.mostrar_proveedor()
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error al eliminar: {ex}"), open=True)
            self.page.update()

    # ---------- Actualizar ----------
    def actualizar_proveedor(self, e, proveedor):
        self.page.clean()
        self.cod_proveedor = ft.TextField(label="Código Proveedor", value=str(proveedor[0]), width=300, disabled=True)
        self.nombre = ft.TextField(label="Nombre", value=proveedor[1], width=300)
        self.direccion = ft.TextField(label="Dirección", value=proveedor[2], width=300)
        self.telefono = ft.TextField(label="Teléfono", value=proveedor[3], width=300)
        self.email = ft.TextField(label="Email", value=proveedor[4], width=300)

        guardar_btn = ft.ElevatedButton("Guardar Cambios", icon=ft.Icons.SAVE, on_click=lambda e: self.guardar_cambios_proveedor(e))
        volver_btn = ft.ElevatedButton("Volver", icon=ft.Icons.ARROW_BACK, on_click=self.mostrar_proveedor)

        self.page.add(
            ft.Column(
                [
                    ft.Text("Editar Proveedor", size=24, weight="bold"),
                    self.cod_proveedor, self.nombre, self.direccion, self.telefono, self.email,
                    ft.Row([guardar_btn, volver_btn], spacing=10),
                ],
                spacing=10,
            )
        )
        self.page.update()

    def guardar_cambios_proveedor(self, e):
        try:
            self.cursor.execute(
                "UPDATE proveedor SET nombre=%s, direccion=%s, telefono=%s, email=%s WHERE cod_proveedor=%s",
                (
                    self.nombre.value, self.direccion.value, self.telefono.value,
                    self.email.value, self.cod_proveedor.value,
                ),
            )
            self.connection.commit()
            self.page.snack_bar = ft.SnackBar(ft.Text("Proveedor actualizado correctamente"), open=True)
            self.mostrar_proveedor()
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error al actualizar: {ex}"), open=True)
            self.page.update()
