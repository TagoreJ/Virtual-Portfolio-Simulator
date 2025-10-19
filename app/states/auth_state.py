import reflex as rx
import os
from typing import TypedDict, Any
from supabase import create_client, Client
from reflex_google_auth import GoogleAuthState
import logging


class User(TypedDict):
    user_id: str
    email: str
    name: str
    avatar_url: str


class AuthState(GoogleAuthState):
    """Manages user authentication and session data."""

    user: User | None = None
    _supabase_client: Client | None = None

    def _get_supabase_client(self) -> Client:
        if self._supabase_client is None:
            url = os.environ.get("SUPABASE_URL")
            key = os.environ.get("SUPABASE_KEY")
            if not url or not key:
                raise ValueError("SupABASE_URL and SUPABASE_KEY must be set in .env")
            self._supabase_client = create_client(url, key)
        return self._supabase_client

    @rx.var
    def is_authenticated(self) -> bool:
        return self.token_is_valid and self.user is not None

    @rx.event(background=True)
    async def on_login(self, token_info: dict[str, Any]):
        async with self:
            if not token_info or "sub" not in token_info:
                logging.error("Invalid token info on login")
                return
            user_data = {
                "user_id": token_info["sub"],
                "email": token_info["email"],
                "name": token_info["name"],
                "avatar_url": token_info["picture"],
            }
            self.user = user_data
        try:
            client = self._get_supabase_client()
            response = (
                client.table("users")
                .select("user_id")
                .eq("user_id", user_data["user_id"])
                .execute()
            )
            if not response.data:
                client.table("users").insert(user_data).execute()
                client.table("portfolios").insert(
                    {"user_id": user_data["user_id"]}
                ).execute()
                logging.info(f"New user created: {user_data['email']}")
            else:
                logging.info(f"User logged in: {user_data['email']}")
            return rx.redirect("/")
        except Exception as e:
            logging.exception(f"Supabase error on login: {e}")
            async with self:
                self.user = None
                self.id_token_json = ""

    @rx.event
    def on_load(self):
        """Check token validity on page load."""
        if not self.token_is_valid:
            return
        token_info = self.tokeninfo
        if token_info and "sub" in token_info:
            self.user = {
                "user_id": token_info["sub"],
                "email": token_info["email"],
                "name": token_info["name"],
                "avatar_url": token_info["picture"],
            }
            from app.states.dashboard_state import DashboardState

            return DashboardState.load_user_data
        else:
            self.user = None

    @rx.event
    def logout(self):
        self.id_token_json = ""
        self.user = None
        return rx.redirect("/login")