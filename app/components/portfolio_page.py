import reflex as rx
from app.components.portfolio.performance_chart import performance_chart
from app.components.portfolio.sector_allocation_chart import sector_allocation_chart
from app.components.portfolio.watchlist import watchlist
from app.components.dashboard.holdings_table import holdings_table
from app.components.trade_page import transaction_history


def portfolio_page() -> rx.Component:
    return rx.el.div(
        performance_chart(),
        rx.el.div(
            sector_allocation_chart(),
            watchlist(),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6 items-start",
        ),
        holdings_table(),
        transaction_history(),
        class_name="animate-fade-in p-4 md:p-8",
    )