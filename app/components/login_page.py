import reflex as rx
from reflex_google_auth import google_login
from app.states.auth_state import AuthState


def login_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
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
                "Sign in to start building your virtual portfolio and compete on the leaderboard.",
                class_name="text-gray-500 mt-2 text-center",
            ),
            rx.el.div(
                google_login(on_success=AuthState.on_login),
                class_name="mt-8 flex justify-center",
            ),
        ),
        class_name="max-w-md w-full bg-white p-8 rounded-2xl shadow-lg border border-gray-200",
        style={
            "transform": "translate(-50%, -50%)",
            "position": "absolute",
            "top": "50%",
            "left": "50%",
        },
    )