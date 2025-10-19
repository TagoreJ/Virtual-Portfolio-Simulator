import reflex as rx
from app.states.auth_state import AuthState


def login_page() -> rx.Component:
    return rx.el.div(
        rx.el.form(
            rx.el.div(
                rx.icon(
                    tag="candlestick-chart", class_name="h-10 w-10 text-purple-500"
                ),
                rx.el.h1("TradeSim", class_name="text-3xl font-bold text-gray-800"),
                class_name="flex items-center justify-center gap-3 mb-6",
            ),
            rx.el.h2(
                "Welcome to the Ultimate Stock Trading Simulator",
                class_name="text-2xl font-semibold text-gray-700 text-center",
            ),
            rx.el.p(
                "Enter your name and email to start trading.",
                class_name="text-gray-500 mt-2 text-center mb-6",
            ),
            rx.el.div(
                rx.el.label("Name", class_name="text-sm font-medium text-gray-700"),
                rx.el.input(
                    name="name",
                    placeholder="Your Name",
                    required=True,
                    class_name="w-full mt-1 px-3 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-purple-500",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label("Email", class_name="text-sm font-medium text-gray-700"),
                rx.el.input(
                    name="email",
                    placeholder="your.email@example.com",
                    type="email",
                    required=True,
                    class_name="w-full mt-1 px-3 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-purple-500",
                ),
                class_name="mb-6",
            ),
            rx.el.button(
                "Start Trading",
                type="submit",
                class_name="w-full py-3 rounded-lg bg-purple-600 text-white font-bold text-lg hover:bg-purple-700 transition-colors",
            ),
            class_name="max-w-md w-full bg-white p-8 rounded-2xl shadow-lg border border-gray-200",
            style={
                "transform": "translate(-50%, -50%)",
                "position": "absolute",
                "top": "50%",
                "left": "50%",
            },
            on_submit=AuthState.login,
            reset_on_submit=True,
        )
    )