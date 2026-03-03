import streamlit as st
from streamlit_calendar import calendar

st.title("🏰 Top Villa Lodge Booking Manager")

# 1. Define your bookings as 'events'
calendar_events = [
    {
        "title": "Tsungie - Deluxe Suite",
        "start": "2026-03-05",
        "end": "2026-03-10",
        "color": "#D4AF37", # Your brand gold
    },
    {
        "title": "Pending: John Doe - Standard",
        "start": "2026-03-07",
        "end": "2026-03-09",
        "color": "#1a1a1a",
    }
]

# 2. Configure the Calendar (Month, Week, Day views)
calendar_options = {
    "headerToolbar": {
        "left": "today prev,next",
        "center": "title",
        "right": "dayGridMonth,timeGridWeek,timeGridDay",
    },
    "initialView": "dayGridMonth",
    "selectable": True,
}

# 3. Display it
state = calendar(events=calendar_events, options=calendar_options)

st.write("Selected Event Data:", state)