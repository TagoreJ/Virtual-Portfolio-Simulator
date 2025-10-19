import reflex as rx
import os
import re
import json
from typing import TypedDict
from supabase import create_client, Client
import logging


class User(TypedDict):
    user_id: str
    email: str
    name: str


class AuthState(rx.State):
    """Manages user authentication and session data."""

    user_json: str = rx.LocalStorage("")
    user: User | None = None
    _supabase_client: Client | None = None

    def _get_supabase_client(self) -> Client:
        if self._supabase_client is None:
            url = os.environ.get("SUPABASE_URL")
            key = os.environ.get("SUPABASE_KEY")
            if not url or not key:
                raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env")
            self._supabase_client = create_client(url, key)
        return self._supabase_client

    @rx.var
    def is_authenticated(self) -> bool:
        return self.user is not None

    @rx.event(background=True)
    async def login(self, form_data: dict):
        async with self:
            if not form_data.get("email") or not form_data.get("name"):
                logging.error("Login form missing name or email.")
                return
            email = form_data["email"].lower().strip()
            name = form_data["name"].strip()
            user_id = re.sub("[^a-zA-Z0-9_.-]", "_", email)
            user_data = {"user_id": user_id, "email": email, "name": name}
            self.user = user_data
            self.user_json = json.dumps(user_data)
        try:
            client = self._get_supabase_client()
            response = (
                client.table("users")
                .select("user_id")
                .eq("user_id", user_data["user_id"])
                .execute()
            )
            if not response.data:
                db_user_data = user_data.copy()
                db_user_data["avatar_url"] = (
                    f"https://api.dicebear.com/9.x/initials/svg?seed={name}"
                )
                client.table("users").insert(db_user_data).execute()
                client.table("portfolios").insert(
                    {"user_id": user_data["user_id"]}
                ).execute()
                logging.info(f"New user created: {user_data['email']}")
            else:
                logging.info(f"User logged in: {user_data['email']}")
            from app.states.dashboard_state import DashboardState

            return DashboardState.load_user_data
        except Exception as e:
            logging.exception(f"Supabase error on login: {e}")
            async with self:
                self.user = None
                self.user_json = ""

    @rx.event
    def on_load(self):
        """Check for user session on page load."""
        if self.user_json:
            try:
                self.user = json.loads(self.user_json)
                from app.states.dashboard_state import DashboardState

                return DashboardState.load_user_data
            except json.JSONDecodeError as e:
                logging.exception(f"Failed to decode user_json from LocalStorage: {e}")
                self.user_json = ""
                self.user = None

    @rx.event
    def logout(self):
        self.user_json = ""
        self.user = None
        return rx.redirect("/")