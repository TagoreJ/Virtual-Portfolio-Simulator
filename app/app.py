import reflex as rx
from app.states.dashboard_state import DashboardState
from app.states.auth_state import AuthState
from app.components.sidebar import sidebar
from app.components.header import header
from app.components.dashboard_page import dashboard_page
from app.components.trade_page import trade_page
from app.components.portfolio_page import portfolio_page
from app.components.leaderboard_page import leaderboard_page
from app.components.login_page import login_page


def dashboard() -> rx.Component:
    def content_area() -> rx.Component:
        return rx.el.main(
            rx.el.div(
                rx.el.h1(
                    DashboardState.active_page,
                    class_name="text-2xl font-bold tracking-tight text-gray-800",
                ),
                rx.match(
                    DashboardState.active_page,
                    ("Dashboard", dashboard_page()),
                    ("Trade", trade_page()),
                    ("Portfolio", portfolio_page()),
                    ("Leaderboard", leaderboard_page()),
                    rx.el.div("Page not found", class_name="p-6 text-red-500"),
                ),
                class_name="p-4 md:p-8",
            ),
            class_name="flex-1 overflow-auto",
        )

    return rx.el.div(
        sidebar(),
        rx.el.div(header(), content_area(), class_name="flex flex-col flex-1"),
        class_name="grid min-h-screen w-full md:grid-cols-[220px_1fr] lg:grid-cols-[280px_1fr]",
    )


def index() -> rx.Component:
    return rx.el.main(
        rx.cond(AuthState.is_authenticated, dashboard(), login_page()),
        class_name="font-['Inter'] bg-gray-50",
        on_mount=AuthState.on_load,
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index)