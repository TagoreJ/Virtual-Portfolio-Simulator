import reflex as rx
from app.states.dashboard_state import DashboardState


def sidebar_link(text: str, icon: str, is_active: bool) -> rx.Component:
    return rx.el.a(
        rx.el.div(
            rx.icon(tag=icon, class_name="w-5 h-5"),
            rx.el.span(text, class_name="text-sm font-medium"),
            class_name=rx.cond(
                is_active,
                "flex items-center gap-3 rounded-lg px-3 py-2 text-white bg-purple-600 transition-all",
                "flex items-center gap-3 rounded-lg px-3 py-2 text-gray-400 transition-all hover:text-gray-200",
            ),
        ),
        on_click=lambda: DashboardState.set_active_page(text),
        href="#",
    )


def sidebar() -> rx.Component:
    nav_items = [
        ("Dashboard", "layout-grid"),
        ("Trade", "arrow-right-left"),
        ("Portfolio", "pie-chart"),
        ("Leaderboard", "trophy"),
    ]
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(tag="candlestick-chart", class_name="h-8 w-8 text-purple-400"),
                rx.el.span("TradeSim", class_name="text-lg font-bold text-white"),
                class_name="flex items-center gap-2",
            ),
            class_name="flex h-14 items-center border-b border-gray-700 px-4 lg:h-[60px] lg:px-6",
        ),
        rx.el.div(
            rx.el.nav(
                rx.foreach(
                    nav_items,
                    lambda item: sidebar_link(
                        item[0], item[1], DashboardState.active_page == item[0]
                    ),
                ),
                class_name="flex flex-col gap-2",
            ),
            class_name="flex-1 p-4",
        ),
        class_name="hidden border-r border-gray-800 bg-gray-900 md:block",
    )