import streamlit as st
from utils.auth import login_st_form, get_current_logged_in_user
from streamlit.errors import StreamlitAPIException
from utils.model import UserModel, set_verified

try:
    st.set_page_config(page_title='Verify Mail', page_icon='✉️', initial_sidebar_state="auto", menu_items=None)
except StreamlitAPIException as e:
    pass

st.title('✉️ Verify Your Mail!')

logged_in = login_st_form()

def verify_code(email, verification_code_1, verification_code_2):
    # Check if verification code is correct
    if verification_code_1 == verification_code_2:
        # Update user data
        set_verified(unique=email)
        st.success('Your email has been verified successfully!')
    else:
        st.error('Invalid verification code! Please check your email and try again.')

if logged_in:
    user_data: UserModel = get_current_logged_in_user()
    # Get query params
    params = st.query_params
    verification_code = params.get('verification_code')
    if verification_code:
        verify_code(user_data.email, verification_code, user_data.verification_token)
    else:
        # Display box to enter verification code
        verification_code = st.text_input('Enter verification code')
        if verification_code:
            verify_code(user_data.email, verification_code, user_data.verification_token)
        else:
            st.warning('Please check your email for the verification code and enter it above.')