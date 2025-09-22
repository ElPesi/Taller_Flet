import flet as ft                  
import mysql.connector            

def connect_to_db():
    """
    Abre una conexión con la base de datos MySQL.
    Centraliza la configuración de conexión.
    """
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

class Herramienta_Cliente:
    def __init__(self, page: ft.Page, main_menu_callback):
        self.page = page
        self.main_menu_callback = main_menu_callback
        self.connection = connect_to_db()
        self.cursor = self.connection.cursor() if self.connection else None
        self.search_field = ft.TextField(label="Buscar", width=300, on_change=self.search)
        self.search_column = ft.Dropdown(
            options=[
                ft.dropdown.Option("cod_cliente"),
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
        self.mostrar_cliente()

    def mostrar_cliente(self):
        self.page.clean()
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
        search_row = ft.Row(
            [
                self.search_column,
                self.search_field,
            ],
            alignment=ft.MainAxisAlignment.START,
        )
        self.data_table = self.create_client_table()
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

    def alta_cliente(self, e):
        self.page.clean()
        self.dni = ft.TextField(label="DNI", width=300)
        self.apellido = ft.TextField(label="Apellido", width=300)
        self.nombre = ft.TextField(label="Nombre", width=300)
        self.direccion = ft.TextField(label="Dirección", width=300)
        self.telefono = ft.TextField(label="Teléfono", width=300)
        self.cod_cliente = ft.TextField(label="Código Cliente", width=300)

        guardar_btn = ft.ElevatedButton("Guardar", icon=ft.Icons.SAVE, on_click=self.guardar_cliente)
        volver_btn = ft.ElevatedButton("Volver", icon=ft.Icons.ARROW_BACK, on_click=self.mostrar_cliente)

        self.page.add(
            ft.Column(
                [
                    ft.Text("Alta de Cliente", size=24, weight="bold"),
                    self.dni,
                    self.apellido,
                    self.nombre,
                    self.direccion,
                    self.telefono,
                    self.cod_cliente,
                    ft.Row([guardar_btn, volver_btn], spacing=10),
                ],
                spacing=10,
            )
        )
        self.page.update()

    def guardar_cliente(self, e):
        try:
            self.cursor.execute(
                "INSERT INTO persona (dni, apellido, nombre, direccion, tele_contac) VALUES (%s, %s, %s, %s, %s)",
                (
                    self.dni.value,
                    self.apellido.value,
                    self.nombre.value,
                    self.direccion.value,
                    self.telefono.value,
                ),
            )
            self.cursor.execute(
                "INSERT INTO cliente (cod_cliente, dni) VALUES (%s, %s)",
                (self.cod_cliente.value, self.dni.value),
            )
            self.connection.commit()
            self.page.snack_bar = ft.SnackBar(ft.Text("Cliente guardado correctamente"))
            self.page.snack_bar.open = True
            self.mostrar_cliente()
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error al guardar: {ex}"))
            self.page.snack_bar.open = True
            self.page.update()

    def consulta_cliente(self, e):
        self.page.clean()
        self.page.add(ft.Text("Consulta de Clientes", size=24, weight="bold"))
        self.page.add(self.create_client_table())
        self.page.add(ft.ElevatedButton("Volver", on_click=self.mostrar_cliente))
        self.page.update()

    def imprimir_clientes(self, e):
        self.page.snack_bar = ft.SnackBar(ft.Text("Función de impresión no implementada"))
        self.page.snack_bar.open = True
        self.page.update()

    def volver_al_menu(self, e):
        self.page.clean()
        self.main_menu_callback(self.page)

    def create_client_table(self):
        if not self.cursor:
            print("No hay conexión a la base de datos")
            return ft.Text("No hay conexión a la base de datos")

        listado_todos_clientes = """
            SELECT per.apellido, per.nombre, per.dni,
                   per.direccion, per.tele_contac, c.cod_cliente
            FROM persona per INNER JOIN cliente c ON per.dni = c.dni
            ORDER BY per.apellido
        """
        self.cursor.execute(listado_todos_clientes)
        datos_clientes = self.cursor.fetchall()
        self.all_data = datos_clientes
        rows = self.get_rows(datos_clientes)

        data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Apellido")),
                ft.DataColumn(ft.Text("Nombres")),
                ft.DataColumn(ft.Text("DNI")),
                ft.DataColumn(ft.Text("Direccion")),
                ft.DataColumn(ft.Text("Teléfono")),
                ft.DataColumn(ft.Text("Código de Cliente")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=rows,
        )
        return data_table

    def get_rows(self, clientes):
        rows = []
        for cliente in clientes:
            eliminar_button = ft.IconButton(
                icon=ft.Icons.DELETE,
                tooltip="Borrar",
                on_click=lambda e, c=cliente: self.eliminar_cliente(e, c),
            )

            actualizar_button = ft.IconButton(
                icon=ft.Icons.EDIT,
                tooltip="Modificar",
                on_click=lambda e, c=cliente: self.actualizar_cliente(e, c),
            )

            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(cliente[0])),
                        ft.DataCell(ft.Text(cliente[1])),
                        ft.DataCell(ft.Text(str(cliente[2]))),
                        ft.DataCell(ft.Text(cliente[3])),
                        ft.DataCell(ft.Text(cliente[4])),
                        ft.DataCell(ft.Text(str(cliente[5]))),
                        ft.DataCell(
                            ft.Row(controls=[eliminar_button, actualizar_button])
                        ),
                    ],
                ),
            )
        return rows

    def search(self, e):
        search_term = self.search_field.value.lower()
        search_column = self.search_column.value
        filtered_data = []

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

        self.data_table.rows = self.get_rows(filtered_data)
        self.page.update()

    def eliminar_cliente(self, e, cliente):
        try:
            dni = cliente[2]
            cod_cliente = cliente[5]
            self.cursor.execute("DELETE FROM cliente WHERE cod_cliente = %s", (cod_cliente,))
            self.cursor.execute("DELETE FROM persona WHERE dni = %s", (dni,))
            self.connection.commit()
            self.page.snack_bar = ft.SnackBar(ft.Text("Cliente eliminado correctamente"))
            self.page.snack_bar.open = True
            self.mostrar_cliente()
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error al eliminar: {ex}"))
            self.page.snack_bar.open = True
            self.page.update()

    def actualizar_cliente(self, e, cliente):
        self.page.clean()
        self.dni = ft.TextField(label="DNI", value=str(cliente[2]), width=300, disabled=True)
        self.apellido = ft.TextField(label="Apellido", value=cliente[0], width=300)
        self.nombre = ft.TextField(label="Nombre", value=cliente[1], width=300)
        self.direccion = ft.TextField(label="Dirección", value=cliente[3], width=300)
        self.telefono = ft.TextField(label="Teléfono", value=cliente[4], width=300)
        self.cod_cliente = ft.TextField(label="Código Cliente", value=str(cliente[5]), width=300, disabled=True)

        guardar_btn = ft.ElevatedButton("Guardar Cambios", icon=ft.Icons.SAVE, on_click=lambda e: self.guardar_cambios_cliente(e, cliente))
        volver_btn = ft.ElevatedButton("Volver", icon=ft.Icons.ARROW_BACK, on_click=self.mostrar_cliente)

        self.page.add(
            ft.Column(
                [
                    ft.Text("Editar Cliente", size=24, weight="bold"),
                    self.dni,
                    self.apellido,
                    self.nombre,
                    self.direccion,
                    self.telefono,
                    self.cod_cliente,
                    ft.Row([guardar_btn, volver_btn], spacing=10),
                ],
                spacing=10,
            )
        )
        self.page.update()

    def guardar_cambios_cliente(self, e, cliente):
        try:
            self.cursor.execute(
                "UPDATE persona SET apellido=%s, nombre=%s, direccion=%s, tele_contac=%s WHERE dni=%s",
                (
                    self.apellido.value,
                    self.nombre.value,
                    self.direccion.value,
                    self.telefono.value,
                    self.dni.value,
                ),
            )
            self.connection.commit()
            self.page.snack_bar = ft.SnackBar(ft.Text("Cliente actualizado correctamente"))
            self.page.snack_bar.open = True
            self.mostrar_cliente()
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error al actualizar: {ex}"))
            self.page.snack_bar.open = True
            self.page.update()


def main_menu_callback(page: ft.Page):
    page.clean()
    page.add(ft.Text("Menú Principal"))


def main(page: ft.Page):
    app = Herramienta_Cliente(page, main_menu_callback)
