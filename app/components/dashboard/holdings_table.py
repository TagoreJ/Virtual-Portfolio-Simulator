import reflex as rx
from app.states.dashboard_state import DashboardState


def holdings_table() -> rx.Component:
    def pl_for_holding(holding: rx.Var) -> rx.Var[float]:
        return (holding["current_price"] - holding["avg_price"]) * holding["quantity"]

    def pl_pct_for_holding(holding: rx.Var) -> rx.Var[float]:
        return (
            (holding["current_price"] - holding["avg_price"])
            / holding["avg_price"]
            * 100
        )

    return rx.el.div(
        rx.el.h3("My Holdings", class_name="text-xl font-bold text-gray-800 mb-4"),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Instrument",
                            class_name="py-3 px-4 text-left text-xs font-semibold text-gray-500 uppercase w-2/5",
                        ),
                        rx.el.th(
                            "Qty.",
                            class_name="py-3 px-4 text-right text-xs font-semibold text-gray-500 uppercase",
                        ),
                        rx.el.th(
                            "Avg. Price",
                            class_name="py-3 px-4 text-right text-xs font-semibold text-gray-500 uppercase",
                        ),
                        rx.el.th(
                            "LTP",
                            class_name="py-3 px-4 text-right text-xs font-semibold text-gray-500 uppercase",
                        ),
                        rx.el.th(
                            "P&L",
                            class_name="py-3 px-4 text-right text-xs font-semibold text-gray-500 uppercase",
                        ),
                    )
                ),
                rx.el.tbody(
                    rx.foreach(
                        DashboardState.holdings,
                        lambda holding: rx.el.tr(
                            rx.el.td(
                                rx.el.div(
                                    rx.image(
                                        src=f"https://api.dicebear.com/9.x/initials/svg?seed={holding['ticker']}",
                                        class_name="h-8 w-8 rounded-full mr-3",
                                    ),
                                    rx.el.div(
                                        rx.el.p(
                                            holding["ticker"],
                                            class_name="font-semibold text-gray-800",
                                        ),
                                        rx.el.p(
                                            holding["name"],
                                            class_name="text-xs text-gray-500 truncate",
                                        ),
                                    ),
                                    class_name="flex items-center",
                                ),
                                class_name="py-3 px-4",
                            ),
                            rx.el.td(
                                holding["quantity"],
                                class_name="py-3 px-4 text-right font-mono text-gray-600",
                            ),
                            rx.el.td(
                                f"₹{holding['avg_price']:.2f}",
                                class_name="py-3 px-4 text-right font-mono text-gray-600",
                            ),
                            rx.el.td(
                                rx.el.div(
                                    rx.el.p(
                                        f"₹{holding['current_price']:.2f}",
                                        class_name="font-mono font-semibold text-gray-800",
                                    ),
                                    rx.el.p(
                                        f"{holding['day_change_pct']:.2f}%",
                                        class_name=rx.cond(
                                            holding["day_change_pct"] >= 0,
                                            "text-xs font-mono text-green-600",
                                            "text-xs font-mono text-red-600",
                                        ),
                                    ),
                                    class_name="flex flex-col items-end",
                                ),
                                class_name="py-3 px-4",
                            ),
                            rx.el.td(
                                rx.el.div(
                                    rx.el.p(
                                        f"₹{pl_for_holding(holding):.2f}",
                                        class_name=rx.cond(
                                            pl_for_holding(holding) >= 0,
                                            "font-mono font-semibold text-green-600",
                                            "font-mono font-semibold text-red-600",
                                        ),
                                    ),
                                    rx.el.p(
                                        f"{pl_pct_for_holding(holding):.2f}%",
                                        class_name=rx.cond(
                                            pl_pct_for_holding(holding) >= 0,
                                            "text-xs font-mono text-green-600",
                                            "text-xs font-mono text-red-600",
                                        ),
                                    ),
                                    class_name="flex flex-col items-end",
                                ),
                                class_name="py-3 px-4",
                            ),
                            class_name="border-b border-gray-200 hover:bg-gray-50",
                        ),
                    )
                ),
                class_name="w-full table-fixed",
            ),
            class_name="overflow-x-auto",
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm mt-6",
    )