import streamlit as st
from utils.auth import create_account_st_form
from streamlit_extras.switch_page_button import switch_page
from streamlit.errors import StreamlitAPIException

try:
    st.set_page_config(page_title='Sign Up', page_icon='✅', initial_sidebar_state="auto", menu_items=None)
except StreamlitAPIException as e:
    pass

if create_account_st_form():
    switch_page('generate report')