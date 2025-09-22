import flet as ft
import mysql.connector

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

class Herramienta_Presupuesto:
    def __init__(self, page: ft.Page, main_menu_callback):
        self.page = page
        self.main_menu_callback = main_menu_callback
        self.connection = connect_to_db()
        self.cursor = self.connection.cursor() if self.connection else None
        self.search_field = ft.TextField(label="Buscar", width=300, on_change=self.search)
        self.search_column = ft.Dropdown(
            options=[
                ft.dropdown.Option("nro_presupuesto"),
                ft.dropdown.Option("cod_cliente"),
                ft.dropdown.Option("descripcion"),
                ft.dropdown.Option("total_presupuesto"),
                ft.dropdown.Option("total_gastado"),
            ],
            value="nro_presupuesto",
            width=200,
            on_change=self.search,
        )
        self.mostrar_presupuesto()

    def mostrar_presupuesto(self):
        self.page.clean()
        header = ft.Row(
            controls=[
                ft.Text("Gestión de Presupuestos", size=20, weight="bold"),
                ft.ElevatedButton(text="Alta", on_click=self.alta_presupuesto),
                ft.ElevatedButton(text="Consulta", on_click=self.consulta_presupuesto),
                ft.ElevatedButton(text="Imprimir", on_click=self.imprimir_presupuestos),
                ft.ElevatedButton(text="Volver al Menú", on_click=self.volver_al_menu),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        search_row = ft.Row(
            [
                self.search_column,
                self.search_field,
            ],
            alignment=ft.MainAxisAlignment.START,
        )
        self.data_table, total_presupuesto, total_gastado = self.create_presupuesto_table()
        self.page.add(
            ft.Container(
                content=ft.Column(
                    controls=[
                        header,
                        search_row,
                        ft.Text(f"Total Presupuestado: ${total_presupuesto}", size=16, weight="bold"),
                        ft.Text(f"Total Gastado: ${total_gastado}", size=16, weight="bold"),
                        self.data_table
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=20,
            )
        )

    def alta_presupuesto(self, e):
        self.page.clean()
        self.nro_presupuesto = ft.TextField(label="Nro Presupuesto", width=300)
        self.cod_cliente = ft.TextField(label="Código Cliente", width=300)
        self.descripcion = ft.TextField(label="Descripción", width=300)
        self.total_presupuesto = ft.TextField(label="Total Presupuesto", width=300)
        self.total_gastado = ft.TextField(label="Total Gastado", width=300)

        guardar_btn = ft.ElevatedButton("Guardar", icon=ft.Icons.SAVE, on_click=self.guardar_presupuesto)
        volver_btn = ft.ElevatedButton("Volver", icon=ft.Icons.ARROW_BACK, on_click=self.mostrar_presupuesto)

        self.page.add(
            ft.Column(
                [
                    ft.Text("Alta de Presupuesto", size=24, weight="bold"),
                    self.nro_presupuesto,
                    self.cod_cliente,
                    self.descripcion,
                    self.total_presupuesto,
                    self.total_gastado,
                    ft.Row([guardar_btn, volver_btn], spacing=10),
                ],
                spacing=10,
            )
        )
        self.page.update()

    def guardar_presupuesto(self, e):
        try:
            self.cursor.execute(
                "INSERT INTO presupuesto (nro_presupuesto, cod_cliente, descripcion, total_presupuesto, total_gastado) VALUES (%s, %s, %s, %s, %s)",
                (
                    self.nro_presupuesto.value,
                    self.cod_cliente.value,
                    self.descripcion.value,
                    self.total_presupuesto.value,
                    self.total_gastado.value,
                ),
            )
            self.connection.commit()
            self.page.snack_bar = ft.SnackBar(ft.Text("Presupuesto guardado correctamente"))
            self.page.snack_bar.open = True
            self.mostrar_presupuesto()
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error al guardar: {ex}"))
            self.page.snack_bar.open = True
            self.page.update()

    def consulta_presupuesto(self, e):
        self.page.clean()
        data_table, total_presupuesto, total_gastado = self.create_presupuesto_table()
        self.page.add(ft.Text("Consulta de Presupuestos", size=24, weight="bold"))
        self.page.add(ft.Text(f"Total Presupuestado: ${total_presupuesto}", size=16, weight="bold"))
        self.page.add(ft.Text(f"Total Gastado: ${total_gastado}", size=16, weight="bold"))
        self.page.add(data_table)
        self.page.add(ft.ElevatedButton("Volver", on_click=self.mostrar_presupuesto))
        self.page.update()

    def imprimir_presupuestos(self, e):
        self.page.snack_bar = ft.SnackBar(ft.Text("Función de impresión no implementada"))
        self.page.snack_bar.open = True
        self.page.update()

    def volver_al_menu(self, e):
        self.page.clean()
        self.main_menu_callback(self.page)

    def create_presupuesto_table(self):
        if not self.cursor:
            print("No hay conexión a la base de datos")
            return ft.Text("No hay conexión a la base de datos"), 0, 0

        listado_todos_presupuestos = """
            SELECT nro_presupuesto, cod_cliente, descripcion, total_presupuesto, total_gastado
            FROM presupuesto
            ORDER BY nro_presupuesto
        """
        self.cursor.execute(listado_todos_presupuestos)
        datos_presupuestos = self.cursor.fetchall()
        self.all_data = datos_presupuestos
        rows = []

        total_presupuesto = 0
        total_gastado = 0

        for presupuesto in datos_presupuestos:
            total_presupuesto += float(presupuesto[3] or 0)
            total_gastado += float(presupuesto[4] or 0)
            eliminar_button = ft.IconButton(
                icon=ft.Icons.DELETE,
                tooltip="Borrar",
                on_click=lambda e, p=presupuesto: self.eliminar_presupuesto(e, p),
            )
            actualizar_button = ft.IconButton(
                icon=ft.Icons.EDIT,
                tooltip="Modificar",
                on_click=lambda e, p=presupuesto: self.actualizar_presupuesto(e, p),
            )
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(presupuesto[0]))),
                        ft.DataCell(ft.Text(str(presupuesto[1]))),
                        ft.DataCell(ft.Text(presupuesto[2])),
                        ft.DataCell(ft.Text(str(presupuesto[3]))),
                        ft.DataCell(ft.Text(str(presupuesto[4]))),
                        ft.DataCell(ft.Row(controls=[eliminar_button, actualizar_button])),
                    ],
                ),
            )

        data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Nro Presupuesto")),
                ft.DataColumn(ft.Text("Código Cliente")),
                ft.DataColumn(ft.Text("Descripción")),
                ft.DataColumn(ft.Text("Total Presupuesto")),
                ft.DataColumn(ft.Text("Total Gastado")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=rows,
        )
        return data_table, total_presupuesto, total_gastado

    def eliminar_presupuesto(self, e, presupuesto):
        try:
            nro_presupuesto = presupuesto[0]
            self.cursor.execute("DELETE FROM presupuesto WHERE nro_presupuesto = %s", (nro_presupuesto,))
            self.connection.commit()
            self.page.snack_bar = ft.SnackBar(ft.Text("Presupuesto eliminado correctamente"))
            self.page.snack_bar.open = True
            self.mostrar_presupuesto()
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error al eliminar: {ex}"))
            self.page.snack_bar.open = True
            self.page.update()

    def actualizar_presupuesto(self, e, presupuesto):
        self.page.clean()
        self.nro_presupuesto = ft.TextField(label="Nro Presupuesto", value=str(presupuesto[0]), width=300, disabled=True)
        self.cod_cliente = ft.TextField(label="Código Cliente", value=str(presupuesto[1]), width=300)
        self.descripcion = ft.TextField(label="Descripción", value=presupuesto[2], width=300)
        self.total_presupuesto = ft.TextField(label="Total Presupuesto", value=str(presupuesto[3]), width=300)
        self.total_gastado = ft.TextField(label="Total Gastado", value=str(presupuesto[4]), width=300)

        guardar_btn = ft.ElevatedButton("Guardar Cambios", icon=ft.Icons.SAVE, on_click=lambda e: self.guardar_cambios_presupuesto(e, presupuesto))
        volver_btn = ft.ElevatedButton("Volver", icon=ft.Icons.ARROW_BACK, on_click=self.mostrar_presupuesto)

        self.page.add(
            ft.Column(
                [
                    ft.Text("Editar Presupuesto", size=24, weight="bold"),
                    self.nro_presupuesto,
                    self.cod_cliente,
                    self.descripcion,
                    self.total_presupuesto,
                    self.total_gastado,
                    ft.Row([guardar_btn, volver_btn], spacing=10),
                ],
                spacing=10,
            )
        )
        self.page.update()

    def guardar_cambios_presupuesto(self, e, presupuesto):
        try:
            self.cursor.execute(
                "UPDATE presupuesto SET cod_cliente=%s, descripcion=%s, total_presupuesto=%s, total_gastado=%s WHERE nro_presupuesto=%s",
                (
                    self.cod_cliente.value,
                    self.descripcion.value,
                    self.total_presupuesto.value,
                    self.total_gastado.value,
                    self.nro_presupuesto.value,
                ),
            )
            self.connection.commit()
            self.page.snack_bar = ft.SnackBar(ft.Text("Presupuesto actualizado correctamente"))
            self.page.snack_bar.open = True
            self.mostrar_presupuesto()
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error al actualizar: {ex}"))
            self.page.snack_bar.open = True
            self.page.update()

    def search(self, e):
        search_term = self.search_field.value.lower()
        search_column = self.search_column.value
        filtered_data = []

        for row in self.all_data:
            if search_column == "nro_presupuesto" and str(row[0]).lower().__contains__(search_term):
                filtered_data.append(row)
            elif search_column == "cod_cliente" and str(row[1]).lower().__contains__(search_term):
                filtered_data.append(row)
            elif search_column == "descripcion" and row[2].lower().__contains__(search_term):
                filtered_data.append(row)
            elif search_column == "total_presupuesto" and str(row[3]).lower().__contains__(search_term):
                filtered_data.append(row)
            elif search_column == "total_gastado" and str(row[4]).lower().__contains__(search_term):
                filtered_data.append(row)

        self.data_table, total_presupuesto, total_gastado = self.create_presupuesto_table(filtered_data)
        self.page.update()

    def create_presupuesto_table(self, data=None):
        if not self.cursor:
            print("No hay conexión a la base de datos")
            return ft.Text("No hay conexión a la base de datos"), 0, 0

        if data is None:
            listado_todos_presupuestos = """
                SELECT nro_presupuesto, cod_cliente, descripcion, total_presupuesto, total_gastado
                FROM presupuesto
                ORDER BY nro_presupuesto
            """
            self.cursor.execute(listado_todos_presupuestos)
            datos_presupuestos = self.cursor.fetchall()
        else:
            datos_presupuestos = data

        rows = []
        total_presupuesto = 0
        total_gastado = 0

        for presupuesto in datos_presupuestos:
            total_presupuesto += float(presupuesto[3] or 0)
            total_gastado += float(presupuesto[4] or 0)
            eliminar_button = ft.IconButton(
                icon=ft.Icons.DELETE,
                tooltip="Borrar",
                on_click=lambda e, p=presupuesto: self.eliminar_presupuesto(e, p),
            )
            actualizar_button = ft.IconButton(
                icon=ft.Icons.EDIT,
                tooltip="Modificar",
                on_click=lambda e, p=presupuesto: self.actualizar_presupuesto(e, p),
            )
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(presupuesto[0]))),
                        ft.DataCell(ft.Text(str(presupuesto[1]))),
                        ft.DataCell(ft.Text(presupuesto[2])),
                        ft.DataCell(ft.Text(str(presupuesto[3]))),
                        ft.DataCell(ft.Text(str(presupuesto[4]))),
                        ft.DataCell(ft.Row(controls=[eliminar_button, actualizar_button])),
                    ],
                ),
            )

        data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Nro Presupuesto")),
                ft.DataColumn(ft.Text("Código Cliente")),
                ft.DataColumn(ft.Text("Descripción")),
                ft.DataColumn(ft.Text("Total Presupuesto")),
                ft.DataColumn(ft.Text("Total Gastado")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=rows,
        )
        return data_table, total_presupuesto, total_gastado
