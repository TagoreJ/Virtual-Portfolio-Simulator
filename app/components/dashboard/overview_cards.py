import reflex as rx
from app.states.dashboard_state import DashboardState


def stat_card(
    label: str,
    value: rx.Var[str],
    change: rx.Var[str],
    change_color: str,
    icon_name: str,
    icon_color: str,
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(label, class_name="text-sm font-medium text-gray-500"),
                rx.el.div(
                    rx.icon(tag=icon_name, class_name=f"h-5 w-5 {icon_color}"),
                    class_name=f"p-2 rounded-md {icon_color.replace('text', 'bg').replace('-500', '-100')}",
                ),
                class_name="flex justify-between items-center",
            ),
            rx.el.p(value, class_name="text-2xl font-bold text-gray-800 mt-2"),
            rx.el.div(
                rx.el.span(change, class_name=f"text-xs font-semibold {change_color}"),
                class_name="flex items-center gap-1 mt-1",
            ),
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm hover:shadow-lg transition-shadow duration-300",
    )


def overview_cards() -> rx.Component:
    return rx.el.div(
        stat_card(
            "Portfolio Value",
            f"₹{DashboardState.portfolio_value:,.2f}",
            f"{rx.cond(DashboardState.day_change >= 0, '+', '')}{DashboardState.day_change:,.2f} ({DashboardState.day_change_pct:.2f}%) Today",
            rx.cond(DashboardState.day_change >= 0, "text-green-600", "text-red-600"),
            "wallet",
            "text-purple-500",
        ),
        stat_card(
            "Total P&L",
            f"₹{DashboardState.total_pl:,.2f}",
            f"{rx.cond(DashboardState.total_pl_pct >= 0, '+', '')}{DashboardState.total_pl_pct:.2f}% All Time",
            rx.cond(DashboardState.total_pl >= 0, "text-green-600", "text-red-600"),
            "trending-up",
            "text-green-500",
        ),
        stat_card(
            "Available Cash",
            f"₹{DashboardState.available_cash:,.2f}",
            "Ready to Invest",
            "text-gray-500",
            "landmark",
            "text-blue-500",
        ),
        class_name="grid gap-4 md:grid-cols-2 lg:grid-cols-3",
    )