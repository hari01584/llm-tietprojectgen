import streamlit as st
from utils.auth import login_st_form, get_current_logged_in_user
from streamlit.errors import StreamlitAPIException
from utils.model import UserModel, coins_delta, get_user_data, get_usage_log

try:
    st.set_page_config(page_title='Admin', page_icon='🕵️', initial_sidebar_state="auto", menu_items=None)
except StreamlitAPIException as e:
    pass

st.title('🕵️ Admin Only!')

logged_in = login_st_form()

def admin_control_widgets():
    st.write("Topup Account")
    with st.form(key="topup_form"):
        target_email = st.text_input("Enter target email:")
        topup_amount = st.number_input("Enter amount to topup:")
        submit = st.form_submit_button("Topup", use_container_width=True)

    if submit:
        if not target_email:
            st.error("Please enter target email.")
            return
        if not topup_amount:
            st.error("Please enter topup amount.")
            return

        target_user = get_user_data(target_email)
        if not target_user:
            st.error("User not found.")
            return
        
        coins_delta(target_email, topup_amount)
        st.success(f"Successfully topped up {topup_amount} credits to {target_email}")

    all_usage_logs_data = get_usage_log()
    # Create pandas dataframe
    import pandas as pd
    import numpy as np
    import pytz

    df = pd.DataFrame(all_usage_logs_data)
    # Sort by date (ISO 8601) (get more recent first)
    df = df.sort_values(by='timestamp', ascending=False)
    # Convert this ISO 8601 to human readable date
    df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)
    ist = pytz.timezone('Asia/Kolkata')
    # Convert the datetime series from UTC to IST
    df['timestamp'] = df['timestamp'].dt.tz_convert(ist)
    df['timestamp'] = df['timestamp'].dt.strftime("%d-%m-%Y %H:%M:%S")

    # Display the dataframe
    st.write(df)

if logged_in:
    user_data: UserModel = get_current_logged_in_user()

    if user_data.is_admin:
        st.success(f"Welcome admin.")
        admin_control_widgets()
    else:
        st.warning(f"Only admin can access this page, You sneaky sneaky user!")