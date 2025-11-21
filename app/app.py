import reflex as rx
from app.states.inventory_state import InventoryState
from app.components.inventory_ui import (
    filter_bar,
    inventory_table,
    items_grid,
    stats_summary,
    empty_state,
)


def upload_section() -> rx.Component:
    """Component for uploading inventory Excel files."""
    return rx.el.div(
        rx.el.h2(
            "Cargar Inventario Diario",
            class_name="text-lg font-semibold text-gray-900 mb-4",
        ),
        rx.el.div(
            rx.upload.root(
                rx.el.div(
                    rx.icon("upload", class_name="h-10 w-10 text-blue-500 mb-3"),
                    rx.el.p(
                        "Arrastra tu archivo Excel aquí o haz clic para seleccionar",
                        class_name="text-sm text-gray-600 font-medium",
                    ),
                    rx.el.p(
                        "Soporta .xlsx (Columnas requeridas: sku, descripcion, familia, existencia)",
                        class_name="text-xs text-gray-400 mt-1",
                    ),
                    class_name="flex flex-col items-center justify-center p-10 border-2 border-dashed border-blue-200 rounded-xl bg-blue-50 hover:bg-blue-100 transition-colors cursor-pointer",
                ),
                id="upload_excel",
                multiple=False,
                accept={
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [
                        ".xlsx"
                    ],
                    "application/vnd.ms-excel": [".xls"],
                },
                border="0px",
                padding="0px",
            ),
            rx.el.div(
                rx.el.button(
                    rx.cond(
                        InventoryState.is_uploading,
                        rx.fragment(
                            rx.spinner(size="2", class_name="mr-2"), "Procesando..."
                        ),
                        rx.fragment(
                            rx.icon("save", class_name="mr-2 h-4 w-4"),
                            "Subir y Procesar",
                        ),
                    ),
                    on_click=InventoryState.handle_upload(
                        rx.upload_files(upload_id="upload_excel")
                    ),
                    disabled=InventoryState.is_uploading,
                    class_name="mt-4 w-full flex justify-center items-center py-2.5 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed",
                ),
                class_name="mt-2",
            ),
            class_name="w-full max-w-xl",
        ),
        class_name="bg-white p-6 rounded-xl shadow-sm border border-gray-200 mb-8",
    )


def special_families_section() -> rx.Component:
    """Component for creating special families."""
    return rx.el.div(
        rx.el.h2(
            "Crear Familia Especial",
            class_name="text-lg font-semibold text-gray-900 mb-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "Nombre de la Nueva Familia",
                    class_name="block text-sm font-medium text-gray-700 mb-1",
                ),
                rx.el.input(
                    placeholder="Ej. Ofertas Verano",
                    on_change=InventoryState.set_new_family_name,
                    class_name="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500",
                    default_value=InventoryState.new_family_name,
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "SKUs (separados por coma)",
                    class_name="block text-sm font-medium text-gray-700 mb-1",
                ),
                rx.el.textarea(
                    placeholder="Ej. SKU001, SKU002, SKU003...",
                    on_change=InventoryState.set_new_family_skus,
                    class_name="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 min-h-[100px]",
                    default_value=InventoryState.new_family_skus,
                ),
                class_name="mb-4",
            ),
            rx.el.button(
                "Crear Familia",
                on_click=InventoryState.create_special_family,
                class_name="w-full md:w-auto px-4 py-2 bg-gray-900 text-white rounded-lg hover:bg-gray-800 font-medium transition-colors",
            ),
            class_name="max-w-xl",
        ),
        class_name="bg-white p-6 rounded-xl shadow-sm border border-gray-200",
    )


def config_page() -> rx.Component:
    """Main configuration page layout."""
    return rx.el.div(
        rx.el.header(
            rx.el.div(
                rx.el.div(
                    rx.el.a(
                        rx.icon("arrow-left", class_name="h-5 w-5 mr-2"),
                        "Volver al Inicio",
                        href="/",
                        class_name="flex items-center text-gray-600 hover:text-gray-900 font-medium transition-colors",
                    ),
                    class_name="flex items-center mr-4",
                ),
                rx.el.h1(
                    "Configuración del Sistema",
                    class_name="text-xl font-bold text-gray-900",
                ),
                class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex items-center",
            ),
            class_name="bg-white shadow-sm border-b border-gray-200",
        ),
        rx.el.main(
            rx.el.div(
                rx.cond(
                    InventoryState.error_message != "",
                    rx.el.div(
                        rx.el.div(
                            rx.icon(
                                "badge_alert", class_name="h-5 w-5 text-red-400 mr-2"
                            ),
                            rx.el.span(InventoryState.error_message),
                            class_name="flex items-center",
                        ),
                        class_name="bg-red-50 border-l-4 border-red-400 p-4 mb-6 rounded-r-md text-red-700",
                    ),
                ),
                rx.cond(
                    InventoryState.success_message != "",
                    rx.el.div(
                        rx.el.div(
                            rx.icon(
                                "check_check", class_name="h-5 w-5 text-green-400 mr-2"
                            ),
                            rx.el.span(InventoryState.success_message),
                            class_name="flex items-center",
                        ),
                        class_name="bg-green-50 border-l-4 border-green-400 p-4 mb-6 rounded-r-md text-green-700",
                    ),
                ),
                upload_section(),
                special_families_section(),
                class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8",
            ),
            class_name="flex-1 bg-gray-50 min-h-[calc(100vh-88px)]",
        ),
        class_name="font-['Inter'] min-h-screen flex flex-col bg-gray-50",
    )


def index() -> rx.Component:
    return rx.el.div(
        rx.el.header(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon("box", class_name="h-8 w-8 text-blue-600 mr-3"),
                        rx.el.h1(
                            "Consulta de Existencias",
                            class_name="text-2xl font-bold text-gray-900",
                        ),
                        class_name="flex items-center",
                    ),
                    rx.el.p(
                        "Sistema de Control de Inventario",
                        class_name="text-sm text-gray-500 mt-1",
                    ),
                    class_name="flex flex-col",
                ),
                rx.el.a(
                    rx.el.button(
                        rx.icon("settings", class_name="h-5 w-5 mr-2"),
                        "Configuración",
                        class_name="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500",
                    ),
                    href="/config",
                    class_name="hidden md:block",
                ),
                class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex justify-between items-center",
            ),
            class_name="bg-white shadow-sm border-b border-gray-200",
        ),
        rx.el.main(
            rx.el.div(
                rx.cond(
                    InventoryState.error_message != "",
                    rx.el.div(
                        rx.el.div(
                            rx.icon(
                                "badge_alert", class_name="h-5 w-5 text-red-400 mr-2"
                            ),
                            rx.el.span(InventoryState.error_message),
                            class_name="flex items-center",
                        ),
                        class_name="bg-red-50 border-l-4 border-red-400 p-4 mb-6 rounded-r-md text-red-700",
                    ),
                ),
                filter_bar(),
                stats_summary(),
                rx.cond(
                    InventoryState.is_loading,
                    rx.el.div(
                        rx.spinner(size="3", class_name="text-blue-600"),
                        rx.el.p(
                            "Cargando inventario...",
                            class_name="mt-4 text-gray-500 font-medium",
                        ),
                        class_name="flex flex-col items-center justify-center py-20",
                    ),
                    rx.cond(
                        InventoryState.filtered_items.length() > 0,
                        rx.el.div(
                            inventory_table(), items_grid(), class_name="space-y-4"
                        ),
                        empty_state(),
                    ),
                ),
                class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8",
            ),
            class_name="flex-1 bg-gray-50 min-h-[calc(100vh-88px)]",
        ),
        class_name="font-['Inter'] min-h-screen flex flex-col bg-gray-50",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, route="/", on_load=InventoryState.load_data)
app.add_page(config_page, route="/config")