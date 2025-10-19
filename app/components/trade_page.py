import reflex as rx
from app.states.trade_state import TradeState
from app.states.dashboard_state import DashboardState


def search_bar() -> rx.Component:
    return rx.el.div(
        rx.icon(
            tag="search",
            class_name="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400",
        ),
        rx.el.input(
            placeholder="Search for stocks (e.g., RELIANCE.NS)",
            on_change=TradeState.set_search_term,
            class_name="w-full pl-10 pr-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-colors",
            default_value=TradeState.search_term,
        ),
        rx.cond(
            TradeState.search_results.length() > 0,
            rx.el.div(
                rx.foreach(
                    TradeState.search_results,
                    lambda result: rx.el.button(
                        rx.el.div(
                            rx.el.p(
                                result["ticker"],
                                class_name="font-semibold text-gray-800",
                            ),
                            rx.el.p(result["name"], class_name="text-sm text-gray-500"),
                            class_name="text-left",
                        ),
                        on_click=lambda: TradeState.select_stock(result["ticker"]),
                        class_name="w-full px-4 py-2 text-left hover:bg-gray-100 rounded-md",
                    ),
                ),
                class_name="absolute top-full mt-2 w-full bg-white border border-gray-200 rounded-lg shadow-lg z-10 max-h-60 overflow-y-auto",
            ),
        ),
        class_name="relative w-full max-w-2xl mx-auto",
    )


def stock_info_card() -> rx.Component:
    def metric(label: str, value: rx.Var, unit: str = "") -> rx.Component:
        return rx.el.div(
            rx.el.p(label, class_name="text-sm text-gray-500"),
            rx.el.p(f"{value}{unit}", class_name="font-semibold text-gray-800"),
            class_name="flex justify-between items-center py-2 border-b border-gray-200 last:border-b-0",
        )

    return rx.el.div(
        rx.cond(
            TradeState.is_loading,
            rx.el.div(
                rx.spinner(class_name="h-8 w-8 text-purple-500"),
                class_name="flex justify-center items-center h-full",
            ),
            rx.cond(
                TradeState.is_stock_selected,
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            TradeState.selected_stock["name"],
                            class_name="text-xl font-bold text-gray-800",
                        ),
                        rx.el.p(
                            f"NSE: {TradeState.selected_stock['ticker']}",
                            class_name="text-sm text-gray-500",
                        ),
                        rx.el.button(
                            rx.icon(
                                tag=rx.cond(
                                    TradeState.watchlist.contains(
                                        TradeState.selected_stock["ticker"]
                                    ),
                                    "star",
                                    "plus-circle",
                                ),
                                class_name="w-5 h-5 mr-2",
                            ),
                            rx.cond(
                                TradeState.watchlist.contains(
                                    TradeState.selected_stock["ticker"]
                                ),
                                "Remove from Watchlist",
                                "Add to Watchlist",
                            ),
                            on_click=lambda: TradeState.toggle_watchlist(
                                TradeState.selected_stock["ticker"]
                            ),
                            class_name=rx.cond(
                                TradeState.watchlist.contains(
                                    TradeState.selected_stock["ticker"]
                                ),
                                "flex items-center text-sm font-semibold text-yellow-500 hover:text-yellow-600",
                                "flex items-center text-sm font-semibold text-purple-600 hover:text-purple-700",
                            ),
                            variant="ghost",
                        ),
                        class_name="flex items-center justify-between",
                    ),
                    rx.el.div(
                        rx.el.p(
                            f"₹{TradeState.selected_stock['current_price']:.2f}",
                            class_name="text-3xl font-bold text-gray-900",
                        ),
                        rx.el.p(
                            f"{TradeState.selected_stock['current_price'] - TradeState.selected_stock['previous_close']:.2f} ({(TradeState.selected_stock['current_price'] - TradeState.selected_stock['previous_close']) / TradeState.selected_stock['previous_close'] * 100:.2f}%)",
                            class_name=rx.cond(
                                TradeState.selected_stock["current_price"]
                                >= TradeState.selected_stock["previous_close"],
                                "text-green-600 font-semibold",
                                "text-red-600 font-semibold",
                            ),
                        ),
                        class_name="flex items-baseline gap-2 mt-2",
                    ),
                    rx.el.div(
                        rx.recharts.area_chart(
                            rx.recharts.cartesian_grid(
                                stroke_dasharray="3 3", vertical=False
                            ),
                            rx.recharts.graphing_tooltip(
                                content_style={"backgroundColor": "#FFFFFF"}
                            ),
                            rx.recharts.x_axis(data_key="date", hide=True),
                            rx.recharts.y_axis(
                                domain=[
                                    "dataMin - abs(dataMin)*0.1",
                                    "dataMax + abs(dataMax)*0.1",
                                ],
                                hide=True,
                            ),
                            rx.recharts.area(
                                type_="monotone",
                                data_key="price",
                                stroke="#8884d8",
                                fill="#8884d8",
                                fill_opacity=0.3,
                                stroke_width=2,
                            ),
                            data=TradeState.historical_data,
                            height=200,
                            margin={"top": 5, "right": 0, "left": 0, "bottom": 5},
                        ),
                        class_name="mt-4",
                    ),
                    rx.el.div(
                        metric(
                            "Previous Close",
                            f"₹{TradeState.selected_stock['previous_close']:.2f}",
                        ),
                        metric(
                            "52-Week High",
                            f"₹{TradeState.selected_stock['fifty_two_week_high']:.2f}",
                        ),
                        metric(
                            "52-Week Low",
                            f"₹{TradeState.selected_stock['fifty_two_week_low']:.2f}",
                        ),
                        metric(
                            "Market Cap",
                            f"₹{TradeState.selected_stock['market_cap']:,}",
                        ),
                        metric("Volume", f"{TradeState.selected_stock['volume']:,}"),
                        metric("Sector", TradeState.selected_stock["sector"]),
                        class_name="mt-4",
                    ),
                    rx.el.p(
                        TradeState.selected_stock["description"],
                        class_name="text-sm text-gray-600 mt-4",
                    ),
                    class_name="p-6",
                ),
                rx.el.div(
                    rx.el.p(
                        "Search for a stock to see its details",
                        class_name="text-gray-500",
                    ),
                    class_name="flex justify-center items-center h-full p-6",
                ),
            ),
        ),
        class_name="bg-white rounded-xl border border-gray-200 shadow-sm h-full overflow-y-auto",
    )


def order_form() -> rx.Component:
    return rx.el.div(
        rx.el.h3("Place Order", class_name="text-xl font-bold text-gray-800 mb-4"),
        rx.cond(
            TradeState.is_stock_selected,
            rx.el.div(
                rx.el.div(
                    rx.el.button(
                        "BUY",
                        on_click=TradeState.set_order_type("BUY"),
                        class_name=rx.cond(
                            TradeState.order_type == "BUY",
                            "w-full py-2 rounded-l-lg bg-green-600 text-white font-semibold",
                            "w-full py-2 rounded-l-lg bg-gray-200 text-gray-700 font-semibold",
                        ),
                    ),
                    rx.el.button(
                        "SELL",
                        on_click=TradeState.set_order_type("SELL"),
                        class_name=rx.cond(
                            TradeState.order_type == "SELL",
                            "w-full py-2 rounded-r-lg bg-red-600 text-white font-semibold",
                            "w-full py-2 rounded-r-lg bg-gray-200 text-gray-700 font-semibold",
                        ),
                    ),
                    class_name="flex",
                ),
                rx.el.div(
                    rx.el.label(
                        "Quantity", class_name="text-sm font-medium text-gray-700"
                    ),
                    rx.el.input(
                        type="number",
                        on_change=TradeState.set_order_quantity,
                        class_name="w-full mt-1 px-3 py-2 rounded-lg border border-gray-300",
                        default_value=TradeState.order_quantity.to_string(),
                    ),
                    class_name="mt-4",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.p("Available Cash", class_name="text-sm text-gray-500"),
                        rx.el.p(
                            f"₹{DashboardState.available_cash:,.2f}",
                            class_name="font-mono text-gray-700",
                        ),
                        class_name="flex justify-between",
                    ),
                    rx.el.div(
                        rx.el.p("Estimated Total", class_name="text-sm text-gray-500"),
                        rx.el.p(
                            f"₹{TradeState.estimated_total:,.2f}",
                            class_name="font-mono font-semibold text-gray-800",
                        ),
                        class_name="flex justify-between mt-1",
                    ),
                    class_name="mt-4 p-3 bg-gray-100 rounded-lg",
                ),
                rx.el.button(
                    f"Submit {TradeState.order_type}",
                    on_click=TradeState.execute_order,
                    disabled=~TradeState.can_submit_order,
                    class_name=rx.cond(
                        TradeState.can_submit_order,
                        rx.cond(
                            TradeState.order_type == "BUY",
                            "w-full mt-4 py-3 rounded-lg bg-green-600 text-white font-bold text-lg hover:bg-green-700",
                            "w-full mt-4 py-3 rounded-lg bg-red-600 text-white font-bold text-lg hover:bg-red-700",
                        ),
                        "w-full mt-4 py-3 rounded-lg bg-gray-400 text-white font-bold text-lg cursor-not-allowed",
                    ),
                ),
            ),
            rx.el.div(
                rx.el.p(
                    "Select a stock to place an order.",
                    class_name="text-gray-500 text-center py-10",
                )
            ),
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm",
    )


def transaction_history() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Transaction History", class_name="text-xl font-bold text-gray-800 mb-4"
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Date",
                            class_name="py-2 px-3 text-left text-xs font-semibold text-gray-500 uppercase",
                        ),
                        rx.el.th(
                            "Ticker",
                            class_name="py-2 px-3 text-left text-xs font-semibold text-gray-500 uppercase",
                        ),
                        rx.el.th(
                            "Type",
                            class_name="py-2 px-3 text-center text-xs font-semibold text-gray-500 uppercase",
                        ),
                        rx.el.th(
                            "Qty",
                            class_name="py-2 px-3 text-right text-xs font-semibold text-gray-500 uppercase",
                        ),
                        rx.el.th(
                            "Price",
                            class_name="py-2 px-3 text-right text-xs font-semibold text-gray-500 uppercase",
                        ),
                        rx.el.th(
                            "Total",
                            class_name="py-2 px-3 text-right text-xs font-semibold text-gray-500 uppercase",
                        ),
                    )
                ),
                rx.el.tbody(
                    rx.foreach(
                        TradeState.transactions,
                        lambda tx: rx.el.tr(
                            rx.el.td(
                                tx["date"], class_name="py-2 px-3 text-sm text-gray-600"
                            ),
                            rx.el.td(
                                tx["ticker"],
                                class_name="py-2 px-3 text-sm font-semibold text-gray-800",
                            ),
                            rx.el.td(
                                rx.el.span(
                                    tx["type"],
                                    class_name=rx.cond(
                                        tx["type"] == "BUY",
                                        "px-2 py-1 text-xs font-semibold text-green-800 bg-green-100 rounded-full",
                                        "px-2 py-1 text-xs font-semibold text-red-800 bg-red-100 rounded-full",
                                    ),
                                ),
                                class_name="py-2 px-3 text-center",
                            ),
                            rx.el.td(
                                tx["quantity"].to_string(),
                                class_name="py-2 px-3 text-right font-mono text-gray-600",
                            ),
                            rx.el.td(
                                f"₹{tx['price']:.2f}",
                                class_name="py-2 px-3 text-right font-mono text-gray-600",
                            ),
                            rx.el.td(
                                f"₹{tx['total']:.2f}",
                                class_name="py-2 px-3 text-right font-mono font-semibold text-gray-800",
                            ),
                        ),
                    ),
                    rx.cond(
                        TradeState.transactions.length() == 0,
                        rx.el.tr(
                            rx.el.td(
                                "No transactions yet.",
                                col_span=6,
                                class_name="py-10 text-center text-gray-500",
                            )
                        ),
                    ),
                ),
                class_name="w-full table-auto",
            ),
            class_name="overflow-x-auto",
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm mt-6",
    )


def trade_page() -> rx.Component:
    return rx.el.div(
        search_bar(),
        rx.el.div(
            rx.el.div(stock_info_card(), class_name="lg:col-span-3 xl:col-span-2"),
            rx.el.div(
                order_form(),
                transaction_history(),
                class_name="lg:col-span-2 xl:col-span-1 space-y-6",
            ),
            class_name="grid grid-cols-1 lg:grid-cols-5 gap-6 mt-6 items-start",
        ),
        class_name="animate-fade-in p-4 md:p-8",
    )