import reflex as rx
from typing import TypedDict, Literal, Any
import yfinance as yf
import datetime
import logging
from app.states.dashboard_state import DashboardState


class StockInfo(TypedDict):
    ticker: str
    name: str
    current_price: float
    previous_close: float
    market_cap: int
    sector: str
    fifty_two_week_high: float
    fifty_two_week_low: float
    volume: int
    description: str


class HistoricalDataPoint(TypedDict):
    date: str
    price: float


class Transaction(TypedDict):
    date: str
    ticker: str
    type: Literal["BUY", "SELL"]
    quantity: int
    price: float
    total: float


class TradeState(rx.State):
    search_term: str = ""
    search_results: list[dict[str, str]] = []
    selected_stock: StockInfo | None = None
    watchlist: list[str] = []
    is_loading: bool = False
    historical_data: list[HistoricalDataPoint] = []
    order_type: Literal["BUY", "SELL"] = "BUY"
    order_quantity: int = 0
    transactions: list[Transaction] = []

    @rx.event
    def set_order_type(self, order_type: Literal["BUY", "SELL"]):
        self.order_type = order_type

    @rx.event
    def set_order_quantity(self, quantity: str):
        try:
            self.order_quantity = int(quantity)
        except (ValueError, TypeError) as e:
            logging.exception(f"Error setting order quantity: {e}")
            self.order_quantity = 0

    @rx.var
    def is_stock_selected(self) -> bool:
        return self.selected_stock is not None

    @rx.var
    def estimated_total(self) -> float:
        if self.selected_stock and self.order_quantity > 0:
            return self.selected_stock["current_price"] * self.order_quantity
        return 0.0

    @rx.var
    async def can_submit_order(self) -> bool:
        dashboard_state = await self.get_state(DashboardState)
        if not self.selected_stock or self.order_quantity <= 0:
            return False
        if self.order_type == "BUY":
            return self.estimated_total <= dashboard_state.available_cash
        for holding in dashboard_state.holdings:
            if holding["ticker"] == self.selected_stock["ticker"]:
                return self.order_quantity <= holding["quantity"]
        return False

    @rx.event
    def set_search_term(self, term: str):
        self.search_term = term
        if len(term) > 1:
            all_stocks = [
                {"ticker": "RELIANCE.NS", "name": "Reliance Industries"},
                {"ticker": "TCS.NS", "name": "Tata Consultancy Services"},
                {"ticker": "HDFCBANK.NS", "name": "HDFC Bank"},
                {"ticker": "INFY.NS", "name": "Infosys"},
                {"ticker": "HINDUNILVR.NS", "name": "Hindustan Unilever"},
                {"ticker": "ICICIBANK.NS", "name": "ICICI Bank"},
                {"ticker": "KOTAKBANK.NS", "name": "Kotak Mahindra Bank"},
                {"ticker": "BHARTIARTL.NS", "name": "Bharti Airtel"},
                {"ticker": "ITC.NS", "name": "ITC Limited"},
                {"ticker": "BAJFINANCE.NS", "name": "Bajaj Finance"},
                {"ticker": "TATAMOTORS.NS", "name": "Tata Motors"},
                {"ticker": "TATASTEEL.NS", "name": "Tata Steel"},
                {"ticker": "WIPRO.NS", "name": "Wipro"},
            ]
            self.search_results = [
                s
                for s in all_stocks
                if term.lower() in s["name"].lower()
                or term.lower() in s["ticker"].lower()
            ]
        else:
            self.search_results = []

    @rx.event(background=True)
    async def select_stock(self, ticker: str):
        async with self:
            self.is_loading = True
            self.search_term = ""
            self.search_results = []
        yield
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            hist = stock.history(period="1y")
            hist_data = [
                {"date": index.strftime("%Y-%m-%d"), "price": row["Close"]}
                for index, row in hist.iterrows()
            ]
            selected = {
                "ticker": ticker,
                "name": info.get("longName", "N/A"),
                "current_price": info.get(
                    "currentPrice", info.get("regularMarketPrice", 0)
                ),
                "previous_close": info.get("previousClose", 0),
                "market_cap": info.get("marketCap", 0),
                "sector": info.get("sector", "N/A"),
                "fifty_two_week_high": info.get("fiftyTwoWeekHigh", 0),
                "fifty_two_week_low": info.get("fiftyTwoWeekLow", 0),
                "volume": info.get("volume", 0),
                "description": info.get(
                    "longBusinessSummary", "No description available."
                ),
            }
            async with self:
                self.selected_stock = selected
                self.historical_data = hist_data
                self.is_loading = False
        except Exception as e:
            logging.exception(f"Error fetching stock data: {e}")
            async with self:
                self.is_loading = False

    @rx.event
    async def toggle_watchlist(self, ticker: str):
        dashboard_state = await self.get_state(DashboardState)
        if not dashboard_state.is_authenticated or not dashboard_state.user:
            return
        client = dashboard_state._get_supabase_client()
        user_id = dashboard_state.user["user_id"]
        try:
            if ticker in self.watchlist:
                self.watchlist.remove(ticker)
                client.table("watchlist").delete().eq("user_id", user_id).eq(
                    "ticker", ticker
                ).execute()
                logging.info(f"Removed {ticker} from watchlist for user {user_id}")
            else:
                self.watchlist.append(ticker)
                client.table("watchlist").insert(
                    {"user_id": user_id, "ticker": ticker}
                ).execute()
                logging.info(f"Added {ticker} to watchlist for user {user_id}")
        except Exception as e:
            logging.exception(f"Error toggling watchlist for {ticker}: {e}")

    @rx.event(background=True)
    async def execute_order(self):
        async with self:
            can_submit = await self.get_var_value(self.can_submit_order)
            dashboard_state = await self.get_state(DashboardState)
            if (
                not can_submit
                or not dashboard_state.is_authenticated
                or (not dashboard_state.user)
            ):
                return
        client = dashboard_state._get_supabase_client()
        user_id = dashboard_state.user["user_id"]
        order_data = {
            "ticker": self.selected_stock["ticker"],
            "name": self.selected_stock["name"],
            "quantity": self.order_quantity,
            "price": self.selected_stock["current_price"],
            "order_type": self.order_type,
            "total": self.estimated_total,
        }
        try:
            transaction_record = {
                "user_id": user_id,
                "ticker": order_data["ticker"],
                "type": order_data["order_type"],
                "quantity": order_data["quantity"],
                "price": order_data["price"],
                "total": order_data["total"],
            }
            client.table("transactions").insert(transaction_record).execute()
            if self.order_type == "BUY":
                await dashboard_state.buy_stock(
                    order_data["ticker"],
                    order_data["name"],
                    order_data["quantity"],
                    order_data["price"],
                )
            else:
                await dashboard_state.sell_stock(
                    order_data["ticker"], order_data["quantity"], order_data["price"]
                )
            async with self:
                self.order_quantity = 0
            logging.info(f"Order executed and saved for user {user_id}: {order_data}")
        except Exception as e:
            logging.exception(f"Failed to execute order for user {user_id}: {e}")