import reflex as rx
from app.states.dashboard_state import DashboardState


def leaderboard() -> rx.Component:
    return rx.el.div(
        rx.el.h3("Leaderboard", class_name="text-xl font-bold text-gray-800 mb-4"),
        rx.el.div(
            rx.foreach(
                DashboardState.leaderboard_users,
                lambda user: rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.p(
                                f"#{user['rank']}",
                                class_name="text-sm font-bold text-purple-600 w-6 text-center",
                            ),
                            rx.image(
                                src=f"https://api.dicebear.com/9.x/notionists/svg?seed={user['name']}",
                                class_name="h-10 w-10 rounded-full",
                            ),
                            rx.el.p(
                                user["name"],
                                class_name="font-semibold text-gray-800 truncate",
                            ),
                            class_name="flex items-center gap-3 flex-1 min-w-0",
                        ),
                        rx.el.div(
                            rx.el.p(
                                f"₹{user['portfolio_value']:,.2f}",
                                class_name="font-mono font-semibold text-gray-800 text-sm",
                            ),
                            rx.el.p(
                                f"+{user['growth_pct']:.2f}%",
                                class_name="text-sm font-semibold text-green-600",
                            ),
                            class_name="text-right flex-shrink-0",
                        ),
                        class_name="flex items-center justify-between gap-4",
                    ),
                    class_name="p-4 rounded-lg hover:bg-gray-50",
                ),
            ),
            class_name="space-y-2",
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm mt-6",
    )