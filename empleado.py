import flet as ft          # Importamos Flet para construir la interfaz gráfica
import mysql.connector     # Importamos conector de MySQL para manejar la base de datos


# ---------- Conexión a la base de datos ----------
def connect_to_db():
    try:
        # Intentamos conectar a la base Taller_Mecanico en localhost
        connection = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="root",
            database="Taller_Mecanico",
            ssl_disabled=True
        )
        if connection.is_connected():   # Si la conexión es exitosa, lo informamos
            print("Conexión exitosa")
            return connection
    except Exception as ex:              # Si falla, mostramos error
        print("Conexión errónea")
        print(ex)
        return None


# ---------- Clase principal para gestión de empleados ----------
class Herramienta_Empleado:
    def __init__(self, page: ft.Page, main_menu_callback):
        # Guardamos referencia a la página principal y al callback para volver al menú
        self.page = page
        self.main_menu_callback = main_menu_callback

        # Conexión y cursor de base de datos
        self.connection = connect_to_db()
        self.cursor = self.connection.cursor() if self.connection else None

        # Campo de búsqueda de empleados
        self.search_field = ft.TextField(label="Buscar", width=300, on_change=self.search)

        # Dropdown para elegir en qué columna buscar (apellido, dni, etc.)
        self.search_column = ft.Dropdown(
            options=[
                ft.dropdown.Option("legajo"),
                ft.dropdown.Option("apellido"),
                ft.dropdown.Option("nombre"),
                ft.dropdown.Option("dni"),
                ft.dropdown.Option("direccion"),
                ft.dropdown.Option("telefono"),
            ],
            value="apellido",   # búsqueda por defecto en "apellido"
            width=200,
            on_change=self.search,
        )

        # Apenas se instancia, se muestra la pantalla de empleados
        self.mostrar_empleado()


    # ---------- Pantalla principal de empleados ----------
    def mostrar_empleado(self):
        self.page.clean()  # limpiamos pantalla para mostrar nuevo contenido

        # Encabezado con botones de navegación
        header = ft.Row(
            controls=[
                ft.Text("Gestión de Empleados", size=20, weight="bold"),
                ft.ElevatedButton(text="Alta", on_click=self.alta_empleado),     # Alta de empleados
                ft.ElevatedButton(text="Consulta", on_click=self.consulta_empleado), # Consulta
                ft.ElevatedButton(text="Imprimir", on_click=self.imprimir_empleados), # Imprimir
                ft.ElevatedButton(text="Volver al Menú", on_click=self.volver_al_menu), # Volver menú principal
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        # Fila con búsqueda (dropdown + campo de texto)
        search_row = ft.Row(
            [self.search_column, self.search_field],
            alignment=ft.MainAxisAlignment.START,
        )

        # Generamos tabla con los datos de empleados
        self.data_table = self.create_empleado_table()

        # Agregamos todo en la página
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


    # ---------- Alta de empleados ----------
    def alta_empleado(self, e):
        self.page.clean()

        # Campos de entrada
        self.legajo = ft.TextField(label="Legajo", width=300)
        self.dni = ft.TextField(label="DNI", width=300)
        self.apellido = ft.TextField(label="Apellido", width=300)
        self.nombre = ft.TextField(label="Nombre", width=300)
        self.direccion = ft.TextField(label="Dirección", width=300)
        self.telefono = ft.TextField(label="Teléfono", width=300)

        # Botones
        guardar_btn = ft.ElevatedButton("Guardar", icon=ft.Icons.SAVE, on_click=self.guardar_empleado)
        volver_btn = ft.ElevatedButton("Volver", icon=ft.Icons.ARROW_BACK, on_click=self.mostrar_empleado)

        # Construcción de formulario
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


    # ---------- Guardar nuevo empleado ----------
    def guardar_empleado(self, e):
        try:
            # Primero insertamos en persona
            self.cursor.execute(
                "INSERT INTO persona (dni, apellido, nombre, direccion, tele_contac) VALUES (%s, %s, %s, %s, %s)",
                (self.dni.value, self.apellido.value, self.nombre.value, self.direccion.value, self.telefono.value),
            )

            # Luego insertamos en empleado (relación con persona por dni)
            self.cursor.execute(
                "INSERT INTO empleado (legajo, dni) VALUES (%s, %s)",
                (self.legajo.value, self.dni.value),
            )

            self.connection.commit()  # confirmamos cambios
            self.page.snack_bar = ft.SnackBar(ft.Text("Empleado guardado correctamente"))
            self.page.snack_bar.open = True
            self.mostrar_empleado()  # recargamos vista
        except Exception as ex:
            # En caso de error, mostramos notificación
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error al guardar: {ex}"))
            self.page.snack_bar.open = True
            self.page.update()


    # ---------- Consulta de empleados ----------
    def consulta_empleado(self, e):
        self.page.clean()
        self.page.add(ft.Text("Consulta de Empleados", size=24, weight="bold"))
        self.page.add(self.create_empleado_table())
        self.page.add(ft.ElevatedButton("Volver", on_click=self.mostrar_empleado))
        self.page.update()


    # ---------- Imprimir empleados (placeholder) ----------
    def imprimir_empleados(self, e):
        self.page.snack_bar = ft.SnackBar(ft.Text("Función de impresión no implementada"))
        self.page.snack_bar.open = True
        self.page.update()


    # ---------- Volver al menú principal ----------
    def volver_al_menu(self, e):
        self.page.clean()
        self.main_menu_callback(self.page)


    # ---------- Crear tabla de empleados ----------
    def create_empleado_table(self):
        if not self.cursor:
            print("No hay conexión a la base de datos")
            return ft.Text("No hay conexión a la base de datos")

        # Consulta que une persona con empleado
        listado_todos_empleados = """
            SELECT per.apellido, per.nombre, per.dni, per.direccion, per.tele_contac, emp.legajo
            FROM persona per INNER JOIN empleado emp ON per.dni = emp.dni
            ORDER BY per.apellido
        """
        self.cursor.execute(listado_todos_empleados)
        datos_empleados = self.cursor.fetchall()
        self.all_data = datos_empleados

        # Convertimos datos a filas
        rows = self.get_rows(datos_empleados)

        # Definición de tabla
        data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Apellido")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("DNI")),
                ft.DataColumn(ft.Text("Dirección")),
                ft.DataColumn(ft.Text("Teléfono")),
                ft.DataColumn(ft.Text("Legajo")),
                ft.DataColumn(ft.Text("Acciones")), # botones de acción
            ],
            rows=rows,
        )
        return data_table


    # ---------- Generar filas de la tabla ----------
    def get_rows(self, empleados):
        rows = []
        for empleado in empleados:
            # Botón eliminar
            eliminar_button = ft.IconButton(
                icon=ft.Icons.DELETE,
                tooltip="Borrar",
                on_click=lambda e, emp=empleado: self.eliminar_empleado(e, emp),
            )
            # Botón actualizar
            actualizar_button = ft.IconButton(
                icon=ft.Icons.EDIT,
                tooltip="Modificar",
                on_click=lambda e, emp=empleado: self.actualizar_empleado(e, emp),
            )

            # Fila completa
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


    # ---------- Buscar empleados ----------
    def search(self, e):
        search_term = self.search_field.value.lower()   # lo que escribe el usuario
        search_column = self.search_column.value        # columna seleccionada
        filtered_data = []

        # Filtramos según columna seleccionada
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

        # Actualizamos tabla con los resultados filtrados
        self.data_table.rows = self.get_rows(filtered_data)
        self.page.update()


    # ---------- Eliminar empleado ----------
    def eliminar_empleado(self, e, empleado):
        try:
            dni = empleado[2]
            legajo = empleado[5]

            # Eliminamos de empleado y persona
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


    # ---------- Editar empleado ----------
    def actualizar_empleado(self, e, empleado):
        self.page.clean()

        # Campos con valores precargados
        self.legajo = ft.TextField(label="Legajo", value=str(empleado[5]), width=300, disabled=True)
        self.dni = ft.TextField(label="DNI", value=str(empleado[2]), width=300, disabled=True)
        self.apellido = ft.TextField(label="Apellido", value=empleado[0], width=300)
        self.nombre = ft.TextField(label="Nombre", value=empleado[1], width=300)
        self.direccion = ft.TextField(label="Dirección", value=empleado[3], width=300)
        self.telefono = ft.TextField(label="Teléfono", value=empleado[4], width=300)

        # Botones
        guardar_btn = ft.ElevatedButton("Guardar Cambios", icon=ft.Icons.SAVE,
                                        on_click=lambda e: self.guardar_cambios_empleado(e, empleado))
        volver_btn = ft.ElevatedButton("Volver", icon=ft.Icons.ARROW_BACK, on_click=self.mostrar_empleado)

        # Construcción de formulario
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


    # ---------- Guardar cambios de edición ----------
    def guardar_cambios_empleado(self, e, empleado):
        try:
            # Solo actualizamos datos de persona (apellido, nombre, etc.)
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
