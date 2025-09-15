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


# ---------- Clase principal para gestión de empleados ----------
class Herramienta_Empleado:
    """
    Clase para gestionar empleados:
    - Alta, consulta, edición y eliminación
    - Búsqueda en vivo con filtros
    """

    def __init__(self, page: ft.Page, main_menu_callback):
        self.page = page
        self.main_menu_callback = main_menu_callback

        self.connection = connect_to_db()
        self.cursor = self.connection.cursor() if self.connection else None

        self.search_field = ft.TextField(label="Buscar", width=300, on_change=self.search)
        self.search_column = ft.Dropdown(
            options=[
                ft.dropdown.Option("legajo"),
                ft.dropdown.Option("apellido"),
                ft.dropdown.Option("nombre"),
                ft.dropdown.Option("dni"),
                ft.dropdown.Option("direccion"),
                ft.dropdown.Option("telefono"),
            ],
            value="apellido",
            width=200,
            on_change=self.search,
        )

        self.mostrar_empleado()

    def mostrar_empleado(self):
        self.page.clean()
        header = ft.Row(
            controls=[
                ft.Text("Gestión de Empleados", size=20, weight="bold"),
                ft.ElevatedButton(text="Alta", on_click=self.alta_empleado),
                ft.ElevatedButton(text="Consulta", on_click=self.consulta_empleado),
                ft.ElevatedButton(text="Imprimir", on_click=self.imprimir_empleados),
                ft.ElevatedButton(text="Volver al Menú", on_click=self.volver_al_menu),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        search_row = ft.Row([self.search_column, self.search_field], alignment=ft.MainAxisAlignment.START)
        self.data_table = self.create_empleado_table()
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

    def alta_empleado(self, e):
        self.page.clean()
        self.legajo = ft.TextField(label="Legajo", width=300)
        self.dni = ft.TextField(label="DNI", width=300)
        self.apellido = ft.TextField(label="Apellido", width=300)
        self.nombre = ft.TextField(label="Nombre", width=300)
        self.direccion = ft.TextField(label="Dirección", width=300)
        self.telefono = ft.TextField(label="Teléfono", width=300)

        guardar_btn = ft.ElevatedButton("Guardar", icon=ft.Icons.SAVE, on_click=self.guardar_empleado)
        volver_btn = ft.ElevatedButton("Volver", icon=ft.Icons.ARROW_BACK, on_click=self.mostrar_empleado)

        self.page.add(
            ft.Column(
                [
                    ft.Text("Alta de Empleado", size=24, weight="bold"),
                    self.legajo, self.dni, self.apellido, self.nombre, self.direccion, self.telefono,
                    ft.Row([guardar_btn, volver_btn], spacing=10),
                ],
                spacing=10,
            )
        )
        self.page.update()

    def guardar_empleado(self, e):
        try:
            self.cursor.execute(
                "INSERT INTO persona (dni, apellido, nombre, direccion, tele_contac) VALUES (%s, %s, %s, %s, %s)",
                (self.dni.value, self.apellido.value, self.nombre.value, self.direccion.value, self.telefono.value),
            )
            self.cursor.execute(
                "INSERT INTO empleado (legajo, dni) VALUES (%s, %s)",
                (self.legajo.value, self.dni.value),
            )
            self.connection.commit()
            self.page.snack_bar = ft.SnackBar(ft.Text("Empleado guardado correctamente"))
            self.page.snack_bar.open = True
            self.mostrar_empleado()
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error al guardar: {ex}"))
            self.page.snack_bar.open = True
            self.page.update()

    def consulta_empleado(self, e):
        self.page.clean()
        self.page.add(ft.Text("Consulta de Empleados", size=24, weight="bold"))
        self.page.add(self.create_empleado_table())
        self.page.add(ft.ElevatedButton("Volver", on_click=self.mostrar_empleado))
        self.page.update()

    def imprimir_empleados(self, e):
        self.page.snack_bar = ft.SnackBar(ft.Text("Función de impresión no implementada"))
        self.page.snack_bar.open = True
        self.page.update()

    def volver_al_menu(self, e):
        self.page.clean()
        self.main_menu_callback(self.page)

    def create_empleado_table(self):
        if not self.cursor:
            return ft.Text("No hay conexión a la base de datos")

        query = """
            SELECT per.apellido, per.nombre, per.dni, per.direccion, per.tele_contac, emp.legajo
            FROM persona per INNER JOIN empleado emp ON per.dni = emp.dni
            ORDER BY per.apellido
        """
        self.cursor.execute(query)
        datos_empleados = self.cursor.fetchall()
        self.all_data = datos_empleados
        rows = self.get_rows(datos_empleados)

        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Apellido")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("DNI")),
                ft.DataColumn(ft.Text("Dirección")),
                ft.DataColumn(ft.Text("Teléfono")),
                ft.DataColumn(ft.Text("Legajo")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=rows,
        )

    def get_rows(self, empleados):
        rows = []
        for empleado in empleados:
            eliminar_button = ft.IconButton(
                icon=ft.Icons.DELETE,
                tooltip="Borrar",
                on_click=lambda e, emp=empleado: self.eliminar_empleado(e, emp),
            )
            actualizar_button = ft.IconButton(
                icon=ft.Icons.EDIT,
                tooltip="Modificar",
                on_click=lambda e, emp=empleado: self.actualizar_empleado(e, emp),
            )
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(empleado[0])),
                        ft.DataCell(ft.Text(empleado[1])),
                        ft.DataCell(ft.Text(str(empleado[2]))),
                        ft.DataCell(ft.Text(empleado[3])),
                        ft.DataCell(ft.Text(empleado[4])),
                        ft.DataCell(ft.Text(str(empleado[5]))),
                        ft.DataCell(ft.Row(controls=[eliminar_button, actualizar_button])),
                    ],
                ),
            )
        return rows

    def search(self, e):
        search_term = self.search_field.value.lower()
        search_column = self.search_column.value
        filtered_data = []

        for row in self.all_data:
            if search_column == "legajo" and str(row[5]).lower().__contains__(search_term):
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

        self.data_table.rows = self.get_rows(filtered_data)
        self.page.update()

    def eliminar_empleado(self, e, empleado):
        try:
            dni = empleado[2]
            legajo = empleado[5]
            self.cursor.execute("DELETE FROM empleado WHERE legajo = %s", (legajo,))
            self.cursor.execute("DELETE FROM persona WHERE dni = %s", (dni,))
            self.connection.commit()
            self.page.snack_bar = ft.SnackBar(ft.Text("Empleado eliminado correctamente"))
            self.page.snack_bar.open = True
            self.mostrar_empleado()
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error al eliminar: {ex}"))
            self.page.snack_bar.open = True
            self.page.update()

    def actualizar_empleado(self, e, empleado):
        self.page.clean()
        self.legajo = ft.TextField(label="Legajo", value=str(empleado[5]), width=300, disabled=True)
        self.dni = ft.TextField(label="DNI", value=str(empleado[2]), width=300, disabled=True)
        self.apellido = ft.TextField(label="Apellido", value=empleado[0], width=300)
        self.nombre = ft.TextField(label="Nombre", value=empleado[1], width=300)
        self.direccion = ft.TextField(label="Dirección", value=empleado[3], width=300)
        self.telefono = ft.TextField(label="Teléfono", value=empleado[4], width=300)

        guardar_btn = ft.ElevatedButton(
            "Guardar Cambios", icon=ft.Icons.SAVE,
            on_click=lambda e: self.guardar_cambios_empleado(e, empleado)
        )
        volver_btn = ft.ElevatedButton("Volver", icon=ft.Icons.ARROW_BACK, on_click=self.mostrar_empleado)

        self.page.add(
            ft.Column(
                [
                    ft.Text("Editar Empleado", size=24, weight="bold"),
                    self.legajo, self.dni, self.apellido, self.nombre, self.direccion, self.telefono,
                    ft.Row([guardar_btn, volver_btn], spacing=10),
                ],
                spacing=10,
            )
        )
        self.page.update()

    def guardar_cambios_empleado(self, e, empleado):
        try:
            self.cursor.execute(
                "UPDATE persona SET apellido=%s, nombre=%s, direccion=%s, tele_contac=%s WHERE dni=%s",
                (self.apellido.value, self.nombre.value, self.direccion.value, self.telefono.value, self.dni.value),
            )
            self.connection.commit()
            self.page.snack_bar = ft.SnackBar(ft.Text("Empleado actualizado correctamente"))
            self.page.snack_bar.open = True
            self.mostrar_empleado()
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error al actualizar: {ex}"))
            self.page.snack_bar.open = True
            self.page.update()
