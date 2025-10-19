import reflex as rx
from app.components.dashboard.overview_cards import overview_cards
from app.components.dashboard.holdings_table import holdings_table
from app.components.dashboard.leaderboard import leaderboard


def dashboard_page() -> rx.Component:
    return rx.el.div(
        overview_cards(),
        rx.el.div(
            rx.el.div(holdings_table(), class_name="lg:col-span-2"),
            leaderboard(),
            class_name="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-6 items-start",
        ),
        class_name="animate-fade-in",
    )