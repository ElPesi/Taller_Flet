import flet as ft
import mysql.connector

# ---------- Conexión a la base de datos ----------
def connect_to_db():
    try:
        # Se conecta al servidor MySQL, a la base "Taller_Mecanico"
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
        # Si falla la conexión, mostramos el error
        print("Conexión errónea")
        print(ex)
        return None


# ---------- Clase para gestionar los presupuestos ----------
class Herramienta_Presupuesto:
    def __init__(self, page: ft.Page, main_menu_callback):
        # Guardamos la referencia a la página de Flet y al callback del menú principal
        self.page = page
        self.main_menu_callback = main_menu_callback

        # Creamos conexión + cursor SQL
        self.connection = connect_to_db()
        self.cursor = self.connection.cursor() if self.connection else None

        # Barra de búsqueda (texto + columna seleccionada)
        self.search_field = ft.TextField(label="Buscar", width=300, on_change=self.search)
        self.search_column = ft.Dropdown(
            options=[
                ft.dropdown.Option("nro_presupuesto"),
                ft.dropdown.Option("cod_cliente"),
                ft.dropdown.Option("descripcion"),
                ft.dropdown.Option("total_presupuesto"),
                ft.dropdown.Option("total_gastado"),
            ],
            value="nro_presupuesto",  # columna de búsqueda por defecto
            width=200,
            on_change=self.search,
        )

        # Al iniciar, mostramos la pantalla principal
        self.mostrar_presupuesto()


    # ---------- Pantalla principal ----------
    def mostrar_presupuesto(self):
        self.page.clean()  # limpiamos la UI

        # Fila de botones principales
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

        # Barra de búsqueda
        search_row = ft.Row([self.search_column, self.search_field], alignment=ft.MainAxisAlignment.START)

        # Creamos tabla + obtenemos totales de presupuestos y gastos
        self.data_table, total_presupuesto, total_gastado = self.create_presupuesto_table()

        # Agregamos todo al layout
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
                ),
                padding=20,
            )
        )


    # ---------- Formulario de alta ----------
    def alta_presupuesto(self, e):
        self.page.clean()

        # Campos para crear un nuevo presupuesto
        self.nro_presupuesto = ft.TextField(label="Nro Presupuesto", width=300)
        self.cod_cliente = ft.TextField(label="Código Cliente", width=300)
        self.descripcion = ft.TextField(label="Descripción", width=300)
        self.total_presupuesto = ft.TextField(label="Total Presupuesto", width=300)
        self.total_gastado = ft.TextField(label="Total Gastado", width=300)

        # Botones
        guardar_btn = ft.ElevatedButton("Guardar", icon=ft.Icons.SAVE, on_click=self.guardar_presupuesto)
        volver_btn = ft.ElevatedButton("Volver", icon=ft.Icons.ARROW_BACK, on_click=self.mostrar_presupuesto)

        # Armamos formulario
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
            )
        )
        self.page.update()


    # ---------- Guardar nuevo presupuesto ----------
    def guardar_presupuesto(self, e):
        try:
            # Insertamos en la tabla
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
            self.connection.commit()  # confirmamos cambios en BD
            self.page.snack_bar = ft.SnackBar(ft.Text("Presupuesto guardado correctamente"))
            self.page.snack_bar.open = True
            self.mostrar_presupuesto()
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error al guardar: {ex}"))
            self.page.snack_bar.open = True
            self.page.update()


    # ---------- Consulta de presupuestos ----------
    def consulta_presupuesto(self, e):
        self.page.clean()
        data_table, total_presupuesto, total_gastado = self.create_presupuesto_table()
        self.page.add(ft.Text("Consulta de Presupuestos", size=24, weight="bold"))
        self.page.add(ft.Text(f"Total Presupuestado: ${total_presupuesto}", size=16, weight="bold"))
        self.page.add(ft.Text(f"Total Gastado: ${total_gastado}", size=16, weight="bold"))
        self.page.add(data_table)
        self.page.add(ft.ElevatedButton("Volver", on_click=self.mostrar_presupuesto))
        self.page.update()


    # ---------- Imprimir (placeholder) ----------
    def imprimir_presupuestos(self, e):
        self.page.snack_bar = ft.SnackBar(ft.Text("Función de impresión no implementada"))
        self.page.snack_bar.open = True
        self.page.update()


    # ---------- Volver al menú ----------
    def volver_al_menu(self, e):
        self.page.clean()
        self.main_menu_callback(self.page)


    # ---------- Crear tabla con todos los presupuestos ----------
    def create_presupuesto_table(self, data=None):
        if not self.cursor:
            return ft.Text("No hay conexión a la base de datos"), 0, 0

        # Si no recibimos datos filtrados, traemos todos
        if data is None:
            self.cursor.execute(
                "SELECT nro_presupuesto, cod_cliente, descripcion, total_presupuesto, total_gastado FROM presupuesto ORDER BY nro_presupuesto"
            )
            datos_presupuestos = self.cursor.fetchall()
        else:
            datos_presupuestos = data

        # Variables para calcular totales
        total_presupuesto = 0
        total_gastado = 0
        rows = []

        # Recorremos cada presupuesto
        for presupuesto in datos_presupuestos:
            total_presupuesto += float(presupuesto[3] or 0)
            total_gastado += float(presupuesto[4] or 0)

            # Botones por fila (editar / borrar)
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

            # Fila de la tabla
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

        # Construcción de la tabla
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


    # ---------- Eliminar presupuesto ----------
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


    # ---------- Editar presupuesto ----------
    def actualizar_presupuesto(self, e, presupuesto):
        self.page.clean()

        # Campos precargados con datos actuales
        self.nro_presupuesto = ft.TextField(label="Nro Presupuesto", value=str(presupuesto[0]), width=300, disabled=True)
        self.cod_cliente = ft.TextField(label="Código Cliente", value=str(presupuesto[1]), width=300)
        self.descripcion = ft.TextField(label="Descripción", value=presupuesto[2], width=300)
        self.total_presupuesto = ft.TextField(label="Total Presupuesto", value=str(presupuesto[3]), width=300)
        self.total_gastado = ft.TextField(label="Total Gastado", value=str(presupuesto[4]), width=300)

        # Botones
        guardar_btn = ft.ElevatedButton("Guardar Cambios", icon=ft.Icons.SAVE,
                                        on_click=lambda e: self.guardar_cambios_presupuesto(e, presupuesto))
        volver_btn = ft.ElevatedButton("Volver", icon=ft.Icons.ARROW_BACK, on_click=self.mostrar_presupuesto)

        # Formulario edición
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
            )
        )
        self.page.update()


    # ---------- Guardar cambios en presupuesto ----------
    def guardar_cambios_presupuesto(self, e, presupuesto):
        try:
            # Ejecutamos UPDATE
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


    # ---------- Buscar presupuestos ----------
    def search(self, e):
        search_term = self.search_field.value.lower()
        search_column = self.search_column.value
        filtered_data = []

        # Filtrado según columna seleccionada
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

        # Actualizamos tabla con datos filtrados
        self.data_table, total_presupuesto, total_gastado = self.create_presupuesto_table(filtered_data)
        self.page.update()
