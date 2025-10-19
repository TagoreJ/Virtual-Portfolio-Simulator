import reflex as rx
from typing import TypedDict


class PortfolioDataPoint(TypedDict):
    date: str
    value: float


class PortfolioState(rx.State):
    """Manages the state for the portfolio analytics page."""

    portfolio_history: list[PortfolioDataPoint] = []