import reflex as rx
from app.states.portfolio_state import PortfolioState


def performance_chart() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Portfolio Performance", class_name="text-xl font-bold text-gray-800 mb-4"
        ),
        rx.el.div(
            rx.recharts.area_chart(
                rx.recharts.cartesian_grid(stroke_dasharray="3 3", vertical=False),
                rx.recharts.graphing_tooltip(
                    content_style={
                        "backgroundColor": "#ffffff",
                        "border": "1px solid #e5e7eb",
                        "borderRadius": "0.5rem",
                    }
                ),
                rx.recharts.x_axis(
                    data_key="date",
                    stroke="#a1a1aa",
                    font_size=12,
                    tick_line=False,
                    axis_line=False,
                ),
                rx.recharts.y_axis(
                    stroke="#a1a1aa", font_size=12, tick_line=False, axis_line=False
                ),
                rx.recharts.area(
                    type_="monotone",
                    data_key="value",
                    stroke="#8b5cf6",
                    fill="#c4b5fd",
                    fill_opacity=0.4,
                    stroke_width=2,
                ),
                data=PortfolioState.portfolio_history,
                height=300,
                margin={"top": 10, "right": 10, "left": 20, "bottom": 10},
            ),
            class_name="-ml-4",
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm mt-6",
    )