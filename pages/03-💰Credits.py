import os
import streamlit as st
from utils.auth import login_st_form, get_current_logged_in_user, redeem_referral_code
from streamlit.errors import StreamlitAPIException
from utils.model import UserModel
from utils.constants import STREAMLIT_DOMAIN

# Get current directory
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
# Go one directory up to get to the root directory
ROOT_DIR = os.path.abspath(os.path.join(DIR_PATH, os.pardir))

QR_CODE_PATH = os.path.join(ROOT_DIR, 'assets', 'qr_code.jpeg')

try:
    st.set_page_config(page_title='Credits', page_icon='💰', initial_sidebar_state="auto", menu_items=None)
except StreamlitAPIException as e:
    pass

st.title('💰 Know about Credits!')

logged_in = login_st_form()

def verify_refer_code(current_user_email, referral_code):
    # Redeem
    [status, message] = redeem_referral_code(current_user_email, referral_code)

    if status:
        st.success(message)
    else:
        st.error(message)

def referal_code_flow(email: str):
    params = st.query_params
    applied_referral_code = params.get('referral_code')
    if applied_referral_code:
        verify_refer_code(email, applied_referral_code)
    else:
        # Display box to enter verification code
        verification_code = st.text_input('Enter referral code')
        if verification_code:
            verify_refer_code(email, applied_referral_code)

if logged_in:
    user_data: UserModel = get_current_logged_in_user()
    referral_code = user_data.referral_code
    referral_code_link = f"{STREAMLIT_DOMAIN}/Credits?referral_code={referral_code}"

    st.success(f"Welcome {user_data.user_name}! You currently have {user_data.credits} credits.")
    st.markdown('Credits are currency of this app, To prevent spamming we have added this feature. You can earn credits by referring your friends or by paying for them. You can use these credits to generate reports.')

    st.markdown('## Get Credits')
    st.write('To get credits, you can follow these steps:')
    st.markdown(f"- Refer friends: Verify your email to get 5 credits, So easy!")
    st.markdown(f"- Refer friends: You can earn credits by referring your friends to use this app. For each friend that signs up using your referral code, you will receive 3 credits (while your friend gets 2). Your referral code is **{referral_code}** or share them this direct link: {referral_code_link}")
    
    st.markdown("Got any referral code? Enter it below to get credits!")
    referal_code_flow(user_data.email)
    # st.markdown('2. Purchase credits: If you don't want to refer friends, you can also purchase credits directly from the app. There will be different packages available for purchase.')

    st.markdown('- Buy credits: You can also buy credits, which charges 167 Rs (~2$) for 10 credits (Quite cheap, right?).. To buy credits, scan the QR code below, pay 167 Rs and [send screenshot of transaction to this email](mailto:tietprojectreport@skullzbones.com) (Please also mention your registered email id used for this app).')
    with st.columns(3)[1]:
        st.image(QR_CODE_PATH)
    st.markdown('- Crypto: Coming Soon... (Not sure if it is worth the efforts, You tell)')
