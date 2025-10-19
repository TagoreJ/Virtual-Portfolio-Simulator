import reflex as rx
from app.states.dashboard_state import DashboardState


def get_badge(rank: rx.Var[int]) -> rx.Component:
    return rx.match(
        rank,
        (
            1,
            rx.el.div(
                rx.icon("award", class_name="text-amber-400"),
                class_name="bg-amber-100 p-2 rounded-full",
            ),
        ),
        (
            2,
            rx.el.div(
                rx.icon("award", class_name="text-gray-400"),
                class_name="bg-gray-100 p-2 rounded-full",
            ),
        ),
        (
            3,
            rx.el.div(
                rx.icon("award", class_name="text-orange-400"),
                class_name="bg-orange-100 p-2 rounded-full",
            ),
        ),
        rx.el.div(
            f"#{rank}",
            class_name="w-10 h-10 flex items-center justify-center font-bold text-lg text-gray-500",
        ),
    )


def leaderboard_card(user: rx.Var) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            get_badge(user["rank"]),
            rx.image(
                src=f"https://api.dicebear.com/9.x/notionists/svg?seed={user['name']}",
                class_name="w-12 h-12 rounded-full border-2 border-white shadow-md",
            ),
            rx.el.div(
                rx.el.p(user["name"], class_name="font-bold text-lg text-gray-800"),
                rx.el.div(
                    rx.el.p(
                        f"₹{user['portfolio_value']:,.2f}",
                        class_name="font-mono font-semibold text-purple-600 text-base",
                    ),
                    rx.el.p(
                        f"{user['growth_pct']:.2f}%",
                        class_name="text-sm font-semibold text-green-600 flex items-center gap-1",
                    ),
                    class_name="flex items-baseline gap-2",
                ),
            ),
            class_name="flex items-center gap-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p("Best Trade", class_name="text-xs text-gray-500"),
                rx.el.p(
                    "+55% on INFY.NS", class_name="text-sm font-semibold text-green-600"
                ),
                class_name="text-center",
            ),
            rx.el.div(
                rx.el.p("Trades", class_name="text-xs text-gray-500"),
                rx.el.p("128", class_name="text-sm font-semibold text-gray-700"),
                class_name="text-center",
            ),
            rx.el.div(
                rx.el.p("Win Rate", class_name="text-xs text-gray-500"),
                rx.el.p("72%", class_name="text-sm font-semibold text-gray-700"),
                class_name="text-center",
            ),
            class_name="grid grid-cols-3 gap-4 border-t border-gray-100 pt-4 mt-4",
        ),
        class_name="bg-white p-5 rounded-2xl border border-gray-200 shadow-sm hover:shadow-lg transition-shadow duration-300",
    )


def leaderboard_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1("Leaderboard", class_name="text-3xl font-bold text-gray-900"),
            rx.el.p(
                "See who's on top of the trading game.", class_name="text-gray-500 mt-1"
            ),
            class_name="mb-8 text-center",
        ),
        rx.el.div(
            rx.foreach(DashboardState.leaderboard_users, leaderboard_card),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
        ),
        class_name="animate-fade-in p-4 md:p-8 max-w-7xl mx-auto",
    )