import flet as ft
import mysql.connector

# ---------- Conexión a la base de datos ----------
def connect_to_db():
    try:
        # Se conecta a MySQL con los parámetros definidos
        connection = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="root",
            database="Taller_Mecanico",
            ssl_disabled=True
        )
        # Si la conexión es correcta devuelve el objeto connection
        if connection.is_connected():
            print("Conexión exitosa")
            return connection
    except Exception as ex:
        # Si ocurre un error al conectar
        print("Conexión errónea")
        print(ex)
        return None


# ---------- Clase principal para gestión de repuestos ----------
class Herramienta_Repuesto:
    def __init__(self, page: ft.Page, main_menu_callback):
        # Página principal de Flet
        self.page = page
        # Callback para regresar al menú principal
        self.main_menu_callback = main_menu_callback
        # Conexión a la base de datos
        self.connection = connect_to_db()
        self.cursor = self.connection.cursor() if self.connection else None

        # Campo de búsqueda (texto)
        self.search_field = ft.TextField(label="Buscar", width=300, on_change=self.search)
        # Selector de columna para filtrar
        self.search_column = ft.Dropdown(
            options=[
                ft.dropdown.Option("cod_repuesto"),
                ft.dropdown.Option("descripcion"),
                ft.dropdown.Option("pcio_unit"),
            ],
            value="descripcion",  # búsqueda por defecto
            width=200,
            on_change=self.search,
        )

        # Apenas se crea la clase se muestra la vista principal
        self.mostrar_repuesto()


    # ---------- Vista principal ----------
    def mostrar_repuesto(self):
        self.page.clean()  # limpia la pantalla

        # Cabecera con botones de acción
        header = ft.Row(
            controls=[
                ft.Text("Herramienta de Gestión de Repuestos", size=20, weight="bold"),
                ft.ElevatedButton(text="Alta", on_click=self.alta_repuesto),      # Cargar nuevo repuesto
                ft.ElevatedButton(text="Consulta", on_click=self.consulta_repuesto), # Ver todos
                ft.ElevatedButton(text="Imprimir", on_click=self.imprimir_repuestos), # Opción no implementada
                ft.ElevatedButton(text="Volver al Menú", on_click=self.volver_al_menu), # Volver al menú principal
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        # Barra de búsqueda (filtros)
        search_row = ft.Row(
            [
                self.search_column,
                self.search_field,
            ],
            alignment=ft.MainAxisAlignment.START,
        )

        # Tabla de datos
        data_table = self.create_repuesto_table()

        # Se arma la página
        self.page.add(
            ft.Container(
                content=ft.Column(
                    controls=[header, search_row, data_table],
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=20,
            )
        )


    # ---------- Alta de repuesto ----------
    def alta_repuesto(self, e):
        self.page.clean()

        # Campos del formulario
        self.cod_repuesto = ft.TextField(label="Código Repuesto", width=300)
        self.descripcion = ft.TextField(label="Descripción", width=300)
        self.precio = ft.TextField(label="Precio Unitario", width=300)

        # Botones
        guardar_btn = ft.ElevatedButton("Guardar", icon=ft.Icons.SAVE, on_click=self.guardar_repuesto)
        volver_btn = ft.ElevatedButton("Volver", icon=ft.Icons.ARROW_BACK, on_click=self.mostrar_repuesto)

        # Renderiza la vista
        self.page.add(
            ft.Column(
                [
                    ft.Text("Alta de Repuesto", size=24, weight="bold"),
                    self.cod_repuesto,
                    self.descripcion,
                    self.precio,
                    ft.Row([guardar_btn, volver_btn], spacing=10),
                ],
                spacing=10,
            )
        )
        self.page.update()


    # ---------- Guardar repuesto en la BD ----------
    def guardar_repuesto(self, e):
        try:
            # Insert SQL
            self.cursor.execute(
                "INSERT INTO repuestos (cod_repuesto, descripcion, pcio_unit) VALUES (%s, %s, %s)",
                (
                    self.cod_repuesto.value,
                    self.descripcion.value,
                    self.precio.value,
                ),
            )
            self.connection.commit()  # confirmar cambios
            # Mensaje de éxito
            self.page.snack_bar = ft.SnackBar(ft.Text("Repuesto guardado correctamente"))
            self.page.snack_bar.open = True
            self.mostrar_repuesto()
        except Exception as ex:
            # Si ocurre error
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error al guardar: {ex}"))
            self.page.snack_bar.open = True
            self.page.update()


    # ---------- Consulta de repuestos ----------
    def consulta_repuesto(self, e):
        self.page.clean()
        self.page.add(ft.Text("Consulta de Repuestos", size=24, weight="bold"))
        self.page.add(self.create_repuesto_table())
        self.page.add(ft.ElevatedButton("Volver", on_click=self.mostrar_repuesto))
        self.page.update()


    # ---------- Imprimir (placeholder) ----------
    def imprimir_repuestos(self, e):
        self.page.snack_bar = ft.SnackBar(ft.Text("Función de impresión no implementada"))
        self.page.snack_bar.open = True
        self.page.update()


    # ---------- Volver al menú ----------
    def volver_al_menu(self, e):
        self.page.clean()
        self.main_menu_callback(self.page)


    # ---------- Crear tabla con todos los repuestos ----------
    def create_repuesto_table(self):
        if not self.cursor:
            print("No hay conexión a la base de datos")
            return ft.Text("No hay conexión a la base de datos")

        # SQL para traer todos los repuestos
        listado_todos_repuestos = """
            SELECT cod_repuesto, descripcion, pcio_unit
            FROM repuestos
            ORDER BY cod_repuesto
        """
        self.cursor.execute(listado_todos_repuestos)
        datos_repuestos = self.cursor.fetchall()

        # Se guarda todo para búsquedas
        self.all_data = datos_repuestos
        rows = self.get_rows(datos_repuestos)

        # Definición de la tabla
        data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Código de Repuesto")),
                ft.DataColumn(ft.Text("Descripción")),
                ft.DataColumn(ft.Text("Precio Unitario")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=rows,
        )
        return data_table


    # ---------- Generar filas de la tabla ----------
    def get_rows(self, repuestos):
        rows = []
        for repuesto in repuestos:
            # Botón eliminar
            eliminar_button = ft.IconButton(
                icon=ft.Icons.DELETE,
                tooltip="Borrar",
                on_click=lambda e, r=repuesto: self.eliminar_repuesto(e, r),
            )
            # Botón actualizar
            actualizar_button = ft.IconButton(
                icon=ft.Icons.EDIT,
                tooltip="Modificar",
                on_click=lambda e, r=repuesto: self.actualizar_repuesto(e, r),
            )

            # Agregar la fila
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(repuesto[0]))),
                        ft.DataCell(ft.Text(repuesto[1])),
                        ft.DataCell(ft.Text(str(repuesto[2]))),
                        ft.DataCell(ft.Row(controls=[eliminar_button, actualizar_button])),
                    ],
                ),
            )
        return rows


    # ---------- Búsqueda ----------
    def search(self, e):
        search_value = self.search_field.value.lower()
        search_column = self.search_column.value

        if not search_value:  # si no hay búsqueda, mostramos todos
            filtered_data = self.all_data
        else:
            # filtrado dinámico
            filtered_data = [
                repuesto for repuesto in self.all_data
                if search_value in str(repuesto[self.get_column_index(search_column)]).lower()
            ]

        # Actualiza filas de tabla
        rows = self.get_rows(filtered_data)
        self.page.controls[2] = self.create_data_table(rows)  # ⚠️ Aquí hay un error: create_data_table no existe
        self.page.update()


    # ---------- Devuelve índice de columna según nombre ----------
    def get_column_index(self, column_name):
        mapping = {
            "cod_repuesto": 0,
            "descripcion": 1,
            "pcio_unit": 2,
        }
        return mapping.get(column_name, 0)


    # ---------- Eliminar repuesto ----------
    def eliminar_repuesto(self, e, repuesto):
        try:
            cod_repuesto = repuesto[0]
            self.cursor.execute("DELETE FROM repuestos WHERE cod_repuesto = %s", (cod_repuesto,))
            self.connection.commit()
            self.page.snack_bar = ft.SnackBar(ft.Text("Repuesto eliminado correctamente"))
            self.page.snack_bar.open = True
            self.mostrar_repuesto()
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error al eliminar: {ex}"))
            self.page.snack_bar.open = True
            self.page.update()


    # ---------- Actualizar repuesto ----------
    def actualizar_repuesto(self, e, repuesto):
        self.page.clean()

        # Cargamos los valores actuales en el formulario
        self.cod_repuesto = ft.TextField(label="Código Repuesto", value=str(repuesto[0]), width=300, disabled=True)
        self.descripcion = ft.TextField(label="Descripción", value=repuesto[1], width=300)
        self.precio = ft.TextField(label="Precio Unitario", value=str(repuesto[2]), width=300)

        # Botones
        guardar_btn = ft.ElevatedButton("Guardar Cambios", icon=ft.Icons.SAVE, on_click=lambda e: self.guardar_cambios_repuesto(e, repuesto))
        volver_btn = ft.ElevatedButton("Volver", icon=ft.Icons.ARROW_BACK, on_click=self.mostrar_repuesto)

        # Renderiza el formulario
        self.page.add(
            ft.Column(
                [
                    ft.Text("Editar Repuesto", size=24, weight="bold"),
                    self.cod_repuesto,
                    self.descripcion,
                    self.precio,
                    ft.Row([guardar_btn, volver_btn], spacing=10),
                ],
                spacing=10,
            )
        )
        self.page.update()


    # ---------- Guardar cambios ----------
    def guardar_cambios_repuesto(self, e, repuesto):
        try:
            # Update SQL
            self.cursor.execute(
                "UPDATE repuestos SET descripcion=%s, pcio_unit=%s WHERE cod_repuesto=%s",
                (
                    self.descripcion.value,
                    self.precio.value,
                    self.cod_repuesto.value,
                ),
            )
            self.connection.commit()
            self.page.snack_bar = ft.SnackBar(ft.Text("Repuesto actualizado correctamente"))
            self.page.snack_bar.open = True
            self.mostrar_repuesto()
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error al actualizar: {ex}"))
            self.page.snack_bar.open = True
            self.page.update()


# ---------- Callbacks de prueba (si se ejecuta solo este archivo) ----------
def main_menu_callback(page: ft.Page):
    page.clean()
    page.add(ft.Text("Menú Principal"))


def main(page: ft.Page):
    app = Herramienta_Repuesto(page, main_menu_callback)
