import reflex as rx
from app.states.auth_state import AuthState


def header() -> rx.Component:
    return rx.el.header(
        rx.el.div(class_name="w-full flex-1"),
        rx.el.div(
            rx.cond(
                AuthState.is_authenticated,
                rx.el.div(
                    rx.el.p(
                        AuthState.user["name"],
                        class_name="text-sm font-semibold text-gray-700",
                    ),
                    rx.image(
                        src=AuthState.user["avatar_url"],
                        class_name="h-9 w-9 rounded-full border-2 border-purple-200",
                    ),
                    rx.el.button(
                        rx.icon(tag="log-out", class_name="h-5 w-5 text-gray-500"),
                        on_click=AuthState.logout,
                        class_name="p-2 rounded-full hover:bg-gray-200",
                        title="Logout",
                    ),
                    class_name="flex items-center gap-3",
                ),
                rx.el.div(),
            ),
            class_name="flex items-center gap-4 md:ml-auto md:gap-2 lg:gap-4",
        ),
        class_name="flex h-14 items-center gap-4 border-b bg-gray-100/40 px-4 lg:h-[60px] lg:px-6",
    )