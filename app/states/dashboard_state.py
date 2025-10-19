import reflex as rx
from typing import TypedDict, Literal
import yfinance as yf
import logging
from app.states.auth_state import AuthState


class Holding(TypedDict):
    ticker: str
    name: str
    quantity: int
    avg_price: float
    current_price: float
    day_change_pct: float


class LeaderboardUser(TypedDict):
    rank: int
    name: str
    portfolio_value: float
    growth_pct: float


class DashboardState(AuthState):
    """Manages the state for the main dashboard."""

    active_page: Literal["Dashboard", "Trade", "Portfolio", "Leaderboard"] = "Dashboard"
    portfolio_value: float = 0.0
    day_change: float = 0.0
    day_change_pct: float = 0.0
    available_cash: float = 0.0
    holdings: list[Holding] = []
    leaderboard_users: list[LeaderboardUser] = []

    @rx.event
    def set_active_page(
        self, page: Literal["Dashboard", "Trade", "Portfolio", "Leaderboard"]
    ):
        self.active_page = page

    @rx.var
    def total_investment(self) -> float:
        return sum((h["quantity"] * h["avg_price"] for h in self.holdings))

    @rx.var
    def current_holdings_value(self) -> float:
        return sum((h["quantity"] * h["current_price"] for h in self.holdings))

    @rx.var
    def total_pl(self) -> float:
        return self.current_holdings_value - self.total_investment

    @rx.var
    def total_pl_pct(self) -> float:
        if self.total_investment == 0:
            return 0.0
        return self.total_pl / self.total_investment * 100

    @rx.var
    def holdings_by_sector(self) -> dict[str, float]:
        sector_values: dict[str, float] = {}
        total_value = self.current_holdings_value
        if total_value == 0:
            return {}
        placeholder_sectors = {
            "RELIANCE.NS": "Energy",
            "TCS.NS": "Technology",
            "HDFCBANK.NS": "Financial Services",
            "INFY.NS": "Technology",
        }
        for h in self.holdings:
            sector = placeholder_sectors.get(h["ticker"], "Other")
            value = h["quantity"] * h["current_price"]
            if sector in sector_values:
                sector_values[sector] += value
            else:
                sector_values[sector] = value
        return {k: round(v / total_value * 100, 2) for k, v in sector_values.items()}

    @rx.var
    def sector_allocation_data(self) -> list[dict[str, str | float]]:
        colors = ["#8884d8", "#82ca9d", "#ffc658", "#ff8042", "#0088fe", "#00c49f"]
        return [
            {"name": sector, "value": percentage, "fill": colors[i % len(colors)]}
            for i, (sector, percentage) in enumerate(self.holdings_by_sector.items())
        ]

    @rx.event(background=True)
    async def load_user_data(self):
        async with self:
            if not self.is_authenticated:
                return
            client = self._get_supabase_client()
            user_id = self.user["user_id"]
            portfolio_res = (
                client.table("portfolios")
                .select("available_cash")
                .eq("user_id", user_id)
                .single()
                .execute()
            )
            if portfolio_res.data:
                self.available_cash = portfolio_res.data["available_cash"]
            holdings_res = (
                client.table("holdings").select("*").eq("user_id", user_id).execute()
            )
            holdings_data = holdings_res.data
            from app.states.trade_state import TradeState

            trade_state = await self.get_state(TradeState)
            transactions_res = (
                client.table("transactions")
                .select("*")
                .eq("user_id", user_id)
                .order("timestamp", desc=True)
                .execute()
            )
            trade_state.transactions = [
                {
                    "date": tx["timestamp"],
                    "ticker": tx["ticker"],
                    "type": tx["type"],
                    "quantity": tx["quantity"],
                    "price": tx["price"],
                    "total": tx["total"],
                }
                for tx in transactions_res.data
            ]
            watchlist_res = (
                client.table("watchlist")
                .select("ticker")
                .eq("user_id", user_id)
                .execute()
            )
            trade_state.watchlist = [item["ticker"] for item in watchlist_res.data]
        if holdings_data:
            yield DashboardState.update_holdings_live_data(holdings_data)

    @rx.event(background=True)
    async def update_holdings_live_data(self, holdings_data: list[dict]):
        tickers = [h["ticker"] for h in holdings_data]
        if not tickers:
            async with self:
                self.holdings = []
                self.portfolio_value = self.available_cash
                self.day_change = 0.0
                self.day_change_pct = 0.0
            return
        try:
            data = yf.download(tickers, period="1d")
            if data.empty:
                raise ValueError("No data returned from yfinance")
            updated_holdings = []
            current_holdings_value = 0
            previous_holdings_value = 0
            for holding in holdings_data:
                ticker = holding["ticker"]
                current_price = (
                    data["Close"][ticker].iloc[-1]
                    if not data["Close"][ticker].empty
                    else holding["avg_price"]
                )
                prev_close = (
                    data["Open"][ticker].iloc[-1]
                    if not data["Open"][ticker].empty
                    else current_price
                )
                day_change_pct = (
                    (current_price - prev_close) / prev_close * 100 if prev_close else 0
                )
                updated_holdings.append(
                    {
                        "ticker": ticker,
                        "name": holding["name"],
                        "quantity": holding["quantity"],
                        "avg_price": holding["avg_price"],
                        "current_price": current_price,
                        "day_change_pct": day_change_pct,
                    }
                )
                current_holdings_value += holding["quantity"] * current_price
                previous_holdings_value += holding["quantity"] * prev_close
            async with self:
                self.holdings = updated_holdings
                self.portfolio_value = self.available_cash + current_holdings_value
                self.day_change = current_holdings_value - previous_holdings_value
                if self.portfolio_value - self.day_change > 0:
                    self.day_change_pct = (
                        self.day_change / (self.portfolio_value - self.day_change) * 100
                    )
                else:
                    self.day_change_pct = 0.0
        except Exception as e:
            logging.exception(f"Failed to update holdings live data: {e}")
            async with self:
                self.holdings = [
                    {
                        "ticker": h["ticker"],
                        "name": h["name"],
                        "quantity": h["quantity"],
                        "avg_price": h["avg_price"],
                        "current_price": h.get("current_price", h["avg_price"]),
                        "day_change_pct": h.get("day_change_pct", 0),
                    }
                    for h in holdings_data
                ]
                holdings_value = sum(
                    (h["quantity"] * h["current_price"] for h in self.holdings)
                )
                self.portfolio_value = self.available_cash + holdings_value

    @rx.event
    async def buy_stock(self, ticker: str, name: str, quantity: int, price: float):
        if not self.is_authenticated:
            return
        total_cost = quantity * price
        if self.available_cash < total_cost:
            logging.warning("Insufficient funds for buy order.")
            return
        client = self._get_supabase_client()
        user_id = self.user["user_id"]
        existing_holding = next(
            (h for h in self.holdings if h["ticker"] == ticker), None
        )
        if existing_holding:
            new_quantity = existing_holding["quantity"] + quantity
            new_avg_price = (
                existing_holding["quantity"] * existing_holding["avg_price"]
                + total_cost
            ) / new_quantity
            existing_holding["quantity"] = new_quantity
            existing_holding["avg_price"] = new_avg_price
            db_op = (
                client.table("holdings")
                .update({"quantity": new_quantity, "avg_price": new_avg_price})
                .eq("user_id", user_id)
                .eq("ticker", ticker)
            )
        else:
            new_holding = {
                "ticker": ticker,
                "name": name,
                "quantity": quantity,
                "avg_price": price,
                "current_price": price,
                "day_change_pct": 0,
            }
            self.holdings.append(new_holding)
            db_op = client.table("holdings").insert({"user_id": user_id, **new_holding})
        try:
            db_op.execute()
            self.available_cash -= total_cost
            client.table("portfolios").update(
                {"available_cash": self.available_cash}
            ).eq("user_id", user_id).execute()
            logging.info(f"BUY successful for {quantity} {ticker} @ {price}")
        except Exception as e:
            logging.exception(f"Supabase error on buy_stock: {e}")

    @rx.event
    async def sell_stock(self, ticker: str, quantity: int, price: float):
        if not self.is_authenticated:
            return
        holding_to_sell = next(
            (h for h in self.holdings if h["ticker"] == ticker), None
        )
        if not holding_to_sell or holding_to_sell["quantity"] < quantity:
            logging.warning("Invalid sell order: Not enough quantity.")
            return
        client = self._get_supabase_client()
        user_id = self.user["user_id"]
        total_proceeds = quantity * price
        try:
            if holding_to_sell["quantity"] > quantity:
                holding_to_sell["quantity"] -= quantity
                client.table("holdings").update(
                    {"quantity": holding_to_sell["quantity"]}
                ).eq("user_id", user_id).eq("ticker", ticker).execute()
            else:
                self.holdings = [h for h in self.holdings if h["ticker"] != ticker]
                client.table("holdings").delete().eq("user_id", user_id).eq(
                    "ticker", ticker
                ).execute()
            self.available_cash += total_proceeds
            client.table("portfolios").update(
                {"available_cash": self.available_cash}
            ).eq("user_id", user_id).execute()
            logging.info(f"SELL successful for {quantity} {ticker} @ {price}")
        except Exception as e:
            logging.exception(f"Supabase error on sell_stock: {e}")