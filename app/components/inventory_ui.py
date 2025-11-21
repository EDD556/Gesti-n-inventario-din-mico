import reflex as rx
from app.states.inventory_state import InventoryState, InventoryItem


def status_badge(stock: int) -> rx.Component:
    """Return a colored badge based on stock level."""
    return rx.cond(
        stock > 10,
        rx.el.span(
            "En Stock",
            class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-100 text-emerald-800",
        ),
        rx.cond(
            stock > 0,
            rx.el.span(
                "Bajo Stock",
                class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800",
            ),
            rx.el.span(
                "Agotado",
                class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800",
            ),
        ),
    )


def filter_bar() -> rx.Component:
    """Component for filtering inventory."""
    return rx.el.div(
        rx.el.div(
            rx.el.label(
                "Fecha", class_name="block text-sm font-medium text-gray-700 mb-1"
            ),
            rx.el.input(
                type="date",
                on_change=InventoryState.set_date,
                class_name="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors",
                default_value=InventoryState.selected_date,
            ),
            class_name="w-full md:w-48",
        ),
        rx.el.div(
            rx.el.label(
                "Buscar SKU / Descripción",
                class_name="block text-sm font-medium text-gray-700 mb-1",
            ),
            rx.el.div(
                rx.icon(
                    "search",
                    class_name="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400",
                ),
                rx.el.input(
                    placeholder="Ej. SKU-123...",
                    on_change=InventoryState.set_search_sku,
                    class_name="w-full pl-10 pr-4 py-2 bg-white border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors",
                    default_value=InventoryState.search_sku,
                ),
                class_name="relative",
            ),
            class_name="w-full md:flex-1",
        ),
        rx.el.div(
            rx.el.label(
                "Familia", class_name="block text-sm font-medium text-gray-700 mb-1"
            ),
            rx.el.select(
                rx.foreach(InventoryState.families, lambda f: rx.el.option(f, value=f)),
                value=InventoryState.selected_family,
                on_change=InventoryState.set_selected_family,
                class_name="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors",
            ),
            class_name="w-full md:w-64",
        ),
        class_name="flex flex-col md:flex-row gap-4 p-4 bg-white rounded-xl shadow-sm border border-gray-100 mb-6",
    )


def inventory_card(item: InventoryItem) -> rx.Component:
    """Mobile card view for an inventory item."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    item.sku,
                    class_name="text-xs font-bold tracking-wider text-gray-500 uppercase",
                ),
                status_badge(item.existencia),
                class_name="flex justify-between items-start mb-2",
            ),
            rx.el.h3(
                item.descripcion,
                class_name="text-base font-semibold text-gray-900 mb-1 line-clamp-2",
            ),
            rx.el.p(item.familia, class_name="text-sm text-gray-500 mb-3"),
            rx.el.div(
                rx.el.div(
                    rx.el.span("Existencia", class_name="text-xs text-gray-500"),
                    rx.el.span(
                        item.existencia, class_name="text-lg font-bold text-gray-900"
                    ),
                    class_name="flex flex-col",
                ),
                class_name="flex items-center pt-3 border-t border-gray-100",
            ),
            class_name="p-4",
        ),
        class_name="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow",
    )


def inventory_row(item: InventoryItem) -> rx.Component:
    """Desktop table row."""
    return rx.el.tr(
        rx.el.td(
            rx.el.span(item.sku, class_name="font-medium text-gray-900"),
            class_name="px-6 py-4 whitespace-nowrap text-sm",
        ),
        rx.el.td(
            rx.el.span(item.descripcion, class_name="text-gray-900"),
            class_name="px-6 py-4 text-sm",
        ),
        rx.el.td(
            rx.el.span(
                item.familia,
                class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-sm",
        ),
        rx.el.td(
            rx.el.span(item.existencia, class_name="font-semibold text-gray-900"),
            class_name="px-6 py-4 whitespace-nowrap text-sm text-right",
        ),
        rx.el.td(
            status_badge(item.existencia),
            class_name="px-6 py-4 whitespace-nowrap text-sm text-center",
        ),
        class_name="hover:bg-gray-50 transition-colors border-b border-gray-100 last:border-0",
    )


def inventory_table() -> rx.Component:
    """Desktop table view."""
    return rx.el.div(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    rx.el.th(
                        "SKU",
                        class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                    ),
                    rx.el.th(
                        "Descripción",
                        class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                    ),
                    rx.el.th(
                        "Familia",
                        class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                    ),
                    rx.el.th(
                        "Existencia",
                        class_name="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider",
                    ),
                    rx.el.th(
                        "Estado",
                        class_name="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider",
                    ),
                ),
                class_name="bg-gray-50 border-b border-gray-200",
            ),
            rx.el.tbody(
                rx.foreach(InventoryState.filtered_items, inventory_row),
                class_name="bg-white divide-y divide-gray-200",
            ),
            class_name="min-w-full divide-y divide-gray-200",
        ),
        class_name="hidden md:block bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden",
    )


def items_grid() -> rx.Component:
    """Mobile grid view."""
    return rx.el.div(
        rx.foreach(InventoryState.filtered_items, inventory_card),
        class_name="md:hidden grid grid-cols-1 gap-4",
    )


def stats_summary() -> rx.Component:
    """Summary statistics."""
    return rx.el.div(
        rx.el.div(
            rx.el.span("Total Items", class_name="text-sm font-medium text-gray-500"),
            rx.el.span(
                InventoryState.total_items,
                class_name="text-2xl font-bold text-gray-900 mt-1",
            ),
            class_name="bg-white p-4 rounded-xl shadow-sm border border-gray-100 flex flex-col",
        ),
        rx.el.div(
            rx.el.span(
                "Total Existencias", class_name="text-sm font-medium text-gray-500"
            ),
            rx.el.span(
                InventoryState.total_stock,
                class_name="text-2xl font-bold text-blue-600 mt-1",
            ),
            class_name="bg-white p-4 rounded-xl shadow-sm border border-gray-100 flex flex-col",
        ),
        class_name="grid grid-cols-2 gap-4 mb-6",
    )


def empty_state() -> rx.Component:
    """Shown when no items are found."""
    return rx.el.div(
        rx.icon("package-open", class_name="h-12 w-12 text-gray-300 mb-3"),
        rx.el.h3(
            "No se encontraron productos",
            class_name="text-lg font-medium text-gray-900",
        ),
        rx.el.p(
            "Intenta ajustar los filtros o seleccionar otra fecha.",
            class_name="text-gray-500 text-center max-w-xs",
        ),
        class_name="flex flex-col items-center justify-center py-12 px-4 bg-white rounded-xl border border-gray-200 border-dashed",
    )