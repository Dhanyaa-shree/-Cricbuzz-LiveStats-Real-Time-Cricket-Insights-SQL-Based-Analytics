import streamlit as st
from datetime import datetime
from utils.cricbuzz_api import get_live_matches


class RealtimeManager:
    """Manage real-time data updates safely"""

    def __init__(self):
        self.last_update = datetime.now()
        self.cached_matches = []

    def refresh_data(self):
        """Fetch fresh data safely"""
        try:
            self.cached_matches = get_live_matches()
        except Exception as e:
            st.warning(f"API error: {e}")
            self.cached_matches = []

        self.last_update = datetime.now()

    def get_matches(self):
        """Auto refresh every 30 seconds"""
        diff = (datetime.now() - self.last_update).total_seconds()

        if diff > 30:
            self.refresh_data()

        return self.cached_matches

    def get_last_update_time(self):
        return self.last_update.strftime("%H:%M:%S")


@st.cache_data(ttl=30)
def get_live_matches_cached():
    """Cached API call (safe)"""
    try:
        return get_live_matches()
    except:
        return []


def auto_refresh_button():
    """Toggle auto refresh safely"""

    if "auto_refresh" not in st.session_state:
        st.session_state.auto_refresh = False

    def toggle():
        st.session_state.auto_refresh = not st.session_state.auto_refresh

    st.button(
        "🔄 Auto Refresh ON" if st.session_state.auto_refresh else "⏸ Auto Refresh OFF",
        on_click=toggle
    )