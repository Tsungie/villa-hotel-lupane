import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from streamlit_calendar import calendar

# --- Page Configuration ---
st.set_page_config(page_title="Top Villa Admin", page_icon="🏨", layout="wide")

st.title("🏨 Top Villa Lodge | Booking Management")
st.markdown("---")

# --- 1. Establish Connection ---
# Uses secrets from .streamlit/secrets.toml
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # Read the data (ttl=0 ensures we always see the latest website inquiries)
    df = conn.read(worksheet="Sheet1", ttl=0)
    
    # --- 2. Calendar View ---
    st.subheader("📅 Occupancy Calendar")
    
    calendar_events = []
    for _, row in df.iterrows():
        # Assign colors based on status
        color = "#D4AF37" if row['Status'] == "Confirmed" else "#333333" # Gold for Confirmed, Charcoal for Pending
        
        calendar_events.append({
            "title": f"{row['Guest Name']} ({row['Room Type']})",
            "start": row['Check-In'],
            "end": row['Check-Out'],
            "color": color
        })

    calendar_options = {
        "headerToolbar": {"left": "prev,next today", "center": "title", "right": "dayGridMonth,timeGridWeek"},
        "initialView": "dayGridMonth",
    }
    
    calendar(events=calendar_events, options=calendar_options)

    # --- 3. Admin Tools (Password Protected) ---
    st.sidebar.header("🔐 Admin Access")
    pwd = st.sidebar.text_input("Enter Password", type="password")

    if pwd == "Villa2026!":
        st.sidebar.success("Access Granted")
        
        st.markdown("---")
        col1, col2 = st.columns(2)

        # --- UPDATE STATUS ---
        with col1:
            st.subheader("🛠️ Update Status")
            pending = df[df['Status'] == "Pending"]
            
            if not pending.empty:
                target = st.selectbox("Select Guest to Confirm", pending['Guest Name'])
                action = st.radio("Set Status To:", ["Confirmed", "Cancelled"], horizontal=True)
                
                if st.button("Update Booking"):
                    df.loc[df['Guest Name'] == target, 'Status'] = action
                    conn.update(worksheet="Sheet1", data=df)
                    st.success(f"Updated {target} to {action}")
                    st.rerun()
            else:
                st.info("No pending bookings.")

        # --- DELETE ENTRIES ---
        with col2:
            st.subheader("🗑️ Delete Booking")
            to_delete = st.selectbox("Select Entry to Remove", df['Guest Name'])
            confirm = st.checkbox(f"Confirm deletion of {to_delete}")
            
            if st.button("Delete Permanently", type="primary"):
                if confirm:
                    df = df[df['Guest Name'] != to_delete]
                    conn.update(worksheet="Sheet1", data=df)
                    st.warning("Entry deleted.")
                    st.rerun()
                else:
                    st.error("Please check the confirmation box.")

    elif pwd:
        st.sidebar.error("Incorrect Password")

except Exception as e:
    st.error(f"Connection Error: {e}")
    st.info("Check your .streamlit/secrets.toml and ensure the Spreadsheet URL is correct.")