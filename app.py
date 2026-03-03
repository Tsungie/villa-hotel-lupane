import streamlit as st
from streamlit_gsheets import GSheetsConnection

# This uses the secrets you put in .streamlit/secrets.toml
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # Try to read the first 5 rows
    df = conn.read(worksheet="Sheet1", ttl=0) # ttl=0 forces a fresh look
    st.write("Connection Successful! Here is the data:")
    st.dataframe(df)
except Exception as e:
    st.error(f"Connection Failed: {e}")