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


class Herramienta_FichaTecnica:
    def __init__(self, page: ft.Page, main_menu_callback):
        self.page = page
        self.main_menu_callback = main_menu_callback
        self.connection = connect_to_db()
        self.cursor = self.connection.cursor() if self.connection else None
        self.search_field = ft.TextField(label="Buscar", width=300, on_change=self.search)
        self.search_column = ft.Dropdown(
            options=[
                ft.dropdown.Option("patente"),
                ft.dropdown.Option("modelo"),
                ft.dropdown.Option("marca"),
                ft.dropdown.Option("anio"),
            ],
            value="patente",
            width=200,
            on_change=self.search,
        )
        self.mostrar_ficha_tecnica()

    def mostrar_ficha_tecnica(self):
        self.page.clean()
        header = ft.Row(
            controls=[
                ft.Text("Gestión de Fichas Técnicas", size=20, weight="bold"),
                ft.ElevatedButton(text="Alta", on_click=self.alta_ficha),
                ft.ElevatedButton(text="Consulta", on_click=self.consulta_ficha),
                ft.ElevatedButton(text="Imprimir", on_click=self.imprimir_fichas),
                ft.ElevatedButton(text="Volver al Menú", on_click=self.volver_al_menu),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        search_row = ft.Row([self.search_column, self.search_field], alignment=ft.MainAxisAlignment.START)
        self.data_table = self.create_ficha_table()
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

    def alta_ficha(self, e):
        self.page.clean()
        self.patente = ft.TextField(label="Patente", width=300)
        self.modelo = ft.TextField(label="Modelo", width=300)
        self.marca = ft.TextField(label="Marca", width=300)
        self.anio = ft.TextField(label="Año", width=300)
        guardar_btn = ft.ElevatedButton("Guardar", icon=ft.Icons.SAVE, on_click=self.guardar_ficha)
        volver_btn = ft.ElevatedButton("Volver", icon=ft.Icons.ARROW_BACK, on_click=self.mostrar_ficha_tecnica)
        self.page.add(
            ft.Column(
                [
                    ft.Text("Alta de Ficha Técnica", size=24, weight="bold"),
                    self.patente, self.modelo, self.marca, self.anio,
                    ft.Row([guardar_btn, volver_btn], spacing=10),
                ],
                spacing=10,
            )
        )
        self.page.update()

    def guardar_ficha(self, e):
        try:
            self.cursor.execute(
                "INSERT INTO ficha_tecnica (patente, modelo, marca, anio) VALUES (%s, %s, %s, %s)",
                (self.patente.value, self.modelo.value, self.marca.value, self.anio.value),
            )
            self.connection.commit()
            self.page.snack_bar = ft.SnackBar(ft.Text("Ficha técnica guardada correctamente"))
            self.page.snack_bar.open = True
            self.mostrar_ficha_tecnica()
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error al guardar: {ex}"))
            self.page.snack_bar.open = True
            self.page.update()

    def consulta_ficha(self, e):
        self.page.clean()
        self.page.add(ft.Text("Consulta de Fichas Técnicas", size=24, weight="bold"))
        self.page.add(self.create_ficha_table())
        self.page.add(ft.ElevatedButton("Volver", on_click=self.mostrar_ficha_tecnica))
        self.page.update()

    def imprimir_fichas(self, e):
        self.page.snack_bar = ft.SnackBar(ft.Text("Función de impresión no implementada"))
        self.page.snack_bar.open = True
        self.page.update()

    def volver_al_menu(self, e):
        self.page.clean()
        self.main_menu_callback(self.page)

    def create_ficha_table(self):
        if not self.cursor:
            return ft.Text("No hay conexión a la base de datos")
        self.cursor.execute("SELECT patente, modelo, marca, anio FROM ficha_tecnica ORDER BY patente")
        datos_fichas = self.cursor.fetchall()
        self.all_data = datos_fichas
        rows = self.get_rows(datos_fichas)
        data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Patente")),
                ft.DataColumn(ft.Text("Modelo")),
                ft.DataColumn(ft.Text("Marca")),
                ft.DataColumn(ft.Text("Año")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=rows,
        )
        return data_table

    def get_rows(self, fichas):
        rows = []
        for ficha in fichas:
            eliminar_button = ft.IconButton(
                icon=ft.Icons.DELETE,
                tooltip="Borrar",
                on_click=lambda e, f=ficha: self.eliminar_ficha(e, f),
            )
            actualizar_button = ft.IconButton(
                icon=ft.Icons.EDIT,
                tooltip="Modificar",
                on_click=lambda e, f=ficha: self.actualizar_ficha(e, f),
            )
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(ficha[0])),
                        ft.DataCell(ft.Text(ficha[1])),
                        ft.DataCell(ft.Text(ficha[2])),
                        ft.DataCell(ft.Text(str(ficha[3]))),
                        ft.DataCell(ft.Row(controls=[eliminar_button, actualizar_button])),
                    ],
                )
            )
        return rows

    def search(self, e):
        search_term = self.search_field.value.lower()
        search_column = self.search_column.value
        filtered_data = []
        for row in self.all_data:
            if search_column == "patente" and row[0].lower().__contains__(search_term):
                filtered_data.append(row)
            elif search_column == "modelo" and row[1].lower().__contains__(search_term):
                filtered_data.append(row)
            elif search_column == "marca" and row[2].lower().__contains__(search_term):
                filtered_data.append(row)
            elif search_column == "anio" and str(row[3]).lower().__contains__(search_term):
                filtered_data.append(row)
        self.data_table.rows = self.get_rows(filtered_data)
        self.page.update()

    def eliminar_ficha(self, e, ficha):
        try:
            patente = ficha[0]
            self.cursor.execute("DELETE FROM ficha_tecnica WHERE patente = %s", (patente,))
            self.connection.commit()
            self.page.snack_bar = ft.SnackBar(ft.Text("Ficha técnica eliminada correctamente"))
            self.page.snack_bar.open = True
            self.mostrar_ficha_tecnica()
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error al eliminar: {ex}"))
            self.page.snack_bar.open = True
            self.page.update()

    def actualizar_ficha(self, e, ficha):
        self.page.clean()
        self.patente = ft.TextField(label="Patente", value=ficha[0], width=300, disabled=True)
        self.modelo = ft.TextField(label="Modelo", value=ficha[1], width=300)
        self.marca = ft.TextField(label="Marca", value=ficha[2], width=300)
        self.anio = ft.TextField(label="Año", value=str(ficha[3]), width=300)
        guardar_btn = ft.ElevatedButton("Guardar Cambios", icon=ft.Icons.SAVE,
                                        on_click=lambda e: self.guardar_cambios_ficha(e, ficha))
        volver_btn = ft.ElevatedButton("Volver", icon=ft.Icons.ARROW_BACK, on_click=self.mostrar_ficha_tecnica)
        self.page.add(
            ft.Column(
                [
                    ft.Text("Editar Ficha Técnica", size=24, weight="bold"),
                    self.patente, self.modelo, self.marca, self.anio,
                    ft.Row([guardar_btn, volver_btn], spacing=10),
                ],
                spacing=10,
            )
        )
        self.page.update()

    def guardar_cambios_ficha(self, e, ficha):
        try:
            self.cursor.execute(
                "UPDATE ficha_tecnica SET modelo=%s, marca=%s, anio=%s WHERE patente=%s",
                (self.modelo.value, self.marca.value, self.anio.value, self.patente.value),
            )
            self.connection.commit()
            self.page.snack_bar = ft.SnackBar(ft.Text("Ficha técnica actualizada correctamente"))
            self.page.snack_bar.open = True
            self.mostrar_ficha_tecnica()
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error al actualizar: {ex}"))
            self.page.snack_bar.open = True
            self.page.update()
