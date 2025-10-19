import reflex as rx
from app.states.trade_state import TradeState


def watchlist_item(ticker: rx.Var[str]) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.image(
                src=f"https://api.dicebear.com/9.x/initials/svg?seed={ticker}",
                class_name="h-8 w-8 rounded-full",
            ),
            rx.el.div(
                rx.el.p(ticker, class_name="font-semibold text-gray-800"),
                rx.el.p("Stock Name", class_name="text-xs text-gray-500"),
                class_name="flex-1 min-w-0",
            ),
            class_name="flex items-center gap-3",
        ),
        rx.el.div(
            rx.el.p("₹1,500.00", class_name="font-mono font-semibold"),
            rx.el.p("+1.25%", class_name="text-green-600 font-mono text-sm"),
            class_name="text-right",
        ),
        rx.el.button(
            rx.icon(tag="x", class_name="w-4 h-4"),
            on_click=lambda: TradeState.toggle_watchlist(ticker),
            variant="ghost",
            size="sm",
            class_name="text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-full",
        ),
        class_name="flex items-center justify-between p-3 hover:bg-gray-50 rounded-lg",
    )


def watchlist() -> rx.Component:
    return rx.el.div(
        rx.el.h3("My Watchlist", class_name="text-xl font-bold text-gray-800 mb-4"),
        rx.el.div(
            rx.foreach(TradeState.watchlist, watchlist_item),
            rx.cond(
                TradeState.watchlist.length() == 0,
                rx.el.div(
                    rx.el.p("Your watchlist is empty.", class_name="text-gray-500"),
                    rx.el.p(
                        "Add stocks from the Trade page.",
                        class_name="text-sm text-gray-400",
                    ),
                    class_name="text-center py-10",
                ),
            ),
            class_name="space-y-2",
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm mt-6",
    )