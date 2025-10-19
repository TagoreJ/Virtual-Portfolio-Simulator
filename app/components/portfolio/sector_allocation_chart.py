import reflex as rx
from app.states.dashboard_state import DashboardState


def sector_allocation_chart() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Sector Allocation", class_name="text-xl font-bold text-gray-800 mb-4"
        ),
        rx.el.div(
            rx.recharts.pie_chart(
                rx.recharts.graphing_tooltip(
                    content_style={
                        "backgroundColor": "#ffffff",
                        "border": "1px solid #e5e7eb",
                        "borderRadius": "0.5rem",
                    }
                ),
                rx.recharts.pie(
                    data=DashboardState.sector_allocation_data,
                    data_key="value",
                    name_key="name",
                    cx="50%",
                    cy="50%",
                    outer_radius=80,
                    label=True,
                ),
                rx.recharts.legend(),
                width="100%",
                height=300,
            )
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm mt-6",
    )